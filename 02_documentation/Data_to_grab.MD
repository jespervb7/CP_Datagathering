# Tables/data to grab

## Tournament info
    - Tournament_ID
        - Randomly generated with UUID
    - Created at
    - Date start
    - Date end
    - City
    - Country
    - Name
    - Year 
   
## Matches
    This table should be made **after** the tournament info table. Tournament_ID does not exists before that point.
    - Tournament_ID
    - Match_ID
        - Randomly generated with UUID
    - Created at
    - Date
    - Time_day
    - Stage
        - The stages the tournament is in. Is it a group stage or the second group stage
    - Poule
    - Category/division
        - The division the game is played in
    - Pitch
    - First_team
    - Second_team
    - First_team goals
    - Second_team goals
    - First_referee
    - Second_referee
    - Table_duty

## Ranking (if possible)
    This table should be made **after** the tournament info table. Tournament_ID does not exists before that point.
    - Tournament_ID
        - Randomly generated
    - Created at
    - Division
    - Team_name
    - Ranking

## Players
    - Tournament_ID
    - Player_ID
        - Randomly generated
    - Created at
    - Team_name
    - First_name
    - Last_name
    - Nationality
    - Date_of_birth
    - Gender

## Referees
    - Tournament_ID
    - Referee_ID
        - Randomly generated
    - Created at
    - First_name
    - Last_name
    - Nationality
    - Date_of_birth
    - ICF_Grade
    - National_Grade
        - If applicable