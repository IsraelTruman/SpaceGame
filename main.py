from UI_Automation_Tests import UI_Automation_Test as UI
from API_Automation_Test import API_Automation_Test as API
import Run_Applicarion as RUN
import time

########################################################################
#                            variables                                 #
########################################################################
url_request_all_players = "https://localhost:5001/api/game/getplayers"
url_request_player_by_id = "https://localhost:5001/api/game/getplayer?playerId="
player_id = 21
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


#########################################################################


def ui_automation():
    page_load = UI.open_game_window("https://localhost", 5001)  # Open web browser with the URL and port parameters.
    if page_load:  # Condition to check if the web browser window opened successfully.
        UI.download_game_message()  # Press Download Game button and print the message from pop up window.
        UI.change_table("Mode", "All9")  # Change the Mode table to All mode.
        UI.change_table("Galaxy", "All")  # Change the Galaxy table to All mode.
        UI.change_page(3)  # Change page to page 3.
        UI.check_player_score("duality")  # Check player called 'duality' and get his Mode, Galaxy and Score.
        UI.check_player_achievements(
            "duality")  # Press on 'duality' player link and get all player achievements from popup window.
        UI.change_page(1)  # Change page to page 3.
        UI.change_table("Galaxy", "Pinwheel")  # Change the Galaxy table to Pinwheel mode.
        UI.get_total_score(
            1314090)  # get all players total score and compare it with 1314090 and print the evaluation result.
        UI.close_game_window()  # Close the web browser window.


def api_automation():
    # Task 1
    player_data = API.get_all_players(url_request_all_players)  # Send REST request to get all players as json.
    champ_list = API.get_champs_sorted_list(
        player_data)  # Get list of all players sorted (using merge_sort function) according to their score.
    champ_file = API.write_champ_player_to_file(
        champ_list)  # Writing the player/s with the highest score to champion.txt file.
    # Task 2
    API.add_player_to_profile_file(json_file,
                                   new_player_profile_data)  # adding new player profile to profile.json file.
    RUN.run_application("Off")  # Shutdown the application.
    time.sleep(5)  # Wait for the shutdown to finish.
    RUN.run_application("On")  # Rerun the application.
    player_id_name, player_id_score = API.get_player_by_id(url_request_player_by_id,
                                                           player_id)  # Get new player name and score.
    champ_score_list_from_file, champ_name_list_from_file = API.get_high_score_from_champ_file(
        champ_file)  # Read the champion.txt and take the player/s name and score.
    API.compare_scores(champ_score_list_from_file, champ_name_list_from_file, player_id_score,
                       player_id_name)  # Compare between the new player score and the champion/s score from champion.txt file.
    # Task 3
    API.create_excel(
        url_request_all_players)  # Create excel file based on the REST request of all players data and summarize their total score.


def main():
    status = RUN.run_application("On")  # Start Space Game application.
    time.sleep(5)  # Wait 5 sec until app is up.
    if status:  # If application is up run automation.
        ui_automation()  # Run all UI automation tests.
        api_automation()  # Run al API automation tests.
    RUN.run_application("Off")  # Shutdown Game Space application.


if __name__ == "__main__":
    main()

