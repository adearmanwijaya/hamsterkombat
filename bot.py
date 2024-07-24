import requests
import json
import time
import random
import base64
from datetime import datetime
from itertools import cycle
from colorama import init, Fore, Style
from fake_useragent import UserAgent
from requests_html import HTMLSession
 
 


def DailyCipherDecode(cipher):
    cipher = cipher[:3] + cipher[4:]
    cipher = cipher.encode("ascii")
    cipher = base64.b64decode(cipher)
    cipher = cipher.decode("ascii")
    return cipher


def TextToMorseCode(text):
    morse_code = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        " ": "/",
        ".": ".-.-.-",
        ",": "--..--",
        "?": "..--..",
        "'": ".----.",
        "!": "-.-.--",
        "/": "-..-.",
        "(": "-.--.",
        ")": "-.--.-",
        "&": ".-...",
        ":": "---...",
        ";": "-.-.-.",
        "=": "-...-",
        "+": ".-.-.",
        "-": "-....-",
        "_": "..--.-",
        '"': ".-..-.",
        "$": "...-..-",
        "@": ".--.-.",
    }
    text = text.upper()
    morse = ""
    for char in text:
        if char in morse_code:
            morse += morse_code[char] + " "
    return morse


#===========================================================================
#===========================================================================
#konfigurasi BOT
# Silahkan Edit dengan Y atau N. kalau Y berarti aktif, kalo n berarti off
# Sesuaikan juga var2 lain sesuai keinginanmu
# Setelah melakukan perubahan, jangan lupa bot.py ditutup dan dibuka kembali

auto_cek_task_list = "y"
auto_absen = "y"
auto_morse = "y"
auto_klaim_kombo = "n"
auto_upgrade_pph = "y"
auto_upgrade_multitap = "y"
auto_upgrade_energy = "y"
auto_minigame = "y"
jeda_antar_akun = "y"
#max_jeda_antar_akun DALAM DETIK
max_jeda_antar_akun = 15
lv_upgrade_multitap = 9
lv_upgrade_energy = 9
harga_maksimal = 5000000

#===========================================================================
# Jangan Edit2 script dibawah ini, kalau mau edit2 yang diatas
#=========================================================================== 

session = HTMLSession()
ua = UserAgent()
# Initialize colorama
init(autoreset=True)

def countdown(t):
    while t:
        menit, detik = divmod(t, 60)
        menit = str(menit).zfill(2)
        detik = str(detik).zfill(2)
        print(Fore.WHITE + Style.BRIGHT + f"Tunggu dulu {menit}:{detik} detik     ", flush=True, end="\r")
        time.sleep(1)
        t -= 1
    print("                                        ", flush=True, end="\r")    
def load_tokens(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []

def get_headers(token: str) -> dict:
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': ua.random,
        'Content-Type': 'application/json'
    }

def get_token(init_data_raw):
    url = 'https://api.hamsterkombatgame.io/auth/auth-by-telegram-webapp'
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': ua.random,
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    data = json.dumps({"initDataRaw": init_data_raw})
    res = session.post(url, headers=headers, data=data)
    
    if res.status_code == 200:
        return res.json()['authToken']
    else:
        error_data = res.json()
        if "invalid" in error_data.get("error_code", "").lower():
            print(Fore.RED + Style.BRIGHT + "\rFailed Get Token. Invalid init data", flush=True)
        else:
            print(Fore.RED + Style.BRIGHT + f"\rFailed Get Token. {error_data}", flush=True)
        return None
		
def authenticate(token):
    url = 'https://api.hamsterkombatgame.io/auth/me-telegram'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def sync_clicker(token):
    url = 'https://api.hamsterkombatgame.io/clicker/sync'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def claim_daily(token):
    url = 'https://api.hamsterkombatgame.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": "streak_days"})
    response = requests.post(url, headers=headers, data=data)
    return response
def upgrade(token, upgrade_type):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-boost'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": upgrade_type, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response


def tap(token, max_taps, available_taps):
    url = 'https://api.hamsterkombatgame.io/clicker/tap'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"count": max_taps, "availableTaps": available_taps, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response

def list_tasks(token):
    url = 'https://api.hamsterkombatgame.io/clicker/list-tasks'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response
def njaluk_kombo(item):
    url = "https://raw.githubusercontent.com/unadavina/hk/main/combo"
    njaluk = requests.get(url)
    KomboSaiki = njaluk.text
    ListKombo = KomboSaiki.split()
    if item == "item":
        List_Kombo = [ListKombo[0], ListKombo[1], ListKombo[2]]
    else:
        List_Kombo = ListKombo[4]
    return List_Kombo
#print(f"List Kombo	: {njaluk_kombo("item")}")
#time.sleep(3000)


def start_minigame(token):
    url = 'https://api.hamsterkombatgame.io/clicker/start-keys-minigame'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response
	

