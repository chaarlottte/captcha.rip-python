import requests, re
from colorama import Fore, Back, Style
from exceptions import *

class solver():
    def __init__(self, key, debug=False):
        self.key = key
        self.enableDebugging = debug
        self.debug(f"Initialized with captcha key {key}.")
        self.debug(f"Checking balance...")

        headers = {
            "authorization": self.key
        }

        resp = requests.get("https://captcha.rip/api/balance", headers=headers).json()
        balance = resp['balance']
        self.log(f"Your balance is currently ${str(balance)}. This is likely enough for {int(balance / 3 * 1000)} captchas to be solved.")

    def getPublicKey(self, url):
        pageSource = requests.get(url).text
        publicKey = re.search("public_key: \"(.+?)\",", pageSource).group(1)
        self.debug(f"Got public key for {url} - {Fore.CYAN}{publicKey}")
        return publicKey

    def getPublicKeyFromText(self, text):
        publicKey = re.search("public_key: \"(.+?)\",", text).group(1)
        self.debug(f"Got public key from text - {Fore.CYAN}{publicKey}")
        return publicKey

    def getBalance(self):
        self.debug(f"Checking balance...")

        headers = {
            "authorization": self.key
        }

        resp = requests.get("https://captcha.rip/api/balance", headers=headers).json()
        return resp["balance"]

    def getCaptchasLeft(self):
        self.debug(f"Checking balance...")
        
        headers = {
            "authorization": self.key
        }

        resp = requests.get("https://captcha.rip/api/balance", headers=headers).json()
        return resp["balance"] / 3 * 1000

    def createTask(self, site, publicKey, service="https://client-api.arkoselabs.com", blob="blob"):
        body = {
            "key": self.key,
            "task": {
                "type": "FunCaptchaTaskProxyless",
                "site_url": str(site),
                "public_key": str(publicKey),
                "service_url": str(service),
                "blob": blob
            }
        }

        self.debug(f"Gathered data for request - {body}")
        resp = requests.post("https://captcha.rip/api/create", json=body).json()
        self.debug(f"Sent request.")

        code = resp["code"]

        match code:
            case 24:
                return PublicKeyBlacklistedError()
            case 25:
                self.log(f"captcha.rip is currently {Fore.RED}{Style.BRIGHT}offline{Fore.LIGHTGREEN_EX}{Style.NORMAL}, sorry.")
                return CaptchaRipOfflineError()

        self.id = resp["id"]
        self.debug(f"Got captcha task ID - {Fore.CYAN}{self.id}")
        return self.id

    def fetchTask(self):
        self.fetchTask(self.id)
    
    def fetchTask(self, id):
        body = {
            "key": self.key,
            "id": id
        }

        self.debug(f"Fetching task with ID {id}.")
        resp = requests.post("https://captcha.rip/api/fetch", json=body).json()
        self.debug(f"Sent request.")

        code = resp["code"]

        if code == 25:
            self.log(f"captcha.rip is currently {Fore.RED}{Style.BRIGHT}offline{Fore.LIGHTGREEN_EX}{Style.NORMAL}, sorry.")
            raise CaptchaRipOfflineError()

        self.debug(f"Got response - {resp}")
        
        if code == 1:
            token = resp["token"]
            self.debug(f"Got captcha token - {Fore.CYAN}{token}")
            return token
        else:
            self.debug(f"Captcha has not been solved yet.")
            return "notReceivedYet"

    def debug(self, s):
        if self.debug:
            print(f"{Back.BLACK}{Fore.LIGHTGREEN_EX}[{Fore.YELLOW}Debug{Fore.LIGHTGREEN_EX}] {s}{Style.RESET_ALL}")

    def log(self, s):
        print(f"{Back.BLACK}{Fore.LIGHTGREEN_EX}[Solver] {s}{Style.RESET_ALL}")
