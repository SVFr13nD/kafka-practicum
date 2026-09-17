yandex_practicum_1
Устанавливаем Dockere: yum isntall docker 
Ставим как плагин Docker Compose, для этого выполнить следующие шаги: 
От сюда [страницу релизов Docker Compose на GitHub](https://github.com/docker/compose/releases) стягиваем docker-compose-linux-x86_64
Далее на хосте где установлен Docker выполняем следующие шаги: sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo mv /путь_куда_вы_сохранили/docker-compose-linux-x86_64 /usr/local/lib/docker/cli-plugins/docker-compose
И дать права на исполнение sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
проверить что все работает через systemctl status docker  и проверить что docker-compose --version  установлен и определяется
Теперь можно создавать docker-compose.yml
version: "3.9"
services:
  kafka-0:
    image: bitnamilegacy/kafka:3.4
    ports:
      - "9094:9094"
    environment:
      - KAFKA_ENABLE_KRAFT=yes
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_CFG_NODE_ID=0
      - KAFKA_CFG_PROCESS_ROLES=broker,controller
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka-0:9093,1@kafka-1:9093,2@kafka-2:9093
      - KAFKA_KRAFT_CLUSTER_ID=[тут нужно прописать ид кластера ]
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093,EXTERNAL://:9094
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka-0:9092,EXTERNAL://[HOST IP\HOST NAME]:9094 -- где [HOST IP\HOST NAME] прописать IP хоста или его имени 
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_INTER_BROKER_LISTENER_NAME=PLAINTEXT
    volumes:
      - kafka_0_data:/bitnami/kafka
  kafka-1:
    image: bitnamilegacy/kafka:3.4
    ports:
      - "9095:9094"
    environment:
      - KAFKA_ENABLE_KRAFT=yes
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_CFG_NODE_ID=1
      - KAFKA_CFG_PROCESS_ROLES=broker,controller
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka-0:9093,1@kafka-1:9093,2@kafka-2:9093
      - KAFKA_KRAFT_CLUSTER_ID=abcdefghijklmnopqrstuv
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093,EXTERNAL://:9094
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka-1:9092,EXTERNAL://[HOST IP\HOST NAME]:9095
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_INTER_BROKER_LISTENER_NAME=PLAINTEXT
    volumes:
      - kafka_1_data:/bitnami/kafka
  kafka-2:
    image: bitnamilegacy/kafka:3.4
    ports:
      - "9096:9094"
    environment:
      - KAFKA_ENABLE_KRAFT=yes
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_CFG_NODE_ID=2
      - KAFKA_CFG_PROCESS_ROLES=broker,controller
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka-0:9093,1@kafka-1:9093,2@kafka-2:9093
      - KAFKA_KRAFT_CLUSTER_ID=abcdefghijklmnopqrstuv
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093,EXTERNAL://:9094
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka-2:9092,EXTERNAL://[HOST IP\HOST NAME]:9096
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_INTER_BROKER_LISTENER_NAME=PLAINTEXT
    volumes:
      - kafka_2_data:/bitnami/kafka
  ui:
    image: provectuslabs/kafka-ui:v0.7.0
    ports:
      - "8080:8080"
    environment:
      - KAFKA_CLUSTERS_0_BOOTSTRAP_SERVERS=kafka-0:9092,kafka-1:9092,kafka-2:9092
      - KAFKA_CLUSTERS_0_NAME=kraft
    depends_on:
      - kafka-0
      - kafka-1
      - kafka-2
volumes:
  kafka_0_data:
  kafka_1_data:
  kafka_2_data:

Запускаем docker compose up -d
Проверяем что все заработало docker ps -a 
Будет что то типо такого: 
CONTAINER ID  IMAGE                                         COMMAND               CREATED         STATUS         PORTS                   NAMES
9e3c014bd8c9  repka.kaspi.kz/bitnamilegacy/kafka:3.4        /opt/bitnami/scri...  13 minutes ago  Up 13 minutes  0.0.0.0:9096->9094/tcp  kafka-course-kafka-2-1
98bbcde024a5  repka.kaspi.kz/bitnamilegacy/kafka:3.4        /opt/bitnami/scri...  13 minutes ago  Up 13 minutes  0.0.0.0:9095->9094/tcp  kafka-course-kafka-1-1
2f2a0f7b4f34  repka.kaspi.kz/bitnamilegacy/kafka:3.4        /opt/bitnami/scri...  13 minutes ago  Up 13 minutes  0.0.0.0:9094->9094/tcp  kafka-course-kafka-0-1
4ae33d30cb4c  repka.kaspi.kz/provectuslabs/kafka-ui:v0.7.0  /bin/sh -c java -...  13 minutes ago  Up 13 minutes  0.0.0.0:8080->8080/tcp  kafka-course-ui-1
В браузере указываем localhost:8080 в моем случае адрес виртуального хоста dns-name-host:8080
Открывает Kafka UI где видим инфу по кластеру и его состояние 
Доп проверка что все работает docker logs -f --tail 100 kafka-course-kafka-0-1