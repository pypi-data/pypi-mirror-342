# PyPQL

**PyPQL** is a lightweight, Pythonic interface for interacting with PostgreSQL databases. It allows developers to build readable, composable, and expressive queries in pure Python — no need to write raw SQL.

## Features

- Intuitive, fluent query syntax
- Built-in support for PostgreSQL async operations via `asyncpg`
- Easy integration with FastAPI and modern Python web frameworks
- Designed for clarity, flexibility, and developer happiness

## Installation

Install from PyPI:

```bash
pip install pypql
```

Or download the ZIP directly from the official website if preferred. GitHub repository coming soon.

## Example

```python
from pypql import Table

users = Table('users')
query = users.select().where(users.age > 18)
print(str(query))  # Outputs: SELECT * FROM users WHERE age > 18;
```

## License

MIT License — see [LICENSE](./LICENSE) for details.