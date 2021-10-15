import random
import json

random.seed(444)
hats = {f"hat:{random.getrandbits(32)}": i for i in (
    {
        "color": "black",
        "price": 49.99,
        "style": "fitted",
        "quantity": 1000,
        "npurchased": 0,
    },
    {
        "color": "maroon",
        "price": 59.99,
        "style": "hipster",
        "quantity": 500,
        "npurchased": 0,
    },
    {
        "color": "green",
        "price": 99.99,
        "style": "baseball",
        "quantity": 200,
        "npurchased": 0,
    })
}


#hats = json.dumps(hats).encode('utf-8')
#print(hats)
import redis

r = redis.Redis(db=1)

with r.pipeline() as pipe:
    for h_id, hat in hats.items():
        pipe.hset(h_id, json.dumps(hat).encode('utf-8'))
    pipe.execute()

