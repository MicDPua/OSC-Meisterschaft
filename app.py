import streamlit as st
import pandas as pd
import random

# Titel der App
st.title("Badminton Meisterschaft")

# Initialisierung der Session-Variablen mit vorgegebenen Spielern
if "players" not in st.session_state:
    st.session_state.players = {
        "Herren-Einzel": [
            "Alexander Ott", "Yong-Hwan Noh", "Sebastian Ferdinand", "Jannik Senss", 
            "Christian Hackstein", "Misha Kovalov", "Christian Becker", "Manuel Menzel",
            "Matthias Bornemann", "Fabian Fischer", "Daniel Druyen", "Robert Marusic",
            "Janis Schmelz", "Veit Kriegel", "Max Pradel", "Florian Weber", 
            "Lukas Endemann", "Raphael Jühe", "Tobias Wegner", "Weiki Chen",
            "Tobias Neumann", "Dennis Starke", "Vincent Bergman", "Cedric Noller",
            "Sebastian Schulz", "Tim Kromat", "Julian Klehr", "John Zickler",
            "Ngoc Hai Long Nguyen", "Lars Heidelberg", "Bogdan Cravcenco", 
            "Sean Bakker", "Arttapon Setchampa", "Sven Klein", "Constantin Wermann",
            "Michael Hansen", "Tobias Vanik", "Marius Buschmeier", "Matthew Decker",
            "Leon de Groot", "Artem Kokorin", "Christian Knoche", "Michael Kroes",
            "Clemens Zintgraf", "Kai Brösing", "Jonas Schneider", "Stanislav Ovsyannikov",
            "Markus Spindler", "Aditya Oka", "Jens Hidle", "Hung Dinh"
        ],
        "Damen-Einzel": [],
        "Herren-Doppel": [],
        "Damen-Doppel": []
    }
if "matches" not in st.session_state:
    st.session_state.matches = {t: [] for t in st.session_state.players}
if "ranking" not in st.session_state:
    st.session_state.ranking = {t: {p: 0 for p in st.session_state.players[t]} for t in st.session_state.players}

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
    if len(players) < 2:
        st.warning("Mindestens zwei Spieler sind erforderlich, um eine Runde zu starten.")
        return []
    
    random.shuffle(players)
    pairs = []
    for i in range(0, len(players) - 1, 2):
        pairs.append((players[i], players[i + 1]))

    if len(players) % 2 == 1:  # Falls eine ungerade Anzahl an Spielern ist
        pairs.append((players[-1], "Freilos"))

    return pairs

st.subheader("Spielplan")
if st.button("Nächste Runde starten"):
    st.session_state.matches[tournament] = generate_matches()

# Spiele anzeigen
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
        if "-" in score:
            score_split = score.split("-")
            if len(score_split) == 2 and score_split[0].isdigit() and score_split[1].isdigit():
                if int(score_split[0]) > int(score_split[1]):
                    winner = player1
                else:
                    winner = player2
                
                st.session_state.ranking[tournament][winner] += 2
                st.success(f"{winner} erhält 2 Punkte")
            else:
                st.error("Bitte ein gültiges Ergebnis im Format '21-18' eingeben.")
        else:
            st.error("Bitte das Ergebnis im Format '21-18' eingeben.")

# Rangliste anzeigen