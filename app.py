import streamlit as st
import pandas as pd
import random
import json

# Funktion zum Laden und Speichern der Daten
DATA_FILE = "tournament_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"players": {}, "matches": {}, "ranking": {}, "match_results": {}, "current_matchday": {}}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "players": st.session_state.players,
            "matches": st.session_state.matches,
            "ranking": st.session_state.ranking,
            "match_results": st.session_state.match_results,
            "current_matchday": st.session_state.current_matchday
        }, f)

# Daten laden
loaded_data = load_data()

# Titel der App
st.title("\U0001F3F8 Badminton Meisterschaft")

# Initialisierung der Session-Variablen
if "players" not in st.session_state:
    st.session_state.players = loaded_data.get("players", {"Herren-Einzel": [], "Damen-Einzel": [], "Herren-Doppel": [], "Damen-Doppel": []})
if "matches" not in st.session_state:
    st.session_state.matches = loaded_data.get("matches", {t: [] for t in st.session_state.players})
if "ranking" not in st.session_state:
    st.session_state.ranking = loaded_data.get("ranking", {t: {} for t in st.session_state.players})
if "match_results" not in st.session_state:
    st.session_state.match_results = loaded_data.get("match_results", {t: {} for t in st.session_state.players})
if "current_matchday" not in st.session_state:
    st.session_state.current_matchday = loaded_data.get("current_matchday", {t: 1 for t in st.session_state.players})

# Seiten-Menü
menu = st.sidebar.radio("\U0001F4CC Menü", ["Spielübersicht & Ergebnisse", "\U0001F3C6 Rangliste", "\U0001F4C5 Spieltage"])

# Turnier Auswahl
tournament = st.selectbox("\U0001F3C6 Wähle ein Turnier", list(st.session_state.players.keys()))

if menu == "Spielübersicht & Ergebnisse":
    # Spieler hinzufügen
    st.subheader("\U0001F4DD Spieler Registrierung")
    new_player = st.text_input("Spielername eingeben")
    if st.button("Hinzufügen"):
        if new_player and new_player not in st.session_state.players[tournament]:
            st.session_state.players[tournament].append(new_player)
            st.session_state.ranking[tournament][new_player] = {"Punkte": 0, "Spiele": 0}
            save_data()
            st.success(f"{new_player} wurde hinzugefügt!")

    # Spieler entfernen
    remove_player = st.selectbox("Spieler entfernen", ["Keinen entfernen"] + st.session_state.players[tournament])
    if st.button("Entfernen") and remove_player != "Keinen entfernen":
        st.session_state.players[tournament].remove(remove_player)
        del st.session_state.ranking[tournament][remove_player]
        save_data()
        st.success(f"{remove_player} wurde entfernt!")

    # Spielpaarungen generieren
    def generate_matches():
        players = st.session_state.players[tournament]
        if len(players) < 2:
            st.warning("Mindestens zwei Spieler sind erforderlich.")
            return []
        random.shuffle(players)
        pairs = [(players[i], players[i + 1]) for i in range(0, len(players) - 1, 2)]
        if len(players) % 2 == 1:
            pairs.append((players[-1], "Freilos"))
        return pairs

    if st.button("Nächste Runde starten"):
        st.session_state.matches[tournament] = generate_matches()
        st.session_state.current_matchday[tournament] += 1
        save_data()

    # Spiele anzeigen
    st.subheader("\U0001F3C3 Aktuelle Matches")
    match_list = st.session_state.matches[tournament]
    df_matches = pd.DataFrame(match_list, columns=["Spieler 1", "Spieler 2"])
    st.table(df_matches)

    # Ergebnisse eintragen
    st.subheader("\U0001F4DD Ergebnisse eintragen")
    for match in match_list:
        player1, player2 = match
        result = st.text_input(f"{player1} vs. {player2} (Format: 21-18, 15-21, 21-19)", key=f"{player1}_{player2}_result")
        if st.button(f"Speichern: {player1} vs.{player2}"):
            try:
                sets = result.split(", ")
                wins_p1 = sum(1 for s in sets if int(s.split("-")[0]) > int(s.split("-")[1]))
                wins_p2 = sum(1 for s in sets if int(s.split("-")[1]) > int(s.split("-")[0]))
                
                if wins_p1 >= 2:
                    winner = player1
                elif wins_p2 >= 2:
                    winner = player2
                else:
                    st.error("Mindestens zwei Gewinnsätze sind nötig.")
                    continue
                
                st.session_state.ranking[tournament][winner]["Punkte"] += 2
                st.session_state.ranking[tournament][player1]["Spiele"] += 1
                st.session_state.ranking[tournament][player2]["Spiele"] += 1
                
                matchday = st.session_state.current_matchday[tournament]
                if matchday not in st.session_state.match_results[tournament]:
                    st.session_state.match_results[tournament][matchday] = []
                
                st.session_state.match_results[tournament][matchday].append({"Spieler 1": player1, "Spieler 2": player2, "Ergebnis": result})
                save_data()
                st.success(f"{winner} erhält 2 Punkte")
            except ValueError:
                st.error("Falsches Format. Beispiel: '21-18, 15-21, 21-19'")