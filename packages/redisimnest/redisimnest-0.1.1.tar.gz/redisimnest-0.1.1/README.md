# Redisimnest _(Redis Imaginary Nesting)_
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**_A sophisticated, prefix-based Redis key management system with customizable, nestable clusters, dynamic key types, and parameterized prefix resolution. Ideal for organizing application state and simplifying Redis interactions in complex systems._**

## Table of Contents
- Installation
- Usage
- Features
- Configuration
- Contributing
- License

## Installation

You can install Redisimnest via pip:

``` bash
pip install redisimnest
```

Alternatively, install from source:
``` bash
git clone https://github.com/yourusername/redisimnest.git
cd redisimnest
pip install .
```
## Usage

Here's a basic example of how to use Redisimnest in your project:
``` python
from asyncio import run
from redisimnest import BaseCluster, Key
from redisimnest.utils import RedisManager

# Define structured key clusters
class App:
    __prefix__ = 'app'
    __ttl__ = 80
    tokens = Key('tokens', default=[])
    pending_users = Key('pending_users')

class User:
    __prefix__ = 'user:{user_id}'
    __ttl__ = 120
    age = Key('age', 0)
    name = Key('name', "Unknown")

class RootCluster(BaseCluster):
    __prefix__ = 'root'
    app = App
    user = User
    project_name = Key('project_name')

# Initialize cluster
redis = RedisManager.get_client()
root = RootCluster(redis_client=redis)

# Use like a high-level Redis interface
async def main():
    await root.project_name.set("RedisimNest")
    await root.user(1).age.set(30)
    print(await root.user(1).age.get())           # ➜ 30
    await root.app.tokens.set(["token1", "token2"])
    await root.app.tokens.expire(60)
    await root.app.clear()                        # Clear all app-prefixed keys

run(main())
```



## Features

- **Prefix-Based Cluster Management:** _Organize Redis keys with flexible, dynamic prefixes._
- **Support for Parameterized Keys:**_ Create keys with placeholders that can be dynamically replaced._
- **TTL Management:** _Automatic and manual control over key TTLs._
- **Cluster Hierarchies:** _Nested clusters with inherited parameters._
- **Typed Key Classes**: _Use Python types to define and validate Redis key value structures._
- **Auto-Binding & Dynamic Access:**_ Smart access to nested clusters and runtime bindings._
- **Command Dispatching:** _Type-aware command routing with serialization/deserialization support._

## Configuration

Redisimnest allows you to customize the following settings:

- `REDIS_HOST`: Redis server hostname (default: localhost).
- `REDIS_PORT`: Redis server port (default: 6379).
- `REDIS_USERNAME` / REDIS_PASS: Optional authentication credentials.
- `REDIS_DELETE_CHUNK_SIZE`: Number of items deleted per operation (default: 50).

You can set these via environment variables or within your settings.py:
``` python
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DELETE_CHUNK_SIZE = 50
```

To apply your custom settings file add ```USER_SETTINGS_FILE=./your_settings.py``` path to .env file

## Contributing

We welcome contributions! To contribute:

**1**. Fork the repository.
**2**. Create a new branch (`git checkout -b feature-branch`).
**3**. Make your changes.
**4**. Write tests for your changes.
**5**. Submit a pull request.

Please ensure all tests pass before submitting your PR.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
