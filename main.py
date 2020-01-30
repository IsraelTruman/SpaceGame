# from UI_Automation_Tests import UI_Automation_Test as UI
from API_Automation_Test import API_Automation_Test as API
import Run_Applicarion as RUN
import time


# The ui_automation function is where API functions order and run.
# The function get the tests_status_dict which hold the status of the automation tests and update it according
# to the test results. When finished the tests_status_dict returned.
# The ui_automation function also make sure to handle dependencies between functions.
def ui_automation(tests_status_dict):
    test_status = UI.open_game_window("http://localhost", 5000)  # Open web browser with the URL and port parameters.
    tests_status_dict[test_status] += 1
    if test_status == "Pass":  # Condition to check if the web browser window opened successfully.
        test_status = UI.download_game_message()  # Press Download Game button and print the message from pop up window.
        tests_status_dict[test_status] += 1
        test_status = UI.change_table("Mode", "All")  # Change the Mode table to All mode.
        tests_status_dict[test_status] += 1
        test_status = UI.change_table("Galaxy", "All")  # Change the Galaxy table to All mode.
        tests_status_dict[test_status] += 1
        test_status = UI.change_page(3)  # Change page to page 3.
        tests_status_dict[test_status] += 1
        test_status = UI.check_player_score(
            "duality")  # Check player called 'duality' and get his Mode, Galaxy and Score.
        tests_status_dict[test_status] += 1
        test_status = UI.check_player_achievements(
            "duality")  # Press on 'duality' player link and get all player achievements from popup window.
        tests_status_dict[test_status] += 1
        test_status = UI.change_page(1)  # Change page to page 3.
        tests_status_dict[test_status] += 1
        test_status = UI.change_table("Galaxy", "Pinwheel")  # Change the Galaxy table to Pinwheel mode.
        tests_status_dict[test_status] += 1
        test_status = UI.get_total_score(
            1314090)  # get all players total score and compare it with 1314090 and print the evaluation result.
        tests_status_dict[test_status] += 1
        test_status = UI.close_game_window()  # Close the web browser window.
        tests_status_dict[test_status] += 1
    return tests_status_dict


# The api_automation function is where API functions order and run.
# The function get the tests_status_dict which hold the status of the automation tests and update it according
# to the test results. When finished the tests_status_dict returned.
# The api_automation function also make sure to handle dependencies between functions.
def api_automation(tests_status_dict):
    champ_file, champ_list = "", ""
    # Task 1
    test_status, player_data = API.get_all_players(
        url_request_all_players)  # Send REST request to get all players as json.
    tests_status_dict[test_status] += 1
    if test_status == "Pass":
        test_status, champ_list = API.get_champs_sorted_list(
            player_data)  # Get list of all players sorted (using merge_sort function) according to their score.
        tests_status_dict[test_status] += 1
    if test_status == "Pass":
        test_status, champ_file = API.write_champ_player_to_file(
            champ_list)  # Writing the player/s with the highest score to champion.txt file.
        tests_status_dict[test_status] += 1
    # Task 2
    test_status = API.add_player_to_profile_file(json_file,
                                                 new_player_profile_data)  # adding new player profile to profile.json file.
    tests_status_dict[test_status] += 1
    if test_status == "Pass":
        test_status = RUN.run_application("Off")  # Kill the application process.
        tests_status_dict[test_status] += 1
        time.sleep(5)  # Wait for the shutdown to finish.
        test_status = RUN.run_application("On")  # Run the application.
        tests_status_dict[test_status] += 1
    test_status, player_id_name, player_id_score = API.get_player_by_id(url_request_player_by_id,
                                                                        player_id)  # Get new player name and score.
    tests_status_dict[test_status] += 1
    if champ_file != "" and test_status == "Pass":
        test_status, champ_score_list_from_file, champ_name_list_from_file = API.get_high_score_from_champ_file(
            champ_file)  # Read the champion.txt and take the player/s name and score.
        tests_status_dict[test_status] += 1
        if test_status == "Pass":
            test_status = API.compare_scores(champ_score_list_from_file, champ_name_list_from_file, player_id_score,
                                             player_id_name)  # Compare between the new player score and the champion/s score from champion.txt file.
            tests_status_dict[test_status] += 1
    # Task 3
    test_status = API.create_excel(
        url_request_all_players)  # Create excel file based on the REST request of all players data and summarize their total score.
    tests_status_dict[test_status] += 1
    return tests_status_dict


# main function is the function that start our application and set if the UI and API tests should run.
# At the end the function print a summary of the tests results.
def main():
    tests_status_dict = {"Pass": 0, "Fail": 0, "Not Tested": 23}
    test_status = RUN.run_application("On")  # Start Space Game application.
    tests_status_dict[test_status] += 1
    time.sleep(5)  # Wait 5 sec until app is up.
    if test_status == "Pass":  # If application is up run automation.
#         tests_status_dict = ui_automation(tests_status_dict)  # Run all UI automation tests.
        tests_status_dict = api_automation(tests_status_dict)  # Run al API automation tests.
    test_status = RUN.run_application("Off")  # Shutdown Game Space application.
    tests_status_dict[test_status] += 1
    print("#" * 50)
    print("   Tests results summary:")
    print("      Pass tests: " + str(tests_status_dict["Pass"]) + ".")
    print("      Fail tests: " + str(tests_status_dict["Fail"]) + ".")
    tests_status_dict["Not Tested"] = tests_status_dict["Not Tested"] - tests_status_dict["Pass"] - tests_status_dict[
        "Fail"]
    print("      Not Tested tests: " + str(tests_status_dict["Not Tested"]) + ".")
    print("#" * 50)


########################################################################
#                            variables                                 #
########################################################################
url_request_all_players = "https://localhost:5001/api/game/getplayers"
url_request_player_by_id = "https://localhost:5001/api/game/getplayer?playerId="
player_id = 21
json_file = "d:\\a\\1\\s\\mslearn-tailspin-spacegame-web-master\\Tailspin.SpaceGame.Web\\SampleData\\profiles.json"
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


if __name__ == "__main__":
    main()
