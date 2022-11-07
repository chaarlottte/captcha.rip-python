# captcha.rip-python
API wrapper for https://captcha.rip written in Python.

captcha.rip is an API built to solve FunCaptcha tasks. This is a python-based wrapper that I built for it to make things easier for myself.

## Installation
Simply run the command `pip install captcha.rip-api`, then use `from captcharip.solver import solver` to use the solver. 

## Usage
You can check some of the [examples](https://github.com/chaarlottte/captcha.rip-python/tree/main/examples) I have provided if you want a more in-depth example than below.

```python
import requests
import json
import time
from captcharip.solver import solver

captchaSolver = solver("yourkey", True) # initialize the solver. params: your captcha.rip API key, whether to enable debug mode
publicKey = captchaSolver.getPublicKey(url) # get a site's public key. params: the URL you want to get the public key from
taskId = captchaSolver.createTask(url, publicKey, "https://client-api.arkoselabs.com") # starts a captcha task and gives you the task's ID. params: url where the captcha is (such as a register page), public key of the site, and the api endpoint for getting the captcha
token = "notReceivedYet"

while(token == "notReceivedYet"):
    token = captchaSolver.fetchTask(taskId) # gets the captcha solution. if there is not one yet, it will return "notReceivedYet". params: task ID
    time.sleep(3)

print(f"Got captcha token - {token}") # It should break out of the loop when it has received the captcha solution. You can then use this for whatever you want.
```

Clearly not the greatest documentation, sorry about that. I'll improve it in the future.

If you have any questions, suggestions, bug reports, etc, feel free to open an issue.
