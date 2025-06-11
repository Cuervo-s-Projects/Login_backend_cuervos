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
http://127.0.0.1:5001/api/auth/login
```

```json
{
  "username": "luis",
  "email": "jluis@gmail.com",
  "password": "1234",
  "password_confirm": "1234"
}

```

### Sign Up

```bash
http://127.0.0.1:5001/api/auth/signup
```

```json
{
  "username": "luis",
  "password": "1234",
}
```
