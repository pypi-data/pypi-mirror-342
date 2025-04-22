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
import asyncio
from pypql import tableobj

users = Table('user', 'password', 'database', 'host', 'table_name')
await users.connect()
await users.insert_single(['name'], ['Bobby']) # Inserts new row with value "Bobby" into name column of users table
await users.close()
```

## License

MIT License — see [LICENSE](./LICENSE) for details.