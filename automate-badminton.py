from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from shutil import which
import time
import random 
import os

load_dotenv()

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")  # NEW: Hide automation
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # NEW
options.add_experimental_option('useAutomationExtension', False)

x = which("chromedriver")
service =  Service(x)
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://centresportifdelapetitebourgogne.ca/en/")
    print("Site opened")
    
    driver.maximize_window()
    print("Maximized")
    close_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME,"once-popup-cross"))
    )
    close_button.click()
    register_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Register"))
    )
    register_button.click()
    print("Found Register button")
    
    time.sleep(5)
    tabs = driver.window_handles
    driver.switch_to.window(tabs[-1])
    print("Tab switched yay :", driver.current_url)
    time.sleep(5)
    try:
        cookie_button =  WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"button.cc-nb-okagree"))
        )
        cookie_button.click()
        print("Cookie founded")
    except Exception as e:
        print("Fcked")
    
    login_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
    )
    login_button.click()
    time.sleep(5)

    driver.find_element(By.ID, "CodeUtilisateur").send_keys(os.getenv("EMAIL"))
    max_attempts = 3
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        print(f"Attempt {attempt} = {max_attempts}")
        driver.find_element(By.ID, "motPasse").send_keys(os.getenv("PASSWORD"))

        loginf_button = WebDriverWait(driver, 15).until( 
            EC.element_to_be_clickable((By.ID, "btnConnexion")) 
        )
        actions = ActionChains(driver)
        actions.move_to_element(loginf_button).pause(random.uniform(1.5, 2.0)).perform()

        loginf_button = driver.find_element(By.ID, "btnConnexion")
        loginf_button.click()
        time.sleep(5)
        try :
            WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Invalid captcha')]")
                )
            )
            print("Invalid Captcha")
            if attempt >= max_attempts:
                print("Attempts aipaye dengey - 409 error")
                break

            wait_time = random.uniform(5,8)
            print("Waiting")
            time.sleep(wait_time)

            continue
        except TimeoutException:
            print("Logged in Finally")
            break

    
    l_dropdown = Select(driver.find_element(By.ID, "ddlLangue"))
    l_dropdown.select_by_value("en")
    print("Language changed yolo")

    avail = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Availabilities / Facility rental"))
    )
    avail.click()
    print("Facility clicked")
    
    input("Press ENTER to exit...")

    

finally:
    driver.quit()
