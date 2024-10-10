import asyncio
from time import time
from datetime import datetime
from urllib.parse import unquote
from random import randint
import aiohttp
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered
from pyrogram.raw.functions.messages import RequestWebView

from bot.config import settings
from bot.utils import logger
from bot.exceptions import InvalidSession
from .headers import headers


class Claimer:
    def __init__(self, tg_client: Client):
        self.session_name = tg_client.name
        self.tg_client = tg_client

    async def get_tg_web_data(self, proxy: str | None) -> str:
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            web_view = await self.tg_client.invoke(RequestWebView(
                peer=await self.tg_client.resolve_peer('TimeFarmCryptoBot'),
                bot=await self.tg_client.resolve_peer('TimeFarmCryptoBot'),
                platform='android',
                from_bot_menu=False,
                url='https://tg-tap-miniapp.laborx.io/'
            ))

            auth_url = web_view.url
            tg_web_data = unquote(
                string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0])

            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error during Authorization: {error}")
            await asyncio.sleep(delay = randint(3, 10))

    async def login(self, http_client: aiohttp.ClientSession, tg_web_data: dict[str]) -> dict[str]:
        try:
            response = await http_client.post(url='https://tg-bot-tap.laborx.io/api/v1/auth/validate-init/v2', data={"initData":tg_web_data,"platform":"android"})
            response.raise_for_status()

            response_json = await response.json()

            json_data = {
                'token': response_json['token'],
                'level': response_json['info']['level'],
                'levelDescriptions': response_json['levelDescriptions']
            }

            return json_data
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Access Token: {error}")
            await asyncio.sleep(delay = randint(3, 10))

    async def get_mining_data(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            response = await http_client.get('https://tg-bot-tap.laborx.io/api/v1/farming/info')
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when getting Profile Data: {error}")
            await asyncio.sleep(delay = randint(3, 10))

    async def get_tasks_list(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            response = await http_client.get('https://tg-bot-tap.laborx.io/api/v1/tasks')
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when getting Tasks Data: {error}")
            await asyncio.sleep(delay = randint(3, 10))

    async def get_task_data(self, http_client: aiohttp.ClientSession, task_id: str) -> dict[str]:
        try:
            response = await http_client.get(f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}')
            response.raise_for_status()

            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when getting Task Data: {error}")
            await asyncio.sleep(delay = randint(3, 10))

    async def upgrade_level(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            response = await http_client.post(url=f'https://tg-bot-tap.laborx.io/api/v1/me/level/upgrade', json={})
            response.raise_for_status()

            response_json = await response.json()

            return response_json

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while Upgrade Level: {error}")
            await asyncio.sleep(delay = randint(3, 10))

    async def task_claim(self, http_client: aiohttp.ClientSession, task_id: str) -> str:
        try:
            response = await http_client.post(url=f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/claims', json={})
            response.raise_for_status()

            return response.text

        except Exception as error:
            #logger.error(f"{self.session_name} | Unknown error while claim task: {error}")
            await asyncio.sleep(delay = randint(3, 10))

    async def task_submiss(self, http_client: aiohttp.ClientSession, task_id: str) -> str:
        try:
            response = await http_client.post(url=f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/submissions', json={})
            response.raise_for_status()

            return response.text

        except Exception as error:
            #logger.error(f"{self.session_name} | Unknown error while submissions task: {error}")
            await asyncio.sleep(delay = randint(3, 10))

    async def start_mine(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            response = await http_client.post('https://tg-bot-tap.laborx.io/api/v1/farming/start', json={})
            response.raise_for_status()

            if response.status == 200:
                return {
                    'ok': True,
                    'code': 200
                }

        except Exception as error:
            #logger.error(f"{self.session_name} | Unknown error when start miner: {error}")
            await asyncio.sleep(delay = randint(3, 10))

            return {
                    'ok': True,
                    'code': response.status
                }

    async def finish_mine(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            response = await http_client.post('https://tg-bot-tap.laborx.io/api/v1/farming/finish', json={})
            response.raise_for_status()

            response_json = await response.json()

            if response.status == 200:
                return {
                    'ok': True,
                    'code': 200,
                    'balance': int(response_json['balance'])
                }

        except Exception as error:
            #logger.error(f"{self.session_name} | Unknown error when Claiming: {error}")
            await asyncio.sleep(delay = randint(3, 10))

            return {
                    'ok': True,
                    'code': response.status
                }

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            logger.info(f"{self.session_name} | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

    async def run(self, proxy: str | None) -> None:
        access_token_created_time = 0
        available = False

        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        async with aiohttp.ClientSession(headers=headers, connector=proxy_conn) as http_client:
            if proxy:
                await self.check_proxy(http_client=http_client, proxy=proxy)

            while True:
                try:
                    if time() - access_token_created_time >= 3600:
                        tg_web_data = await self.get_tg_web_data(proxy=proxy)
                        login_data = await self.login(http_client=http_client, tg_web_data=tg_web_data)

                        http_client.headers["Authorization"] = f"Bearer {login_data['token']}"
                        headers["Authorization"] = f"Bearer {login_data['token']}"

                        level_num = int(login_data['level'])
                        levelDescriptions = login_data['levelDescriptions']

                        access_token_created_time = time()

                        tasks_data = await self.get_tasks_list(http_client=http_client)

                        for task in tasks_data:
                            task_id = task["id"]
                            task_title = task["title"]
                            task_type = task["type"]
                            if "submission" in task.keys():
                                status = task["submission"]["status"]
                                if status == "CLAIMED":
                                    continue

                                if status == "COMPLETED":
                                    task_data_claim = await self.task_claim(http_client=http_client, task_id=task_id)
                                    if task_data_claim == "OK":
                                        logger.success(f"{self.session_name} | Successful claim | "
                                                    f"Task Title: <g>{task_title}</g>")
                                        continue

                            if task_type == "TELEGRAM":
                                continue
                                
                            task_data_submiss = await self.task_submiss(http_client=http_client, task_id=task_id)
                            if task_data_submiss != "OK":
                                #logger.error(f"{self.session_name} | Failed Send Submission Task: {task_title}")
                                continue

                            task_data_x = await self.get_task_data(http_client=http_client, task_id=task_id)
                            status = task_data_x["submission"]["status"]
                            if status != "COMPLETED":
                                logger.error(f"{self.session_name} | Task is not completed: {task_title}")
                                continue

                            task_data_claim_x = await self.task_claim(http_client=http_client, task_id=task_id)
                            if task_data_claim_x == "OK":
                                logger.success(f"{self.session_name} | Successful claim | "
                                                    f"Task Title: <g>{task_title}</g>")
                                continue

                    
                    mining_data = await self.get_mining_data(http_client=http_client)

                    balance = int(float(mining_data['balance']))
                    farmingReward = int(mining_data['farmingReward'])
                    farmingDurationInSec = int(mining_data['farmingDurationInSec'])
                    
                    if mining_data['activeFarmingStartedAt'] != None:
                        available = True

                    if int(farmingDurationInSec / 60) != settings.SLEEP_BETWEEN_CLAIM:
                        settings.SLEEP_BETWEEN_CLAIM = int(farmingDurationInSec / 60)

                    logger.info(f"{self.session_name} | Balance: <c>{balance}</c> | "
                                f"Earning: <e>{available}</e> | "
                                f"Speed: <g>x{(level_num + 1)}</g>")

                    if available == False:
                        status_start = await self.start_mine(http_client=http_client)
                        if status_start['ok'] and status_start['code'] == 200:
                            logger.success(f"{self.session_name} | Successful Mine Started | "
                                    f"Balance: <c>{balance}</c> | "
                                    f"Speed: Farming (<g>x{(level_num + 1)}</g>)")

                    if available:
                        retry = 1
                        while retry <= settings.CLAIM_RETRY:
                            status = await self.finish_mine(http_client=http_client)
                            if status['ok'] and status['code'] == 200:
                                mining_data = await self.get_mining_data(http_client=http_client)
                                new_balance = int(float(mining_data['balance']))
                                balance = new_balance

                                if(new_balance == int(status['balance'])):
                                    status_start = await self.start_mine(http_client=http_client)
                                    if status_start['ok'] and status_start['code'] == 200:
                                        logger.success(f"{self.session_name} | Successful claim | "
                                                f"Balance: <c>{new_balance}</c> (<g>+{farmingReward}</g>)")
                                        logger.info(f"Next claim in {settings.SLEEP_BETWEEN_CLAIM}min")
                                        break
                            elif status['code'] == 403:
                                break

                            logger.info(f"{self.session_name} | Retry <y>{retry}</y> of <e>{settings.CLAIM_RETRY}</e>")
                            retry += 1

                    available = False

                    if (settings.AUTO_UPGRADE_FARM is True and level_num < settings.MAX_UPGRADE_LEVEL): 
                        next_level = level_num + 1
                        max_level_bot = len(levelDescriptions) - 1
                        if next_level <= max_level_bot:
                            for level_data in levelDescriptions:
                                lvl_dt_num = int(level_data['level'])
                                if next_level == lvl_dt_num:
                                    lvl_price = int(level_data['price'])
                                    if lvl_price <= balance:
                                        logger.info(f"{self.session_name} | Sleep 5s before upgrade level farming to {next_level} lvl")
                                        await asyncio.sleep(delay = randint(3, 10))

                                        out_data = await self.upgrade_level(http_client=http_client)
                                        if out_data['balance']:
                                            logger.success(f"{self.session_name} | Level farming upgraded to {next_level} lvl | "
                                            f"Balance: <c>{out_data['balance']}</c> | "
                                            f"Speed: <g>x{level_data['farmMultiplicator']}</g>")
                                            
                                            await asyncio.sleep(delay = randint(3, 10))
                                    

                except InvalidSession as error:
                    raise error

                except Exception as error:
                    logger.error(f"{self.session_name} | Unknown error: {error}")
                    await asyncio.sleep(delay = randint(3, 10))

                else:
                    sleep = randint(3200, 7200)
                    logger.info(f"{self.session_name} | Sleep {sleep}s...")
                    await asyncio.sleep(sleep)             

async def run_claimer(tg_client: Client, proxy: str | None):
    try:
        await Claimer(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
