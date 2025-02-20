import streamlit as st
import pandas as pd
import random

# Titel der App
st.title("Badminton Meisterschaft")

# Initialisierung der Session-Variablen
if "players" not in st.session_state:
    st.session_state.players = {
        "Herren-Einzel": [],
        "Damen-Einzel": [],
        "Herren-Doppel": [],
        "Damen-Doppel": []
    }
if "matches" not in st.session_state:
    st.session_state.matches = {
        "Herren-Einzel": [],
        "Damen-Einzel": [],
        "Herren-Doppel": [],
        "Damen-Doppel": []
    }
if "ranking" not in st.session_state:
    st.session_state.ranking = {
        "Herren-Einzel": {},
        "Damen-Einzel": {},
        "Herren-Doppel": {},
        "Damen-Doppel": {}
    }

# Turnier Auswahl
tournament = st.selectbox("Wähle ein Turnier", ["Herren-Einzel", "Damen-Einzel", "Herren-Doppel", "Damen-Doppel"])

# Spieler hinzufügen
st.subheader("Spieler Registrierung")
new_player = st.text_input("Spielername eingeben")
if st.button("Hinzufügen"):
    if new_player and new_player not in st.session_state.players[tournament]:
        st.session_state.players[tournament].append(new_player)
        st.session_state.ranking[tournament][new_player] = 0
        st.success(f"{new_player} wurde hinzugefügt!")

# Spielpaarungen generieren
def generate_matches():
    players = st.session_state.players[tournament]
    random.shuffle(players)
    pairs = []
    for i in range(0, len(players) - 1, 2):
        pairs.append((players[i], players[i + 1]))
    return pairs

st.subheader("Spielplan")
if st.button("Nächste Runde starten"):
    st.session_state.matches[tournament] = generate_matches()

table_data = []
for match in st.session_state.matches[tournament]:
    player1, player2 = match
    table_data.append([player1, player2, ""])

df_matches = pd.DataFrame(table_data, columns=["Spieler 1", "Spieler 2", "Ergebnis"])
st.table(df_matches)

# Ergebnisse eintragen
st.subheader("Ergebnisse eintragen")
for match in st.session_state.matches[tournament]:
    player1, player2 = match
    score = st.text_input(f"Ergebnis für {player1} vs. {player2}")
    if st.button(f"Speichern: {player1} vs. {player2}"):
        winner = player1 if "-" in score and int(score.split("-")[0]) > int(score.split("-")[1]) else player2
        st.session_state.ranking[t