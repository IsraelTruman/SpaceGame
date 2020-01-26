import requests
import json
import re
import xlwt
import datetime

now = datetime.datetime.now()


# The get_all_players function get the API to retrieve all players and pars them to list and return the list.
# NOTE: verify=False to avoid getting the SSL Certificate Verify Failed error.
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


# The get_player_by_id function get the API URL to get profile and profile id and use them to create the API to get
# specific player by ID.
# NOTE: verify=False to avoid getting the SSL Certificate Verify Failed error.
def get_player_by_id(url_player_by_id, id_player=1):
    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Trying to get player profile with id " + str(id_player) + "...")
    try:
        url_id = url_player_by_id + str(id_player)
        player = requests.get(url=url_id, verify=False)
        if player.status_code in [200, 201]:
            player_data = player.json()
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Player profile with id " + str(
                id_player) + " retrieved successfully.")
            return player_data["userName"], player_data["score"]["highScore"]
        else:
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " couldn't retrieve player with ID " + str(id_player) + ".")
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " An Http Error " + str(player.status_code) + " occurred.")
    except requests.exceptions.RequestException as error:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't retrieve player with id " + str(id_player))
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Request got the following error: " + str(error))


# The write_player_to_file get player name and his high score and write them to Champion Score.txt file.
# example of how the file should look:
# --------------------------------------------------------------------
# Player Name		Score
# <PlayerName>		<Score>
def write_champ_player_to_file(list_champ):
    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Writing highest score/s to 'Champion Score.txt' file...")
    try:
        with open('C:\\Users\\israel_tr\\PycharmProjects\\Space Game\\Champion Score.txt', 'w') as champion_file:
            champion_file.write("-" * 68 + "\n")
            champion_file.write("Player Name" + " " * 9 + "Score" + "\n")
            for champ in list_champ:
                champion_file.write(champ[0] + " " * (20 - len(champ[0])) + str(champ[1]) + "\n")
            champion_file.close()
            file_location = 'C:\\Users\\israel_tr\\PycharmProjects\\Space Game\\Champion Score.txt'
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " 'Champion Score.txt' file created successfully.")
            print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " File location: " + file_location)
            return file_location
    except EnvironmentError:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't create 'Champion Score.txt' file.")


# The add_player_profile get json file, open it in read mode and retrieve the list of players profile.
# Than check if the profile exist in the list.
# If yes, only print the message "Player profile already exist".
# If not, appending it to the list and print the message "Player profile was added successfully"
# *** NOTE: in that case there is no option for updating profiles simultaneously. ***
def add_player_to_profile_file(target_json_file, profile_data):
    flag_add = False
    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Trying to add new player profile...")
    try:
        with open(target_json_file, 'r', encoding='utf-8') as f:
            try:
                list_of_players = json.loads(f.read().replace("`", '"').replace("'", '"').replace('u"', '"'))
                if profile_data not in list_of_players:
                    list_of_players.append(profile_data)
                    flag_add = True
                else:
                    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Player profile already exist in target file: ")
                    print(target_json_file)
            except ValueError:
                print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't read profile file:")
                print(target_json_file)
    except EnvironmentError:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't read profile file:")
        print(target_json_file)
    if flag_add:
        try:
            with open(target_json_file, 'w', encoding='utf-8') as fw:
                try:
                    json.dump(list_of_players, fw, ensure_ascii=False, indent=4)
                    print(str(now.strftime(
                        "%Y-%m-%d %H:%M:%S")) + " Player profile was added successfully to target file: " + target_json_file)
                except TypeError:
                    print(str(now.strftime(
                        "%Y-%m-%d %H:%M:%S")) + " Couldn't add target profile to target file: " + target_json_file)
        except EnvironmentError:
            print(str(
                now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't add target profile to target file: " + target_json_file)


# The merge_sort function get the data of all players and sort them according to the highScore value in ascending mode.
# The function set a minimum parameter the first value of the list and compare all hte other list objects.
# if it find other object to be smaller the minimum parameter will be replaced with it and keep on checking the list.
# When the minimum value found it removed from the list. and appended to new list.
# The function will keep on running until the data list length is 1.
def merge_sort(data):
    if len(data) > 1:
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]
        merge_sort(left_half)
        merge_sort(right_half)
        i, j, k = 0, 0, 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][1] < right_half[j][1]:
                data[k] = left_half[i]
                i += 1
                k += 1
            else:
                data[k] = right_half[j]
                j += 1
                k += 1
        while i < len(left_half):
            data[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            data[k] = right_half[j]
            j += 1
            k += 1


def get_champs_sorted_list(data_of_players):
    print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Collecting players names and scores for all players profile...")
    if type(data_of_players) == list and len(data_of_players) != 0:
        sorting_list = list([i["userName"], i["score"]["highScore"]] for i in data_of_players)
        merge_sort(sorting_list)
        list_of_champs = [sorting_list[-1]]
        for i in range(len(sorting_list)):
            if sorting_list[-i - 1][1] == sorting_list[-i - 2][1]:
                list_of_champs.append(sorting_list[-i - 2])
            else:
                break
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Players names and scores collected successfully.")
        return list_of_champs
    else:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't collect players names and scores.")


def get_high_score_from_champ_file(file):
    try:
        with open(file, 'r') as f:
            text = f.read()
            player_score = re.findall(r'\D+\S+\s+(\d+)', text)
            player_name = re.findall(r'\n(\S+)\s+\d+', text)
            if player_score:
                print(str(now.strftime(
                    "%Y-%m-%d %H:%M:%S")) + " Champion/s highest score/s found successfully in champion file.")
                print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " File location: " + file)
            else:
                print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Champion/s highest score/s in champion file.")
                player_score = []
                player_name = []
            return player_score, player_name
    except ValueError:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't read profile file:")
        print(file)


