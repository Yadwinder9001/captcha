from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time

# Instantiate the WebDriver
#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

print("Setting up webdriver...\n")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 " \
             "Safari/537.36 "
options = webdriver.ChromeOptions()
options.headless = False
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)

# Load the target page
captcha_page_url = "https://login.thetimes.co.uk?gotoUrl=https://www.thetimes.co.uk/"
driver.get(captcha_page_url)
#time.sleep(10)
current_url = driver.current_url

# Solve the Captcha
print("Solving Captcha")
solver = TwoCaptcha("API KEY")
response = solver.recaptcha(sitekey='6Lfl3pAlAAAAAG6IQn_NPGeLnCVWC7QdDCIAZpkM', url=current_url)
code = response['code']
print(f"Successfully solved the Captcha. The solve code is {code}")

#time.sleep(50)
# Set the solved Captcha
recaptcha_response_element = driver.find_element(By.ID, 'g-recaptcha-response')
driver.execute_script(f'arguments[0].value = "{code}";', recaptcha_response_element)
#callback = f"___grecaptcha_cfg.clients[0].P.P.callback('{code}')"
print(recaptcha_response_element)

#js_executor = driver.execute_script
#print(js_executor(callback))

driver.execute_script(f"___grecaptcha_cfg.clients[0].P.P.callback('{code}')")

# Pause the execution so you can see the screen after submission before closing the driver
input("Press enter to continue")
driver.close()
