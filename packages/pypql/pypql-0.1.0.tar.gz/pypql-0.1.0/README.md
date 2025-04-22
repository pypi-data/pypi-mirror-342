# PyPQL

**PyPQL** is a lightweight, Pythonic interface for interacting with PostgreSQL databases. It allows developers to build readable, composable, and expressive queries in pure Python — no need to write raw SQL.

## Features

- Intuitive, fluent query syntax
- Built-in support for PostgreSQL async operations via `asyncpg`
- Easy integration with FastAPI and modern Python web frameworks
- Designed for clarity, flexibility, and developer happiness

## Installation

PyPQL is not yet on PyPI. For now, you can clone the repo or download the ZIP:

```bash
git clone https://github.com/xAblivpypql.git
cd pypql
python setup.py install
```

## Example

```python
from pypql import Table

users = Table('users')
query = users.select().where(users.age > 18)
print(str(query))  # Outputs: SELECT * FROM users WHERE age > 18;
```

## License

MIT License — see [LICENSE](./LICENSE) for details.