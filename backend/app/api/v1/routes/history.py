from typing import Literal

from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel, Field

from app.services.history_service import HistoryService

router = APIRouter()
service = HistoryService("storage/chat_history.json")


class ConversationCreate(BaseModel):
    title: str = Field(default="New chat", max_length=80)
    mode: str = "chat"


class ConversationUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=80)


class MessageCreate(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)
    image_data: str | None = None


@router.get("/conversations")
def list_conversations() -> list[dict[str, object]]:
    return service.list_conversations()


@router.post("/conversations", status_code=status.HTTP_201_CREATED)
def create_conversation(payload: ConversationCreate) -> dict[str, object]:
    return service.create_conversation(payload.title, payload.mode)


@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str) -> dict[str, object]:
    conversation = service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post("/conversations/{conversation_id}/messages", status_code=status.HTTP_201_CREATED)
def add_conversation_message(conversation_id: str, payload: MessageCreate) -> dict[str, object]:
    message = service.add_conversation_message(
        conversation_id, payload.role, payload.content, payload.image_data
    )
    if not message:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return message


@router.patch("/conversations/{conversation_id}")
def rename_conversation(conversation_id: str, payload: ConversationUpdate) -> dict[str, object]:
    conversation = service.rename_conversation(conversation_id, payload.title)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(conversation_id: str) -> Response:
    if not service.delete_conversation(conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("")
def add_history_message(role: str, content: str) -> dict[str, object]:
    return service.add_message(role, content)


@router.get("")
def get_history() -> list[dict[str, object]]:
    return service.get_history()
