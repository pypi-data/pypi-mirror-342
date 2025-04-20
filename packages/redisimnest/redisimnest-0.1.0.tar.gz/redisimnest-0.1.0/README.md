# RediSimNest

A sophisticated, prefix-based Redis key management system with customizable clusters, dynamic key types, and parameterized prefix resolution. Ideal for organizing application state and simplifying Redis interactions in complex systems.

## Table of Contents
- Installation
- Usage
- Features
- Configuration
- Contributing
- License
- Acknowledgments

## Installation

You can install RediSimNest via pip:

    pip install redisimnest

Alternatively, install from source:

    git clone https://github.com/yourusername/redisimnest.git
    cd redisimnest
    pip install .

## Usage

Here's a basic example of how to use RediSimNest in your project:

    from redisimnest import Key, BaseCluster

    # Define a cluster with a parameterized prefix
    class MyCluster(BaseCluster):
        __prefix__ = "user:{user_id}:data"

    cluster = MyCluster(user_id=123)
    print(cluster.get_full_prefix())  # Output: user:123:data

Check out the full documentation for more advanced use cases and examples.

## Features

- Prefix-Based Cluster Management: Organize Redis keys with flexible, dynamic prefixes.
- Support for Parameterized Keys: Create keys with placeholders that can be dynamically replaced.
- TTL Management: Automatic and manual control over key TTLs.
- Cluster Hierarchies: Nested clusters with inherited parameters.
- Typed Key Classes: Use Python types to define and validate Redis key value structures.
- Auto-Binding & Dynamic Access: Smart access to nested clusters and runtime bindings.
- Command Dispatching: Type-aware command routing with serialization/deserialization support.

## Configuration

RediSimNest allows you to customize the following settings:

- REDIS_HOST: Redis server hostname (default: localhost).
- REDIS_PORT: Redis server port (default: 6379).
- REDIS_USERNAME / REDIS_PASS: Optional authentication credentials.
- REDIS_DELETE_CHUNK_SIZE: Number of items deleted per operation (default: 50).

You can set these via environment variables or within your settings.py:

    import os

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DELETE_CHUNK_SIZE = 50

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Write tests for your changes.
5. Submit a pull request.

Please ensure all tests pass before submitting your PR.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to redis-py for the Redis client.
- Inspired by Django's settings and configuration systems.
