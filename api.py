from datetime import datetime
from pydantic import BaseModel

from KafkaContext import kafkaContext
from fastapi import FastAPI

app = FastAPI()


class Message(BaseModel):  # 继承了BaseModel，定义了People的数据格式
    topic: str
    msg: str


@app.get("/")
def read_root():
    return {"time": datetime.now(), "status": "ok"}


@app.get("/health/client")
def health_client():
    return {
        "data": kafkaContext.is_client_connected()
    }


@app.get("/health/producer")
def health_producer():
    return {
        "data": kafkaContext.is_producer_connected()
    }


@app.get("/producer/add_topic/{topic}")
def add_topic(topic: str):
    kafkaContext.add_topic(topic)
    return {
        "status": "ok",
        "data": topic
    }


@app.post("/producer/send_msg")
def send_msg(message: Message):
    return {
        "status": "ok",
        "data": kafkaContext.send_msg(message.topic, message.msg)
    }
