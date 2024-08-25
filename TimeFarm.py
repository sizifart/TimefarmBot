import requests
import time
from colorama import Fore, Style, init
import json
from datetime import datetime, timedelta, timezone
import argparse
import urllib.parse
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_arguments():
    parser = argparse.ArgumentParser(description='TimeFarm BOT')
    parser.add_argument('--task', type=str, choices=['y', 'n'], help='Claim Task (y/n)')
    parser.add_argument('--upgrade', type=str, choices=['y', 'n'], help='Auto Upgrade (y/n)')
    args = parser.parse_args()
    
    clear_terminal()
    
    ascii=("\033[1;93m" + r"""

    ███████╗██╗███████╗     ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
    ██╔════╝██║╚══███╔╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗
    ███████╗██║  ███╔╝     ██║     ██║   ██║██║  ██║█████╗  ██████╔╝
    ╚════██║██║ ███╔╝      ██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗
    ███████║██║███████╗    ╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║
    ╚══════╝╚═╝╚══════╝     ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝

""" + "\033[0m" + "\033[1;96m" +
r"""----------------------------------""" + "\033[0m")
    ascii2=("\033[1;93mTIMEFARM AUTO BOT v1.1\033[0m")
    ascii3=("\033[1;92mPrepared and Developed by: F.Davoodi\033[0m")
    ascii5=("\033[1;96m----------------------------------\033[0m")
    ascii6=("\033[1;38;2;139;69;19;48;2;173;216;230m--------[TimeFarm Bot]--------\033[0m")
    ascii7=("\033[1;96m----------------------------------\033[0m")
    
    print(ascii)
    print(ascii2)
    print(ascii3)
    print(ascii5)
    print(ascii6)
    print(ascii7)

    if args.task is None:
        task_input = input("Do you want to auto claim tasks? (y/n) : ").strip().lower()
        args.task = task_input if task_input in ['y', 'n'] else 'n'
    
    if args.upgrade is None:
        upgrade_input = input("Do you want auto upgrade clock?  (y/n): ").strip().lower()
        args.upgrade = upgrade_input if upgrade_input in ['y', 'n'] else 'n'
        clear_terminal()    

    return args

args = parse_arguments()
cek_task_enable = args.task
cek_upgrade_enable = args.upgrade

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://tg-tap-miniapp.laborx.io',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://tg-tap-miniapp.laborx.io/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}

