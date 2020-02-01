import datetime
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeDriverManager().install())
now = datetime.datetime.now()
driver = webdriver.Chrome('d:\\a\\1\\\s\\\chromedriver.exe')  # Set the location of the chromedriver.exe file.


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
        return "Pass"
    except TimeoutException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't load page " + url + ":" + str(
            port) + ". Make sure your application is running.")
        driver.quit()
        return "Fail"


# The close_game_window close the web browser.
def close_game_window():
    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Trying to close browser window...")
    time.sleep(5)
    driver.quit()
    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " browser window closed successfully")
    return "Pass"


# The download_game_message find the Download Game button on screen and click on it.
# After the pop-up window is opened the function get the message that appear in the window and print it to console.
def download_game_message():
    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Trying to get message from Download Game button...")
    try:
        download_button = driver.find_element_by_link_text("Download game")
        download_button.click()
        text_message = driver.find_element(By.XPATH, "//*[@id='pretend-modal']/div/div/div[2]").get_attribute(
            'textContent').strip().replace("\n", "")
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Download Game message is:")
#         print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " \"" + text_message + "\".")
    except TimeoutException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't find 'Download Game' button element.")
        driver.quit()
        return "Fail"
    except ElementClickInterceptedException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't click on 'Download Game' button.")
        return "Fail"
    except ElementNotVisibleException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Button 'Download Game' is not visible.")
        return "Fail"
    except NoSuchElementException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't find 'Download Game' button.")
        return "Fail"
    try:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Trying to close Download Game pop-up window...")
        close_message_button = driver.find_element(By.XPATH, "//*[@id='pretend-modal']//button[@class='close']")
        time.sleep(3)
        close_message_button.click()
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Download Game pop-up window closed successfully.")
        return "Pass"
    except ElementClickInterceptedException:
        print(str(
            now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't click on close 'Download Game' pop-up window button.")
        return "Fail"
    except ElementNotVisibleException:
        print(
            str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Button close 'Download Game' pop-up window is not visible.")
        return "Fail"
    except NoSuchElementException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't find 'Download Game' pop-up window close button.")
        return "Fail"


# The change_page function get a page number as an integer and look for the link with that text.
# After the element is found an API request is sent to make sure the link is valid.
# If yes, it move to the page.
# if no, print error that page has HTTP error.
def change_page(page_num):
    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Trying to change page to " + str(page_num) + "...")
    try:
        page = driver.find_element_by_partial_link_text(str(page_num) + "\n")
        page_url = page.get_attribute("href")
        response = requests.get(url=page_url, verify=False)
        time.sleep(3)
        if response.status_code not in [200, 201]:
            print(
                str(now.strftime("%Y-%m-%d %H:%M:%S")) + " This page got error " + str(response.status_code) + ".")
            return "Fail"
        else:
            try:
                page.click()
                print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Changing page to page " + str(page_num) + ".")
                return "Pass"
            except NoSuchElementException:
                print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " The requested 'page " + str(
                    page_num) + "' element not found.")
                return "Fail"
            except ElementClickInterceptedException:
                print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't click on 'page " + str(page_num) + "' link.")
                return "Fail"
            except ElementNotVisibleException:
                print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " 'Page " + str(page_num) + "' link is not visible.")
                return "Fail"
    except NoSuchElementException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " The requested 'page " + str(page_num) + "' element not found.")
        return "Fail"
    except ElementClickInterceptedException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't click on 'page " + str(page_num) + "' link.")
        return "Fail"
    except ElementNotVisibleException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " 'Page " + str(page_num) + "' link is not visible.")
        return "Fail"


# The check_player_score get a player name as string and locate it at table,
# get the score, Galaxy and Mode parameters and print them to console.
def check_player_score(player):
    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Trying to get " + player + " score ...")
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
            return "Pass"
        else:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Player '" + player + "' not appear in the table.")
            return "Pass"
    except NoSuchElementException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't find table with players information.")
        return "Fail"


# The check_player_achievements get a player name as string and locate it at table, and click on the name link.
# After the player pop-up window opened it check hat the player name appeared and get the list of achievements.
# Afterword it prints them in console and close the pop-up window.
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
                    return "Pass"
                except NoSuchElementException:
                    print(str(now.strftime(
                        "%Y-%m-%d %H:%M:%S")) + " Couldn't find '" + player + "' pop-up window close button.")
                    return "Fail"
                except ElementClickInterceptedException:
                    print(str(now.strftime(
                        "%Y-%m-%d %H:%M:%S")) + " Couldn't click on '" + player + "' pop-up window close button.")
                    return "Fail"
                except ElementNotVisibleException:
                    print(str(now.strftime(
                        "%Y-%m-%d %H:%M:%S")) + " Close button of '" + player + "' pop-up window is not visible.")
                    return "Fail"
            else:
                return "Fail"
        except NoSuchElementException:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't find '" + player + "' achievements.")
            return "Fail"
        except ElementNotVisibleException:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Player  '" + player + "' achievements are not visible.")
            return "Fail"
    except NoSuchElementException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't find '" + player + "' link in 'Space leaders' table.")
        return "Fail"
    except ElementClickInterceptedException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't click on '" + player + "' link.")
        return "Fail"
    except ElementNotVisibleException:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Player  '" + player + "' link is not visible.")
        return "Fail"


# The change_table get a table name and a value in table as strings.
# Afterward it compared the table name with "galaxy" or "mode" to verify which table to change.
# Any other table name will print error.
# Later it checks if value exist in the table:
# If no, it return an error message that the value not exist in the table.
# If yes, it checks if the value is a link.
# If yes, click on it and print message to console.
# If not, print message to console that it already selected.
def change_table(table_name, table_value):
    time.sleep(3)
    if table_name.lower() == "galaxy":
        table_items_xpath = ".//div[@class='row nav-buttons']/h4[text()='Galaxy']/../ul/li"
    elif table_name.lower() == "mode":
        table_items_xpath = ".//div[@class='row nav-buttons']/h4[text()='Mode']/../ul/li"
    else:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " There is no such table: " + table_name)
        return "Fail"
    found_table_value = False
    list_from_table = driver.find_elements(By.XPATH, table_items_xpath)
    if len(list_from_table) >= 1:  # In case we couldn't get the list from the table we still get an empty list.
        for i in list_from_table:
            if i.text == table_value and len(i.find_elements_by_tag_name('a')) == 0:
                print(str(now.strftime(
                    "%Y-%m-%d %H:%M:%S")) + " '" + table_name + "' table already in default value: " + table_value)
                found_table_value = True
                break
            elif i.text == table_value and len(i.find_elements_by_tag_name('a')) == 1:
                try:  # If 'x' button could not be clicked.
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
            return "Fail"
        return "Pass"
    else:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't get information from '" + table_name + "' table.")
        return "Fail"


# The get_total_score function get an integer to compare with the total score of all players table.
# Later it prints the evaluation result to console.
def get_total_score(compare_score):
    all_players_scores = driver.find_elements(By.XPATH, ".//div[@class='col-sm-2 score-data']")
    if len(all_players_scores) >= 1:  # In case we couldn't get the list from the table we still get an empty list.
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
        return "Pass"
    else:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't get players score element.")
        return "Fail"
