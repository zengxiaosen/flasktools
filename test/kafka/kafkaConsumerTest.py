import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from kafka.structs import TopicPartition
import time
import threading
class Kafka_consumer():

    def __init__(self, kafkahost, kafkaport, kafkatopic, groupid):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkaTopic = kafkatopic
        self.groupId = groupid
        self.consumer = KafkaConsumer(self.kafkaTopic,
                                      group_id=self.groupId,
                                      bootstrap_servers='{kafka_host}:{kafka_port}'.format(
                                          kafka_host=self.kafkaHost,
                                          kafka_port=self.kafkaPort
                                      ))


    def consume_data(self):
        try:
            for message in self.consumer:
                yield 'topic:%s; partition:%s; offset:%s; messageKey:%s; messageValue:%s' % (message.topic, message.partition, message.offset, message.key, message.value)
        except KeyboardInterrupt as e:
            print(e)

class ThreadConsumerGroup1(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
    def run(self):
        time.sleep(0.5)
        consumer = Kafka_consumer('127.0.0.1', 9092, "test", 'threadConsumerGroup1')
        message = consumer.consume_data()
        for i in message:
            print('Threadid: %s, %s' % (self.id, i))

class ThreadConsumerGroup2(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
    def run(self):
        consumer = Kafka_consumer('127.0.0.1', 9092, "test", 'threadConsumerGroup2')
        message = consumer.consume_data()
        for i in message:
            print('Threadid: %s, %s' % (self.id, i))

def main():
    t1 = ThreadConsumerGroup1(1)
    t2 = ThreadConsumerGroup2(2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

if __name__ == '__main__':
    main()