def klaim_MiniGame(token,jeda):
	token_suffix = token[-10:]
	prefix_acak = '0' + str(jeda) + str(random.randint(10000000000, 99999999999))[:10]
	cipher = f'{prefix_acak}|{token_suffix}'
	base64_cipher = base64.b64encode(cipher.encode()).decode()
	url = 'https://api.hamsterkombatgame.io/clicker/claim-daily-keys-minigame'
	headers = get_headers(token)
	headers['accept'] = 'application/json'
	headers['content-type'] = 'application/json'
	data = json.dumps({"cipher": base64_cipher})
	response = requests.post(url, headers=headers, data=data)
    # Tambahkan pengecekan status code dan konten respons
	if response.status_code == 200:
		try:
			# Coba parse JSON dan lanjutkan proses
			return response
		except json.JSONDecodeError:
			print(Fore.RED + Style.BRIGHT + "Gagal mengurai JSON dari respons.", flush=True)
			return None
	elif response.status_code == 400:
		try:
			# Coba parse JSON dan lanjutkan proses
			return response
		except json.JSONDecodeError:
			print(Fore.RED + Style.BRIGHT + "Gagal mengurai JSON dari respons.", flush=True)
			return None
	elif response.status_code == 500:
		print(Fore.RED + Style.BRIGHT + f"Gagal claim MiniGame, Internal Server Error", flush=True)
		return response
	else:
		print(Fore.RED + Style.BRIGHT + f"Gagal claim MiniGame, status code: {response.status_code}", flush=True)
		return None

    
def GetAccountConfigRequest(token):
    url = 'https://api.hamsterkombatgame.io/clicker/config'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def exchange(token):
    url = 'https://api.hamsterkombatgame.io/clicker/select-exchange'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"exchangeId": 'binance'})
    response = requests.post(url, headers=headers, data=data)
    return response



def claim_cipher(token, MorseHarian):
    url = 'https://api.hamsterkombatgame.io/clicker/claim-daily-cipher'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"cipher": MorseHarian})
    response = requests.post(url, headers=headers, data=data)
    
    # Tambahkan pengecekan status code dan konten respons
    if response.status_code == 200:
        try:
            # Coba parse JSON dan lanjutkan proses
            return response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "Gagal mengurai JSON dari respons.", flush=True)
            return None
    elif response.status_code == 400:
        try:
            # Coba parse JSON dan lanjutkan proses
            return response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "Gagal mengurai JSON dari respons.", flush=True)
            return None
    elif response.status_code == 500:
        print(Fore.RED + Style.BRIGHT + f"Gagal claim cipher, Internal Server Error", flush=True)
        return response
    else:
        print(Fore.RED + Style.BRIGHT + f"Gagal claim cipher, status code: {response.status_code}", flush=True)
        return None

def check_task(token, task_id):
    url = 'https://api.hamsterkombatgame.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": task_id})
    response = requests.post(url, headers=headers, data=data)
    return response
def cek_booster(token):
    url = 'https://api.hamsterkombatgame.io/clicker/boosts-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response
def use_booster(token,idboost):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-boost'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": idboost, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response

def read_upgrade_list(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]



def get_available_upgrades(token):
    url = 'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        try:
            upgrades = response.json()['upgradesForBuy']
            # print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade	] : Berhasil mendapatkan list upgrade.", flush=True)
            return upgrades
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Upgrade	] : Gagal mendapatkan response JSON.", flush=True)
            return []
    else:
        print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade	] : Gagal mendapatkan daftar upgrade: Status {response.status_code}", flush=True)
        return []


def buy_upgrade(token, upgrade_id, upgrade_name):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-upgrade'
    headers = get_headers(token)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    time.sleep(3)
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        try:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade	] : Upgrade {upgrade_name} berhasil dibeli.", flush=True)
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Upgrade	] : Gagal mengurai JSON saat upgrade.", flush=True)
    else:
        try:
            error_response = response.json()
            if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade	] : Koin tidak cukup wkwkw :V                             ", flush=True)
                return 'insufficient_funds'
            elif error_response.get('error_code') == 'UPGRADE_COOLDOWN':
                cooldown_seconds = error_response.get('cooldownSeconds', 0)
                menit, detik = divmod(cooldown_seconds, 60)
                jam, menit = divmod(menit, 60)
                jam = str(jam).zfill(2)
                menit = str(menit).zfill(2)
                detik = str(detik).zfill(2)
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade	] : {upgrade_name} cooldown. Nunggu {jam} Jam {menit} Menit {detik} Detik.", flush=True)
                return {'cooldown': True, 'cooldown_seconds': cooldown_seconds}
            else:
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade	] : Failed upgrade {upgrade_name}: {error_response}", flush=True)
                return {'error': True, 'message': error_response}
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade	] : Gagal mendapatkan respons JSON. Status: {response.status_code}", flush=True)
            return {'error': True, 'status_code': response.status_code}
