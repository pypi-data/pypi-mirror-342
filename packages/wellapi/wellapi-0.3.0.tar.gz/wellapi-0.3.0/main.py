from typing import Annotated

from wellapi import WellApi as FastAPI
from wellapi.params import Header

app = FastAPI(
    debug=True,
    servers=[{"url": "http://localhost:8000", "description": "Local server"}],
)




@app.get("/hello")
def hello(test: Annotated[list[str] | None, Header()]):
    """
    A simple hello world endpoint.
    :return:
    """
    print(test)
    return test
