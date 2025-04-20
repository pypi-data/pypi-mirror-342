from typing import Any, Optional
import re

from .exceptions import MissingParameterError

from .utils.de_serialization import deserialize, serialize
from .utils.method_maps import DESERIALIZE_COMMANDS, SERIALIZE_COMMANDS, default_methods
from .utils.misc import get_pretty_representation
from .utils.prefix import validate_prefix
from .settings import TTL_AUTO_RENEW



# ====================================================================================================
# ==============             KEY ARGUMENT PASSING             ==============#
# ====================================================================================================
class KeyArgumentPassing:
    """Handles single and multi param passing to format prefix"""

    def __call__(self, *args, **kwargs):
        """Support positional arguments"""
        for key, arg in zip(self._placeholder_keys, args):
            if key not in kwargs:
                kwargs[key] = arg

        # Validate all placeholders provided
        missing = [k for k in self._placeholder_keys if k not in kwargs]
        if missing:
            raise MissingParameterError(
                f"Missing required param(s) {missing} for key prefix '{self.prefix_template}'"
            )

        if self._placeholder_keys:
            formatted_key = self.prefix_template.format(**kwargs)
            self.key = f"{self._parent.get_full_prefix()}:{formatted_key}"
        else:
            self.key = f"{self._parent.get_full_prefix()}:{self.prefix_template}"

        return self


    def __getitem__(self, value):
        """Support single argument"""
        if len(self._placeholder_keys) != 1:
            raise ValueError(
                f"Key with multiple placeholders ({', '.join(self._placeholder_keys)}) "
                "cannot be used with [] syntax. Use .__call__(...) instead."
            )
        return self(**{self._placeholder_keys[0]: value})



# ============================================================================================================================================
# ============================================================================================================================================
# ===========================                         BASE KEY                         ===========================#
# ============================================================================================================================================
# ============================================================================================================================================
class Key(KeyArgumentPassing):
    def __init__(
        self, 
        prefix_template: str, 
        default: Optional[Any] = None, 
        ttl: Optional[int] = None,
        ttl_auto_renew: bool = TTL_AUTO_RENEW
    ):
        self.prefix_template = prefix_template
        self.default = default
        self._own_ttl = ttl  # Changed from self.ttl
        self._placeholder_keys = re.findall(r"\{(.*?)\}", prefix_template) if prefix_template else []
        self.key = None
        self.ttl_auto_renew = ttl_auto_renew

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        cls._generate_methods()
        return instance

    def _resolve_ttl(self):
        # Key-level TTL
        if getattr(self, '_own_ttl', None) is not None:
            return self._own_ttl

        # Subcluster → parent TTLs
        cluster = self._parent
        while cluster:
            ttl = getattr(cluster.__class__, '__ttl__', None)
            if ttl is not None:
                return ttl
            cluster = cluster._parent

        return None  # No TTL found
    
    @property
    def the_ttl(self):
        return self._resolve_ttl()
    
    async def _dispatch_method(self, method: str, *args, **kwargs) -> Any:
        if method not in default_methods:
            raise AttributeError(f"Unsupported method: '{method}'.")

        redis_method = getattr(self._parent._redis, method, None)
        if not callable(redis_method):
            raise AttributeError(f"Redis client does not support method: '{method}'.")

        # Serialize payloads for write operations
        if method in SERIALIZE_COMMANDS:
            if args:
                args = (serialize(args[0]), *args[1:])
            elif 'value' in kwargs:
                kwargs['value'] = serialize(kwargs['value'])

        # Inject TTL inline where supported
        if method == "set" and self.the_ttl is not None:
            kwargs.setdefault("ex", self.the_ttl)
        
        if method == "restore":
            ttl_ms = (self.the_ttl or 0) * 1000
            result = await redis_method(self.key, ttl_ms, *args, **kwargs)

            # Also apply TTL again if needed (usually redundant with ttl_ms but keep it if needed)
            if self.the_ttl:
                await self._parent._redis.expire(self._name, self.the_ttl)

            return result  # ✅ Early return here


        # Call Redis method
        print(f'{self.key=}')
        if not self.key:
            self.__call__()
        
        result = await redis_method(self.key, *args, **kwargs)

        # Apply TTL manually if method doesn't support it inline
        if method in {"restore"} and self.the_ttl is not None:
            await self._parent._redis.expire(self._name, self.the_ttl)

        # Handle auto-renew on read if enabled
        if self.ttl_auto_renew and method in DESERIALIZE_COMMANDS and self.the_ttl is not None:
            await self._parent._redis.expire(self._name, self.the_ttl)

        # Fallback to default if result is None
        if result is None:
            return self.default if self.default is not None else None

        # Deserialize result for read operations
        if method in DESERIALIZE_COMMANDS:
            return deserialize(result)

        return result

    def __set_name__(self, owner, name: str):
        self._name = name

    
    def __get__(self, instance, owner):
        self._parent = instance
        validate_prefix(self.prefix_template, instance.__class__.__name__)
        return self

    
    @classmethod
    def _generate_methods(cls):
        """
        Dynamically generate all supported Redis methods for this key class.
        Each generated method will automatically invoke `_dispatch_method`.
        """
        supported_methods = default_methods
        # print(f"KEY_TYPE: {key_type}")
        # pprint(supported_methods)

        for method in supported_methods:
            def make_wrapper(method_name):
                def method_wrapper(self, *args, **kwargs):
                    return self._dispatch_method(method_name, *args, **kwargs)
                return method_wrapper
            setattr(cls, method, make_wrapper(method))
    
    
    def describe(self):
        return {
            "name": self._name,
            "prefix": self.prefix_template,
            "params": self._placeholder_keys,
            "ttl": self._resolve_ttl()
        }

    @property
    def __doc__(self):
        return get_pretty_representation(self.describe())
    
    def __repr__(self):
        return (
            f"<Key(name='{self._name}' "
            f"template='{self.prefix_template}')>"
        )