def get_available_upgrades_combo(token):
    url = 'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        try:
            upgrades = response.json()['upgradesForBuy']
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Kombo Harian	] : Berhasil mendapatkan list upgrade.", flush=True)
            return upgrades
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Kombo Harian	] : Gagal mendapatkan response JSON.", flush=True)
            return []
    else:
        print(Fore.RED + Style.BRIGHT + f"\r[ Kombo Harian	] : Gagal mendapatkan daftar upgrade: Status {response.status_code}", flush=True)
        return []


def buy_upgrade_combo(token, upgrade_id):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-upgrade'
    headers = get_headers(token)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        try:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Kombo Harian	] : Combo {upgrade_id} berhasil dibeli.", flush=True)
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Kombo Harian	] : Gagal mengurai JSON saat upgrade.", flush=True)
        return response
    else:
        try:
            error_response = response.json()
            if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
                print(Fore.RED + Style.BRIGHT + f"\r[ Kombo Harian	] : Koin ora cukup.", flush=True)
                return 'insufficient_funds'
            else:
                # print(f"error saat beli combo: {error_response}")
                # print(Fore.RED + Style.BRIGHT + f"\r[ Kombo Harian	] : Error: {error_response.get('error_message', 'No error message provided')}", flush=True)
                return error_response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + f"\r[ Kombo Harian	] : Gagal mendapatkan respons JSON. Status: {response.status_code}", flush=True)
            return None

def auto_upgrade_pph_earn(token, harga_maksimal):
    upgrade_list = read_upgrade_list('upgrade_list.txt')
    insufficient_funds = False
    cooldown_upgrades = {}  # Dictionary untuk menyimpan waktu cooldown yang tersisa untuk setiap upgrade

    while not insufficient_funds:
        available_upgrades = get_available_upgrades(token)
        best_upgrade = None
        best_value = 0

        current_time = time.time()

        for upgrade in available_upgrades:
            if upgrade['id'] in upgrade_list and upgrade['isAvailable'] and not upgrade['isExpired']:
                # Periksa apakah upgrade sedang dalam cooldown dan apakah cooldown sudah berakhir
                if upgrade['id'] in cooldown_upgrades and current_time < cooldown_upgrades[upgrade['id']]:
                    continue  # Skip upgrade ini karena masih dalam cooldown

                price = upgrade['price']
                # Skip upgrade jika harga lebih dari harga_maksimal
                if price > harga_maksimal:
                    #print(Fore.YELLOW + Style.BRIGHT + f"[ Upgrade	] : Upgrade {upgrade['name']} dilewati karena harga terlalu tinggi: {price}", flush=True)
                    continue

                profit_per_hour = upgrade['profitPerHour']
                try:
                    value = profit_per_hour / price  # Menghitung nilai per dolar yang diinvestasikan
                except ZeroDivisionError:
                   value = 0

                if value > best_value:
                    best_value = value
                    best_upgrade = upgrade

        if best_upgrade:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade	] : Mencoba upgrade: {best_upgrade['name']} Profit : {best_upgrade['profitPerHour']} Harga : {best_upgrade['price']}", flush=True)
            result = buy_upgrade(token, best_upgrade['id'], best_upgrade['name'])
            if result == 'insufficient_funds':
                print(Fore.RED + Style.BRIGHT + "[ Upgrade	] : Koin ora cukup.", flush=True)
                insufficient_funds = True
            elif isinstance(result, dict) and 'cooldown' in result:
                cooldown_seconds = result['cooldown_seconds']
                cooldown_end_time = current_time + cooldown_seconds
                cooldown_upgrades[best_upgrade['id']] = cooldown_end_time
                print(Fore.YELLOW + Style.BRIGHT + f"[ Upgrade	] : {best_upgrade['name']} masih dalam cooldown. Nunggu {cooldown_seconds // 60} menit {cooldown_seconds % 60} detik..", flush=True)
            elif isinstance(result, dict) and 'error' in result:
                print(Fore.RED + Style.BRIGHT + f"[ Upgrade	] : Gagal upgrade dengan error: {result.get('message', 'No error message provided')}", flush=True)
        else:
            print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade	] : Tidak ada upgrade yang memenuhi kriteria saat ini.", flush=True)
            break  # Keluar dari loop jika tidak ada upgrade yang tersedia
