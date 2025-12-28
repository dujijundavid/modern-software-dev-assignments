# Security Considerations

Security patterns and best practices for AI-powered FastAPI applications.

---

## SQL Injection Prevention

### The Problem

SQL injection occurs when untrusted user input is concatenated into SQL queries:

```python
# ❌ VULNERABLE: Direct string concatenation
def get_note(id: str):
    query = f"SELECT * FROM notes WHERE id = {id}"
    # If id = "1; DROP TABLE notes--", disaster!
    cursor.execute(query)
```

### The Solution: Parameterized Queries

```python
# ✅ SECURE: Parameterized query
def get_note(id: int):
    query = "SELECT * FROM notes WHERE id = ?"
    cursor.execute(query, (id,))  # Automatically escaped
```

### With SQLAlchemy

```python
# ✅ SECURE: SQLAlchemy automatically parameterizes
from sqlalchemy import select

def get_note(id: int):
    stmt = select(Note).where(Note.id == id)
    result = session.execute(stmt).scalar_one()
    return result
```

### Anti-Patterns to Avoid

```python
# ❌ Don't: f-strings
query = f"SELECT * FROM notes WHERE title = '{title}'"

# ❌ Don't: String format
query = "SELECT * FROM notes WHERE title = '{}'".format(title)

# ❌ Don't: % formatting
query = "SELECT * FROM notes WHERE title = '%s'" % title

# ✅ Do: Parameterized queries
query = "SELECT * FROM notes WHERE title = ?"
cursor.execute(query, (title,))
```

---

## Input Validation

### Validate Length

```python
from fastapi import HTTPException

MAX_TITLE_LENGTH = 200
MAX_CONTENT_LENGTH = 10000

@app.post("/notes")
async def create_note(note: NoteCreate):
    if len(note.title) > MAX_TITLE_LENGTH:
        raise HTTPException(status_code=400, detail="Title too long")
    
    if len(note.content) > MAX_CONTENT_LENGTH:
        raise HTTPException(status_code=400, detail="Content too long")
    
    return await create_note(note)
```

### Validate Format

```python
from pydantic import BaseModel, validator, EmailStr

class NoteCreate(BaseModel):
    title: str
    content: str
    email: EmailStr  # Automatic email validation
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v
    
    @validator('content')
    def content_must_not_be_html(cls, v):
        if '<script>' in v.lower():
            raise ValueError('HTML tags not allowed')
        return v
```

### Sanitize Input

```python
import html

def sanitize_user_input(text: str) -> str:
    """Sanitize user input to prevent XSS"""
    # Escape HTML entities
    text = html.escape(text)
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    return text
```

---

## Secrets Management

### Environment Variables

```python
# .env file (NEVER commit this)
NOTION_TOKEN=secret_your_token_here
OPENAI_API_KEY=sk-your-key-here
```

### Load with python-dotenv

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not NOTION_TOKEN:
    raise ValueError("NOTION_TOKEN environment variable not set")
```

### .gitignore Configuration

```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Secrets
*.pem
*.key
secrets/
```

### For Production

```python
# Use secrets management service (AWS Secrets Manager, etc.)
# Or use Kubernetes secrets
# Or use vault
```

---

## CORS Configuration

### For Local Development

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### For Production

```python
import os

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Specific origins only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Specific methods
    allow_headers=["Content-Type", "Authorization"],  # Specific headers
)
```

---

## Logging Security

### What NOT to Log

```python
# ❌ Don't log sensitive data
logger.info(f"User {username} logged in with password {password}")
logger.debug(f"API call: {request_with_api_key}")

# ✅ Do log safely
logger.info(f"User {username[:3]}*** logged in")  # Partial redaction
logger.debug(f"API call to {endpoint}")  # No secrets
```

### Log Levels

```python
import logging

# DEBUG: Detailed information for diagnosing problems
logger.debug(f"Database query: {query}")

# INFO: Confirmation that things are working
logger.info(f"Note created: {note_id}")

# WARNING: Something unexpected happened
logger.warning(f"Rate limit exceeded for IP {ip_address}")

# ERROR: Serious problem
logger.error(f"Failed to connect to database: {e}")

# CRITICAL: Critical error
logger.critical(f"Application cannot start: {e}")
```

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

# Structured logs are easier to parse and analyze
logger.info(
    "note_created",
    note_id=note.id,
    user_id=user.id,
    timestamp=note.created_at,
)
```

---

## Error Message Security

### Generic Messages to Clients

```python
from fastapi import HTTPException

# ❌ Don't reveal internal details
try:
    result = database.query(query)
except DatabaseError as e:
    raise HTTPException(
        status_code=500,
        detail=f"Database error: {e}"  # Exposes internal state!
    )

# ✅ Do use generic messages
try:
    result = database.query(query)
except DatabaseError as e:
    logger.error(f"Database error: {e}")  # Log details internally
    raise HTTPException(
        status_code=500,
        detail="An error occurred processing your request"
    )
```

### Custom Exception Handlers

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    """Generic 404 handler"""
    return JSONResponse(
        status_code=404,
        content={"error": "Resource not found"}
    )

@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    """Generic database error handler"""
    logger.error(f"Database error: {exc}")  # Log details
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

---

## API Security

### HTTP Status Codes

| Status | Usage | Example |
|--------|-------|---------|
| 200 | Success | Note retrieved |
| 201 | Created | Note created |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Error | Server error |

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/extract")
@limiter.limit("10/minute")  # 10 requests per minute
async def extract_items(request: Request):
    return await extract_action_items()
```

### Authentication (Future)

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.post("/protected")
async def protected_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user = authenticate_token(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {"message": "Access granted"}
```

---

## File Upload Security

### Validate File Types

```python
ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf"}

@app.post("/upload")
async def upload_file(file: UploadFile):
    # Check file extension
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename")
    
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {ext} not allowed"
        )
    
    # Check file size (in memory first)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(status_code=400, detail="File too large")
    
    return {"filename": file.filename}
```

### Sanitize Filenames

```python
import re

def sanitize_filename(filename: str) -> str:
    """Remove dangerous characters from filename"""
    # Remove path separators
    filename = os.path.basename(filename)
    
    # Remove non-alphanumeric (except dash, underscore, dot)
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    
    return filename
```

---

## Dependency Vulnerabilities

### Regular Updates

```bash
# Check for vulnerabilities
pip-audit

# Update dependencies
poetry update

# Check outdated packages
poetry show --outdated
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-r", "week1/app", "week2/app"]
```

---

## Security Checklist

### Before Deployment

- [ ] No secrets in code or repository
- [ ] All inputs validated and sanitized
- [ ] Parameterized queries for all database access
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Error messages don't leak information
- [ ] Logging doesn't include sensitive data
- [ ] Dependencies updated and scanned
- [ ] File uploads validated
- [ ] HTTPS enforced in production

### Regular Reviews

- [ ] Run `pip-audit` monthly
- [ ] Review access logs
- [ ] Update dependencies regularly
- [ ] Review error logs for attack patterns
- [ ] Security audit before major releases
