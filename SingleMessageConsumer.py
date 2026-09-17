import json
from confluent_kafka import Consumer
conf = {
    "bootstrap.servers": "[HOST IP\HOST NAME]:9094",
    "group.id": "single-message-consumer-group",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
    "session.timeout.ms": 6000,
}
consumer = Consumer(conf)
consumer.subscribe(["yandex_practicum_2"])
try:
    while True:
        msg = consumer.poll(0.1)
        if msg is None:
            continue
        if msg.error():
            print("Ошибка Kafka:", msg.error())
            continue
        try:
            value = msg.value().decode("utf-8")
            # Десериализация JSON
            message = json.loads(value)
            print(
                f"Получено сообщение: {message}, "
                f"partition={msg.partition()}, offset={msg.offset()}"
            )
            # Ручной commit
            consumer.commit(asynchronous=False)
        except Exception as error:
            print("Ошибка десериализации:", error)
            continue
finally:
    consumer.close()
