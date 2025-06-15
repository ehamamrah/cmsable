# CMSable

A Django-based CMS project with PostgreSQL and Docker.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd cmsable
```

2. Create a `.env` file in the project root and add the following variables:
```
DEBUG=1
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://postgres:postgres@db:5432/cmsable
POSTGRES_DB=cmsable
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. Create the Django project (first time only):
```bash
docker-compose exec web django-admin startproject cmsable .
```

5. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

6. Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

The application will be available at http://localhost:8000

## Development

- The Django application runs on port 8000
- PostgreSQL runs on port 5432
- All data is persisted in a Docker volume

## Project Structure

```
cmsable/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
└── README.md
``` 