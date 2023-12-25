# for implicit waits
import time
# for DataFrames
import pandas as pd
# for chrome driver
from selenium import webdriver
# for XPATH
from selenium.webdriver.common.by import By
# for explicit waits
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ------------------------------------------------------------------------------------------------------------------
# setting up driver and chrome options
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
# driver.maximize_window()


# ------------------------------------------------------------------------------------------------------------------
# function for logging in the user with static username and password
def user_login():
    website = "https://twitter.com/"
    driver.get(website)
    time.sleep(5)

    # click on login button
    signin_button = driver.find_element(By.XPATH, "//a[@href='/login']")
    signin_button.click()
    time.sleep(2)

    # putting in the username
    username = driver.find_element(
        By.XPATH, '//input[@class="r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf '
                  'r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7"]')
    username.send_keys("you_know_razi")     # the_username

    # clicking the "Next" button
    next_button = driver.find_element(
        By.XPATH, '//div[contains(@class,"css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-ywje51 '
                  'r-usiww2 r-13qz1uu r-2yi16 r-1qi8awa r-ymttw5 r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l")]')
    next_button.click()
    time.sleep(2)

    # putting in the password
    password = driver.find_element(
        By.XPATH, '//input[@class="r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf '
                  'r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7"]')
    password.send_keys("finalflash77.")     # the_password

    # clicking the "Login" button
    login_button = driver.find_element(By.XPATH, '//div[@data-testid="LoginForm_Login_Button"]')
    login_button.click()
    time.sleep(2)


# ------------------------------------------------------------------------------------------------------------------
# function that takes a tweet as argument and returns the username and tweet text as list
def get_tweet(element):
    try:
        the_user = element.find_element(By.XPATH, ".//span[contains(text(), '@')]").text
        the_text = element.find_element(By.XPATH, ".//div[@lang='en']").text
        # make a list to return
        tweet_data = [the_user, the_text]
    except:
        tweet_data = ["the_user", "the_text"]
    return tweet_data


# ------------------------------------------------------------------------------------------------------------------
# scrapes the current view from the page that appears after searching "Python" on Twitter
def scrape_screen():
    # getting the website
    website = "https://twitter.com/search?q=python&src=typed_query&f=top"
    driver.get(website)

    # looping through tweets to scrape user and text
    user_data = []
    text_data = []
    tweet_ids = set()

    # implementing infinite scrolling while scraping
    scrolling = True
    while scrolling:
        # searching using XPATH
        tweets = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))

        # looping
        for tweet in tweets[-15:]:
            # function call to get the scraped sweet
            tweet_list = get_tweet(tweet)
            # joining the user and text from tweet_list to make a unique id
            tweet_id = tweet_list[0].join(tweet_list[1])
            # adding tweet_id to set if its unique
            if tweet_id not in tweet_ids:
                # add tweet_id to tweet_ids set
                tweet_ids.add(tweet_id)
                # append the data to their respective lists
                user_data.append(tweet_list[0])
                text_data.append(" ".join(tweet_list[1].split()))

        # scrolling
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            # breaking the loop when end of page is reached
            if new_height == last_height:
                scrolling = False
                break
            # this way of breaking the loop is used when a specific sample size is required
            # if len(user_data) > 100:
            #     scrolling = False
            #     break
            else:
                last_height = new_height
                break

    # exporting the lists to CSV file
    df_tweets = pd.DataFrame({"user": user_data, "text": text_data})
    df_tweets.to_csv("tweets_infinite_scrolling.csv", index=False)
    print(df_tweets)


# ------------------------------------------------------------------------------------------------------------------
# used to infinitely scroll a page defined by the static Twitter url
def infinite_scrolling():
    # getting the website
    website = "https://twitter.com/rileyjsilverman/status/1683240575137648640"
    driver.get(website)

    # scrolling
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height


# ------------------------------------------------------------------------------------------------------------------
# main function
user_login()
scrape_screen()
# infinite_scrolling()


# https://twitter.com/search?q=python&src=typed_query&f=top : the page that appears after searching "Python" on Twitter
# https://twitter.com/rileyjsilverman/status/1683240575137648640 : Twitter Support post
