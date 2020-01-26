import datetime
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

now = datetime.datetime.now()
driver = webdriver.Chrome('c:\\drivers\\chromedriver.exe')  # Set the location of the chromedriver.exe file.


# The open_game_window function start the web chrome browser with the url and port sent as parameters.
# It tries to start the window and check if the Download Game appear on screen.
# If not, it raise and exception TimeoutException and print message to the console and close the web browser.
# If yes, print message to the console.
def open_game_window(url, port):
    driver.get(url + ":" + str(port))
    driver.maximize_window()
    try:
        wait = WebDriverWait(driver, 3)
        condition = expected_conditions.presence_of_element_located((By.LINK_TEXT, "Download game"))
        wait.until(condition)
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " " + url + ":" + str(port) + " web page opened successfully.")
        return True
    except TimeoutException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't load page " + url + ":" + str(
            port) + ". Make sure your application is running.")
        driver.quit()
        return False


# The close_game_window close the web browser.
def close_game_window():
    time.sleep(5)
    driver.quit()


# The
def download_game_message():
    click_button_pass = False
    try:
        download_button = driver.find_element_by_link_text("Download game")
        download_button.click()
        text_message = driver.find_element(By.XPATH, "//*[@id='pretend-modal']/div/div/div[2]").get_attribute(
            'textContent')
        click_button_pass = True
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Download Game message is:")
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " \"" + text_message.strip().replace("\n", "") + "\".")
    except TimeoutException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't find 'Download Game' button element.")
        driver.quit()
    except ElementClickInterceptedException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't click on 'Download Game' button.")
    except ElementNotVisibleException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Button 'Download Game' is not visible.")
    except NoSuchElementException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't find 'Download Game' button.")
    if click_button_pass:
        try:
            close_message_button = driver.find_element(By.XPATH, "//*[@id='pretend-modal']//button[@class='close']")
            time.sleep(3)
            close_message_button.click()
        except ElementClickInterceptedException:
            print(str(
                now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't click on close 'Download Game' pop-up window button.")
        except ElementNotVisibleException:
            print(
                str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Button close 'Download Game' pop-up window is not visible.")
        except NoSuchElementException:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't find 'Download Game' pop-up window close button.")


def change_page(page_num):
    try:
        page = driver.find_element_by_partial_link_text(str(page_num) + "\n")
        page_url = page.get_attribute("href")
        response = requests.get(url=page_url, verify=False)
        time.sleep(3)
        if response.status_code not in [200, 201]:
            print(
                str(now.strftime("%Y-%m-%d %H:%M:%S")) + " This page got error " + str(response.status_code) + ".")
        else:
            page.click()
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " changing page to page " + str(page_num) + ".")
    except NoSuchElementException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " The requested 'page " + str(page_num) + "' element not found.")
    except ElementClickInterceptedException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't click on 'page " + str(page_num) + "' link.")
    except ElementNotVisibleException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " 'Page " + str(page_num) + "' link is not visible.")


def check_player_score(player):
    try:
        leader_list = driver.find_element(By.XPATH, ".//div[@class='col-sm-9 leader-scores']").text.split("\n")
        if player in leader_list:
            player_index = leader_list.index(player)
            player_mode = leader_list[player_index + 1]
            player_galaxy = leader_list[player_index + 2]
            player_score = leader_list[player_index + 3]
            print(str(now.strftime(
                "%Y-%m-%d %H:%M:%S")) + " Player '" + player + "' has the score of " + player_score + " in Mode "
                  + player_mode + " and Galaxy " + player_galaxy)
        else:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Player '" + player + "' not appear in the table.")
    except NoSuchElementException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't find table with players information.")


