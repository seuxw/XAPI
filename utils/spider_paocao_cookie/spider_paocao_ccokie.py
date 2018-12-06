# -*- coding: utf-8 -*-

import configparser
import logging
import os
import time

from PIL import Image, ImageFilter
import pytesseract
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def sele():
    """身份验证的 JSID 获取.

    Return:
        若获取成功，则返回JSID字符串，
        若获取失败，则返回空字符串
    """
    logger = logging.getLogger("sele.py")
    logger.info("Start sele")

    try:
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)

        # 测试时使用URL
        driver.get("http://ids1.seu.edu.cn/amserver/UI/Login")
        # driver.get("http://zccx.seu.edu.cn")
        driver.set_window_size(1200, 800)

        driver.get_screenshot_as_file("utils/spider_paocao_cookie/screen.png")
        element = driver.find_element_by_css_selector(
            "body > table:nth-child(2) > tbody > tr:nth-child(2) > td > table:nth-child(1) > tbody > tr:nth-child(5) > td:nth-child(4) > img")

        left = int(element.location['x'])
        top = int(element.location['y'])
        right = int(element.location['x'] + element.size['width'])
        bottom = int(element.location['y'] + element.size['height'])
        # TODO： Fix
        im = Image.open('utils/spider_paocao_cookie/screen.png')
        im = im.crop((left, top, right, bottom))
        w, h = im.size
        im = im.resize((w*3, h*3))
        im.save('utils/spider_paocao_cookie/screen1.png')

        code = pytesseract.image_to_string(im)
        print(code)

        im.close()

        elem1 = driver.find_element_by_id("IDToken1")
        elem2 = driver.find_element_by_id("IDToken2")
        elem3 = driver.find_element_by_name("inputCode")

        time.sleep(3)

        conf = configparser.ConfigParser()
        conf.read("utils/spider_paocao_cookie/paocao.cfg")
        elem1.send_keys(conf["CARD_INFO"]["CARDNO"])
        elem2.send_keys(conf["CARD_INFO"]["CARDPSWD"])
        elem3.send_keys(code)

        login = driver.find_element_by_css_selector(
            "body > table:nth-child(2) > tbody > tr:nth-child(2) > td > table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(5) > img")
        login.click()

        jsid = ""
        for i in driver.get_cookies():
            if i['name'] == 'JSESSIONID':
                jsid = i['value']
                break
        time.sleep(3)
        driver.quit()
        logger.info("Success sele")
        return jsid

    except Exception as e:
        logger.exception("A error happened in running sele.py")
        driver.quit()
        return ""


if __name__ == "__main__":
    print(sele())
