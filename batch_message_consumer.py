from confluent_kafka import Consumer
# Конфигурация подключения к калстеру Кафки
conf = {
    "bootstrap.servers":"kps-grf1-lp1:9094", # Адрес брокера
    "group.id": "batch-message-consumer-group", # Группа ид
    "auto.offset.reset": "earliest", # читать с самого раннего доступного оффсета
    "enable.auto.commit": True, # Авто коммит оффсета
    "session.timeout.ms": 6000, # Время после которого будет Тайм Аут
}
consumer = Consumer(conf)
consumer.subscribe(["yandex_practicum_2"])
try:
    while True:
        # Получаем пачку до 10 сообщений
        messages = consumer.consume( # Собираем пачку до 10 смс и после этого только комминтим
            num_messages=10,
            timeout=1.0
        )
        if not messages:
            continue

        print(f"Получен batch: {len(messages)} сообщений")
        for msg in messages:
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