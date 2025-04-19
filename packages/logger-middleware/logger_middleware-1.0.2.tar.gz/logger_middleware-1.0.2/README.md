## Функционал
Логирование любого действия сервиса на FastAPI с помощью middleware

## Примеры использования
### Настройки env переменных
```env
APP_VERSION=dev или test или prod
```
Если запускаете локльно(APP_VERSION=dev), то нужно еще запустить сервис [маркетинга](https://github.com/profcomff/marketing-api) на localhost:port и прописать этот порт на котором запущен в env своего сервиса
```env
MARKETING_PORT=8080(либо ваш порт)
```
Или перед запуском сервиса в терминале
```env
export MARKETING_PORT=8080(либо ваш порт)
```

### FastAPI
```python
pip install logger_middleware
```
```python
from fastapi import FastAPI
from logger_middleware import LoggerMiddleware

app = FastAPI()

app.add_middleware(LoggerMiddleware, sevice_id = 0)
```


## Contributing 
 - Основная [информация](https://github.com/profcomff/.github/wiki/%255Bdev%255D-Backend-%25D1%2580%25D0%25B0%25D0%25B7%25D1%2580%25D0%25B0%25D0%25B1%25D0%25BE%25D1%2582%25D0%25BA%25D0%25B0) по разработке наших приложений

 - [Ссылка](https://github.com/profcomff/auth-lib/blob/main/CONTRIBUTING.md) на страницу с информацией по разработке auth-lib
