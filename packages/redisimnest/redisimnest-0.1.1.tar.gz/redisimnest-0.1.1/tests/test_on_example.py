from datetime import datetime
import pytest
from asyncio import run
from ..redisimnest.key import Key 
from ..redisimnest.base_cluster import BaseCluster
from ..redisimnest.exceptions import MissingParameterError
from ..redisimnest.utils import RedisManager
from redis.exceptions import DataError



class Message:
    __prefix__ = 'messages'
    __ttl__ = 50

    message = Key('message:{message_id}', "Unknown Message", 50)
    complex_data = Key('complex_data', {})


class Admin:
    __prefix__ = 'admin:{admin_id}'
    messages = Message
    fist_name = Key('fist_name')

class User:
    __prefix__ = 'user:{user_id}'
    __ttl__ = 120

    messages = Message
    fist_name = Key('firt_name')
    age = Key('age', 0)

class App:
    __prefix__ = 'app'
    __ttl__ = 80

    pending_users = Key('pending_users')
    tokens = Key('tokens', [])


class RootCluster(BaseCluster):
    __prefix__ = 'root'
    __ttl__ = None

    app = App
    user = User
    admin = Admin

    project_name = Key('project_name')
    date = Key('the_date', "Unkown date")

redis_client = RedisManager.get_client()
root = RootCluster(redis_client=redis_client)



class TestSmoke:
    def test_child_cluster_access(self):
        user = root.user
        app = root.app
        admin = root.admin


    def test_key_access(self):
        admin_fist_name = root.admin(123).fist_name
        user_fist_name = root.user(123).fist_name


class TestPrefix:
    def test_cluster_prefix(self):
        admin = root.admin(123)
        assert admin.get_full_prefix() == 'root:admin:123'

    
    def test_child_cluster_prefix(self):
        with pytest.raises(MissingParameterError):
            message = root.admin.messages#.get_full_prefix()
        
        messages = root.admin(123).messages

        assert messages.get_full_prefix() == 'root:admin:123:messages'

        with pytest.raises(MissingParameterError):
            message = root.admin(123).messages.message()
        
        message = root.admin(123).messages.message(123)

        assert message.key == 'root:admin:123:messages:message:123'


class TestTTLDrilling:
    def test_key_level_ttl(self):
        key = root.admin(admin_id=1).messages.message(message_id=42)
        assert key.the_ttl == 50, "Key-level TTL should override all others"

    def test_subcluster_level_ttl(self):
        key = root.user(user_id=5).messages.message(message_id=99)
        assert key.the_ttl == 50, "Subcluster-level TTL should override parent clusters if key has no own TTL"

    def test_cluster_level_ttl(self):
        key = root.app.pending_users
        print(key.the_ttl)
        assert key.the_ttl == 80, "Cluster-level TTL should apply when key and subcluster TTL are not defined"

    def test_fallback_to_root_ttl(self):
        key = root.project_name
        assert key.the_ttl is None, "Fallback to root cluster TTL if no other TTL is defined"

    def test_no_ttl_set_defaults_to_none(self):
        key = root.admin(admin_id=1).fist_name
        assert key.the_ttl is None, "Keys without TTL and no inherited TTL should default to None"

    def test_overridden_in_subcluster_vs_parent(self):
        # root.user has TTL 120, but messages (as subcluster) defines TTL = 50
        key = root.user(user_id=42).messages.message(message_id=9)
        assert key.the_ttl == 50, "Subcluster TTL should take precedence over parent"

    def test_distinct_ttl_across_siblings(self):
        admin_key = root.admin(admin_id=1).messages.message(message_id=101)
        user_key = root.user(user_id=1).messages.message(message_id=202)
        assert admin_key.the_ttl == 50
        assert user_key.the_ttl == 50
        # Even though both keys share the same subcluster (`messages`), they resolve from different parents

    def test_root_ttl_does_not_leak(self):
        key = root.admin(admin_id=1).fist_name
        assert key.the_ttl is None, "Root TTL must not leak into fully defined children if TTLs aren't declared there"





async def main_test():
    await root.project_name.set("RedisimNest")
    assert await root.project_name.get() == "RedisimNest"

    await root.user(user_id=1).age.set(30)
    assert await root.user(1).age.get() == 30

    print(await root.app.tokens.get())
    # assert await root.app.tokens.get() == []

    key = root.user(123).fist_name
    await key.set("Ali")
    ttl = await key.ttl()
    print(ttl)
    assert 0 < ttl <= 120

    key = root.user(123).fist_name
    await key.set("Ali")
    await key.expire(10)
    ttl = await key.ttl()
    assert ttl <= 10
    await key.persist()
    assert await key.ttl() == -1  # TTL removed

    key = root.project_name
    await key.set("Initial")
    await key.rename("root:new_project_name")
    assert await root._redis.exists("root:new_project_name")

    key = root.app.pending_users
    await key.set(["u1", "u2"])
    dumped = await key.dump()
    await key.unlink()
    assert not await key.exists()
    await key.restore(dumped)
    assert await key.get() == ["u1", "u2"]

    key = root.user(5).age
    try:
        await key.set("not an int")
    except DataError:
        pass
        
    await root.admin(admin_id="7").fist_name.set("Zahra")
    usage = await root.admin(7).fist_name.memory_usage()
    assert usage > 0

    key = root.app.tokens
    await key.set(["token1"])
    assert await key.exists()
    await key.touch()
    ttl = await key.ttl()
    assert ttl >= 0  # Confirm it's still a valid key

    await root.project_name.set("the project Name")
    app_keys = set(await root.app.subkeys())
    print('clear result: ', await root.app.clear())
    all_keys = set(await root.subkeys())
    assert all_keys is not None
    assert all_keys.intersection(app_keys) == set()

    now = datetime.now()
    await root.date.set(now)
    assert await root.date.get() == now



class TestHandlers:
    def test_handers(self):
        run(main_test())