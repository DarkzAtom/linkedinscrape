from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def prepare_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def main():
    url = "https://www.linkedin.com/jobs/search/?currentJobId=3832062288&geoId=103644278&keywords=%22utilization%20review%22%20nurse&location=United%20States&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"
    driver = prepare_browser()
    driver.get(url)
    try:
        driver.implicitly_wait(7)
    except TimeoutException as e:
        main()
    time.sleep(2)
    while True:
        last_height = driver.execute_script('return document.body.scrollHeight')
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')

        if new_height == last_height:
            try:
                infnt_scrl_btn = driver.find_element(By.CSS_SELECTOR, 'button.infinite-scroller__show-more-button.infinite-scroller__show-more-button--visible')
                infnt_scrl_btn.click()
                butt_counter +=1
                if butt_counter > 44:
                    break
            except (NoSuchElementException, TimeoutException):
                break

        else:
            butt_counter = 0
            pass

    jobslist_cont = driver.find_element(By.CSS_SELECTOR, 'ul.jobs-search__results-list')
    jobslist = jobslist_cont.find_elements(By.TAG_NAME, 'li')
    jobslist_setsorted = set()
    for job in jobslist:
        jobslist_setsorted.add(job)
    jobslist_nodup = list(jobslist_setsorted)
    joblist = jobslist_nodup
    joblist_contents = [job.get_attribute('innerHTML') for job in joblist]

    final_joblist = []

    for content in joblist_contents:
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.select_one('h3.base-search-card__title').get_text(strip=True)
        company = (soup.select_one('h4.base-search-card__subtitle')).select_one('a').get_text(strip=True)
        a_tag_link = soup.select_one('a.base-card__full-link.absolute.top-0.right-0.bottom-0.left-0.p-0.z-2')
        company_linkedin_link = a_tag_link['href'] if a_tag_link is not None else None
        location = soup.select_one('div.base-search-card__metadata span').get_text(strip=True)
        item = {
            'Title': title,
            "Company's Name": company,
            "Company's Link": company_linkedin_link,
            "Company's Location": location
        }
        final_joblist.append(item)

    print(final_joblist)
    print(len(final_joblist))





  

if __name__ == "__main__":
    main()


