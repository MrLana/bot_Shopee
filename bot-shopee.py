import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Konfigurasi
SHOPEE_URL = "https://shopee.co.id"
PRODUCT_URL = "URL_PRODUK_SHOPEE"  # Ganti dengan URL produk flash sale
FLASH_SALE_TIME = "2023-12-31 20:00:00"  # Format: YYYY-MM-DD HH:MM:SS
USERNAME = "email_atau_username_anda"
PASSWORD = "password_anda"

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def login(driver):
    print("Melakukan login...")
    driver.get(f"{SHOPEE_URL}/buyer/login")
    
    # Tunggu dan isi form login
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Email/Username/Nomor Telepon']"))
    ).send_keys(USERNAME)
    
    driver.find_element(By.XPATH, "//input[@placeholder='Kata Sandi']").send_keys(PASSWORD)
    
    driver.find_element(By.XPATH, "//button[contains(text(),'Masuk')]").click()
    
    # Tunggu login selesai (verifikasi captcha mungkin muncul)
    time.sleep(10)

def wait_until_sale_time():
    sale_time = datetime.strptime(FLASH_SALE_TIME, "%Y-%m-%d %H:%M:%S")
    print(f"Menunggu hingga waktu flash sale: {sale_time}")
    
    while True:
        current_time = datetime.now()
        if current_time >= sale_time:
            break
        time_diff = (sale_time - current_time).total_seconds()
        print(f"Waktu tersisa: {time_diff:.1f} detik", end="\r")
        time.sleep(0.1)
    
    print("\nWaktu flash sale telah tiba!")

def buy_product(driver):
    print("Membuka halaman produk...")
    driver.get(PRODUCT_URL)
    
    try:
        # Cek apakah flash sale sudah aktif
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Flash Sale')]"))
        )
        
        # Klik tombol "Beli Sekarang"
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Beli Sekarang')]"))
        ).click()
        
        print("Tombol beli berhasil diklik!")
        
        # Proses checkout
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Checkout')]"))
        ).click()
        
        print("Proses checkout berhasil!")
        
        # Pilih metode pembayaran (contoh: ShopeePay)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'ShopeePay')]"))
        ).click()
        
        # Klik tombol Bayar
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Bayar')]"))
        ).click()
        
        print("Pembelian berhasil dilakukan!")
        
    except Exception as e:
        print(f"Gagal melakukan pembelian: {str(e)}")

def main():
    driver = setup_driver()
    try:
        login(driver)
        wait_until_sale_time()
        buy_product(driver)
    except Exception as e:
        print(f"Terjadi error: {str(e)}")
    finally:
        time.sleep(10)  # Tunggu sebelum menutup browser
        driver.quit()

if __name__ == "__main__":
    main()