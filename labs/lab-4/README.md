# Лабораторная работа №4

## Дополнительное задание

### Введение 

В данной лабораторной работе была првоедена работа с секретами для CI/CD

### Создание секретов

В качестве утилиты для создания и использования секретов был использован Vault
![image](https://github.com/user-attachments/assets/b88d6f65-9d13-4e26-bd0e-70476575aa67)

Данная утилита была настроена на локальном хосте по адресу 127.0.0.1:8201
![image](https://github.com/user-attachments/assets/8c2a87cf-5891-49c5-8316-6784b35133ac)

### Связь с GitHub

Чтобы наш CI/CD узнал про секреты, которые локально храняться на моей машине, github должен знать белый IP-адрес, на который можно отправлять GET запросы на получением секретов./
Чтобы получить белый IP-адрес было использовано тунелирование с помощью [VK Tunnel](https://dev.vk.com/ru/libraries/tunnel) (как альтернатива ngrok).

![image](https://github.com/user-attachments/assets/9eb80bdf-b420-4c6d-9b32-7c212a3346ff)

Перейдя по данному адресу, был добавлен тестовый секрет foo="hello" по адресу secret/hello

![image](https://github.com/user-attachments/assets/ff3f72e4-6d8c-4de8-918a-02e098ca1de4)

### CI/CD

Для данного задания был написан простенький CI/CD файл для тестирования секретов.

```
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Install Vault CLI
        run: |
          sudo snap install vault
      - name: Retrieve secrets from Vault
        run: |
          export VAULT_ADDR="https://user181687390-tqqghisk.tunnel.vk-apps.com/"
          export VAULT_TOKEN=${{ secrets.VAULT_TOKEN }}
          export SECRET=$(vault kv get -field=foo secret/hello)
          echo "Этот секрет можно было бы использовать например для подключения к БД по адресу из другого тунеля, но...."
          echo "Hello"
          echo $SECRET
        
      - name: Deploy
        run: |
          echo "Секреты с локалхоста доехали всё супер"
```

Пайплайн обращается к секретам, установленным в GitHub репозитории:
* secrets.VAULT_ADDR
* secrets.VAULT_TOKEN

### Итог

В итоге данный CI/CD файл подтягивает секреты с локального хоста по белому IP-адресу и может использовать их как вздумается девопсу.

![image](https://github.com/user-attachments/assets/51356e0d-48b4-4b30-b433-3a0f9ce8d52e)

Во вкладке Retrieve secrets from Vault можно заметить, что был выведен наш секрет (конечно не стоит выводить секреты в логи, иначе никакие это не секреты, но в данном случае секрет был выведен только для того, чтобы проверить, что он действительно подтянулся)
