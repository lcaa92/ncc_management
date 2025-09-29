# NCC School Management System

A comprehensive Django-based school management system with REST API, designed for managing students, teachers, courses, payments, and leads.

## Features

- **Student Management**: Track student information, enrollment status, and group assignments
- **Teacher Management**: Manage teacher profiles, payment information, and class assignments
- **Course Management**: Handle products/courses with pricing and duration
- **Financial Management**: Track payments and teacher compensation
- **CRM**: Manage leads and potential students
- **REST API**: Full API with JWT authentication for frontend applications
- **Soft Delete**: All models support soft deletion with timestamps
- **Comprehensive Testing**: Full test coverage for models and API endpoints

## Technology Stack

- **Backend**: Django 5.2+ with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT tokens via Simple JWT
- **Package Management**: uv (Python 3.11)
- **Testing**: pytest with coverage
- **Code Quality**: flake8, black, isort
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## Project Structure

```
ncc_school_management/
├── api/                    # API views, serializers, and URLs
├── comercial/              # Product/course management
├── common/                 # Shared models and utilities
├── crm/                    # Customer relationship management
├── financial/              # Payment and financial tracking
├── management/             # Student, teacher, and class management
├── ncc_school_management/  # Django project settings
├── .github/workflows/      # CI/CD configuration
├── docker-compose.yml      # Docker services
├── Dockerfile             # Application container
├── Makefile               # Development utilities
└── pyproject.toml         # Project configuration
```

## Quick Start

### Prerequisites

- Python 3.11+
- uv package manager
- PostgreSQL 15+
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ncc_school_management
   ```

2. **Install dependencies**
   ```bash
   make install-dev
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Set up the database**
   ```bash
   make migrate
   ```

5. **Create a superuser**
   ```bash
   make superuser
   ```

6. **Start the development server**
   ```bash
   make runserver
   ```

The API will be available at `http://localhost:8000/api/`

### Using Docker

1. **Start all services**
   ```bash
   make docker-up
   ```

2. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## API Documentation

### Authentication

The API uses JWT authentication. To authenticate:

1. **Get tokens**
   ```bash
   curl -X POST http://localhost:8000/api/auth/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
   ```

2. **Use access token**
   ```bash
   curl -H "Authorization: Bearer <access_token>" \
     http://localhost:8000/api/students/
   ```

### Available Endpoints

- **Authentication**
  - `POST /api/auth/token/` - Get JWT tokens
  - `POST /api/auth/token/refresh/` - Refresh access token

- **Students**
  - `GET /api/students/` - List students
  - `POST /api/students/` - Create student
  - `GET /api/students/{id}/` - Get student details
  - `PUT /api/students/{id}/` - Update student
  - `DELETE /api/students/{id}/` - Delete student

- **Teachers**
  - `GET /api/teachers/` - List teachers
  - `POST /api/teachers/` - Create teacher
  - `GET /api/teachers/{id}/` - Get teacher details
  - `PUT /api/teachers/{id}/` - Update teacher
  - `DELETE /api/teachers/{id}/` - Delete teacher

- **Products**
  - `GET /api/products/` - List products
  - `POST /api/products/` - Create product
  - `GET /api/products/{id}/` - Get product details
  - `PUT /api/products/{id}/` - Update product
  - `DELETE /api/products/{id}/` - Delete product

- **Contracts**
  - `GET /api/contracts/` - List contracts
  - `POST /api/contracts/` - Create contract
  - `GET /api/contracts/{id}/` - Get contract details
  - `PUT /api/contracts/{id}/` - Update contract
  - `DELETE /api/contracts/{id}/` - Delete contract

- **Students Groups**
  - `GET /api/students-groups/` - List student groups
  - `POST /api/students-groups/` - Create student group
  - `GET /api/students-groups/{id}/` - Get group details
  - `PUT /api/students-groups/{id}/` - Update group
  - `DELETE /api/students-groups/{id}/` - Delete group

