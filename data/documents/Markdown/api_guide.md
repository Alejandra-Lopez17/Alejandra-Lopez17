---
api_version: 2.1.0
dependencies:
  - jwt
  - cryptography
---

# API Documentation

## Authentication Flow

```python
from api_client import Auth
auth = Auth()
token = auth.login(username, password)

