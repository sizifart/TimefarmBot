import requests
import json
import urllib.parse

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

def get_access_token_and_info(query_data):
    url = 'https://tg-bot-tap.laborx.io/api/v1/auth/validate-init/v2'
    try:
        payload = {
            "initData": query_data,
            "platform": "ios"
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        token_info = response.json()
        with open('data.txt', 'a') as file:
            file.write(f"{token_info['token']}\n")
        
        return token_info
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Query Anda Salah")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def main():
    # Clear the data.txt file at the beginning
    open('data.txt', 'w').close()
    
    with open('query.txt', 'r') as file:
        queries = file.readlines()
    
    for query_data in queries:
        query_data = query_data.strip()
        get_access_token_and_info(query_data)

if __name__ == "__main__":
    main()
