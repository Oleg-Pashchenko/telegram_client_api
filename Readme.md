```python:
host: http://telegram.api.olegpash.tech
```

#### Methods:
- ```/send-telegram-code/```
- ```/auth/```
- ```/auth-with-2fa/```
- ```/get-updates/```

---

#### Answer structure: 
```json
{
  "status": true | false,
  "answer": {
    "param1": "v1",
    ...
  },
  "execution_time": 1.23
}

```

Если status - false, значит выводим ошибку, она возвращается в ```['answer']['error']```


---

###### Описание метода ``/send-telegram-code/``:
Вызывать в самом начале, нужен для получения смс кода и регистрации api_id, api_hash в системе. В ответ возвращает session_name. 

Request data:
```
{
    api_id: int
    api_hash: str
    phone: str
}
```

Response data:
```json
{
  "status": true,
  "answer": {
    "session_name": "47398448"
  },
  "execution_time": 1.52
}
```
---

###### Описание метода ``/auth/``:
Вызывать вторым. Работает в случае если у человека нет 2FA кода. 

Request data:
```
{
    session_name: str
    sms_code: str
}
```

Response data:
```json
{
  "status": true,
  "answer": true,
  "execution_time": 1.52
}
```
---
###### Описание метода ``/auth-with-2fa/``:
Вызывать третьим при необходимости. Работает в случае если у человека есть 2FA код. 

Request data:
```
{
    session_name: str
    secret_password: str
}
```

Response data:
```json
{
  "status": true,
  "answer": true,
  "execution_time": 1.52
}
```
---


###### Описание метода ``/get-updates/``:
Вызывать когда авторизация уже пройдена раз в минуту. 

Request data:
```
{
    session_name: str
}
```

Response data:
```json
{
  "messages": [],
  "calls": [
    {"group_name":  "Prosto Group", "group_image":  ""}
  ]
}
```
---




