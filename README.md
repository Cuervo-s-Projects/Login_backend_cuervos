# Login Service - EducaRural

Este servicio proporciona un endpoint de login para autenticar usuarios mediante Flask y MongoDB.

---

## Tecnologías utilizadas

- **Flask**
- **MongoDB**
- **JWT (JSON Web Tokens)**
- **Flask-Mail**
- **Swagger (Flasgger)**

---
## Variables de entorno

Crea un archivo .env con las siguientes variables:
```env
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=tu_password

SECRET_KEY=tu_clave_secreta
JWT_SECRET_KEY=tu_clave_secreta
```
---

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar servicio

```bash
python main.py
```
---
## Documentación interactiva

Una vez corriendo el servidor, accede a la documentación:
```bash
http://127.0.0.1:5000/apidocs
```
---
## Endpoints

### Login

```bash
POST /api/login
```

```json
{
  "username": "luis",
  "password": "1234",
}

```
---
### Sign Up POST

```bash
POST /api/signup
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
---
### Verificación de correo electrónico

```bash
GET /api/verify-email/{token}
```

---
### Obtener perfil de usuario

```bash
GET /api/profile
Authorization: Bearer <TOKEN>
```
#### Respuesta:
```json
{
  "_id": "6858a9d9c1e99b58e1659dc5",
  "age": 20,
  "date_birth": "Tue, 17 Jun 2025 21:33:47 GMT",
  "first_name": "Gonzales",
  "last_name": "luis",
  "username": "luis"
}
```
---
## Estructura del proyecto
```
Login/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   ├── repository.py
│   ├── routes.py
│   ├── services.py
│   └── utils.py
├── config/
│   ├── __init_.py
│   └── db.py
├── tests/
│   ├── __init_.py
│   ├── conftest.py
│   ├── test_email.py
│   └── test_jwt.py
├── swagger/
│   ├── login.yaml
│   ├── profile.yaml
│   ├── signup.yaml
│   └── verify_email.yaml
├── .env
├── main.py
├── config.py
└── requirements.txt

```