from pydantic import BaseModel


class Message(BaseModel):
    messageId: str
    receiptHandle: str
    body: str
    attributes: dict
    messageAttributes: dict
    md5OfBody: str
    eventSource: str
    eventSourceARN: str
    awsRegion: str


class SQSEvent(BaseModel):
    Records: list[Message]
