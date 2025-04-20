# Redisimnest _(Redis Imaginary Nesting)_

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**_A sophisticated, prefix-based Redis key management system with customizable, nestable clusters, dynamic key types, and parameterized prefix resolution. Ideal for organizing application state and simplifying Redis interactions in complex systems._**

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Detailed Information](#detailed-information)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features <a name="features"></a>

- **`Prefix-Based Cluster Management:`** _Organize Redis keys with flexible, dynamic prefixes._
- **`Support for Parameterized Keys:`**_ Create keys with placeholders that can be dynamically replaced._
- **`TTL Management:`** _Automatic and manual control over key TTLs._
- **`Cluster Hierarchies:`** _Nested clusters with inherited parameters._
- **`Auto-Binding & Dynamic Access:`**_ Smart access to nested clusters and runtime bindings._
- **`Command Dispatching:`** _Type-aware command routing with serialization/deserialization support._

## Installation <a name="installation"></a>

You can install Redisimnest via pip:

### Install via pip:
```bash
pip install redisimnest
```

### Install from source:
```bash
git clone https://github.com/yourusername/redisimnest.git
cd redisimnest
pip install .
```

## Usage <a name="usage"></a>

Here’s a basic example of how to use Redisimnest in your project:

```python
from asyncio import run
from redisimnest import BaseCluster, Key
from redisimnest.utils import RedisManager

# Define structured key clusters with dynamic TTL and parameterized keys
class App:
    __prefix__ = 'app'
    __ttl__ = 80  # TTL for keys within this cluster
    tokens = Key('tokens', default=[])
    pending_users = Key('pending_users')

class User:
    __prefix__ = 'user:{user_id}'  # Parameterized prefix for user-specific keys
    __ttl__ = 120  # TTL for user keys
    age = Key('age', 0)
    name = Key('name', "Unknown")

class RootCluster(BaseCluster):
    __prefix__ = 'root'
    app = App
    user = User
    project_name = Key('project_name')

# Initialize the Redis client and root cluster
redis = RedisManager.get_client()
root = RootCluster(redis_client=redis)

# Async operation: Setting and getting keys
async def main():
    await root.project_name.set("RedisimNest")
    await root.user(1).age.set(30)
    print(await root.user(1).age.get())  # ➜ 30
    await root.app.tokens.set(["token1", "token2"])
    await root.app.tokens.expire(60)
    await root.app.clear()  # Clear all keys under the 'app' prefix

run(main())
```

## Detailed Information <a name="detailed-information"></a>

### Cluster and Key: Advanced Redis Management with Flexibility and Control

**Redisimnest** offers a sophisticated and elegant approach to managing Redis data with its core concepts of **Cluster** and **Key**. These components, designed with flexibility and fine-grained control in mind, enable you to organize, manage, and scale your Redis keys efficiently. This system also integrates key features like TTL drilling, parameterized prefixes, and efficient clearing cluster data.

### Cluster: Prefix-Based Grouping and Management

A **Cluster** in **Redisimnest** is a logical grouping of Redis keys that share a common **prefix**. The cluster's prefix acts as an identity for the keys within it, allowing them to be easily managed as a cohesive unit. Each cluster is self-contained and has several key attributes:

- **`__prefix__`**: Every cluster must have a unique prefix that distinguishes it from others. This prefix is fundamental to its identity and is used in the construction of all keys within the cluster.
- **`__ttl__`**: Optional Time-To-Live (TTL) setting at the cluster level. If a child cluster does not have its own TTL, it inherits the TTL from its parent cluster. However, if the child cluster has its own TTL, it takes precedence over the parent's TTL. This structure allows for flexible TTL management while ensuring that keys without a specified TTL default to the parent's TTL settings.
- **`get_full_prefix()`**: This method returns the complete Redis key prefix for the cluster. It resolves the prefix by concatenating the prefixes of all ancestor clusters, starting from the root cluster down to the current cluster. Additionally, it resolves and includes any parameters specific to the current cluster, ensuring that the final prefix is fully formed with all necessary contextual information.

- **`subkeys()`**: The `subkeys` method allows you to retrieve a list of keys that begin with the current cluster's full prefix. It uses Redis’s SCAN method to efficiently scan and identify all keys that match the current cluster's prefix, including any subkeys that are nested under the cluster. This ensures a comprehensive and performant way of discovering keys associated with the cluster and its parameters.

- **`clear()`**: The `clear` method is used to delete all keys within the cluster. **Warning**: Clearing a cluster will delete all data within it, and **Redisimnest** does **not** prevent accidental data loss. It is **highly recommended to use caution when invoking this method**, especially for clusters that are important or non-recoverable. **Redisimnest** does not enforce safety on clear operations, so be careful when clearing clusters, particularly the **root cluster**.

### Key: Parameterized, Flexible Redis Keys

Each **Key** in a cluster represents an individual Redis entry and follows the cluster’s prefix conventions. Keys can be parameterized, making them more flexible and dynamic. Here's how it works:

- **Parameterized Prefixes**: The prefix of a key is based on the cluster’s prefix, and can also accept dynamic parameters. For example, a key might have a structure like `user:{user_id}:session`, where the `{user_id}` is a placeholder that is replaced with the actual value when the key is created or accessed.
- **TTL Management**: Keys within a cluster inherit TTL settings from their parent cluster but can also have their own TTL, which takes precedence. The TTL behavior is further refined with **TTL drilling**, enabling you to set expiration policies at various levels (cluster, key) to fine-tune how long data persists in Redis.

### Key Usage Warnings

**Warning**: When defining clusters or keys with parameterized prefixes, ensure that parameters are passed **at the correct place**. 

- If a cluster’s prefix includes parameters (e.g., `'user:{user_id}'`), make sure to provide the required values for those parameters **when chaining to subclusters or keys**. Failure to do so will result in an error.
  
  **Example**:  
  ```python
  # Correct usage:
  await root.user(123).age.set(30)
  
  # Incorrect usage (will raise an error):
  await root.user.age.set(30)  # 'user:{user_id}' is missing the user_id parameter
  ```
  
- Similarly, for keys with parameterized prefixes, **always pass the necessary parameters when accessing them**. Omitting them will lead to an error.

  **Example**:  
  ```python
  # Correct usage:
  await root.user(123).name.set("John")
  
  # Incorrect usage (will raise an error):
  await root.user.name.set("John")  # Missing the required parameter 'user_id'
  ```

Always pass parameters as part of the chaining syntax to avoid errors and ensure correct key resolution.

### **Allowed Usage with `[]` Brackets**

You can use **`[]` brackets** for clusters or keys that require **only a single parameter**. This allows for a simplified, compact syntax when accessing parameters.

- **Allowed usage**: If a key or cluster requires just **one parameter**, you can pass it inside the brackets:

  **Example**:  
  ```python
  await root.user[123].name.set("John")
  ```

- **Forbidden usage**: **Multiple parameters cannot** be passed using `[]` syntax. If more than one parameter is required, use the regular chaining syntax to properly pass each one.

  **Example**:  
  ```python
  # Incorrect usage (raises an error):
  await root.user[123, 'extra_param'].name.set("John")
  
  # Correct usage:
  await root.user(123, 'extra_param').name.set("John")
  ```

Using `[]` is a convenient shorthand, but it’s important to remember it is limited to a **single parameter** only.

## Configuration <a name="configuration"></a>

Redisimnest allows you to customize the following settings:

- `REDIS_HOST`: Redis server hostname (default: localhost).
- `REDIS_PORT`: Redis server port (default: 6379).
- `REDIS_USERNAME` / `REDIS_PASS`: Optional authentication credentials.
- `REDIS_DELETE_CHUNK_SIZE`: Number of items deleted per operation (default: 50).

You can set these via environment variables or within your settings.py:
```python
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DELETE_CHUNK_SIZE = 50
```

To apply your custom settings file, add the following line to your `.env` file:

```bash
USER_SETTINGS_FILE=./your_settings.py
```

## Contributing <a name="contributing"></a>

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Write tests for your changes.
5. Submit a pull request.

Please ensure all tests pass before submitting your PR.

## License <a name="license"></a>

This project is licensed under the MIT License - see the LICENSE file for details.