def check_player_achievements(player):
    try:
        player_in_list = driver.find_element_by_link_text(player)
        player_in_list.click()
        time.sleep(1)
        try:
            player_details_and_achievements = driver.find_element_by_xpath(
                ".//div[@class='content']//h1[text()='{}']/..".format(player))
            achievements = player_details_and_achievements.find_elements_by_xpath("./ul/li")
            achievements_list = list(achieve.text for achieve in achievements)
            if player in player_details_and_achievements.text:
                print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Player " + player + " achievements are as follow: ")
                print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " " + ", ".join(achievements_list))
                try:
                    close_button = driver.find_element(By.XPATH,
                                                       ".//div[@class='modal fade profile in']//button[@class='close']")
                    close_button.click()
                except NoSuchElementException:
                    print(
                        str(now.strftime(
                            "%Y-%m-%d %H:%M:%S")) + " Couldn't find '" + player + "' pop-up window close button.")
                except ElementClickInterceptedException:
                    print(str(
                        now.strftime(
                            "%Y-%m-%d %H:%M:%S")) + " Couldn't click on '" + player + "' pop-up window close button.")
                except ElementNotVisibleException:
                    print(str(
                        now.strftime(
                            "%Y-%m-%d %H:%M:%S")) + " Close button of '" + player + "' pop-up window is not visible.")
        except NoSuchElementException:
            print(str(
                now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't find '" + player + "' achievements.")
        except ElementNotVisibleException:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Player  '" + player + "' achievements are not visible.")
    except NoSuchElementException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't find '" + player + "' link in 'Space leaders' table.")
    except ElementClickInterceptedException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't click on '" + player + "' link.")
    except ElementNotVisibleException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Player  '" + player + "' link is not visible.")


def change_table(table_name, table_value):
    time.sleep(3)
    if table_name.lower() == "galaxy":
        table_items_xpath = ".//div[@class='row nav-buttons']/h4[text()='Galaxy']/../ul/li"
    elif table_name.lower() == "mode":
        table_items_xpath = ".//div[@class='row nav-buttons']/h4[text()='Mode']/../ul/li"
    else:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " There is no such table: " + table_name)
        return False
    found_table_value = False
    list_from_table = driver.find_elements(By.XPATH, table_items_xpath)
    if len(list_from_table) >= 1:   # In case we couldn't get the list from the table we still get an empty list.
        for i in list_from_table:
            if i.text == table_value and len(i.find_elements_by_tag_name('a')) == 0:
                print(str(now.strftime(
                    "%Y-%m-%d %H:%M:%S")) + " '" + table_name + "' table already in default value: " + table_value)
                found_table_value = True
                break
            elif i.text == table_value and len(i.find_elements_by_tag_name('a')) == 1:
                try:   # If 'x' button could not be clicked.
                    i.find_elements_by_tag_name('a')[0].click()
                    time.sleep(3)
                    print(str(
                        now.strftime("%Y-%m-%d %H:%M:%S")) + " '" + table_name + "' table set to: " + table_value)
                    found_table_value = True
                    break
                except ElementClickInterceptedException:
                    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't click on '" + table_value + "' link.")
                except ElementNotVisibleException:
                    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + "'" + table_value + "' link is not visible.")
            else:
                continue
        if not found_table_value:
            print(str(now.strftime(
                "%Y-%m-%d %H:%M:%S")) + " '" + table_value + "' is not an option under '" + table_name + "' table.")
    else:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't get information from '" + table_name + "' table.")


def get_total_score(compare_score):
    all_players_scores = driver.find_elements(By.XPATH, ".//div[@class='col-sm-2 score-data']")
    if len(all_players_scores) >= 1:   # In case we couldn't get the list from the table we still get an empty list.
        scores = list(i.text for i in all_players_scores)
        int_scores = list(int(x.replace(",", "")) for x in scores[1::2])
        if sum(int_scores) > compare_score:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " The total score is : " + str(
                sum(int_scores)) + " and it's grater than: " + str(compare_score))
        elif sum(int_scores) < compare_score:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " The total score is : " + str(
                sum(int_scores)) + " and it's less than: " + str(compare_score))
        else:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " The total score is : " + str(
                sum(int_scores)) + " and it's equal to: " + str(compare_score))
    else:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't get players score element.")
