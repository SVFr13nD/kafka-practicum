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