# Code Patterns and Conventions

## Database Layer
- Custom exceptions: `DatabaseError`, `NotFoundError`
- SQLAlchemy 2.0+ async patterns
- Service layer pattern for business logic

## API Structure
- Routers in: `app/routers/`
- Services in: `app/services/`
- Global exception handlers in FastAPI apps

## Testing
- Test paths configured for weeks 1-8
- pytest with async test support
- TestClient for endpoint testing

## Error Handling
- Consistent error response format
- HTTP status codes aligned with REST best practices
