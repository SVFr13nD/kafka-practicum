from confluent_kafka import Producer
conf = {"bootstrap.servers":"kps-grf1-lp1:9094"}
producer = Producer(conf)
for i in range(1, 21):
    producer.produce(
        topic="yandex_practicum_2",
        key=f"key-{i}",
        value=f"message-{i}"
    )
producer.flush()
print("20 messages sent!!!")