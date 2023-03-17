from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
import pandas as pd
import numpy as np

opts = Options()
opts.add_argument("Mozilla/5.0")
driver = webdriver.Chrome(options=opts)
time.sleep(2)
filter = "&occ=Software%20Engineer&filterType=RATING_OVERALL"

# Starting Point
url_main = 'https://www.glassdoor.sg/Reviews/index.htm?overall_rating_low=1&page=1&occ=Software%20Engineer&filterType=RATING_OVERALL'

url_login = 'https://www.glassdoor.sg/index.htm'

def logIn():
    driver.get(url_login)
    name = "junwei__lam@hotmail.com"
    pw = "junweiLAM99"
    try:
        username = driver.find_element(By.ID, 'inlineUserEmail')
        button = driver.find_element(By.XPATH, '//*[@id="InlineLoginModule"]/div/div[1]/div/div/div/div/form/div[2]/button')
        username.send_keys(name)
        button.click()
        time.sleep(2)
        password = driver.find_element(By.ID, 'inlineUserPassword')
        password.send_keys(pw)
        sign_in = driver.find_element(By.XPATH, '//*[@id="InlineLoginModule"]/div/div[1]/div/div/div/div/form/div[2]/button')
        sign_in.click()
        time.sleep(2)
    except:
        time.sleep(2)
        pass

logIn()
driver.get(url_main)

unsuccessful_links = []
companies = []

def scraping_pages(num_pages):

    url_root = "https://www.glassdoor.sg/Reviews/index.htm?overall_rating_low=1&page="
    nums = [x+1 for x in range(num_pages)]
    url_mains = list(map(lambda n: url_root + str(n) + filter, nums))
    time.sleep(2)

    for u in url_mains:
        driver.get(u)
        time.sleep(2)

        #elems = driver.find_elements(By.XPATH, '//*[@id="Explore"]/div[3]/div/div[4]/div[2]')
        elems = driver.find_elements(By.TAG_NAME, 'a')

        company_links = []

        for elem in elems:
            # print(elem.text)
            company_link = elem.get_attribute('href')
            try:
                if company_link.find("Salary") != -1 and company_link is not None:
                    company_links.append(company_link)
            except:
                pass

        for url in company_links:
            try:
                driver.get(url)
                time.sleep(2)
                
                salary_elems = driver.find_elements(By.TAG_NAME, 'a')

                for elem in salary_elems:
                    salary_link = elem.get_attribute('href')
                    if 'Software-Engineer' in salary_link and salary_link is not None:
                        driver.get(salary_link)
                        salary = driver.find_element(By.XPATH,'//*[@id="Container"]/div/div[2]/main/div[1]/div/div[1]/div[5]/div[1]/div/h2').text
                        numOfSalary = driver.find_element(By.XPATH, '//*[@id="Container"]/div/div[2]/main/div[1]/div/div[1]/div[5]/div[1]/p[2]').text
                        time.sleep(2)
                        print(salary)
                        print(numOfSalary)
                        overview_elems = driver.find_elements(By.TAG_NAME,'a')
                        for overviewElem in overview_elems:
                            overview_link = overviewElem.get_attribute('href')
                            if 'Overview' in overview_link and overview_link is not None:
                                driver.get(overview_link)
                                companyName = driver.find_element(By.XPATH, '//*[@id="DivisionsDropdownComponent"]').text
                                print(companyName)
                                companySize = driver.find_element(By.XPATH, '//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[3]/div').text
                                print(companySize)
                                companyIndustry = driver.find_element(By.XPATH, '//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[6]/a').text
                                print(companyIndustry)
                                time.sleep(2)
                                review_elems = driver.find_elements(By.TAG_NAME, 'a')
                                for reviewElems in review_elems:
                                    review_link = reviewElems.get_attribute('href')
                                    if ('%s-Review'%companyName) in review_link and review_link is not None:
                                        driver.get(review_link)
                                        time.sleep(2)
                                        numOfReviews = driver.find_element(By.XPATH, '//*[@id="EmpLinksWrapper"]/div[2]/div/div[1]/a[1]/div').text
                                        print(numOfReviews)
                                        companyRating = driver.find_element(By.XPATH, '//*[@id="EmpStats"]/div[1]/div[1]/div[1]').text.split("\n")[0]
                                        print(companyRating)
                                        olClass = driver.find_element(By.CLASS_NAME, 'empReviews')
                                        htmlReviews = olClass.find_elements(By.XPATH,'./li')
                                        print("Length is %s"%len(htmlReviews))
                                        reviews = []

                                        for i in range(len(htmlReviews)):
                                            review_rating = htmlReviews[i].find_element(By.CLASS_NAME,'ratingNumber').text
                                            employee_status = htmlReviews[i].find_elements(By.XPATH, './div[1]/div[1]/div[1]/div[1]/span')
                                            
                                            print(review_rating)
                                            print(employee_status)
                                            reviews.append({
                                                "Star_Rating": review_rating,
                                                "Employee_Status": employee_status,
                                            })

                                        companies.append({
                                            "Name": companyName,
                                            "Size": companySize,
                                            "Industry": companyIndustry,
                                            "Average_Salary": salary,
                                            "No_Of_Salary": numOfSalary,
                                            "Rating": companyRating,
                                            "No_Of_Reviews": numOfReviews,
                                            "Reviews": reviews
                                            })
                                        print(companies)

                # companies.append({
                #     "NAME": companyName,
                #     "SIZE": companySize,
                #     "AVERAGE SALARY": salary,
                # })

            except:
                unsuccessful_links.append(url)
                #print("unsuccessful links: %s" % url)
                time.sleep(10)
        print(f'Finished scraping {len(companies)} companies')
        df = pd.DataFrame(companies)
    return df
scraping_pages(1)
df = pd.DataFrame(companies)
df_csv = df.to_csv('scraping.csv', index=False)

driver.close()
driver.quit()

