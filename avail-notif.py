import chromedriver_autoinstaller, os, random, smtplib, time
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

# Define your email settings as repo secrets
sender_email = os.environ['GMAIL_SENDER']
receiver_email = os.environ['GMAIL_RECIPIENT']
# in case you want to send to another email
receiver_email2 = os.environ['GMAIL_RECIPIENT_2']
# password of the sender email
password = os.environ['GMAIL_APP_PW'] # https://myaccount.google.com/apppasswords

display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

def send_email():
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        subject = "python email test"
        body = "Just testing\n\n"
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, receiver_email, message)
        server.sendmail(sender_email, receiver_email2, message)
        print("Email sent!")
        server.quit()
    except Exception as e:
        print(f"Email error: {str(e)}")

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

    chrome_options = webdriver.ChromeOptions()    
    # Add your options as needed    
    options = [
        # Define window size here
        "--window-size=1200,1200",
        "--ignore-certificate-errors"
 
        #"--headless",
        #"--disable-gpu",
        #"--window-size=1920,1200",
        #"--ignore-certificate-errors",
        #"--disable-extensions",
        #"--no-sandbox",
        #"--disable-dev-shm-usage",
        #'--remote-debugging-port=9222'
    ]

    for option in options:
        chrome_options.add_argument(option)
	    
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

        # scroll down before taking screenshot
        driver.execute_script('document.getElementsByTagName("html")[0].style.scrollBehavior = "auto"')
        element=driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/div[1]/p[3]")
        element.location_once_scrolled_into_view
        #driver.save_screenshot('./pokemon-cafe.png')
        if available:
            print("Slot(s) AVAILABLE!")
            driver.save_screenshot('./pokemon-cafe-slot-found.png')
            # TODO: send email & text with screenshot if slots detected
            #send_email_notification(available_slots)	
        else:
            print("No available slots found :(")
            driver.save_screenshot('./pokemon-cafe-availability-slot-not-found.png')
        driver.quit()
    except NoSuchElementException:
        pass

num_iterations = 1
day_of_month='28'
num_of_guests=3
location = 'Tokyo'
#location = 'Osaka'
[create_booking(day_of_month, num_of_guests, location) for x in range(num_iterations)]
