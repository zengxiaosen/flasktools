
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import time

class Kafka_producer():
    def __init__(self, kafkahost, kafkaport, kafkatopic):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkaTopic = kafkatopic
        self.producer = KafkaProducer(bootstrap_servers='{kafka_host}:{kafka_port}'.format(
            kafka_host=self.kafkaHost,
            kafka_port=self.kafkaPort
        ))

    def sendjsondata(self, params):
        try:
            params_message = json.dumps(params)
            producer = self.producer
            producer.send(self.kafkaTopic, params_message.encode('utf-8'))
            producer.flush()
        except KafkaError as e:
            print(e)


def main():
    ##生产模块
    producer = Kafka_producer("127.0.0.1", 9092, "test")

    for i in range(10000000000000):
        params = 'test---' + str(i)
        print(params)
        producer.sendjsondata(params)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
