# List of default methods
default_methods = [
    "set", "__setitem__", "get", "__getitem__", "dump", "exists",
    "expire", "pexpire", "expireat", "pexpireat", "persist",
    "ttl", "pttl", "expiretime", "object", "type", "memory_usage",
    "touch", "unlink", "rename", "renamenx", "restore", "lock"
]

RAW_COMMANDS = {
    "ttl", "pttl", "expiretime", "exists", "type", "memory_usage",
    "touch", "unlink", "expire", "pexpire", "expireat", "pexpireat", 
    "persist", "rename", "renamenx", "lock", "object"
}


SERIALIZE_COMMANDS = {
    "set", "__setitem__"
}

# Deserializing commands (methods that read data from a key)
DESERIALIZE_COMMANDS = {
    "get", "__getitem__"
}
