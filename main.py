import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from twilio.rest import Client

DRIVER_PATH = './chromedriver'
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)


def get_jobs(driver=False):
    if not driver:
        return False
    
    driver.get("https://somalijobs.com/jobs")
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    jobs_container = soup.find(id="jobs-container")
    job_cards = jobs_container.find_all("a",class_="job-middle-grid")

    jobs  = ""
    for job_card in job_cards:
        JOB_TITLE = job_card.find('h4',class_="jmg-title").text.strip()
        JOB_PROVIDER = job_card.find('h4',class_="jmg-company-title").text.strip()
        # JOB_OVERVIEW = job_card.find('div',class_="job-listing-1-overview").text
        JOB_TIME = job_card.find('span',class_='skl-6').text.split('\n')[2].strip()
        JOB_CATEGORY = job_card.find('span',class_='skl-2').text.split('\n')[2].strip()
        JOB_CITY = job_card.find('span',class_='skl-3').text.split('\n')[2].strip()
        JOB_LINK = "https://somalijobs.com"+job_card.attrs['href'].strip()

        if JOB_CATEGORY in ["Ict/technology/computers","Data Clerk/collection/enumerators"]:
            # SEND ME SMS
            pass

        jobs += """
            ### {} ###

                #Company#  : {}
                #Category# : {}
                #Location# : {}
                #Type#     : {}
                #Link#     : {}
                
        """.format(JOB_TITLE,JOB_PROVIDER,JOB_CATEGORY,JOB_CITY,JOB_TIME,JOB_LINK)
    return jobs




def subscribe(phone_number,category):
    pass



def send_sms(to,content):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                        from_='+15017122661',
                        to='+15558675310'
                    )

    print(message.sid)


print(get_jobs(driver=driver))
