from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

pages = [10, 20, 30, 40, 50, 60, 70]


titleList = []
companyList = []
locList = []
salList = []
#linkList = []
descList = []


for page in pages:
    source = requests.get('https://www.indeed.co.uk/jobs?q=wind+technician&l=essex&radius=100'.format(page)).text

    soup = BeautifulSoup(source, 'lxml')

    #print ('Page: %s' %page)

    results = soup.findAll("div", {"class": "result"})

    for jobs in soup.find_all(class_='result'):

            try:
                title = jobs.find('a', rel='noopener').text.strip()
            except Exception as e:
                title = None
            print('Title:', title)


            try:
                company = jobs.find('span', class_='company').text.strip()
            except Exception as e:
                company = None
            print('Company:', company)

            try:
                location = jobs.find('span', class_='location').text.strip()
            except Exception as e:
                location = None
            print('Location:', location)

            try:
                salary = jobs.find('span', class_='no-wrap').text.strip()
            except Exception as e:
                salary = None
            print('Salary:', salary)

            link = jobs.a['href']
            if 'http' not in link:
                link = ("https://www.indeed.co.uk" + link)
            print('Link:', link)

            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                job_description = soup.find('div', id='jobDescriptionText').decode_contents(formatter="html")
            except Exception as e:
                job_description = None
            print('job_description:', job_description)

            titleList.append(title)
            companyList.append(company)
            locList.append(location)
            salList.append(salary)
            #linkList.append(link)
            descList.append(job_description)

            print('--------')

            time.sleep(0.5)

df = pd.DataFrame({
        'Title':titleList,
        'Company':companyList,
        'Location':locList,
        'Salary':salList,
        #'Link':linkList,
        'Description':descList})

df.to_csv('indeed.csv',index=False)
