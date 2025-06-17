# CMSable

A Django-based Content Management System with PostgreSQL, fully dockerized and focused on best practices for UI and UX.

## Prerequisites

- Docker
- Docker Compose
- Make (optional, but recommended)

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd cmsable
```

2. Build and start the containers:
```bash
make build
make up
```

3. Run migrations:
```bash
make migrate
```

4. Seed the database with initial data:
```bash
make seed
```

The application will be available at `http://localhost:8000`

## Available Commands

### Docker Commands

- `make build` - Build Docker images
- `make up` - Start containers in detached mode
- `make down` - Stop and remove containers
- `make restart` - Restart containers
- `make logs` - View container logs
- `make ps` - List containers

### Django Commands

- `make shell` - Open Django shell
- `make migrate` - Run database migrations
- `make makemigrations` - Create new migrations
- `make superuser` - Create a superuser
- `make seed` - Seed the database with initial data [This will also fetch 30 videos from thmanyah youtube channel]

## Default Superuser

After running `make seed`, a superuser is created with the following credentials:

- Email: test@test.com
- Username: testuser
- Password: TestProject2025
- Role: admin


## Development

1. Start the development environment:
```bash
make up
```

2. View logs:
```bash
make logs
```

3. Access Django shell:
```bash
make shell
```

4. Create a new superuser:
```bash
make superuser
```

## Database

The project uses PostgreSQL 17. The database is automatically configured through Docker Compose.

## API Endpoints [Postman Collection Available]

### Authentication API
- `POST /auth/token/` You will need to pass username and password on Body

### Posts API
- `GET /api/v1/posts/discovery/` - Public endpoint to discover posts


> **Note:** All API endpoints below require authentication. Include the Bearer token in the Authorization header:
> ```
> Authorization: Bearer <your_token>
> ```

- `GET /api/v1/posts/` - List all posts (authenticated)
- `POST /api/v1/posts/` - Create a new post (requires admin/content manager/editor role)
- `GET /api/v1/posts/{id}/` - Get post details
- `PUT /api/v1/posts/{id}/` - Update a post
- `DELETE /api/v1/posts/{id}/` - Delete a post
- `POST /api/v1/posts/auto-create/` This API require only link and category_ids, It will automatically fetch details from shared link [**Only youtube supported for now**]
### Categories API
- `GET /api/v1/posts/categories/` - List active categories

## Features

- User authentication and authorization
- Role-based access control
- Post management with categories
- Automated post creation from video links
- RESTful API endpoints
- Dockerized development environment