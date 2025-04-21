# Check_rkn

[![PyPI](https://img.shields.io/pypi/v/check-rkn)](https://pypi.org/project/check-rkn/)

This is library, that check blocked websites on [blocklist.rkn.gov.ru](https://blocklist.rkn.gov.ru/). Library uses [Selenium](https://pypi.org/project/selenium/) and [anticaptchaofficial](https://pypi.org/project/anticaptchaofficial/). *WARNING!*  You need to register on [anti-captcha.com](https://anti-captcha.com/) to get the api key and top up your balance (For residents of the Russian federation: MIR cards are available, you can also pay with cryptocurrency)

## How to install

```shell
pip install check-rkn
```


## How to use

```python 
from check_rkn.check_rkn import check_website

result = check_website("your_url", "your_api_key")
print(result) # True if website is blocked or False if no

```

## License - [Apache 2.0](NOTICE)
