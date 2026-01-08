# Semgrep Scan Results - Week 6

**Scan Date**: 2026-01-08
**Semgrep Version**: 1.146.0
**Rules Run**: 460
**Files Scanned**: 14
**Total Findings**: 6 (all blocking)

---

## Executive Summary

Semgrep identified **6 critical security vulnerabilities** across the backend and frontend code. All findings are marked as "blocking" and require immediate remediation.

---

## Detailed Findings

### 1. ❌ Wildcard CORS Configuration
**Severity**: HIGH
**Rule ID**: `python.fastapi.security.wildcard-cors.wildcard-cors`
**File**: [backend/app/main.py:24](backend/app/main.py#L24)

**Issue**: CORS policy allows any origin using wildcard `'*'`

```python
allow_origins=["*"],
```

**Impact**: Any website can make requests to your API, potentially exposing user data to malicious actors.

**Remediation**: Replace `["*"]` with a whitelist of allowed origins.

---

### 2. ❌ SQL Injection via SQLAlchemy text()
**Severity**: CRITICAL
**Rule ID**: `python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text`
**File**: [backend/app/routers/notes.py:71-79](backend/app/routers/notes.py#L71-L79)

**Issue**: User input directly interpolated into SQL query using `sqlalchemy.text()`

```python
sql = text(
    f"""
    SELECT id, title, content, created_at, updated_at
    FROM notes
    WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'
    ORDER BY created_at DESC
    LIMIT 50
    """
)
```

**Impact**: Attackers can execute arbitrary SQL queries, potentially accessing, modifying, or deleting database data.

**Remediation**: Use SQLAlchemy's parameterized queries with proper operators like `or_()`, `and_()`, and `like()`.

---

### 3. ⚠️ Arbitrary Code Execution via eval()
**Severity**: CRITICAL
**Rule ID**: `python.lang.security.audit.eval-detected.eval-detected`
**File**: [backend/app/routers/notes.py:104](backend/app/routers/notes.py#L104)

**Issue**: Direct evaluation of user input using `eval()`

```python
result = str(eval(expr))  # noqa: S307
```

**Impact**: Attackers can execute arbitrary Python code on the server, leading to complete system compromise.

**Remediation**: Remove this endpoint entirely. If eval-like functionality is needed, use a sandboxed expression evaluator with strict allowlisting.

---

### 4. ❌ Command Injection via subprocess with shell=True
**Severity**: CRITICAL
**Rule ID**: `python.lang.security.audit.subprocess-shell-true.subprocess-shell-true`
**File**: [backend/app/routers/notes.py:112](backend/app/routers/notes.py#L112)

**Issue**: Shell command execution with user input using `shell=True`

```python
completed = subprocess.run(cmd, shell=True, capture_output=True, text=True)  # noqa: S602,S603
```

**Impact**: Attackers can execute arbitrary shell commands, potentially leading to server compromise.

**Remediation**: Use `shell=False` with a list of arguments, or remove this debug endpoint entirely.

---

### 5. ⚠️ Dynamic URL Use with urllib
**Severity**: MEDIUM-HIGH
**Rule ID**: `python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected`
**File**: [backend/app/routers/notes.py:120](backend/app/routers/notes.py#L120)

**Issue**: Dynamic URL passed to `urllib.urlopen()`

```python
with urlopen(url) as res:  # noqa: S310
```

**Impact**: Attackers may be able to read arbitrary files on the server using `file://` URLs or perform SSRF attacks.

**Remediation**: Validate and sanitize URLs, or use the `requests` library with proper URL validation.

---

### 6. ❌ Cross-Site Scripting (XSS) via innerHTML
**Severity**: HIGH
**Rule ID**: `javascript.browser.security.insecure-document-method.insecure-document-method`
**File**: [frontend/app.js:14](frontend/app.js#L14)

**Issue**: User-controlled data rendered using `innerHTML`

```javascript
li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
```

**Impact**: Attackers can inject malicious scripts that execute in other users' browsers, potentially stealing cookies or session tokens.

**Remediation**: Use `textContent` instead of `innerHTML`, or properly sanitize HTML with a library like DOMPurify.

---

## Remediation Priority

### Must Fix (Assignment Requires 3+):
1. ✅ **SQL Injection** (CRITICAL) - [notes.py:71](backend/app/routers/notes.py#L71)
2. ✅ **Arbitrary Code Execution** (CRITICAL) - [notes.py:104](backend/app/routers/notes.py#L104)
3. ✅ **Command Injection** (CRITICAL) - [notes.py:112](backend/app/routers/notes.py#L112)

### Should Fix:
4. **Wildcard CORS** (HIGH) - [main.py:24](backend/app/main.py#L24)
5. **XSS via innerHTML** (HIGH) - [app.js:14](frontend/app.js#L14)

### Nice to Have:
6. **Dynamic urllib Use** (MEDIUM-HIGH) - [notes.py:120](backend/app/routers/notes.py#L120)

---

## Additional Notes

### Hardcoded Secret (Not Detected by Semgrep)
**File**: [backend/app/services/extract.py:13](backend/app/services/extract.py#L13)

```python
API_TOKEN = "sk_live_51HACKED_EXAMPLE_DO_NOT_USE_abcdefghijklmnopqrstuvwxyz"
```

While Semgrep didn't flag this, it's a critical security issue. The API token should be stored in environment variables.

---

## Next Steps

1. Fix the SQL injection vulnerability
2. Remove or secure the eval() endpoint
3. Remove or secure the subprocess endpoint
4. Update CORS configuration
5. Fix XSS vulnerability in frontend
6. Move hardcoded secrets to environment variables
7. Run tests to ensure fixes don't break functionality
8. Update [week6_writeup.md](week6_writeup.md) with detailed explanations
