from pydantic import BaseModel


class WorkspaceCreate(BaseModel):
    organization: str
    name: str
