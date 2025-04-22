from typing import Annotated

from pydantic import BaseModel, Field

from main import app
from wellapi.exceptions import HTTPException, RequestValidationError
from wellapi.models import RequestAPIGateway, ResponseAPIGateway
from wellapi.params import Query, Depends
from wellapi.security import OAuth2PasswordBearer


class OtherResponse(BaseModel):
    message: str


class OtherBody(BaseModel):
    name: str
    age: int


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    if token != "fake-token":
        raise HTTPException(status_code=403, detail="Not authenticated")

    return token


class Session:
    def __init__(self):
        self.session = "session"


def db() -> Session:
    print("DB connection")
    return Session()


@app.post(
    "/ping/{ping_id}",
    dependencies=[Depends(verify_token)],
    status_code=201,
    tags=["ping"],
)
def ping(ping_id: int, item: list[OtherBody], token: Annotated[str, Depends(verify_token)]) -> OtherResponse:
    return OtherResponse(
        message=f"Pong {ping_id}. {token}",
    )


@app.post("/ping", dependencies=[Depends(verify_token)], status_code=201, tags=["ping"])
def ping_v2(item: list[OtherBody], param: Annotated[FilterParams, Query()]) -> OtherResponse:
    return OtherResponse(
        message=f"Pong {param.limit} {param.offset}",
    )


@app.sqs("ping-sqs")
def ping_sqs(events: list[OtherBody]):
    print(events)


@app.job("rate(5 minutes)", name="ping_job")
def ping_job(dbbb: Annotated[Session, Depends(db)]):
    print(f"Ping job {dbbb.session}")


@app.middleware()
def db_connection(request: RequestAPIGateway, next_call) -> ResponseAPIGateway:
    print("Before request")
    response = next_call(request)
    print("After request")
    return response


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    return ResponseAPIGateway(exc.errors(), status_code=422)
