Как запустить см предыдущий README по яндкес практики 1 ( README_yandex_practicum_1.md)

ШАГ 1 Создание топика 
Команда выглядит так docker exec -it kafka-course-kafka-0-1 kafka-topics.sh --create --topic yandex_practicum_2 --bootstrap-server kafka-0:9092 --partitions 3 --replication-factor 2

Где 
kafka-course-kafka-0-1 - имя контейнера 
kafka-topics.sh - кафка скрипт по управлению топиками 
--create - команда создать 
--topic yandex_practicum_2  топик с название yandex_practicum_2
--bootstrap-server kafka-0:9092 внутренний адрес брокера 
--partitions 3 количество партиций 
--replication-factor 2 количество реплик 

ШАГ 2 Создание продюсера 
Листинг взять из примера лекции и добавлен в producer.py 
Принци работы продюсера, отправляет 20 сообщений в топик yandex_practicum_2 но перед этим происходит серелизация в JSON
Сообщение содержит два поля id и text
Которые серелизуюцая в :
{
    "id": 1,
    "text": "message-1"
}
Так выглядит обработка ошибки серилизации: 
except Exception as error:
    print("Ошибка сериализации:", error)
Так же было настроено: 
acks: all — Producer ждёт подтверждения успешной записи сообщения для повышения надежности доставки сообщений 
и retries: 5 если во время произошла ошибка, консюмер потоврит отправку сообщения 
flush() ожидает завершения отправки сообщений
После этого в консоль выводится:
Messages sent!!!

ЛОГ работы продюсера: 
C:\kafka-practicum\producer.py 
Отправляем: {"id": 1, "text": "message-1"}
Отправляем: {"id": 2, "text": "message-2"}
Отправляем: {"id": 3, "text": "message-3"}
Отправляем: {"id": 4, "text": "message-4"}
Отправляем: {"id": 5, "text": "message-5"}
Отправляем: {"id": 6, "text": "message-6"}
Отправляем: {"id": 7, "text": "message-7"}
Отправляем: {"id": 8, "text": "message-8"}
Отправляем: {"id": 9, "text": "message-9"}
Отправляем: {"id": 10, "text": "message-10"}
Отправляем: {"id": 11, "text": "message-11"}
Отправляем: {"id": 12, "text": "message-12"}
Отправляем: {"id": 13, "text": "message-13"}
Отправляем: {"id": 14, "text": "message-14"}
Отправляем: {"id": 15, "text": "message-15"}
Отправляем: {"id": 16, "text": "message-16"}
Отправляем: {"id": 17, "text": "message-17"}
Отправляем: {"id": 18, "text": "message-18"}
Отправляем: {"id": 19, "text": "message-19"}
Отправляем: {"id": 20, "text": "message-20"}
Messages sent!!!
Process finished with exit code 0

ШАГ 2 создание Консюмера

Было создано два консюмера SingleMessageConsumer.py и batch_message_consumer.py

SingleMessageConsumer.py его предназначение считывать по одному сообщению, обрабатывать его и коммитить оффсет автоматически. 
batch_message_consumer.py его преназначение считывать минимум по 10 сообщений за один poll, обрабатывать сообщения в цикле и один раз коммитить оффсет после обработки пачки.
Листинг кода взят с лекции

Как работает SingleMessageConsumer.py 
Консюмер п получает сообщения из топика `yandex_practicum_2` по одному, десериализует их из JSON и выводит полученные данные в консоль.
Подключается консбюмер под группой "single-message-consumer-group" и с выключенным "enable.auto.commit"

Для получения сообщений используется метод `poll()`
Если за указанное время сообщение не было получено:
Консюмер продолжает ожидать следующие сообщения.
Если Кафка возвращает ошибку, сообщение об ошибке выводится в консоль.
После этого Консюмер не завершает работу, а продолжает получать следующие сообщения.