def check_and_upgrade(token, upgrade_id, required_level):
    upgrades = get_available_upgrades_combo(token)
    if upgrades:
        for upgrade in upgrades:
      
            if upgrade['id'] == upgrade_id and upgrade['level'] < required_level + 1:
                print(Fore.CYAN + Style.BRIGHT + f"[ Kombo Harian	] : Upgrading {upgrade_id}", end="", flush=True)
                req_level_total = required_level +1
                for _ in range(req_level_total - upgrade['level']):
                    result = buy_upgrade_combo(token, upgrade_id)
                    # print("buying..")
                    if isinstance(result, dict) and 'error_code' in result and result['error_code'] == 'UPGRADE_NOT_AVAILABLE':
                        # print("ada error")
                        needed_upgrade = result['error_message'].split(':')[-1].strip().split()
                        needed_upgrade_id = needed_upgrade[1]
                        needed_upgrade_level = int(needed_upgrade[-1])
                        print(Fore.YELLOW + Style.BRIGHT + f"\r[ Kombo Harian	] : Mencoba membeli {needed_upgrade_id} level {needed_upgrade_level}", end="", flush=True)
                        if check_and_upgrade(token, needed_upgrade_id, needed_upgrade_level):
                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Kombo Harian	] : Berhasil upgrade {needed_upgrade_id} ke level {needed_upgrade_level}. Coba lagi upgrade {upgrade_id}.", flush=True)
                            continue  # Setelah berhasil, coba lagi upgrade asli
                        else:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Kombo Harian	] : Gagal upgrade {needed_upgrade_id} ke level {needed_upgrade_level}", flush=True)
                            return False
                    elif result == 'insufficient_funds':
                        print("coin")
                        print(Fore.RED + Style.BRIGHT + f"\r[ Kombo Harian	] : Koin ora cukup untuk upgrade {upgrade_id}", flush=True)
                        return False
                    elif result.status_code != 200:
                        print(f"error response : {result}")
                        print(Fore.RED + Style.BRIGHT + f"\r[ Kombo Harian	] : Gagal upgrade {upgrade_id} dengan error: {result}", flush=True)
                        return False
                print(Fore.GREEN + Style.BRIGHT + f"\r[ Kombo Harian	] : Upgrade {upgrade_id} berhasil dilakukan ke level {required_level}", flush=True)
                return True
    # print(Fore.GREEN + Style.BRIGHT + f"\r[ Kombo Harian	] : Upgrade {upgrade_id} berhasil dilakukan ke level {required_level}", flush=True)
    return False
import requests

def claim_daily_combo(token):
    url = 'https://api.hamsterkombatgame.io/clicker/claim-daily-combo'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(Fore.GREEN + Style.BRIGHT + "\r[ Kombo Harian	] : Berhasil mengklaim kombo harian.                                          ", flush=True)
        return response.json()
    else:
        error_response = response.json()
        if error_response.get('error_code') == 'DAILY_COMBO_DOUBLE_CLAIMED':
            print(Fore.RED + Style.BRIGHT + "\r[ Kombo Harian	] : Kombo Sudah pernah dikalim          ", flush=True)
        else:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Kombo Harian	] : Beli Kombo dulu...", flush=True)
        return error_response
    
def check_combo_purchased(token):
    url = 'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        purchased_combos = data.get('dailyCombo', {}).get('upgradeIds', [])
        return purchased_combos
    else:
        print(Fore.RED + Style.BRIGHT + f"Gagal mendapatkan status combo. Status: {response.status_code}", flush=True)
        return None

