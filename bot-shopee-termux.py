import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Konfigurasi
PRODUCT_URL = "https://shopee.co.id/produk-anda"  # Ganti dengan URL produk
FLASH_SALE_TIME = "2025-07-06 20:00:00"  # Format: YYYY-MM-DD HH:MM:SS
CHECK_INTERVAL = 2  # detik

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
    "Referer": "https://shopee.co.id/",
}

def is_flash_sale_active():
    try:
        response = requests.get(PRODUCT_URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        return "flash sale" in soup.text.lower() or "beli sekarang" in soup.text.lower()
    except Exception as e:
        print(f"Error memeriksa produk: {e}")
        return False

def wait_until_sale_time():
    sale_time = datetime.strptime(FLASH_SALE_TIME, "%Y-%m-%d %H:%M:%S")
    print(f"Menunggu hingga waktu flash sale: {sale_time}")

    while True:
        now = datetime.now()
        if now >= sale_time:
            break
        remaining = (sale_time - now).total_seconds()
        print(f"Waktu tersisa: {remaining:.1f} detik", end="\r")
        time.sleep(1)

    print("\nWaktu flash sale tiba!")

def pantau_flash_sale():
    print("Memantau produk...")
    while True:
        if is_flash_sale_active():
            print("🔥 Flash sale aktif atau tombol 'Beli Sekarang' tersedia!")
            break
        print("Belum ada flash sale. Cek lagi dalam beberapa detik...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    wait_until_sale_time()
    pantau_flash_sale()
