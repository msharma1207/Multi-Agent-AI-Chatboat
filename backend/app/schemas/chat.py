from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    model: str | None = None
    provider: str | None = None
    mode: str | None = None
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    model: str
    provider: str
    mode: str = "chat"
    image_data: str | None = None
