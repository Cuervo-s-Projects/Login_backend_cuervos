# 📋 CHANGELOG

Este documento registra todos los cambios importantes realizados en el proyecto.

---

## [Unreleased]

### 🚀 Added
- Endpoint de registro de usuario con validación de correo electrónico.
- Generación de tokens JWT al iniciar sesión.

### 🛠️ Changed
- Refactorización de métodos en el repositorio.
- Mejoras en los modelos de MongoDB.

### 🐛 Fixed
- Error al enviar correos sin configuración SMTP.
- Fallo en la actualización de la información del usuario.

---

## [0.2.2] - 2025-06-23

### 🚀 Added
- Endpoint `/profile` protegido con JWT para obtener la identidad del usuario autenticado.

### 🛠️ Changed
- Refactor del sistema de autenticación para simplificar el uso del campo `identity` en JWT.

___

## [0.2.1] - 2025-06-22

### 🐛 Fixed
- Error al enviar correos electrónicos sin configuración adecuada.
- Problema en la actualización de datos del usuario.

---

## [0.2.0] - 2025-06-22

### 🎉 Added
- Implementación del flujo de verificación de correo electrónico utilizando `itsdangerous`.

### 🛠️ Changed
- Ajustes en las condiciones del registro de nuevos usuarios.

---

## [0.1.3] - 2025-06-17

### 🛠️ Changed
- Actualización de los códigos de estado HTTP en las respuestas JSON de los endpoints.

---

## [0.1.2] - 2025-06-11

### 🎉 Added
- Manejo de errores comunes: usuario no encontrado, contraseña incorrecta, y correos duplicados.
- Configuración de CORS para permitir conexión con frontend en React.
- Generación y entrega de tokens JWT.

---

## [0.1.1] - 2025-06-09

### 🎉 Added
- Documentación de endpoints mediante Swagger para pruebas y desarrollo.

---

## [0.1.0] - 2025-06-08

### 🎉 Added
- Estructura inicial del proyecto con Flask y MongoDB.
- Soporte para configuración externa mediante `.env` y `python-decouple`.

---

## 🔜 Próximamente

### 🧩 In development
- Sistema de roles de usuario (admin, user).
- Sistema de recuperación de contraseña vía correo electrónico.

