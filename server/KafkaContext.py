import random
from kafka import KafkaProducer, KafkaClient
import time


def _get_kafka_producer_connection(host, port) -> KafkaProducer:
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers=f'{host}:{port}')
            break
        except Exception as e:
            print('producer failed to connect, retrying', e)
            time.sleep(5)

    print('producer connected', producer)
    return producer


def _get_kafka_client_connection(host, port) -> KafkaClient:
    while True:
        try:
            client = KafkaClient(bootstrap_servers=f'{host}:{port}')
            break
        except Exception as e:
            print('client failed to connect, retrying', e)
            time.sleep(5)

    print('client connected', client)
    return client


class KafkaContext:
    # 构建一个单例模式的producer

    def __init__(self, host='kafka', port=9092):
        self.__host = host
        self.__port = port
        self.__client = None
        self.__producer = None

    def __connect_client(self):
        self.__client = _get_kafka_client_connection(self.__host, self.__port)

    def __connect_producer(self):
        self.__producer = _get_kafka_producer_connection(self.__host, self.__port)

    def is_client_connected(self) -> bool:
        if self.__client is None:
            return False
        return self.__client.bootstrap_connected()

    def is_producer_connected(self) -> bool:
        return self.__producer is not None

    def add_topic(self, topic: str):
        if self.__client is None:
            self.__connect_client()
        self.__client.add_topic(topic)

    def send_msg(self, topic: str, msg: str) -> str:
        if self.__producer is None:
            self.__connect_producer()
        # convert msg to bytes
        msg_bytes = bytes(msg, encoding='utf-8')
        self.__producer.send(topic, msg_bytes)

        return msg


kafkaContext = KafkaContext()
