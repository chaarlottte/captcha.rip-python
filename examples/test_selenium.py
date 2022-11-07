from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from urllib.parse import quote
import json
import time

from captcha.solver import solver

siteKeyPattern = 'public_key: "(.+?)",'
url = "https://client-demo.arkoselabs.com/solo-animals"

with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)
    key = config["captcha.rip key"]
    enableDebug = config["debug"]

def main():
    driver = Chrome()
    driver.get(url)
    captchaSolver = solver(enableDebug, True)
    publicKey = captchaSolver.getPublicKeyFromText(driver.page_source)
    taskId = captchaSolver.createTask(url, publicKey, "https://client-api.arkoselabs.com")
    token = "notReceivedYet"

    while(token == "notReceivedYet"):
        token = captchaSolver.fetchTask(taskId)
        time.sleep(3)

    print(f"Got captcha token - {token}")
    script = """
    document.getElementById('FunCaptcha-Token').value = decodeURIComponent('{0}');
    document.getElementById('verification-token').value = decodeURIComponent('{0}');
    document.getElementById('submit-btn').disabled = false;
    """.format(
        quote(token)
    )
    driver.execute_script(script)
    driver.find_element(By.ID, "submit-btn").click()
    
    if "Solved!" in driver.page_source:
        print("Captcha solved successfully.")

if __name__ == '__main__':
    main()