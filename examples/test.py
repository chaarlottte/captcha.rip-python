import requests
import json
import time
from captcharip.solver import solver

with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)
    key = config["captcha.rip key"]
    enableDebug = config["debug"]

def main():
    captchaSolver = solver(key, enableDebug)
    publicKey = captchaSolver.getPublicKey("https://client-demo.arkoselabs.com/solo-animals")
    taskId = captchaSolver.createTask("https://client-demo.arkoselabs.com/solo-animals", publicKey, "https://client-api.arkoselabs.com")
    token = "notReceivedYet"

    while(token == "notReceivedYet"):
        token = captchaSolver.fetchTask(taskId)
        time.sleep(3)

    print(f"Got captcha token - {token}")

    body = {
        "name": "",
        "verification-token": token,
        "fc-token": token
    }

    resp = requests.post("https://client-demo.arkoselabs.com/solo-animals/verify", json=body).text
    print(resp)

if __name__ == '__main__':
    main()