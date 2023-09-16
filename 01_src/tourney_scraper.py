"""
[Script Name]
Tourney_scraper

[Description]
This webscraper automatically scrapes webpages from the tourney website. 
The website is for Canoe Polo matches and their scores. 

[Usage]
This should be an automated script. No input required.

[Author]
Jesper van Beemdelust

"""

# Import necessary libraries
 
from utils.get_web_data import get_html
from datetime import datetime
import json
import pandas as pd
import uuid

def get_tournaments_metadata() -> list:

    """This function grabs the tournament metadata and returns it in a list.
    The UUID's from each tournament are reused in the function: get_match_data. The uuid is concatinated to the url

    Returns:
        list: of tournament metadata, such as the start and enddate, but also the UUID.
    """

    tournaments_metadata = [["Raw_UUID", "Startdate", "Enddate", "Tournament_name", "ID"]]

    response = get_html(base_url)
    json_data = (response.json())

    for tournament in json_data["tournaments"]:
        print(tournament)
        original_uuid = tournament['id']['value']
        tournament_name = tournament["name"]
        tournament_id = uuid.uuid4()

        try:
            start_date = tournament["startDate"]["value"]
        except TypeError:
            print("Something went wrong with grabbing the start date")
            start_date = None

        try:
            end_date = tournament["endDate"]["value"]
        except TypeError:
            print("Something went wrong with grabbing the end date")
            end_date = None
        
        data_to_append = [
            original_uuid, 
            start_date, 
            end_date, 
            tournament_name,
            tournament_id
            ]
        tournaments_metadata.append(data_to_append)

    return tournaments_metadata

def get_match_data(tournament_uuid: str, tournament_id: str) -> list:

    """This function gets the data from each tournament and returns the data as a list

    Returns:
        list: Data of the tournament such as matches, teams played
    """
    
    match_data_to_return = []

    url_to_send_get = f"https://www.tourney.nz/data/tournament/{tournament_uuid}"
    print(url_to_send_get)
        
    response = get_html(url_to_send_get)
    json_data = (response.json())
    
    #TODO: The code, the for loops, below is slightly ugly, but I couldn't come up with a quick neater solution. Too many nested loops which makes it hard to read.

    # Data is separeted by day
    for gameday in json_data["gameDates"]:

        # If gametimes is empty. Skip that tournament.
        if len(gameday["gameTimes"]) == 0:
            continue

        gameday_date = gameday["date"]["value"]
        gametimes = gameday["gameTimes"]

        # A game day can have multiple pitches.
        for pitch in gameday["pitches"]:
            pitch_number = pitch["name"]

            # Counter for the matches played on a pitch. Start with 0 as it's used for slicing the gametimes and adding the gametime to the right match
            match_counter = 0

            # For each match on pitch. Save the match data.
            for match in pitch["games"]:
                try:
                    match_time_of_day = gametimes[match_counter]
                except IndexError:
                    match_time_of_day = "Unknown"
                match_uuid = match["id"]["value"]
                poule = match["group"]
                team1 = match["team1"]
                team1_original = match["team1Original"]
                team1_score = match["team1Score"]
                team1_defaulted = match["team1Defaulted"]
                team2 = match["team2"]
                team2_original = match["team2Original"]
                team2_score = match["team2Score"]
                team2_defaulted = match["team2Defaulted"]
                dutyteam = match["dutyTeam"]
                dutyteamoriginal = match["dutyTeamOriginal"]
                gamestatus = match["status"]

                data_to_append = [
                    gameday_date,
                    match_time_of_day,
                    pitch_number,
                    poule,
                    team1,
                    team1_original,
                    team1_score,
                    team1_defaulted,
                    team2,
                    team2_original,
                    team2_score,
                    team2_defaulted,
                    dutyteam,
                    dutyteamoriginal,
                    gamestatus,
                    match_uuid,
                    tournament_id
                 ]
                
                match_data_to_return.append(data_to_append)

                match_counter += 1

    return match_data_to_return

def main():

    # Grabbing the tournaments metadata. Links to their respective urls to start the webscrapping process
    tournaments_metadata = get_tournaments_metadata()

    match_data_list = [["Date", "Time_of_day","Pitch","Poule", "Team 1", "Team1_Original", "Team1_Score", "Team1_Defaulted","Team 2", "Team2_Original", "team2_Score", "Team2_Defaulted", "Dutyteam", "Dutyteam_Original", "Gamestatus", "Match_UUID", "Tournament_UUID"]]

    # Grabbing data from each tournament
    for tournament in tournaments_metadata[1:2]:
        # Check for valid UUID 
        if isinstance(tournament[0], str):
            match_data = get_match_data(tournament[0], tournament[4])
            for row in match_data:
                match_data_list.append(row)
        else:
            print("Invalid UUID")

    df = pd.DataFrame(match_data_list)
    df.to_csv("test.csv", index=False)

if __name__ == "__main__":
    base_url = "https://www.tourney.nz/data/tournaments"
    main()