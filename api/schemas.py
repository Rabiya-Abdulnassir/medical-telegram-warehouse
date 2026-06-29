from pydantic import BaseModel


class ProductResponse(BaseModel):
    product: str
    mentions: int


class ActivityResponse(BaseModel):
    date: str
    total_posts: int


class MessageResponse(BaseModel):
    message_id: int
    channel: str
    text: str
    views: int


class VisualContentResponse(BaseModel):
    channel: str
    total_messages: int
    images: int