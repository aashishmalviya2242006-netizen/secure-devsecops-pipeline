from pydantic import BaseModel


class LogCreate(BaseModel):
    service: str
    level: str
    message: str


class LogResponse(BaseModel):
    id: int
    service: str
    level: str
    message: str
