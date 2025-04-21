from os import remove

from anticaptchaofficial.imagecaptcha import imagecaptcha
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def solve_captcha(api_key: str, image_captcha: str) -> str:
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(api_key)

    solver.set_soft_id(0)

    captcha_text = solver.solve_and_return_solution(image_captcha)
    
    if captcha_text != 0:
        return captcha_text
    else:
        print("error")


def paste_solution(api_key: str, webdriver) -> None:
    blocklist_url = "https://blocklist.rkn.gov.ru"
    
    webdriver.get(blocklist_url)

    img = webdriver.find_element(By.XPATH, '//*[@id="captcha_image"]')
    img.screenshot("captcha.png")

    solution = solve_captcha(api_key, "captcha.png")
    
    webdriver.find_element(By.XPATH, '//*[@id="captcha"]').send_keys(solution)

    remove("captcha.png")


def check_website(url: str, api_key: str) -> bool:
    """
    Function calls selenium, substitutes user url and captcha solution,
    and returns True if the site is blocked or False if not
    """
    op = webdriver.FirefoxOptions()
    op.add_argument("--headless")
    browser = webdriver.Firefox(options=op)

    paste_solution(api_key, browser)

    url = url.replace("/", "")
    url = url.replace("https:", "")
    url = url.replace("http:", "")
    url = url.replace("w.", "")
    url = url.replace("w", "")

    browser.find_element(By.XPATH, '//*[@id="inputMsg"]').send_keys(url)

    click_button = browser.find_element(By.XPATH, '//*[@id="send_but2"]')
    click_button.click()
    
    print("\033c\033[3J", end="")

    try:
        browser.find_element(
            By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[2]/table/thead/tr/td[1]"
        ).text
        return True
    except NoSuchElementException:
        return False

    browser.close()
