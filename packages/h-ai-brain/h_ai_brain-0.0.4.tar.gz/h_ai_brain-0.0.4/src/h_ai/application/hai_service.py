import datetime

from h_message_bus import NatsPublisherAdapter
from h_message_bus.domain.twitter_get_user_request_message import TwitterGetUserRequestMessage
from h_message_bus.domain.twitter_get_user_response_message import TwitterGetUserResponseMessage
from h_message_bus.domain.vector_save_request_message import VectorSaveRequestMessage

from ..application.web_docs_service import WebDocsService


class HaiService:
    def __init__(self, nats_publisher_adapter: NatsPublisherAdapter):
        self.nats_publisher_adapter = nats_publisher_adapter
        self.web_docs_service = WebDocsService()

    async def detect_and_store_documentation(self, twitter_screen_name: str):
        req_message = TwitterGetUserRequestMessage.create_message(twitter_screen_name)
        response = await self.nats_publisher_adapter.request(req_message)
        twitter_user = TwitterGetUserResponseMessage.from_hai_message(response)

        if twitter_user.url is not None:
            print(f"Documentation found for {twitter_user.screen_name}: {twitter_user.url}")
            docs = await self.web_docs_service.discover_documentation(twitter_user.url)

            for doc in docs:
                collection_name = f"{twitter_user.screen_name}_docs"
                chapters = doc.chapters
                for chapter in chapters:
                    i = 0
                    for text in chapter.paragraphs:
                        document_id = f"{doc.title}_{chapter.heading}_{i}"

                        req_metadata = {
                            "source": doc.url,
                            "updated": datetime.datetime.utcnow().isoformat()
                        }
                        i = i + 1

                        request = VectorSaveRequestMessage.create_message(
                            collection_name=collection_name,
                            document_id=document_id,
                            content=text,
                            metadata=req_metadata)

                        await self.nats_publisher_adapter.publish(request)

        else:
            print(f"No documentation found for {twitter_user.screen_name}")