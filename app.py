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
        return {
            "players": {"Herren-Einzel": [], "Damen-Einzel": [], "Herren-Doppel": [], "Damen-Doppel": []},
            "matches": {}, "ranking": {}, "match_results": {}, "current_matchday": {}
        }

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
st.title("🏸 Badminton Meisterschaft")

# Sicherstellen, dass die Hauptstrukturen existieren
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
menu = st.sidebar.radio("📌 Menü", ["Spielübersicht & Ergebnisse", "🏆 Rangliste", "📅 Spieltage"])

# Turnier Auswahl
if len(st.session_state.players.keys()) == 0:
    st.warning("Es gibt noch keine Turniere. Bitte neue Spieler hinzufügen.")
else:
    tournament = st.selectbox("🏆 Wähle ein Turnier", list(st.session_state.players.keys()))

    if menu == "Spielübersicht & Ergebnisse":
        # Spieler hinzufügen
        st.subheader("📌 Spieler Registrierung")
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
        st.subheader("🏸 Aktuelle Matches")
        match_list = st.session_state.matches[tournament]
        df_matches = pd.DataFrame(match_list, columns=["Spieler 1", "Spieler 2"])
        st.table(df_matches)

    elif menu == "🏆 Rangliste":
        st.subheader("🏆 Rangliste")
        rank_data = [[p, d["Punkte"], d["Spiele"]] for p, d in st.session_state.ranking[tournament].items()]
        df_rank = pd.DataFrame(rank_data, columns=["Spieler", "Punkte", "Spiele"]).sort_values(by="Punkte", ascending=False)
        st.table(df_rank)

    elif menu == "📅 Spieltage":
        st.subheader(f"📅 Ergebnisse für {tournament}")
        matchdays = st.session_state.match_results[tournament]
        if not matchdays:
            st.info("Noch keine Ergebnisse eingetragen.")
        else:
            selected_matchday = st.selectbox("Wähle einen Spieltag", sorted(matchdays.keys()))
            results_df = pd.DataFrame(matchdays[selected_matchday])
            st.table(results_df)