from colorama import Fore, Back, Style

class CaptchaRipOfflineError(Exception):
    def __init__(self):
        super().__init__(f"{Fore.RED}{Style.BRIGHT}Captcha.rip is currently offline.{Style.RESET_ALL}")

class PublicKeyBlacklistedError(Exception):
    def __init__(self):
        super().__init__(f"{Fore.RED}{Style.BRIGHT}The public key you are using is blacklisted.{Style.RESET_ALL}")

class CaptchaRipError(Exception):
    def __init__(self, json):
        self.message = json["message"]
        self.code = str(json["code"])
        super().__init__(f"Error with the captcha.rip API: {self.message} (Code {self.code})")