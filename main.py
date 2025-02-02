from utils.core import create_sessions
from utils.telegram import Accounts
from utils.fomo import Fomo
from data.config import hello,USE_PROXY
import asyncio
import os

async def main():
    print(hello)
    action = int(input('Выберите действие:\n1. Начать сбор монет\n2. Создать сессию\n>'))
    
    if not os.path.exists('sessions'):
        os.mkdir('sessions')
    
    if action == 2:
        await create_sessions()

    if action == 1:
        accounts = await Accounts().get_accounts()
                
        tasks = []
        if USE_PROXY:
            proxy_dict = {}
            with open('proxy.txt','r',encoding='utf-8') as file:
                list = [i.strip().split() for i in file.readlines()]
                proxy = []
                for info in list:
                    if info!=[]:
                        proxy.append((info[0],''.join(info[1:]).replace('.session','')))
                for prox,name in proxy:
                    proxy_dict[name] = prox
            for thread, account in enumerate(accounts):
                if account in proxy_dict:
                    tasks.append(asyncio.create_task(Fomo(account=account, thread=thread, proxy=proxy_dict[account]).main()))
                else:
                    tasks.append(asyncio.create_task(Fomo(account=account, thread=thread,proxy = None).main()))
        else:
            for thread, account in enumerate(accounts):
                tasks.append(asyncio.create_task(Fomo(account=account, thread=thread,proxy = None).main()))
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
