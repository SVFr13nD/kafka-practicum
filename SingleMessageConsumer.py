from confluent_kafka import Consumer
# Конфигурация подключения к калстеру Кафки
conf = {
    "bootstrap.servers":"kps-grf1-lp1:9094", # Адрес брокера
    "group.id": "single-message-consumer-group", # Группа ид
    "auto.offset.reset": "earliest", # читать с самого раннего доступного оффсета
    "enable.auto.commit": True, # Авто коммит оффсета
    "session.timeout.ms": 6000, # Время после которого будет Тайм Аут
}
consumer = Consumer(conf)
consumer.subscribe(["yandex_practicum_2"]) # На какой топик подписаться
try:
    while True:
        # Получаем одно сообщение
        msg = consumer.poll(0.1) # вот тут читает сразу как только появляется новое сообщение, не ждет обработку батчами
        if msg is None:
            continue
        if msg.error():
            print(f"Ошибка: {msg.error()}")
            continue
        key = msg.key().decode("utf-8") if msg.key() else None
        value = msg.value().decode("utf-8") if msg.value() else None

        print(
            f"Получено сообщение: key={key}, value={value}, "
            f"partition={msg.partition()}, offset={msg.offset()}"
        )
finally:
    consumer.close()