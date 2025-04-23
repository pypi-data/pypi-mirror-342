import csv
import io
from abc import abstractmethod
from typing import Any, Callable, Dict, List, Optional, Union

from glom import glom

from filum_utils.clients.google import GoogleCloudStorageClient
from filum_utils.clients.notification import PublisherType
from filum_utils.config import config
from filum_utils.enums import BaseStatus, ObjectType
from filum_utils.errors import BaseError, ErrorMessage
from filum_utils.services.file import FileService
from filum_utils.services.subscription import SubscriptionService
from filum_utils.types.action import Action
from filum_utils.types.campaign import Campaign
from filum_utils.types.common import TriggerFunctionResponse
from filum_utils.types.engagement_campaign import EngagementCampaign
from filum_utils.types.organization import Organization
from filum_utils.types.subscription import (
    CallableResponse,
    MetadataGroup,
    SmartDistributionConfig,
    SmartDistributionParams,
    Subscription,
    SubscriptionData
)
from filum_utils.utils.datetime_formatter import DateTimeFormatter
from filum_utils.utils.segment_users import SegmentUserUtil
from filum_utils.utils.smart_distributions import SmartDistributionUtil

Event = Optional[Dict[str, Any]]
User = Optional[Dict[str, Any]]


class BaseCampaignSubscriptionService(SubscriptionService):
    def __init__(
        self,
        subscription: Subscription,
        action: Action,
        organization: Organization,
        campaign_id: str = None
    ):
        super().__init__(subscription, organization)
        self.action = action
        self.campaign_id = campaign_id
        self.smart_distribution = self.subscription.get("smart_distribution", {})

    @property
    def _object_type(self) -> str:
        return ObjectType.ACTION

    @property
    def _object_id(self) -> int:
        return self.action["id"]

    @property
    def _notification_publisher_type(self) -> str:
        return PublisherType.VoC

    @property
    def _user_limit(self) -> int:
        return self.trigger_data.get("user_limit_per_trigger") or 0

    @abstractmethod
    def update_status(self, updated_status: str):
        ...

    @abstractmethod
    def _get_trigger_completed_notification_subtitle(self, channel_name: str, success_count: int) -> str:
        ...

    def handle_real_time_trigger(
        self,
        process_real_time_fn: Callable[
            [Action, Union[Campaign, EngagementCampaign], Organization, Event, SubscriptionData, Any],
            CallableResponse
        ],
        event: [Dict[str, Any]],
        **kwargs,
    ) -> TriggerFunctionResponse:
        result = self._handle_trigger(
            process_real_time_fn,
            event,
            **kwargs
        )

        return {
            "is_finished": True,
            "success_count": result.get("success_count"),
            "error_message": None,
        }

    def handle_segment_manual_trigger(
        self,
        process_segment_manual_fn: Callable[
            [Action, Union[Campaign, EngagementCampaign], Organization, List[User], SubscriptionData, Any],
            CallableResponse
        ],
        properties: List[str],
        last_current_index: int = 0,
        last_success_count: int = 0,
        channel_name: str = None,
        segment_user_file_name: Optional[str] = None,
        smart_distribution_params: Optional[SmartDistributionParams] = None,
        **kwargs,
    ) -> TriggerFunctionResponse:
        self._validate_last_current_index(last_current_index)

        segment_id = self.trigger_data.get("segment_id")
        if not segment_id:
            raise BaseError(
                message=ErrorMessage.MISSING_SEGMENT_ID,
                data={
                    "Campaign ID": self._parent_id,
                }
            )

        if not segment_user_file_name:
            return self._handle_initial_segment_trigger(channel_name, properties)

        # Resumed trigger: Process next batch from the existing CSV
        users = self._get_users_in_csv_file(
            segment_user_file_name,
            last_current_index,
            limit=config.FILE_RECORD_LIMIT
        )

        return self._handle_manual_trigger(
            process_fn=process_segment_manual_fn,
            users=users,
            object_record_limit=config.FILE_RECORD_LIMIT,
            last_current_index=last_current_index,
            last_success_count=last_success_count,
            channel_name=channel_name,
            segment_user_file_name=segment_user_file_name,
            smart_distribution_params=smart_distribution_params,
            **kwargs,
        )

    def handle_file_manual_trigger(
        self,
        process_file_manual_fn: Callable,
        last_current_index: int = 0,
        last_success_count: int = 0,
        channel_name: str = None,
        **kwargs,
    ):
        self._validate_last_current_index(last_current_index)

        file_name = self.trigger_data.get("file_name")
        if not file_name:
            raise BaseError(
                message=ErrorMessage.MISSING_FILE,
                data={
                    "Campaign ID": self._parent_id,
                }
            )

        users = self._get_users_in_csv_file(
            file_name,
            last_current_index,
            limit=config.FILE_RECORD_LIMIT
        )

        return self._handle_manual_trigger(
            process_fn=process_file_manual_fn,
            users=users,
            object_record_limit=config.FILE_RECORD_LIMIT,
            last_current_index=last_current_index,
            last_success_count=last_success_count,
            channel_name=channel_name,
            **kwargs,
        )

    def handle_object_manual_trigger(
        self,
        process_object_manual_fn: Callable,
        **kwargs,
    ):
        ...

    def _get_users_in_csv_file(
        self,
        file_name: str,
        current_index: int = 0,
        limit: int = config.FILE_RECORD_LIMIT
    ) -> List[Dict[str, Any]]:
        file_content_bytes = self.filum_client.get_uploaded_file(file_name)
        return FileService.get_rows(
            file_name,
            file_content_bytes,
            current_index=current_index,
            limit=limit,
        )

    def _exceeded_user_limit(self, current_total_users: int) -> bool:
        return current_total_users >= self._user_limit if self._user_limit else False

    def _validate_last_current_index(self, last_current_index: int):
        current_index = self.subscription_data.get("last_current_index") or 0
        if not current_index or current_index == last_current_index:
            return

        raise BaseError(
            message=ErrorMessage.MISMATCH_LAST_CURRENT_INDEX,
            data={
                "Campaign ID": self._parent_id,
                "Current Index": current_index,
                "Last Current Index": last_current_index
            }
        )

    def _handle_initial_segment_trigger(
        self,
        channel_name: Optional[str] = None,
        properties: Optional[List[str]] = None
    ):
        is_smart_config_enabled = self.smart_distribution.get("enabled", False)
        user_metadata_property_name = None
        if is_smart_config_enabled:
            user_metadata_property_name = glom(self.smart_distribution, "config.property_name")
            properties.append(user_metadata_property_name)

        # Fetch all users from the segment
        segment_id = self.trigger_data["segment_id"]
        users = self._fetch_segment_users(properties, segment_id)
        if not users:
            return self._process_campaign_completion(
                channel_name=channel_name,
                success_count=0
            )

        segment_user_file_name = self._handling_upload_segment_users_file(users, properties)

        # Get metadata groups if available
        smart_distribution_params = None
        if user_metadata_property_name:
            metadata_groups = self._get_metadata_groups(users)
            smart_distribution_params = SmartDistributionParams(
                metadata_groups=metadata_groups,
                user_metadata_property_name=user_metadata_property_name
            )

            has_more_remaining_send = False
            for _, metadata_group in metadata_groups.items():
                if metadata_group["remaining_send"] <= 0:
                    continue

                has_more_remaining_send = True
                break

            if not has_more_remaining_send:
                return self._process_campaign_completion(
                    channel_name=channel_name,
                    success_count=0
                )

        # Publish with metadata groups if available
        self._handle_publish_subscription(
            last_current_index=0,
            last_success_count=0,
            segment_user_file_name=segment_user_file_name,
            smart_distribution_params=smart_distribution_params
        )
        return {
            "is_finished": False,
            "success_count": 0,
            "error_message": None,
        }

    def _handling_upload_segment_users_file(
        self,
        users: List[Dict[str, Any]],
        properties: List[str]
    ) -> str:
        """Generate and upload a CSV file with segment users.
        
        Args:
            users: List of users to include in the CSV
            properties (List[str]): List of segment properties to include in the CSV
            
        Returns:
            str: GCS path of the uploaded CSV file
        """
        # Generate file name with organization, campaign, distribution and date
        current_datetime = DateTimeFormatter.get_current_datetime().strftime("%Y%m%d%H%M")
        distribution_id = self.distribution_id
        segment_user_file_name = f"{self.organization['id']}/{self.campaign_id}"
        segment_user_file_name = (
            f"{segment_user_file_name}/{distribution_id}/{current_datetime}.csv"
            if distribution_id
            else f"{segment_user_file_name}/{current_datetime}.csv"
        )

        # Transform the list of users into CSV-formatted bytes
        csv_buffer = io.StringIO()
        csv_writer = csv.DictWriter(csv_buffer, fieldnames=properties)
        csv_writer.writeheader()

        for user in users:
            # Use empty string for missing values
            row = {prop: user.get(prop, "") for prop in properties}
            csv_writer.writerow(row)

        csv_bytes = csv_buffer.getvalue().encode('utf-8')

        # Upload the CSV file to Google Cloud Storage
        storage_client = GoogleCloudStorageClient()
        storage_client.upload_file(segment_user_file_name, io.BytesIO(csv_bytes))
        csv_buffer.close()

        return segment_user_file_name

    def _fetch_segment_users(
        self,
        properties: List[str],
        segment_id: str,
    ) -> List[Dict[str, Any]]:
        """Fetch users from a segment with pagination.
        
        Args:
            properties (List[str]): List of properties to fetch for each user
            segment_id (str): ID of the segment to fetch users from
        Returns:
            List[Dict[str, Any]]: List of users with the requested properties
        """
        limit = config.SEGMENT_RECORD_LIMIT
        page = 0
        users = []
        while True:
            offset = page * limit
            next_users: List[Dict[str, Any]] = self.filum_client.get_user_csv_reader(
                custom_properties=properties,
                segment_id=segment_id,
                organization=self.organization,
                offset=offset,
                limit=limit
            )
            if not next_users:
                break

            users.extend(next_users)
            page += 1
            if len(next_users) < limit:
                break

        return users

    def _handle_manual_trigger(
        self,
        process_fn: Callable,
        users: List[Dict[str, Any]],
        object_record_limit: int,
        last_current_index: int = 0,
        last_success_count: int = 0,
        channel_name: str = None,
        segment_user_file_name: Optional[str] = None,
        smart_distribution_params: Optional[SmartDistributionParams] = None,
        **kwargs
    ):
        result: CallableResponse = self._handle_trigger(
            process_fn=process_fn,
            data=users,
            smart_distribution_params=smart_distribution_params,
            **kwargs,
        )

        success_count = result.get("success_count") or 0
        total_success_count = last_success_count + success_count

        total_users_in_page = len(users) if users else 0
        has_more_users = total_users_in_page >= object_record_limit

        current_index = total_users_in_page + last_current_index

        updated_metadata_groups = result.get("metadata_groups")
        has_more_remaining_send = False
        user_limit_exceeded = False
        if not updated_metadata_groups:
            user_limit_exceeded = self._exceeded_user_limit(current_index)
        else:
            for _, metadata_group in updated_metadata_groups.items():
                if metadata_group["remaining_send"] <= 0:
                    continue

                has_more_remaining_send = True
                break

        stop_running = not has_more_remaining_send or user_limit_exceeded or not has_more_users
        if stop_running:
            return self._process_campaign_completion(
                channel_name=channel_name,
                success_count=total_success_count
            )

        params = {
            "last_current_index": current_index,
            "last_success_count": total_success_count
        }
        if segment_user_file_name:
            params["segment_user_file_name"] = segment_user_file_name

        smart_distribution_params = smart_distribution_params or {}
        user_metadata_property_name = smart_distribution_params.get("user_metadata_property_name")
        if user_metadata_property_name and not updated_metadata_groups:
            raise BaseError(
                message=ErrorMessage.MISSING_METADATA_GROUPS_TO_PUBLISH_SUBSCRIPTION
            )

        if user_metadata_property_name and updated_metadata_groups:
            params["smart_distribution_params"] = {
                "user_metadata_property_name": user_metadata_property_name,
                "metadata_groups": updated_metadata_groups
            }

        # handle running next page
        error_message = self._handle_publish_subscription(
            **params
        )

        return {
            "is_finished": stop_running,
            "success_count": success_count,
            "error_message": error_message,
        }

    def _handle_trigger(
        self,
        process_fn: Callable,
        data: Any,
        **kwargs,
    ):
        params = {
            "action": self.action,
            "campaign": self.parent,
            "data": data,
            "subscription_data": self.subscription_data,
            "organization": self.organization,
            **kwargs
        }

        return process_fn(**params)

    def _handle_trigger_completed(
        self,
        channel_name: Optional[str],
        success_count: int
    ) -> str:
        update_status_error_message = self._handle_trigger_function_with_try_except(
            "Update Subscription Status",
            self.update_status,
            fn_params={
                "updated_status": BaseStatus.COMPLETED
            }
        )

        update_subscription_data_error_message = self._update_subscription_data_with_try_except({
            "last_current_index": 0
        })

        notify_error_message = ""
        if channel_name:
            subtitle = self._get_trigger_completed_notification_subtitle(
                channel_name, success_count
            )
            notify_error_message = self._handle_trigger_function_with_try_except(
                "Create Notification",
                self._notify,
                fn_params={
                    "publisher_type": f"{self._notification_publisher_type}",
                    "title": f"{self._parent_name} has been distributed successfully to your recipients",
                    "subtitle": subtitle,
                }
            )

        error_messages = {
            update_subscription_data_error_message,
            update_status_error_message,
            notify_error_message,
        }
        return " ".join([error_message for error_message in error_messages if error_message])

    def _get_metadata_groups(self, users: List[Dict[str, Any]]) -> Optional[Dict[str, MetadataGroup]]:
        """Calculate metadata group distribution limits based on smart distribution configuration.
        
        Args:
            users: List of user dictionaries
            
        Returns:
            Dictionary of metadata groups with calculated limits, or None if smart distribution is not enabled
        """
        # Extract configuration parameters
        smart_config: SmartDistributionConfig = self.smart_distribution["config"]
        if not smart_config:
            raise BaseError(message=ErrorMessage.MISSING_CONFIG_IN_SMART_DISTRIBUTION)

        # Extract configuration parameters
        metadata_id = smart_config["metadata_id"]
        user_metadata_property_name = smart_config["property_name"]

        # Get actual responses for the current month
        actual_responses_per_metadata_value = (
            self.filum_client.get_this_month_answered_response_counts_by_metadata(
                organization_id=self.organization["id"],
                campaign_id=self.campaign_id,
                metadata_id=metadata_id
            )
        )

        # Count users by metadata value
        total_users_by_metadata_value = SegmentUserUtil.count_grouped_users_by_metadata_value(
            users,
            user_metadata_property_name
        )

        # Calculate distribution limits
        user_limit_per_trigger = (
            self.subscription_data.get("trigger_data", {}).get("user_limit_per_trigger") or 0
        )

        smart_distribution_util = SmartDistributionUtil(
            smart_config,
            total_users_by_metadata_value,
            actual_responses_per_metadata_value,
            user_limit_per_trigger,
        )
        return smart_distribution_util.calculate_send_limit_per_metadata()

    def _handle_publish_subscription(
        self,
        last_current_index: int,
        last_success_count: int,
        segment_user_file_name: Optional[str] = None,
        smart_distribution_params: Optional[SmartDistributionParams] = None,
    ):
        # Update subscription data with segment_user_file_name and metadata_groups if provided
        updated_data = {
            "last_current_index": last_current_index
        }

        request_data = {
            "last_current_index": last_current_index,
            "last_success_count": last_success_count
        }
        if segment_user_file_name:
            updated_data["segment_user_file_name"] = segment_user_file_name
            request_data["segment_user_file_name"] = segment_user_file_name

        if smart_distribution_params:
            metadata_groups = smart_distribution_params["metadata_groups"]
            user_metadata_property_name = smart_distribution_params["user_metadata_property_name"]

            updated_data["metadata_groups"] = metadata_groups
            request_data["metadata_groups"] = metadata_groups

            updated_data["user_metadata_property_name"] = user_metadata_property_name
            request_data["user_metadata_property_name"] = user_metadata_property_name

        update_subscription_data_error_message = self._update_subscription_data_with_try_except(updated_data)

        # Publish subscription with segment_user_file_name if provided
        publish_subscription_error_message = self._handle_trigger_function_with_try_except(
            "Publish Subscription",
            self.subscription_client.publish,
            fn_params={
                "request_data": request_data
            }
        )

        error_message = None
        if update_subscription_data_error_message or publish_subscription_error_message:
            error_message = (
                f"{update_subscription_data_error_message} {publish_subscription_error_message}"
            )

        return error_message

    def _update_subscription_data_with_try_except(self, updated_data: Dict[str, Any]) -> str:
        return self._handle_trigger_function_with_try_except(
            "Update Subscription Data",
            self.update_subscription_data,
            fn_params={
                "updated_data": updated_data
            }
        )

    def _process_campaign_completion(
        self,
        channel_name: str,
        success_count: int = 0,
    ) -> Dict[str, Any]:
        error_message = self._handle_trigger_function_with_try_except(
            "Update Campaign Status to Completed",
            self._handle_trigger_completed,
            fn_params={
                "channel_name": channel_name,
                "success_count": success_count
            }
        )
        return {
            "is_finished": True,
            "success_count": success_count,
            "error_message": error_message,
        }

    @staticmethod
    def _handle_trigger_function_with_try_except(
        fn_name: str,
        fn: Callable,
        fn_params: Dict[str, Any] = None
    ) -> str:
        error_message = None
        try:
            fn_params = fn_params if fn_params else {}
            fn(**fn_params)
        except BaseError as e:
            error_message = e.message
        except Exception:
            error_message = ErrorMessage.IMPLEMENTATION_ERROR

        return f"{fn_name}: {error_message}" if error_message else ""
