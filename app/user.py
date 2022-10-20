# Importing required libraries
import datetime
import os
import time
import pandas as pd
from numpy.core.defchararray import strip
from app import app
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import render_template, request

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


# Creating List variable
list2 = []


@app.route('/uploader', methods=['GET', 'POST'])
def uploadfile():

    if request.method == 'POST':
        # Getting upload file
        f = request.files['file']
        f.save(f.filename)
        # Getting required data
        country = request.form['c']
        time = request.form['t']
        time = int(time)

        with open('upload.csv', encoding='utf-8-sig') as f:
            for row in f:
                list2.append(row)
        # Making loop to run according to variable
        for i in range(len(list2)):
            print(list2[i])
            keyword = list2[i]
            x = FBAdsScraper(country, keyword, time)
            x.scrape_ads()

        return render_template('upload.html')


@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST' or request.method == 'GET':
        # Adding required variable from html form
        country = request.form['c']
        keyword = request.form['k']
        time = request.form['t']
        time = int(time)

        # Calling method to perform certain value
        x = FBAdsScraper(country, keyword, time)
        x.scrape_ads()
    else:
        return render_template('index.html')

    return render_template('index.html')


# Creating list data
data = []


# Creating class which includes methods inside of it
class FBAdsScraper:

    def __init__(self, country, keyword, time):
        self.country = country

        self.keyword = keyword

        self.time = time

        self.ads = []


    def scrape_ads(self):
        # Making fb scraper link
        driver.get(
            "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country={}&q={}".format(
                self.country,
                self.keyword))
        driver.implicitly_wait(1)
        time.sleep(1)


        # Setting time with user input
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=self.time)

        # Making automatic scroll
        while True:
            if datetime.datetime.now() >= endTime:
                break
            else:
                height = driver.execute_script("return document.documentElement.scrollHeight")
                driver.execute_script("window.scrollTo(0, " + str(height) + ");")

        ads = driver.find_element(by=By.CLASS_NAME, value='_8n_0').find_elements(by=By.CLASS_NAME, value='_99s6')
        i = 1

        # Using for loop to go through each scanned data
        for ad in ads:
            try:
                status = ad.find_element(by=By.CLASS_NAME, value='fxk3tzhb').text
            except:
                status = ""
            try:
                title = ad.find_element(by=By.CLASS_NAME, value='_7jyr').text
            except:
                title = ""
            try:
                adsId = ad.find_element(by=By.CLASS_NAME, value='s4swhuz0').text
            except:
                adsId = ""
            try:
                page = ad.find_element(by=By.CLASS_NAME, value='_3qn7').text
            except:
                page = ""
            try:
                link = ad.find_element(by=By.CLASS_NAME, value='_8jh5').text
            except:
                link = ""
            try:
                date = ad.find_element(by=By.XPATH, value='.//span[@class = "j1p9ls3c igvuwmsz tes86rjd lm3k4kh0 '
                                                          'i6uybxyu qc5lal2y nnmaouwa aeinzg81"]').text
            except:
                date = ""
            try:
                fbLink = ad.find_element(by=By.CLASS_NAME, value='rse6dlih').get_attribute('href')
            except:
                fbLink = ""
            try:
                image = ad.find_element(by=By.CLASS_NAME, value='_7jys').get_attribute('src')
            except:
                image = ""
            try:
                video = ad.find_element(by=By.TAG_NAME, value='video').get_attribute('src')
            except:
                video = ""


            # Appending data according to the scan result
            data.append({
                "Keyword": strip(self.keyword),
                "Status": status,
                "Page": page,
                "Title": title,
                "Link": link,
                "Id": adsId,
                "Date": date,
                "Facebook Link": fbLink,
                "Image": image,
                "Video": video
            })

            print(i, " Data stored.")
            i = i + 1
        # Storing data to pandas dataframe and converting it to csv file.
        pd.DataFrame(data).to_csv('data.csv')

# END
# DEVELOPED WITH LOVE BY SARAK DAHAL
