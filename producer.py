from confluent_kafka import Producer
conf = {"bootstrap.servers":"kps-grf1-lp1:9094"}
producer = Producer(conf)
producer.produce(
    topic="yandex_practicum_2",
    key="key-1",
    value="message-1"
)
producer.flush()
print("Message sent!!!")