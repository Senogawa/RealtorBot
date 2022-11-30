import aioschedule
from database_methods import run_command, get_users_list
import asyncio
from threading import Thread
import time


async def check_users_subscriptions():
    users_data = await run_command("SELECT * FROM users;")
    for user in users_data:
        last_period = int(user["period"]) - int(time.time())
        if last_period < 0 or last_period == 0:
            await run_command(f"DELETE FROM users WHERE member_id='{user['member_id']}';", "SET")
            print(f"{time.ctime(time.time())} |INFO| Пользователь с id {user['member_id']} удален из базы подписок |INFO|")



async def create_schedule_task(g):
    aioschedule.every(g).seconds.do(check_users_subscriptions)
    print("|INFO| Проверка базы запущена |INFO|")
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

def start_async_job():
    asyncio.run(create_schedule_task(3))


if __name__ == "__main__":
    asyncio.run(check_users_subscriptions())