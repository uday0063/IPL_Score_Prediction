import streamlit as st
import pickle
import pandas as pd

teams = [
    'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
    'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
    'Rajasthan Royals', 'Delhi Capitals'
]

cities = [
    'Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
    'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
    'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
    'Sharjah', 'Mohali', 'Bengaluru'
]

pipe = pickle.load(open('pipe.pkl', 'rb'))
st.title('IPL Win Predictor')

col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))

bowling_team_options = [team for team in teams if team != batting_team]
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(bowling_team_options))

selected_city = st.selectbox('Select host city', sorted(cities))

target = st.number_input('Target', step=1, format="%d")

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('Score', step=1, format="%d")
with col4:
    overs = st.number_input('Overs completed', step=1, format="%d", min_value=0, max_value=20)
    if overs < 0 or overs > 20:
        st.error("Overs must be between 0 and 20.")
with col5:
    wickets = st.number_input('Wickets out', step=1, format="%d")

if overs > 0 and score > (overs * 36):
    st.error("The score entered is not possible with the overs completed.")
    prediction_allowed = False
else:
    prediction_allowed = True

if st.button('Predict Probability') and prediction_allowed:
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [wickets_left],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    st.header(f"{batting_team} - {round(win * 100)}%")
    st.header(f"{bowling_team} - {round(loss * 100)}%")