def compare_scores(list_of_champs_score, list_of_champs_name, player_score, player_name):
    plural = ("\'s" if len(list_of_champs_score) > 1 else "")
    champ_name = "' and '".join(list_of_champs_name)
    if int(list_of_champs_score[0]) > player_score:
        print(str(now.strftime(
            "%Y-%m-%d %H:%M:%S")) + " Champion" + plural + "'" + champ_name + "' score" + plural + " '" + str(
            list_of_champs_score[0]) +
              "' greater than player '" + player_name + "' score " + str(player_score))
    elif int(list_of_champs_score[0]) < player_score:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Player '" + player_name + "' score " + str(
            player_score) + " greater than champion" + plural + "'"
              + champ_name + "' score" + plural + " '" + str(list_of_champs_score[0]) + "'")
    else:
        print(str(now.strftime(
            "%Y-%m-%d %H:%M:%S")) + " Champion" + plural + "'" + champ_name + "' score" + plural + " '" + str(
            list_of_champs_score[0]) +
              "' equal to player '" + player_name + "' score '" + str(player_score) + "'")


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
        font.colour_index = 1  # white
        style.font = font
        # borders
        # borders = xlwt.Borders()
        # borders.left = 1
        # borders.left_colour = xlwt.Style.colour_map['light_blue']
        # borders.right = 1
        # borders.right_colour = xlwt.Style.colour_map['light_blue']
        # borders.top = 1
        # borders.top_colour = xlwt.Style.colour_map['light_blue']
        # borders.bottom = 1
        # borders.bottom_colour = xlwt.Style.colour_map['light_blue']
        # style.borders = borders
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
        all_player_sheet.write_merge(len(player_db), len(player_db), 0, 2, "Total", style=style)
        all_player_sheet.write(len(player_db), 3, xlwt.Formula("sum(D2:D" + str(len(player_db)) + ")"), style=style)
        wb.save('C:\\Users\\israel_tr\\PycharmProjects\\Space Game\\Total Score.xls')
        print(str(
            now.strftime("%Y-%m-%d %H:%M:%S")) + " Excel file with all players and total score created successfully.")
    else:
        print(str(now.strftime("%Y-%m-%d %H:%M:%S")) + " Couldn't create excel file with all players and total score.")
