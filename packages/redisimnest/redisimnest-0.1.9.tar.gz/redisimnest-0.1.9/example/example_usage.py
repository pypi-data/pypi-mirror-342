from asyncio import run
from redisimnest import BaseCluster, Key
from redisimnest.utils import RedisManager
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

    # # Check existence first
    # exists = bool(await root.project_name.exists())
    # print(f"Key exists: {exists}")

    # # If exists is False, then assert None for get
    # assert exists is False

run(main_test())