Лоог работы консюмера SingleMessageConsumer.py 
C:\kafka-practicum\SingleMessageConsumer.py 
Получено сообщение: {'id': 4, 'text': 'message-4'}, partition=1, offset=42
Получено сообщение: {'id': 11, 'text': 'message-11'}, partition=1, offset=43
Получено сообщение: {'id': 20, 'text': 'message-20'}, partition=1, offset=44
Получено сообщение: {'id': 1, 'text': 'message-1'}, partition=2, offset=93
Получено сообщение: {'id': 3, 'text': 'message-3'}, partition=2, offset=94
Получено сообщение: {'id': 6, 'text': 'message-6'}, partition=2, offset=95
Получено сообщение: {'id': 7, 'text': 'message-7'}, partition=2, offset=96
Получено сообщение: {'id': 9, 'text': 'message-9'}, partition=2, offset=97
Получено сообщение: {'id': 12, 'text': 'message-12'}, partition=2, offset=98
Получено сообщение: {'id': 18, 'text': 'message-18'}, partition=2, offset=99
Получено сообщение: {'id': 2, 'text': 'message-2'}, partition=0, offset=126
Получено сообщение: {'id': 5, 'text': 'message-5'}, partition=0, offset=127
Получено сообщение: {'id': 8, 'text': 'message-8'}, partition=0, offset=128
Получено сообщение: {'id': 10, 'text': 'message-10'}, partition=0, offset=129
Получено сообщение: {'id': 13, 'text': 'message-13'}, partition=0, offset=130
Получено сообщение: {'id': 14, 'text': 'message-14'}, partition=0, offset=131
Получено сообщение: {'id': 15, 'text': 'message-15'}, partition=0, offset=132
Получено сообщение: {'id': 16, 'text': 'message-16'}, partition=0, offset=133
Получено сообщение: {'id': 17, 'text': 'message-17'}, partition=0, offset=134
Получено сообщение: {'id': 19, 'text': 'message-19'}, partition=0, offset=135


Что же касается консюмера batch_message_consumer.py

batch_message_consumer.py получает сообщения из топика `yandex_practicum_2` пачками, консюмер подключается под своей отдельной группой:batch-message-consumer-group , десериализует каждое сообщение из JSON и выводит полученные данные в консоль.
В отличие от `SingleMessageConsumer`, который получает по одному сообщению через `poll()`, Batch Consumer использует метод `consume()`:
вот кусочек кода: 
messages = consumer.consume(
    num_messages=10,
    timeout=1.0
)
`num_messages=10` означает, что Консюмер может получить за один вызов до 10 сообщений.
`timeout=1.0` означает, что Консюмер ожидает сообщения до одной секунды.
Если сообщения не были получены:
Коонсюмер продолжает ожидать следующую пачку.
Для каждого сообщения выполняется проверка:
Если Кафка возвращает ошибку, она выводится в консоль.
Переменная `error` устанавливается в `True`, чтобы после обработки пачки не выполнять commit при наличии ошибок.
Консюмер при этом продолжает работать.
 
Лог работы консюмера batch_message_consumer.py
олучено сообщение: {'id': 1, 'text': 'message-1'}, partition=2, offset=93
Получено сообщение: {'id': 3, 'text': 'message-3'}, partition=2, offset=94
Получено сообщение: {'id': 6, 'text': 'message-6'}, partition=2, offset=95
Получено сообщение: {'id': 7, 'text': 'message-7'}, partition=2, offset=96
Получено сообщение: {'id': 9, 'text': 'message-9'}, partition=2, offset=97
Получено сообщение: {'id': 12, 'text': 'message-12'}, partition=2, offset=98
Получено сообщение: {'id': 18, 'text': 'message-18'}, partition=2, offset=99
Получено сообщение: {'id': 4, 'text': 'message-4'}, partition=1, offset=42
Получено сообщение: {'id': 11, 'text': 'message-11'}, partition=1, offset=43
Получено сообщение: {'id': 20, 'text': 'message-20'}, partition=1, offset=44
Batch committed