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
st.subheader("Aktuelle Matches")
table_data = []
for match in st.session_state.matches[tournament]:
    player1, player2 = match
    table_data.append([player1, player2, ""])

df_matches = pd.DataFrame(table_data, columns=["Spieler 1", "Spieler 2", "Ergebnis"])
st.table(df_matches)

# Ergebnisse eintragen mit zwei Gewinnsätzen
st.subheader("Ergebnisse eintragen")
for match in st.session_state.matches[tournament]:
    player1, player2 = match
    set1 = st.text_input(f"1. Satz ({player1} vs. {player2})", key=f"{player1}_{player2}_set1")
    set2 = st.text_input(f"2. Satz ({player1} vs. {player2})", key=f"{player1}_{player2}_set2")
    set3 = st.text_input(f"3. Satz (falls nötig)", key=f"{player1}_{player2}_set3")

    if st.button(f"Speichern: {player1} vs. {player2}", key=f"save_{player1}_{player2}"):
        scores = [set1, set2, set3] if set3 else [set1, set2]

        if all("-" in score and len(score.split("-")) == 2 for score in scores):
            wins_player1 = sum(1 for s in scores if int(s.split("-")[0]) > int(s.split("-")[1]))
            wins_player2 = sum(1 for s in scores if int(s.split("-")[1]) > int(s.split("-")[0]))

            if wins_player1 >= 2:
                winner = player1
            elif wins_player2 >= 2:
                winner = player2
            else:
                st.error("Mindestens zwei Gewinnsätze sind nötig.")
                continue

            st.session_state.ranking[tournament][winner] += 2
            st.success(f"{winner} erhält 2 Punkte")
        else:
            st.error("Bitte gültige Sätze im Format '21-18' oder '30-29' eingeben.")

# Rangliste anzeigen
st.subheader("Rangliste (Live-Aktualisierung)")
rank_df = pd.DataFrame(list(st.session_state.ranking[tournament].items()), columns=["Spieler", "Punkte"])
rank_df = rank_df.sort_values(by="Punkte", ascending=False)
st.table(rank_df)