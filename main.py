import requests, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from termcolor import cprint

extension_code = 'ncokmkfeehmcgmpmnobehdoblgonipec'



def main(zero, ads_id, seed, password):
    try:
        # working with ads brow
        open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + ads_id
        close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + ads_id
        resp = requests.get(open_url).json()
        chrome_driver = resp["data"]["webdriver"]
        chrome_options = Options()
        service = Service(executable_path=chrome_driver)
        chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # ads browser has been opened
        url = f'chrome-extension://{extension_code}/home.html'
        driver.get(url)
        time.sleep(5)
        # Goes to the main page
        sign_in_with_phrase_x_path = '//*[@id="root"]/div[1]/div/div[2]/div/div/div[3]/div/div[2]/button'
        try:
            wait_elem = WebDriverWait(driver, 4).until(EC.presence_of_element_located(
                (By.XPATH, sign_in_with_phrase_x_path)))
        except:
            if driver.current_url != url:
                driver.get(url)

        wait_elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, sign_in_with_phrase_x_path)))
        driver.find_element(By.XPATH, sign_in_with_phrase_x_path).click()

        words = seed.split()
        for x in range(12):
            phrase_word_x_path_11 = '//*[@id="headlessui-combobox-input-:ra:"]'
            phrase_word_x_path_12 = '//*[@id="headlessui-combobox-input-:rb:"]'
            phrase_word_x_path = f'//*[@id="headlessui-combobox-input-:r{x}:"]'
            if x == 10:
                phrase_word_x_path = phrase_word_x_path_11
            if x == 11:
                phrase_word_x_path = phrase_word_x_path_12

            wait_elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, phrase_word_x_path)))
            # insert a word from phrase
            driver.find_element(By.XPATH, phrase_word_x_path).send_keys(words[x])
            driver.find_element(By.XPATH, phrase_word_x_path).click()

        time.sleep(1)
        confirm_butt_x_path = '//*[@id="confirm"]'
        driver.find_element(By.XPATH, confirm_butt_x_path).click()

        my_pass_x_path = '//*[@id="password"]/div[1]/input'
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, my_pass_x_path)))
        driver.find_element(By.XPATH, my_pass_x_path).send_keys(password)
        driver.find_element(By.XPATH, my_pass_x_path).click()

        confirm_pass_x_path = '//*[@id="password"]/div[2]/input'
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, confirm_pass_x_path)))
        driver.find_element(By.XPATH, confirm_pass_x_path).send_keys(password)
        driver.find_element(By.XPATH, confirm_pass_x_path).click()

        time.sleep(1)
        sign_in_the_wallet_x_path = '//*[@id="root"]/div[1]/div/div[2]/div/div[2]/button[1]'
        driver.find_element(By.XPATH, sign_in_the_wallet_x_path).click()

        time.sleep(4)

        #quit.
        driver.quit()
        requests.get(close_url)
        cprint(f'{zero + 1}. {ads_id} = Successfully logged', 'green')

    except Exception as ex:
        cprint(f'{zero + 1}. {ads_id} = already wallet logged', 'yellow')
        driver.quit()
        requests.get(close_url)


with open("id_users.txt", "r") as f:
    id_users = [row.strip() for row in f]

with open("seeds.txt", "r") as f:
    seeds = [row.strip() for row in f]

zero = -1
for ads_id in id_users:
    zero = zero + 1
    seed = seeds[zero]
    password = ''  # password for wallet

    main(zero, ads_id, seed, password)
