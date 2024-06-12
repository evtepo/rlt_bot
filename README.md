### Запуск проекта

1. Клонируйте репозиторий проекта:
     ```git clone https://github.com/Maslov300/Async-API_sprint1/```
2. Сделай сборку и поднятие контейнеров - docker-compose up --build
3. Зайдите внутрь контейнера ```docker exec -it <CONTAINER ID> bash``` (Узнать CONRAINER ID - ```docker ps```)
4. Ввести команды внутри контейнера:
     ```mongoimport --host localhost --port 27017 --username admin --password password123 --authenticationDatabase admin --db sampleDB --collection indexes --file sample_collection.metadata.json --jsonArray```
      
     ```bsondump --outFile=sample_collection.json sample_collection.bson```
   
     ```mongoimport --host localhost --port 27017 --username admin --password password123 --authenticationDatabase admin --db sampleDB --collection sample_collection --file sample_collection.json```
