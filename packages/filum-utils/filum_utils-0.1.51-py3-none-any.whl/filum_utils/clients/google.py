import json
from typing import BinaryIO, List

from google.cloud import pubsub_v1, storage

from filum_utils.config import config
from filum_utils.types.conversation import PubsubMessageType


class GoogleCloudClient:
    def __init__(self, project_id: str = config.GOOGLE_PROJECT_ID):
        self._project_id = project_id

    def publish_messages(
        self,
        messages: List[PubsubMessageType],
        topic_id: str = config.GOOGLE_PUBSUB_TOPIC_ID,
    ):
        publisher_options = pubsub_v1.types.PublisherOptions()
        publisher = pubsub_v1.PublisherClient(publisher_options=publisher_options)

        topic_path = publisher.topic_path(self._project_id, topic_id)

        for message in messages:
            message = json.dumps(message)
            data = message.encode("utf-8")
            publisher.publish(topic_path, data=data)


class GoogleCloudStorageClient:
    def __init__(
        self,
        project_id: str = config.GOOGLE_PROJECT_ID,
        bucket_name: str = config.GCP_UPLOADS_BUCKET
    ):
        self._project_id = project_id

        self._storage_client = storage.Client(project=self._project_id)
        self._bucket = self._storage_client.bucket(bucket_name)

    def upload_file(self, file_name: str, file_obj: BinaryIO):
        blob = self._bucket.blob(file_name)
        blob.upload_from_file(file_obj)
