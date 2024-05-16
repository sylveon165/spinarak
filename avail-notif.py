import time, random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

def create_booking(day_of_month, num_of_guests, location):
    '''Create a reservation for Pokemon Cafe in Tokyo
    Keyword arguments:
    day_of_month -- day of the month to book
    num_of_guests -- number of guests to book (1-8)
    '''

    if location == "Tokyo":
        website = "https://reserve.pokemon-cafe.jp/"
    elif location == "Osaka":
        website = "https://osaka.pokemon-cafe.jp/"

    chrome_options = Options()
    #chrome_options.add_argument("--headless=new")
    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_experimental_option("detach", True)
    #chromedriver = "chromedriver"
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(website)

    try:
        driver.find_element(By.XPATH, "//*[@id=\"forms-agree\"]/div/div[1]/label").click()
        driver.find_element(By.XPATH, "//*[@id=\"forms-agree\"]/div/div[2]/button").click()
        time.sleep(random.randint(3, 6))
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/div/a").click()
        time.sleep(random.randint(3, 6))
        select = Select(driver.find_element(By.NAME, 'guest'))
        time.sleep(random.randint(2, 3))
	
        select.select_by_index(num_of_guests)
        #time.sleep(random.randint(5, 10))

        # Check if the updated page indicates availability
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # Find all calendar-day-cell elements
        calendar_cells = soup.find_all("li")
        #calendar_cells = soup.find_all("li", class_="calendar-day-cell")
      
        available = False
        # Check each calendar cell for availability
        available_slots = []
        for cell in calendar_cells:
            if "(full)" not in cell.text.lower() and "n/a" not in cell.text.lower():
                #available_slots.append(cell.text.strip())
                available = True
#
#        if available_slots:
#            driver.find_element(By.XPATH, "//*[contains(text(), " + str(day_of_month) + ")]").click()
#            driver.find_element(By.XPATH, "//*[@class='button']").click()
        # TODO: send email if slots detected
#            send_email_notification(available_slots)
        # scroll down before taking screenshot
        driver.execute_script('document.getElementsByTagName("html")[0].style.scrollBehavior = "auto"')
        element=driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/div[1]/p[3]")
        element.location_once_scrolled_into_view
        driver.save_screenshot('./pokemon-cafe.png')
        if available:
            print("Slot(s) AVAILABLE!")
            # TODO: send email & text with screenshot if slots detected
            #send_email_notification(available_slots)	
        else:
            print("No available slots found :(")
        driver.quit()
    except NoSuchElementException:
        pass

num_iterations = 1
day_of_month='28'
num_of_guests=3
location = 'Tokyo'
#location = 'Osaka'
[create_booking(day_of_month, num_of_guests, location) for x in range(num_iterations)]