- **Lessons**
  - `GET /api/lessons/` - List lessons
  - `POST /api/lessons/` - Create lesson
  - `GET /api/lessons/{id}/` - Get lesson details
  - `PUT /api/lessons/{id}/` - Update lesson
  - `DELETE /api/lessons/{id}/` - Delete lesson

- **Payments**
  - `GET /api/payments/` - List payments
  - `POST /api/payments/` - Create payment
  - `GET /api/payments/{id}/` - Get payment details
  - `PUT /api/payments/{id}/` - Update payment
  - `DELETE /api/payments/{id}/` - Delete payment

- **Teacher Payments**
  - `GET /api/teacher-payments/` - List teacher payments
  - `POST /api/teacher-payments/` - Create teacher payment
  - `GET /api/teacher-payments/{id}/` - Get payment details
  - `PUT /api/teacher-payments/{id}/` - Update payment
  - `DELETE /api/teacher-payments/{id}/` - Delete payment

- **Leads**
  - `GET /api/leads/` - List leads
  - `POST /api/leads/` - Create lead
  - `GET /api/leads/{id}/` - Get lead details
  - `PUT /api/leads/{id}/` - Update lead
  - `DELETE /api/leads/{id}/` - Delete lead

### Filtering and Search

All list endpoints support:
- **Filtering**: Use query parameters (e.g., `?status=active`)
- **Search**: Use `search` parameter for text search
- **Ordering**: Use `ordering` parameter (e.g., `?ordering=-created_at`)
- **Pagination**: Results are paginated (20 items per page)

## Development

### Available Commands

```bash
# Development
make install-dev          # Install development dependencies
make migrate              # Run database migrations
make makemigrations       # Create new migrations
make runserver            # Start development server
make shell                # Start Django shell
make superuser            # Create superuser

# Testing
make test                 # Run all tests
make test-coverage        # Run tests with coverage
make test-fast            # Run tests without migrations

# Code Quality
make lint                 # Run flake8 linter
make format               # Format code with black and isort
make format-check         # Check code formatting

# Docker
make docker-build         # Build Docker images
make docker-up            # Start Docker services
make docker-down          # Stop Docker services
make docker-logs          # Show Docker logs

# Utilities
make clean                # Clean temporary files
make requirements         # Generate requirements files
```

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-coverage

# Run specific test file
uv run pytest api/tests.py

# Run tests with verbose output
uv run pytest -v
```

### Code Quality

The project uses several tools to maintain code quality:

- **flake8**: Linting with 120 character line limit
- **black**: Code formatting
- **isort**: Import sorting
- **pytest**: Testing framework
- **coverage**: Test coverage reporting

```bash
# Check code quality
make lint
make format-check

# Fix formatting issues
make format
```

## Models

### Core Models

- **Student**: Student information with status tracking
- **Teacher**: Teacher profiles with payment information
- **Product**: Courses/products with pricing
- **Contract**: Student enrollment in products
- **StudentsGroup**: Class groups with scheduled lessons
- **Lesson**: Individual class sessions
- **Payment**: General payments
- **TeacherPayments**: Teacher compensation
- **Lead**: Potential students/customers

### Common Features

All models include:
- **Timestamps**: `created_at`, `updated_at`
- **Soft Delete**: `deleted_at` field
- **Help Text**: All fields have descriptive help text
- **String Representation**: Meaningful `__str__` methods

## Deployment

### Production Settings

For production deployment:

1. **Set environment variables**
   ```bash
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ALLOWED_HOSTS=your-domain.com
   ```

2. **Use production database**
   ```bash
   DB_HOST=your-production-db-host
   DB_NAME=your-production-db-name
   ```

3. **Collect static files**
   ```bash
   make collectstatic
   ```

### Docker Production

```bash
# Build production image
docker build -t ncc-school-management:prod .

# Run with production settings
docker run -e DEBUG=False -e SECRET_KEY=your-key ncc-school-management:prod
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Check code quality (`make lint && make format-check`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the GitHub repository.
