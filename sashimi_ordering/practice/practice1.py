from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pyngrok import ngrok
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def initial():
    def connNgrok():
        ngrok.kill()
        port = 5000
        ngrok.connect(port)
        public_url = ngrok.get_tunnels()[0].public_url
        print(" * ngrok tunnel \"{}\" -> \http://127.0.0.1:{}/\"".format(public_url, port))
        return public_url
    url = connNgrok()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    channelID="2000738845"
    driver.get("https://developers.line.biz/console/channel/"+channelID+"/messaging-api")
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div[3]/div/div[3]/div[2]/a").click()
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div[3]/div/div[3]/div[2]/form/div/div[1]/input").send_keys(['f','a','n','j','o','h','n','s','o','n','0','2','1','5','@','g','m','a','i','l','.','c','o','m'])
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div[3]/div/div[3]/div[2]/form/div/div[2]/input").send_keys(['9','2','0','2','1','5','f','u','c','k'])
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div[3]/div/div[3]/div[2]/form/div/div[4]/button").click()
    time.sleep(5)
    # driver.find_element(
    #     By.XPATH, "/html/body/div/div/div/section/div/div/div[1]/nav/ul/li[2]/button").click()
    # time.sleep(3)
    driver.find_element(
        By.XPATH, "/html/body/div/div/div/section/div/div/section/div/section[2]/div[1]/aside/div/div[2]/button[2]").click()
    time.sleep(3)
    textarea = driver.find_element(
        By.XPATH, "/html/body/div/div/div/section/div/div/section/div/section[2]/div[1]/section/div/div/textarea")
    time.sleep(3)
    textarea.send_keys(Keys.CONTROL + 'a')
    textarea.send_keys(Keys.DELETE)
    textarea.send_keys(str(url))
    driver.find_element(
        By.XPATH, "/html/body/div/div/div/section/div/div/section/div/section[2]/div[1]/aside/div/div[2]/button[1]").click()
    return driver


def verify(driver):
    time.sleep(5)
    driver.find_element(
        By.XPATH, "/html/body/div/div/div/section/div/div/section/div/section[2]/div[1]/aside/div/div[2]/button[1]").click()
    time.sleep(3)
    driver.quit()

if __name__ == "__main__":
    driver=initial()
    verify(driver)