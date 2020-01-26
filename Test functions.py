import time
import requests
import datetime
import requests
import json
import re
import xlwt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

now = datetime.datetime.now()
# driver = webdriver.Chrome('c:\\drivers\\chromedriver.exe')  # Set the location of the chromedriver.exe file.
# driver.get("https://localhost:5001")
# driver.maximize_window()
# time.sleep(3)

url_request_all_players = "https://localhost:5001/api/game/getplayers"


def get_all_players(url_all_players):
    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Trying to retrieve all players...")
    try:
        players = requests.get(url=url_all_players, verify=False)
        if players.status_code in [200, 201]:
            players_data = players.json()
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Players retrieved successfully.")
            return players_data
        else:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " couldn't retrieve players.")
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " An Http Error " + str(players.status_code) + " occurred.")
    except requests.exceptions.RequestException as err:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " couldn't retrieve players.")
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + "Request got the following error: ")
        print(str(err))


def create_excel(url_request_all_players):
    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Creating excel file with all players and total score...")
    player_db = get_all_players(url_request_all_players)
    if player_db:
        style = xlwt.XFStyle()
        # cell color
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['light_blue']
        style.pattern = pattern
        # font
        font = xlwt.Font()
        font.bold = True
        font.colour_index = 1  # Header and footer color white
        style.font = font
        # borders
        style_border = xlwt.XFStyle()
        borders = xlwt.Borders()
        borders.left = 1
        borders.left_colour = xlwt.Style.colour_map['light_blue']
        borders.right = 1
        borders.right_colour = xlwt.Style.colour_map['light_blue']
        borders.top = 1
        borders.top_colour = xlwt.Style.colour_map['light_blue']
        borders.bottom = 1
        borders.bottom_colour = xlwt.Style.colour_map['light_blue']
        style_border.borders = borders
        wb = xlwt.Workbook()
        all_player_sheet = wb.add_sheet('All Players', True)
        all_player_sheet.col(0).width = 256 * 11
        all_player_sheet.col(1).width = 256 * 11
        all_player_sheet.col(2).width = 256 * 11
        all_player_sheet.col(3).width = 256 * 11
        all_player_sheet.write(0, 0, "profileId", style=style)
        all_player_sheet.write(0, 1, "userName", style=style)
        all_player_sheet.write(0, 2, "gameMode", style=style)
        all_player_sheet.write(0, 3, "highScore", style=style)
        for row in range(1, len(player_db)):
            all_player_sheet.write(row, 0, int(player_db[row - 1]["score"]["profileId"]), style=style_border)
            all_player_sheet.write(row, 1, str(player_db[row - 1]["userName"]), style=style_border)
            all_player_sheet.write(row, 2, str(player_db[row - 1]["score"]["gameMode"]), style=style_border)
            all_player_sheet.write(row, 3, int(player_db[row - 1]["score"]["highScore"]), style=style_border)
        all_player_sheet.write_merge(len(player_db), len(player_db), 0, 2, "Total:", style=style)
        all_player_sheet.write(len(player_db), 3, xlwt.Formula("sum(D2:D" + str(len(player_db)) + ")"), style=style)
        wb.save('C:\\Users\\israel_tr\\PycharmProjects\\Space Game\\Total Score.xls')
        print(str(
            now.strftime("%Y-%m-%d %H:%M:%S")) + " Excel file with all players and total score created successfully.")
    else:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't create excel file with all players and total score.")



url_request_all_players = "https://localhost:5001/api/game/getplayers"
json_file = "C:\\mslearn-tailspin-spacegame-web-master\\Tailspin.SpaceGame.Web\\SampleData\\profiles.json"
new_player_profile_data = {
    "id": "21",
    "userName": "jhonsnow",
    "avatarUrl": "images\/vatars\/default.svg",
    "achievements": [
        "Winterhall Commander",
        "Space Race",
        "King of the Winter"
    ]
}


create_excel(url_request_all_players)

