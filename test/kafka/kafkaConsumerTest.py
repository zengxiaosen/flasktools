import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import time

class Kafka_consumer():

    def __init__(self, kafkahost, kafkaport, kafkatopic, groupid):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkaTopic = kafkatopic
        self.groupId = groupid
        self.consumer = KafkaConsumer(self.kafkaTopic, group_id=self.groupId,
                                      bootstrap_servers='{kafka_host}:{kafka_port}'.format(
                                          kafka_host=self.kafkaHost,
                                          kafka_port=self.kafkaPort
                                      ))

    def consume_data(self):
        try:
            for message in self.consumer:
                yield message
        except KeyboardInterrupt as e:
            print(e)


def main():
    consumer = Kafka_consumer('127.0.0.1', 9092, "test", 'test-python-test')
    message = consumer.consume_data()
    for i in message:
        print(i.value)

if __name__ == '__main__':
    main()