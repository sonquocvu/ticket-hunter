from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from stageDataHandling import StateDataHandling
import os
import psutil


class ChromeHandling:

    def __init__(self):
        self.kill_chrome_if_nedded()
        self.guiApp = None

    def __del__(self):
        print("Close the webpage")
        if self.guiApp:
            self.guiApp['-STOP-BUTTON-'].click()

    def __waiting_machine(self, driver, timeout, elementType, path):
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((elementType, path)))

    def __setup_driver(self, user):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option("useAutomationExtension", False)
        chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
        chromeOptions.add_experimental_option("detach", True)
        chromeOptions.add_argument("--disable-notifications")
        chromeOptions.add_argument("--start-maximized")
        chromeOptions.add_argument(rf"user-data-dir=C:\Users\{user}\AppData\Local\Google\Chrome\User Data")
        chromeOptions.add_argument("profile-directory=Default")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=chromeOptions)
        return driver

    def kill_chrome_if_nedded(self):
        for proc in psutil.process_iter():
            if 'chrome.exe' in proc.name():
                print("Chrome process has been found out, start killing it.")
                os.system("taskkill /f /im chrome.exe")

    def __enter_essential_infor(self, driver, lastName, firstName, email, phone, attribute=None):
        # Enter essential information to buy the ticket
        attribute = driver.find_element(By.NAME, "lastName")
        attribute.clear()
        attribute.clear()
        attribute.send_keys(lastName)
        attribute.send_keys(Keys.ENTER)

        attribute = driver.find_element(By.NAME, "firstName")
        attribute.clear()
        attribute.send_keys(firstName)
        attribute.send_keys(Keys.ENTER)

        attribute = driver.find_element(By.NAME, "email")
        attribute.clear()
        attribute.send_keys(email)
        attribute.send_keys(Keys.ENTER)

        attribute = driver.find_element(By.NAME, "confirmEmail")
        attribute.clear()
        attribute.send_keys(email)
        attribute.send_keys(Keys.ENTER)

        attribute = driver.find_element(By.NAME, "phoneNumber")
        attribute.clear()
        attribute.send_keys(phone)
        attribute.send_keys(Keys.ENTER)

    def __choose_seats(self, driver, m_seatCoordinateTable: dict, vipRow: str, normalRow: str):
        m_vipSeatCoordinateList = m_seatCoordinateTable["Vip"][vipRow]
        m_normalSeatCoordinateList = m_seatCoordinateTable["Normal"][normalRow]
        selectedSeatsList = []

        # Choose seats in the Vip row
        log = ""
        numOfVipSeats = len(m_vipSeatCoordinateList)
        for i in range(numOfVipSeats):
            try:
                seat = driver.find_element(By.XPATH,
                                           f"//*[@cx={m_vipSeatCoordinateList[i][0]} and @cy={m_vipSeatCoordinateList[i][1]}]")
                if 'rgb(255, 255, 255)' in seat.get_attribute("style"):     # If seat
                    # is available
                    next_seat = None
                    if i < (numOfVipSeats - 1):
                        next_seat = driver.find_element(By.XPATH,
                                                        f"//*[@cx={m_vipSeatCoordinateList[i + 1][0]} and @cy={m_vipSeatCoordinateList[i + 1][1]}]")
                    if len(selectedSeatsList) == 1 or i == (numOfVipSeats - 1) or 'rgb(255, 255, 255)' in next_seat.get_attribute("style"):
                        while 'rgb(255, 255, 255)' in seat.get_attribute("style"):
                            seat.click()
                        selectedSeatsList.append(seat)
                else:
                    if len(selectedSeatsList) == 1 and 'rgb(244, 67, 54)' in seat.get_attribute("style"):
                        selectedSeatsList[0].click()
                        selectedSeatsList.pop()
            except Exception as e:
                print(f"Be unable to select the vip seat {vipRow}-{i}, the exception: {e}")

            if len(selectedSeatsList) == 2:
                break

        # Choose seats in the Normal row
        selectedSeatsList.clear()
        for i in range(len(m_normalSeatCoordinateList)):
            try:
                seat = driver.find_element(By.XPATH, f"//*[@cx={m_normalSeatCoordinateList[i][0]} and @cy={m_normalSeatCoordinateList[i][1]}]")
                if 'rgb(255, 255, 255)' in seat.get_attribute("style"):
                    while 'rgb(255, 255, 255)' in seat.get_attribute("style"):
                        seat.click()
                    selectedSeatsList.append(seat)
                elif 'rgb(244, 67, 54)' in seat.get_attribute("style"):
                    continue
            except Exception as e:
                print(f"Be unable to select the normal seat {normalRow}-{i}, the exception: {e}")

            if len(selectedSeatsList) == 4:
                break

        driver.find_element(By.XPATH, "//table[@ng-click='submitTicketInfo()']").click()

    def __buy_tickets(self, link: str, lastName: str, firstName: str, email: str, phone: str, stage: str, vipRow: str, normalRow: str, guiApp):
        self.guiApp = guiApp
        stageDataObj = StateDataHandling()
        m_seatCoordinateTable = stageDataObj.get_seats_coordinate(stage)

        # Access page to buy tickets
        log = str
        userName = os.getlogin()
        tickeBox = self.__setup_driver(str(userName))
        while True:
            try:
                tickeBox.get(link)
                self.__waiting_machine(tickeBox, 5, By.XPATH, "//h3[contains(text(), 'Lịch sự kiện')]")
            except Exception as e:
                print(f"Be unable to access the link due to {e}")
            else:
                break

        # Check page until permitting to buy tickets
        events = None
        counts = 0
        while True:
            events = tickeBox.find_elements(By.XPATH, "//a[contains(@data-href, '/event/')]")
            if len(events) > 0:
                print("Find out event successfully")
                break
            else:
                counts = counts + 1
                tickeBox.refresh()
                self.__waiting_machine(tickeBox, 5, By.XPATH, "//h3[contains(text(), 'Lịch sự kiện')]")
                print(f"Refresh page in {counts} time to search events")

        for i in range(len(events)):
            try:
                events[i].click()
                self.__waiting_machine(tickeBox, 5, By.XPATH, "//a[contains(text(), 'Nhập mã giảm giá')]")
            except TimeoutException:
                events[i].click()
                self.__waiting_machine(tickeBox, 5, By.XPATH, "//a[contains(text(), 'Nhập mã giảm giá')]")
                break
            except Exception as e:
                print(f"Be unable to click event {i} due to {e}")
            else:
                print(f"Click event {i} successfully")
                break

        while 1:
            try:
                self.__choose_seats(tickeBox, m_seatCoordinateTable, vipRow, normalRow)
                self.__waiting_machine(tickeBox, 10, By.NAME, "lastName")
            except Exception as e:
                print(f"Be unable to select seats due to {e}")
            else:
                break

        self.__enter_essential_infor(tickeBox, lastName, firstName, email, phone)
        tickeBox.find_element(By.XPATH, "//*[@ng-click='submitOrder()']").click()

    def start(self, link: str, lastName: str, firstName: str, email: str, phone: str, stage: str, vipRow: str, normalRow: str, guiApp):
        self.__buy_tickets(link, lastName, firstName, email, phone, stage, vipRow, normalRow, guiApp)
