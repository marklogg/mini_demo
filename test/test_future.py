import asyncio
import functools


def callback(future, n):
    print('{}: future done: {}'.format(n, future.result()))


async def register_callbacks(fut):
    print('registering callbacks on future')
    fut.add_done_callback(functools.partial(callback, n=1))
    fut.add_done_callback(functools.partial(callback, n=2))


async def main(fut):
    await register_callbacks(fut)
    print(f'{fut}')
    print('setting result of future')
    fut.set_result('the result')


event_loop = asyncio.get_event_loop()
try:
    all_done = asyncio.Future()
    event_loop.run_until_complete(main(all_done))
finally:
    event_loop.close()
