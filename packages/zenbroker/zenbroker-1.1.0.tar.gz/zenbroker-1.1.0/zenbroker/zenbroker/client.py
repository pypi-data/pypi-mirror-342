import httpx
from typing import Dict, Any
from pydantic import BaseModel, Field, HttpUrl

class PostPublishEventPayload(BaseModel):
    applicationId: str = Field(..., description="Application ID")
    channel: str = Field(..., description="ChannelID")
    data: Dict[str, Any]

class PostPublishEventResponse(BaseModel):
    message: str = Field(..., description="Message from the server")
    id: str = Field(..., description="ID of the message")

class ZenbrokerClient:
    def __init__(self, base_url: HttpUrl, application_id: str) -> None:
        self._url: str = str(base_url)
        self._application_id: str = str(application_id)

        self._api = httpx.Client(base_url=self._url)
    
    def publish(self, channel: str, data: Dict[str, Any]) -> PostPublishEventResponse:
        post_data: PostPublishEventPayload = PostPublishEventPayload(
            applicationId=self._application_id,
            channel=channel,
            data=data
        )

        response = self._api.post(
            url="/producer/emit",
            json=post_data.model_dump()
        )

        response.raise_for_status()
        result = response.json()

        return PostPublishEventResponse(
            id=result['id'],
            message=result['message']
        )
    
