import json
from confluent_kafka import Producer
class Message:
    def __init__(self, id, text):
        self.id = id
        self.text = text
conf = {
    "bootstrap.servers": "[HOST IP\HOST NAME]:9094",
    "acks": "all",
    "retries": 5
}
producer = Producer(conf)
for i in range(1, 21):
    message = Message(i, f"message-{i}")
    try:
        message_json = json.dumps({
            "id": message.id,
            "text": message.text
        })
        print("Отправляем:", message_json)
        producer.produce(
            topic="yandex_practicum_2",
            key=f"key-{i}",
            value=message_json
        )
    except Exception as error:
        print("Ошибка сериализации:", error)
producer.flush()
print("Messages sent!!!")
