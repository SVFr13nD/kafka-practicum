import json
from confluent_kafka import Consumer
conf = {
    "bootstrap.servers": "kps-grf1-lp1:9094",
    "group.id": "batch-message-consumer-group",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
    "session.timeout.ms": 6000,
}
consumer = Consumer(conf)
consumer.subscribe(["yandex_practicum_2"])
try:
    while True:
        messages = consumer.consume(
            num_messages=10,
            timeout=1.0
        )
        if not messages:
            continue
        error = False
        for msg in messages:
            if msg.error():
                print("Ошибка Kafka:", msg.error())
                error = True
                continue
            try:
                value = msg.value().decode("utf-8")
                # Десериализация JSON
                message = json.loads(value)
                print(
                    f"Получено сообщение: {message}, "
                    f"partition={msg.partition()}, offset={msg.offset()}"
                )
            except Exception as e:
                print("Ошибка десериализации:", e)
                error = True
                continue
        # Если batch обработался без ошибок
        if error == False:
            consumer.commit(asynchronous=False)
            print("Batch committed")
finally:
    consumer.close()