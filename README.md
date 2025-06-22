# Login Service - EducaRural

Este servicio proporciona un endpoint de login para autenticar usuarios mediante Flask y MongoDB.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar servicio

```bash
python main.py
```

### Login

```bash
http://127.0.0.1:5001/api/login
```

```json
{
  "username": "luis",
  "password": "1234",
}

```

### Sign Up

```bash
http://127.0.0.1:5001/api/signup
```

```json
{
  "age": 20,
  "date_birth": "Tue, 17 Jun 2025 21:33:47 GMT",
  "email": "luis@gmail.com",
  "first_name": "Gonzales",
  "last_name": "luis",
  "password": 1234,
  "password_confirm": 1234,
  "username": "luis"
}
```
