"""
summary: Testing some API code.

pip install fastapi
pip install uvicorn

docker build -t fastapitest .
docker run -d --name mycontainer -p 8000:8000 -t noctsol/fastapitest:00.02


/docs   for default swagger doc




"""
from typing import Union


from fastapi import FastAPI, Query
# import requests
import random
import helpu



app = FastAPI()


"""
Quick test end point for GET Method

Returns:
    string: returns some json
"""

validation =  Query(default=None, min_length=10)


@app.get("/")
async def hello():
    return "This is my localAPI"


@app.get("/my-first-api")
async def hello(name: str | None = validation):

    if name is None:
        text = 'Hello!'

    else:
        text = 'Hello ' + name + '!'

    return text

@app.get("/api/v1/testget")
async def testget(user_id: str | None = validation):

    rand_states = ["CO","AZ","NY"]
    rand_city = ["Glendale","Phoenix","Denver"]

    json_dict = {
        "request_id": helpu.guid(),
        "user_id" : user_id,
        "geo_info": {
            "city": random.choice(rand_states),
            "state": random.choice(rand_city)

        }
    }

    return json_dict



# if __name__ == '__main__':
#     app.run(debug=True, port=8000)