def cek_farming(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/farming/info'
    headers['authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=headers)
    return response.json()
    

def start_farming(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/farming/start'
    headers['authorization'] = f'Bearer {token}'
    response = requests.post(url, headers=headers, json={})
    return response.json()

def finish_farming(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/farming/finish'
    headers['authorization'] = f'Bearer {token}'
    response = requests.post(url, headers=headers, json={})
    return response.json()

def cek_task(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/tasks'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def submit_task(token, task_id):
    url = f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/submissions'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json={})
    return response.json()

def claim_task(token, task_id):
    url = f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/claims'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json={})
    return response.json()

def upgrade_level(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/me/level/upgrade'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://tg-tap-miniapp.laborx.io',
        'referer': 'https://tg-tap-miniapp.laborx.io/',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.post(url, headers=headers)
    return response.json()

def auto_upgrade(token):
    while True:
        response = upgrade_level(token)
        if 'error' in response:
            if response['error']['message'] == "Not enough balance":
                print(Fore.RED + Style.BRIGHT + f"\rUpgrade : Don't have enough balance to upgrade.", flush=True)
                break
            elif response['error']['message'] == "Forbidden":
                print(Fore.RED + Style.BRIGHT + f"\rUpgrade : Error upgrade.", flush=True)
            elif response['error']['message'] == "Max level reached":
                print(Fore.RED + Style.BRIGHT + f"\rUpgrade : Has reached the maximum level.", flush=True)
                break
            else:
                print(Fore.RED + Style.BRIGHT + f"\rUpgrade : Error upgrade. {response['error']['message']}", flush=True)
                break
        else:
            print(Fore.GREEN + Style.BRIGHT + f"\rUpgrade : Upgrade successful, next...", flush=True)

def claim_referral_balance(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/balance/referral/claim'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site'
    }
    response = requests.post(url, headers=headers, json={})
    return response.json()            
            

def animated_loading(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\r{Fore.CYAN + Style.BRIGHT}Wait {remaining_time} seconds.....", end="", flush=True)
            time.sleep(0.25)


def main():
    while True:
     
        if os.path.exists('data.txt'):
            with open('data.txt', 'r') as file:
                tokens = [line.strip() for line in file.readlines()]
      
        for token in tokens:
            try:
                # Removed query_data and user details extraction
                balance_info = cek_farming(token)  # Replace with actual balance info retrieval logic
                
                print(Fore.CYAN + Style.BRIGHT + f"\n------Account {tokens.index(token) + 1}------")
                print(Fore.YELLOW + Style.BRIGHT + f"Balance : {int(float(balance_info['balance'])):,}".replace(',', '.'))
                if cek_upgrade_enable == 'y':
                    print(Fore.YELLOW + Style.BRIGHT + f"\rUpgrade : Upgrading Clock..", end="", flush=True)
                    auto_upgrade(token)
                if cek_task_enable == 'y':
                    print(Fore.YELLOW + Style.BRIGHT + f"\rTask : Checking ...", end="", flush=True)
                    tasks = cek_task(token)
      
                    if tasks:
                        for task in tasks:
                            if task.get('submission', {}).get('status') == 'CLAIMED':
                                print(Fore.GREEN + Style.BRIGHT + f"\rTask : Claimed Already", flush=True)
                            elif task.get('submission', {}).get('status') == 'STARTED':
                                print(Fore.YELLOW + Style.BRIGHT + f"\rTask : Submitting ...", end="", flush=True)
                                submit_task(token, task['id'])
                                print(Fore.GREEN + Style.BRIGHT + f"\rTask : Submitted Successful", flush=True)
                                print(Fore.YELLOW + Style.BRIGHT + f"\rTask : Claiming ...", end="", flush=True)
                                claim_task(token, task['id'])
                                print(Fore.GREEN + Style.BRIGHT + f"\rTask : Claimed Successful", flush=True)
                            else:
                                print(f"\rTask : Submit task: {task['title']}", end="", flush=True)
                                if task.get('submission', {}).get('status') == 'SUBMITTED':
                                    print(Fore.YELLOW + Style.BRIGHT + f"\rTask : Submit task: {task['title']} | Already Submitted", flush=True)
                                else:
                                    response = submit_task(token, task['id'])
                                    if response is not None:
                                        if 'error' in response:
                                            print(Fore.RED + Style.BRIGHT + f"\rTask : Submit task: {task['title']} | {response['error']['message']}", end="", flush=True)
                                        else:
                                            print(Fore.GREEN + Style.BRIGHT + f"\rTask : Submit task: {task['title']} | Submitted", flush=True)
                                    time.sleep(3)  # Tunggu 3 detik sebelum mengklaim
                                print(f"\rTask : Claim task: {task['title']}", end="", flush=True)
                                response = claim_task(token, task['id'])
                                if response is not None:
                                    if 'error' in response:
                                        if response['error']['message'] == "Failed to claim reward":
                                            print(Fore.RED + Style.BRIGHT + f"\rTask : Claim task: {task['title']} | Failed to claim reward", end="", flush=True)
                                    else:
                                        print(Fore.GREEN + Style.BRIGHT + f"\rTask : Claim task: {task['title']} | Claimed", flush=True)
                print(Fore.YELLOW + Style.BRIGHT + f"\rFarming : Checking ...", end="", flush=True)
                time.sleep(2)
                farming_response = finish_farming(token)
                if farming_response is not None:
                    if 'error' in farming_response:
                        if farming_response['error']['message'] == "Too early to finish farming":

                            cek_farming_response = cek_farming(token)
                            if cek_farming_response:
                                started_at = datetime.fromisoformat(cek_farming_response['activeFarmingStartedAt'].replace('Z', '+00:00')).astimezone(timezone.utc)
                                duration_sec = cek_farming_response['farmingDurationInSec']
                                end_time = started_at + timedelta(seconds=duration_sec)
                                time_now = datetime.now(timezone.utc)

                                remaining_time = end_time - time_now
                                if remaining_time.total_seconds() > 0:
                                    hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                                    minutes, _ = divmod(remainder, 60)
                                    print(Fore.RED + Style.BRIGHT + f"\rFarming : Claim farming in {int(hours)} hours {int(minutes)} minutes", flush=True)
                                else:
                                    print(Fore.GREEN + Style.BRIGHT + f"\rFarming : Farming can be claimed now", flush=True)
                        elif farming_response['error']['message'] == "Farming didn't start":
                            print(Fore.YELLOW + Style.BRIGHT + f"\rFarming : Starting Farming..", end="", flush=True)
                            time.sleep(2)
                            start_farming_response = start_farming(token)
                            if start_farming_response is not None:
                                print(Fore.GREEN + Style.BRIGHT + f"\rFarming : Started | Reward : {int(start_farming_response['farmingReward']):,}".replace(',', '.'), flush=True)
                            else:
                                if 'error' in start_farming_response:
                                    if start_farming_response['error']['message'] == "Farming already started":
                                        print(Fore.RED + Style.BRIGHT + f"\rFarming : Farming Already Started", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"\rFarming : Gagal Start Farming", flush=True)
                        else:
                            print(f"\rFarming : {farming_response['error']['message']}", flush=True)
                    else:
                        print(Fore.GREEN + Style.BRIGHT + f"\rFarming : Claimed | Balance: {int(farming_response['balance']):,}".replace(',', '.'), flush=True)
                        print(Fore.YELLOW + Style.BRIGHT + f"\rFarming : Checking Farming..", end="", flush=True)
                        time.sleep(2)
                        cek_farming_response = cek_farming(token)
                        if cek_farming_response is not None:
                                if cek_farming_response['activeFarmingStartedAt'] is None:
                                    print(Fore.RED + Style.BRIGHT + f"\rFarming : Farming not started", flush=True)
                                    print(Fore.YELLOW + Style.BRIGHT + f"\rFarming : Starting Farming..", end="", flush=True)
                                    time.sleep(2)
                                    start_farming_response = start_farming(token)
                                    if start_farming_response is not None:
                                        print(Fore.GREEN + Style.BRIGHT + f"\rFarming : Started | Reward : {int(start_farming_response['farmingReward']):,}".replace(',', '.'), flush=True)
                                    else:
                                        if 'error' in start_farming_response:
                                            if start_farming_response['error']['message'] == "Farming already started":
                                                print(Fore.RED + Style.BRIGHT + f"\rFarming : Farming Already Started", flush=True)
                                            else:
                                                print(Fore.RED + Style.BRIGHT + f"\rFarming : Gagal Start Farming", flush=True)
                                else:
                                    print(Fore.YELLOW + Style.BRIGHT + f"\rFarming : Farming Already Started", flush=True)                              
                        else:
                            print(Fore.RED + Style.BRIGHT + f"\rFarming : Gagal Cek Farming", flush=True)
                  
                print(Fore.YELLOW + Style.BRIGHT + f"\rClaim Referral Balance : Claiming ...", end="", flush=True)
                claim_response = claim_referral_balance(token)

                if 'error' in claim_response:
                    print(Fore.RED + Style.BRIGHT + f"\rClaim Referral Balance : Not enough Refer Balance", flush=True)
                else:
                    print(Fore.GREEN + Style.BRIGHT + f"\rClaim Referral Balance : Balance Claimed Successful", flush=True)
                    print(Fore.GREEN + Style.BRIGHT + f"Claimed Balance: {current_balance:,}".replace(',', '.'))

            except Exception as e:
                print(Fore.GREEN + Style.BRIGHT + f"\n\rReferral Balance Claimed Successful", flush=True)
                
        animated_loading(3600)
        clear_terminal()    
 
if __name__ == "__main__":
    main()