# MAIN CODE
cek_task_dict = {}
claimed_ciphers = set()
claimed_minigame = set()
combo_upgraded = {}
def main():
    global cek_task_dict, claimed_ciphers, claimed_minigame, auto_klaim_kombo, combo_upgraded
    
    print_welcome_message()
    print(Fore.GREEN + Style.BRIGHT + "Bot dijalankan....")
    init_data = load_tokens('initdata.txt')
    token_cycle = cycle(init_data)

    token_dict = {}  # Dictionary to store successful tokens
    while True:
        init_data_raw = next(token_cycle)
        token = token_dict.get(init_data_raw)
        #Jeda waktu antara bermain Minigame dan klaim Hadiah
        jeda_minigame = random.randint(7, 15)
        #print(f"jeda MiniGame: {jeda_minigame}")
        #time.sleep(1000000)
		
        if token:
            print(Fore.RED + Style.BRIGHT + f"\n\n\n\rAkun: Pernah dibot", flush=True)
            #jeda waktu antar akun,dalam detik
            if jeda_antar_akun == "y":
                jeda = random.randint(1, max_jeda_antar_akun)
            else:
                jeda = 0   
            countdown(jeda)
			
            #print(Fore.RED + Style.BRIGHT + f"\rToken: {token}\n", end="", flush=True)
        else:
            #print(Fore.GREEN + Style.BRIGHT + f"\n\n\rMendapatkan token...              ", flush=True)

            token = get_token(init_data_raw)
            # print(token)
            if token:
                token_dict[init_data_raw] = token
                print(Fore.GREEN + Style.BRIGHT + f"\n\n\rAkun: Aktif", flush=True)
                #print(Fore.GREEN + Style.BRIGHT + f"\rToken: {token}   \n", flush=True)
            else:
                print(Fore.RED + Style.BRIGHT + f"\rBeralih ke akun selanjutnya\n", flush=True)
                continue  # Lanjutkan ke iterasi berikutnya jika gagal mendapatkan token

         # Inisialisasi status combo_upgraded untuk token ini jika belum ada
        if init_data_raw not in combo_upgraded:
            combo_upgraded[init_data_raw] = False

        response = authenticate(token)
   
        ## TOKEN AMAN
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get('telegramUser', {}).get('username', 'Username Kosong')
            firstname = user_data.get('telegramUser', {}).get('firstName', 'Kosong')
            lastname = user_data.get('telegramUser', {}).get('lastName', 'Kosong')
            print(Fore.GREEN + Style.BRIGHT + f"~~~~~~[{Fore.WHITE + Style.BRIGHT} {username} | {firstname} {lastname} {Fore.GREEN + Style.BRIGHT}]~~~~~~")
            # Sync Clicker
            print(Fore.GREEN + f"\rGetting info user...", end="", flush=True)
            response = sync_clicker(token)
            if response.status_code == 200:
                clicker_data = response.json()['clickerUser']
                print(Fore.YELLOW + Style.BRIGHT + f"\r[ Level		] : {clicker_data['level']}")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Total Earned	] : {int(clicker_data['totalCoins'])}")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Coin		] : {int(clicker_data['balanceCoins'])}")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Energy	] : {clicker_data['availableTaps']}")
                boosts = clicker_data['boosts']
                boost_max_taps_level = boosts.get('BoostMaxTaps', {}).get('level', 0)
                boost_earn_per_tap_level = boosts.get('BoostEarnPerTap', {}).get('level', 0)
                
                print(Fore.CYAN + Style.BRIGHT + f"[ Level Energy	] : {boost_max_taps_level}")
                print(Fore.CYAN + Style.BRIGHT + f"[ Level Tap	] : {boost_earn_per_tap_level}")
                print(Fore.CYAN + Style.BRIGHT + f"[ Exchange	] : {clicker_data['exchangeId']}")
                # print(clicker_data['exchangeId'])
                if clicker_data['exchangeId'] == None:
                    print(Fore.GREEN + '\rSeting exchange to Binance..',end="", flush=True)
                    exchange_set = exchange(token)

                    if exchange_set.status_code == 200:
                        print(Fore.GREEN + Style.BRIGHT +'\rSukses set exchange ke Binance', flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT +'\rGagal set exchange', flush=True)
                print(Fore.CYAN + Style.BRIGHT + f"[ Pendapatan/Jam] : {clicker_data['earnPassivePerHour']}\n")
                
                
                print(Fore.GREEN + f"\r[ Tap Status	] : Tapping ...", end="", flush=True)



                response = tap(token, clicker_data['maxTaps'], clicker_data['availableTaps'])
                if response.status_code == 200:
                    print(Fore.GREEN + Style.BRIGHT + "\r[ Tap Status	] : Sukses Tap Tap...            ", flush=True)
                    print(Fore.CYAN + Style.BRIGHT + f"\r[ Booster	] : Checking booster...", end="", flush=True)
                    response = cek_booster(token)
                    if response.status_code == 200:
                        booster_info = response.json()['boostsForBuy']
                        for boost in booster_info:
                            if boost['id'] == 'BoostFullAvailableTaps':
                                stock = boost['maxLevel'] - boost['level'] 
                                cooldown = boost['cooldownSeconds']
                                menit, detik = divmod(cooldown, 60)
                                jam, menit = divmod(menit, 60)
                                jam = str(jam).zfill(2)
                                menit = str(menit).zfill(2)
                                detik = str(detik).zfill(2)
                                if jam == '00':
                                    jamnya = ""
                                else:
                                    jamnya = f"{jam} Jam "
                                if menit == '00':
                                    menitnya = ""
                                else:
                                    menitnya = f"{menit} Menit "
                                if stock == -1:
                                    stock ="Habis"
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Booster	] : Stok {stock} | Cooldown {jamnya}{menitnya}{detik} Detik    ", flush=True)
                        if cooldown == 0:
                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Boosted ] : Aktivasi Booster..", end="", flush=True)
                            response = use_booster(token,"BoostFullAvailableTaps")
                            if response.status_code == 200:
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Boosted ] : Booster Activated", flush=True)   
                            elif response.status_code == 400:
                                error_info = response.json()
                                if error_info.get('error_code') == 'BOOST_COOLDOWN':
                                    cooldown_seconds = int(error_info.get('error_message').split()[-2])
                                    cooldown_minutes = cooldown_seconds // 60
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Boosted ] : Booster dalam cooldown {cooldown_minutes} menit", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Boosted ] : Gagal mengaktifkan booster", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + f"\r[ Boosted ] : Gagal mengaktifkan booster", flush=True)

                        

                    else:
                        print(Fore.RED + Style.BRIGHT + "\r[ Booster	] : Tap Status : Gagal Tap           ", flush=True)

                
                else:
                    print(Fore.RED + Style.BRIGHT + "\r[ Tap Status	] : Gagal Tap           ", flush=True)
                    # continue 
                time.sleep(1)
                              
                # Absen Harian
                if auto_absen == 'y':
                    print(Fore.GREEN + f"\r[ Absen Harian	] : Checking...", end="", flush=True)  
                    response = claim_daily(token)
                    if response.status_code == 200:
                        daily_response = response.json()['task']
                        if daily_response['isCompleted']:
                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Absen Harian	] :  Hari ke {daily_response['days']} | Selesai..", flush=True)
                        else:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Absen Harian	] :  Hari ke {daily_response['days']} | Sudah absen sebelumya", flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT + f"\r[ Absen Harian	] :  Gagal Ngabsen.. {response.status_code}", flush=True)
                else:
                    print(Fore.BLUE + f"\r[ Absen Harian	] : --> OFF", flush=True)   
                    
                # Ambil data Morse dan di decode jadi Daily Cipher
                MorseHarian = ""   
                if auto_morse == 'y':
                    response = GetAccountConfigRequest(token)
                    if response.status_code == 200:
                        DataMorse = response.json()
                    MorseHarian = DailyCipherDecode(DataMorse["dailyCipher"]["cipher"])
                    KodeMorse = TextToMorseCode(MorseHarian)
                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Morse Harian	] : Kata: {MorseHarian} , Morse: {KodeMorse}")
                    if token not in claimed_ciphers:
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Klaim Morse	] : Claiming Morse...", end="", flush=True)
                        response = claim_cipher(token, MorseHarian)
                        try:
                            if response.status_code == 200:
                                bonuscoins = response.json()['dailyCipher']['bonusCoins']
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Klaim Morse	] : Berhasil claim Morse | {bonuscoins} bonus coin", flush=True)
                                claimed_ciphers.add(token)
                            else:
                                error_info = response.json()
                                if error_info.get('error_code') == 'DAILY_CIPHER_DOUBLE_CLAIMED':
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Klaim Morse	] : Morse sudah pernah diklaim", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Klaim Morse	] : Gagal klaim Morse dengan error: {error_info.get('error_message', 'No error message')}", flush=True)
                        except json.JSONDecodeError:
                            print(Fore.RED + Style.BRIGHT + "\r[ Klaim Morse	] : Gagal mengurai JSON dari respons.", flush=True)
                        except Exception as e:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Klaim Morse	] : Terjadi error: {str(e)}", flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT + f"\r[ Klaim Morse	] : Morse sudah pernah di-klaim sebelumnya.", flush=True)
                else:
                    print(Fore.BLUE + f"\r[ Klaim Morse	] : --> OFF", flush=True)
                    
                    
                    
				# Main mini Game
                if auto_minigame == 'y':
                    response = start_minigame(token)
                    if response.status_code == 200:
                        print(Fore.GREEN + Style.BRIGHT + "\r[ Mini Game	] : Persiapan main MiniGame            ", flush=True)
                        countdown(jeda_minigame)
                    if token not in claimed_minigame:
                        print(Fore.GREEN + Style.BRIGHT + "\r[ Mini Game	] : Bermain MiniGame            ", flush=True)
                        response = klaim_MiniGame(token,jeda_minigame)
                        try:
                            if response.status_code == 200:
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Mini Game	] : Berhasil Klaim MiniGame            ", flush=True)
                                claimed_minigame.add(token)
                            else:
                                error_info = response.json()
                                if error_info.get('error_code') == 'DAILY_KEYS_MINI_GAME_DOUBLE_CLAIMED':
                                    print(Fore.BLUE + Style.BRIGHT + f"[ Mini Game	] : Sudah main MiniGame sebelumnya            ", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Mini Game	] : Gagal main MiniGame dengan error: {error_info.get('error_message', 'No error message')}", flush=True)
                        except json.JSONDecodeError:
                            print(Fore.RED + Style.BRIGHT + "\r[ Mini Game	] : Gagal mengurai JSON dari respons.", flush=True)
                        except Exception as e:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Mini Game	] : Terjadi error: {str(e)}", flush=True)
                    else:
                        print(Fore.BLUE + Style.BRIGHT + f"[ Mini Game	] : Sudah main MiniGame sebelumnya            ", flush=True)
                else:
                    print(Fore.BLUE + f"\r[ Mini Game	] : --> OFF            ", flush=True)
				
                # kombo harian
                if auto_klaim_kombo == 'y' and not combo_upgraded[init_data_raw]:
                    cek = claim_daily_combo(token)
                    if cek.get('error_code') != 'DAILY_COMBO_DOUBLE_CLAIMED':
                        purchased_combos = check_combo_purchased(token)
                        if purchased_combos is None:
                            print(Fore.RED + Style.BRIGHT + "\r[ Kombo Harian	] : Gagal mendapatkan status kombo, akan mencoba lagi dengan akun berikutnya.", flush=True)
                        else:
                            for combo in njaluk_kombo("item"):
                                if combo in purchased_combos:
                                    print(Fore.BLUE + Style.BRIGHT + f"\r[ Kombo Harian	] : {combo} sudah dibeli.", flush=True)
                                elif combo == "none":
                                    continue
                                else:
                                    print(Fore.GREEN + f"\r[ Kombo Harian	] : Beli {combo}", end="", flush=True)
                                    result = buy_upgrade_combo(token, combo)
                                    if result == 'insufficient_funds':
                                        print(Fore.RED + Style.BRIGHT + f"\r[ Kombo Harian	] : Gagal membeli {combo}, koin tidak cukup", flush=True)
                                    elif 'error_code' in result and result['error_code'] == 'UPGRADE_NOT_AVAILABLE':
                                        #print(upgrade_details = result['error_message'])
                                        upgrade_details = result['error_message'].split(':')[-1].strip().split()
                                        upgrade_key = upgrade_details[1]
                                        upgrade_level = int(upgrade_details[-1])
                                        print(Fore.RED + Style.BRIGHT + f"\r[ Kombo Harian	] : Gagal beli {combo} membutuhkan {upgrade_key} level {upgrade_level}", flush=True)    
                                        print(Fore.YELLOW + Style.BRIGHT + f"\r[ Kombo Harian	] : Mencoba membeli {upgrade_key} level {upgrade_level}", flush=True)    
                                        result = check_and_upgrade(token, upgrade_key, upgrade_level)
                            combo_upgraded[init_data_raw] = True
                            required_combos = set(njaluk_kombo("item"))
                            purchased_combos = set(check_combo_purchased(token))
                            if purchased_combos == required_combos:
                                print(Fore.GREEN + Style.BRIGHT + "\r[ Kombo Harian	] : Semua kombo telah dibeli, mencoba mengklaim Bonus 5jt.                 ", end="" ,flush=True)
                                claim_daily_combo(token)
                            elif combo == "none":
                                print(Fore.BLUE + f"\r[ Kombo Harian	] Kombo belum siap, nunggu update server...", flush=True)
                                print(Fore.RED + Style.BRIGHT + f"\r[ Kombo Harian	] Belum berhasil klaim Kombo Harian..", flush=True)
								
                            else:
                                print(Fore.RED + Style.BRIGHT + f"\r[ Kombo Harian	] : Gagal. Kombo yang belum dibeli: {required_combos - purchased_combos}               " , flush=True)
                                combo_upgraded[init_data_raw] = False
                                # Tambahkan loop untuk mencoba lagi
                                continue
                else:
                    print(Fore.BLUE + f"\r[ Kombo Harian	] : --> OFF", flush=True)
				
				
				
				
                # List Tasks
                if auto_cek_task_list == 'y':
                    print(Fore.GREEN + f"\r[ List Task	] : Checking...", end="", flush=True)
                    if token not in cek_task_dict:  # Pastikan token ada dalam dictionary
                        cek_task_dict[token] = False  # Inisialisasi jika belum ada
                    if not cek_task_dict[token]:  # Cek status cek_task untuk token ini
                        response = list_tasks(token)
                        cek_task_dict[token] = True  # Set status cek_task menjadi True setelah dicek
                        if response.status_code == 200:
                            tasks = response.json()['tasks']
                            all_completed = all(task['isCompleted'] or task['id'] == 'invite_friends' for task in tasks)
                            if all_completed:
                                print(Fore.GREEN + Style.BRIGHT + "\r[ List Task	] : Semua task sudah diklaim\n", flush=True)
                            else:
                                for task in tasks:
                                    if not task['isCompleted']:
                                        print(Fore.YELLOW + Style.BRIGHT + f"\r[ List Task	] : Claiming {task['id']}...", end="", flush=True)
                                        response = check_task(token, task['id'])
                                        if response.status_code == 200 and response.json()['task']['isCompleted']:
                                            print(Fore.GREEN + Style.BRIGHT + f"\r[ List Task	] : Pernah Diklaim sebelumnya {task['id']}\n", flush=True)
                                        else:
                                            print(Fore.RED + Style.BRIGHT + f"\r[ List Task	] : Gagal Claim {task['id']}\n", flush=True)
                        else:
                            print(Fore.RED + Style.BRIGHT + f"\r[ List Task	] : Gagal mendapatkan list task {response.status_code}\n", flush=True)
                else:
                    print(Fore.BLUE + f"\r[ Task Harian	] : --> OFF", flush=True) 
                 #Upgrade Energi
                if auto_upgrade_energy == 'y':
                    response = cek_booster(token)
                    if response.status_code == 200:
                        booster_info = response.json()['boostsForBuy']
                        for boost in booster_info:
                            if boost['id'] == 'BoostMaxTaps':
                                lvenergi = boost['level']
                                lvsekarang = lvenergi-1
                        if lvenergi <= lv_upgrade_energy:
                            print(Fore.GREEN + f"\r[ Upgrade	] : Upgrading Energy....", end="", flush=True)
                            upgrade_response = use_booster(token, "BoostMaxTaps")
                            if upgrade_response.status_code == 200:
                                level_boostmaxtaps = upgrade_response.json()['clickerUser']['boosts']['BoostMaxTaps']['level']
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade	] : Energi Sukses Diupgrade Kelevel {level_boostmaxtaps}", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + "\r[ Upgrade	] : Upgrade Energi Gagal..", flush=True)
                        else:
                            print(Fore.BLUE + Style.BRIGHT + f"\r[ Upgrade	] : Energi tidak diupgrade,sudah Level: {lvsekarang}", flush=True)
                else:
                    print(Fore.BLUE + f"\r[ Upgrade Energi] : --> OFF", flush=True)
                 #Upgrade MultiTap
                if auto_upgrade_energy == 'y':
                    response = cek_booster(token)
                    if response.status_code == 200:
                        booster_info = response.json()['boostsForBuy']
                        for boost in booster_info:
                            if boost['id'] == 'BoostEarnPerTap':
                                lvtap = boost['level']
                                lvsekarang = lvtap-1
                        if lvtap <= lv_upgrade_energy:
                            print(Fore.GREEN + f"\r[ Upgrade	] : Upgrading MultiTap....", end="", flush=True)
                            upgrade_response = use_booster(token, "BoostEarnPerTap")
                            if upgrade_response.status_code == 200:
                                level_boostmaxtaps = upgrade_response.json()['clickerUser']['boosts']['BoostEarnPerTap']['level']
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade	] : MultiTap Sukses Diupgrade Kelevel {level_boostmaxtaps}", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + "\r[ Upgrade	] : Upgrade MultiTap Gagal..", flush=True)
                        else:
                            print(Fore.BLUE + Style.BRIGHT + f"\r[ Upgrade	] : MultiTap tidak diupgrade, sudah Level: {lvsekarang}", flush=True)
                else:
                    print(Fore.BLUE + f"\r[ Upgrade MultiTap]: --> OFF", flush=True)

                
                # cek upgrade
                if auto_upgrade_pph == 'y':
                    print(Fore.GREEN + f"\r[ Upgrade	] : Checking...", end="", flush=True)
                    auto_upgrade_pph_earn(token, harga_maksimal)
                else:
                    print(Fore.BLUE + f"\r[ Auto Upgrade	] : --> OFF", flush=True)
                    
            else:
                print(Fore.RED + Style.BRIGHT + f"\r Gagal mendapatkan info user {response.status_code}", flush=True) 
            print(Fore.GREEN + Style.BRIGHT + "\r==========================================")



        ## TOKEN MATI        
        elif response.status_code == 401:
            error_data = response.json()
            if error_data.get("error_code") == "NotFound_Session":
                print(Fore.RED + Style.BRIGHT + f"=== [ Token Invalid {token} ] ===")
                token_dict.pop(init_data_raw, None)  # Remove invalid token
                token = None  # Set token ke None untuk mendapatkan token baru di iterasi berikutnya
            else:
                print(Fore.RED + Style.BRIGHT + "Authentication failed with unknown error")
        else:
            print(Fore.RED + Style.BRIGHT + f"Error with status code: {response.status_code}")
            token = None  # Set token ke None jika terjadi error lain
            
        time.sleep(1)

def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "Hamster Kombat BOT!")
    print(Fore.GREEN + Style.BRIGHT + "Update Link: https://github.com/adearman/hamsterkombat")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.BLUE + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA")
    print(Fore.RED + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)")
    print(Fore.GREEN + Style.BRIGHT + "\n=============================================")
    print(Fore.YELLOW + Style.BRIGHT + "\n\rRecode By Una Davina ( https://t.me/unadavina )")
    print(Fore.GREEN + Style.BRIGHT + "\n=============================================")
#print kombo
    print(Fore.GREEN + Style.BRIGHT + f"\r\nKombo Tanggal: {njaluk_kombo("tanggal")}", flush=True)
    print(Fore.GREEN + Style.BRIGHT + f"\rKombo: {njaluk_kombo("item")}", flush=True)
    print(Fore.GREEN + Style.BRIGHT + "\n=============================================")

if __name__ == "__main__":
    main()
