# CTO Classroom Booking

Aplicación web desarrollada con Django para gestionar la reserva de aulas en el centro CTO. Este proyecto forma parte del curso de desarrollo web impartido por Intecap.

## Funcionalidades

- Registro y autenticación de usuarios
- Visualización de aulas disponibles
- Reservas por fecha y hora
- Panel de administración para gestionar aulas y horarios

## Tecnologías

- Django 4.x
- SQLite (por defecto)
- Bootstrap (para el frontend)

## Instalación

```bash
git clone https://github.com/d6314x/reserva-aulas-django-app.git
cd reserva-aulas-django-app


python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

