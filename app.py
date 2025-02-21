import streamlit as st
import pandas as pd
import random
import json

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
st.title("🏸 Badminton Meisterschaft")

if "players" not in st.session_state:
    st.session_state.players = loaded_data.get("players", {
        "Herren-Einzel": [
            "Alexander Ott", "Yong-Hwan Noh", "Sebastian Ferdinand", "Jannik Senss",
            "Christian Hackstein", "Misha Kovalov", "Christian Becker", "Manuel Menzel"
        ],
        "Damen-Einzel": [], "Herren-Doppel": [], "Damen-Doppel": []
    })
if "matches" not in st.session_state:
    st.session_state.matches = loaded_data.get("matches", {t: [] for t in st.session_state.players})
if "ranking" not in st.session_state:
    st.session_state.ranking = loaded_data.get("ranking", {
        t: {p: {"Punkte": 0, "Spiele": 0} for p in st.session_state.players[t]}
        for t in st.session_state.players
    })
if "match_results" not in st.session_state:
    st.session_state.match_results = loaded_data.get("match_results", {t: {} for t in st.session_state.players})
if "current_matchday" not in st.session_state:
    st.session_state.current_matchday = loaded_data.get("current_matchday", {t: 1 for t in st.session_state.players})

menu = st.sidebar.radio("📌 Menü", ["Spielübersicht & Ergebnisse", "📊 Rangliste", "📅 Spieltag Ergebnisse"])

tournament = st.selectbox("🏆 Wähle ein Turnier", list(st.session_state.players.keys()))

if menu == "Spielübersicht & Ergebnisse":
    st.subheader("📌 Spieler Registrierung")
    new_player = st.text_input("Spielername eingeben")
    if st.button("Hinzufügen"):
        if new_player and new_player not in st.session_state.players[tournament]:
            st.session_state.players[tournament].append(new_player)
            st.session_state.ranking[tournament][new_player] = {"Punkte": 0, "Spiele": 0}
            save_data()
            st.success(f"{new_player} wurde hinzugefügt!")

    st.subheader("❌ Spieler entfernen")
    remove_player = st.selectbox("Spieler auswählen", ["Keinen entfernen"] + st.session_state.players[tournament])
    if st.button("Entfernen") and remove_player != "Keinen entfernen":
        st.session_state.players[tournament].remove(remove_player)
        del st.session_state.ranking[tournament][remove_player]
        save_data()
        st.success(f"{remove_player} wurde entfernt!")

    def generate_matches():
        players = st.session_state.players[tournament]
        if len(players) < 2:
            st.warning("Mindestens zwei Spieler sind erforderlich, um eine Runde zu starten.")
            return []
        random.shuffle(players)
        pairs = [(players[i], players[i + 1]) for i in range(0, len(players) - 1, 2)]
        if len(players) % 2 == 1:
            pairs.append((players[-1], "Freilos"))
        return pairs

    st.subheader("🎲 Spielplan")
    if st.button("Nächste Runde starten"):
        st.session_state.matches[tournament] = generate_matches()
        save_data()

    st.subheader("🏸 Aktuelle Matches")
    df_matches = pd.DataFrame(st.session_state.matches[tournament], columns=["Spieler 1", "Spieler 2"])
    st.table(df_matches)

    st.subheader("📝 Ergebnisse eintragen")
    for match in st.session_state.matches[tournament]:
        player1, player2 = match
        result = st.text_input(f"{player1} vs. {player2} (Format: 21-18, 15-21, 21-19)", key=f"{player1}_{player2}_result")
        if st.button(f"Speichern: {player1} vs. {player2}", key=f"save_{player1}_{player2}"):
            if result:
                st.session_state.match_results[tournament][st.session_state.current_matchday[tournament]] = {
                    "Spieler 1": player1, "Spieler 2": player2, "Ergebnis": result
                }
                st.session_state.ranking[tournament][player1]["Spiele"] += 1
                st.session_state.ranking[tournament][player2]["Spiele"] += 1
                st.session_state.ranking[tournament][player1 if int(result.split('-')[0]) > int(result.split('-')[1]) else player2]["Punkte"] += 2
                save_data()
                st.success("Ergebnis gespeichert!")

if menu == "📊 Rangliste":
    st.subheader("🏆 Rangliste (Live-Aktualisierung)")
    df_rank = pd.DataFrame([{**{"Spieler": p}, **st.session_state.ranking[tournament][p]} for p in st.session_state.ranking[tournament]])
    df_rank = df_rank.sort_values(by="Punkte", ascending=False)
    st.table(df_rank)

if menu == "📅 Spieltag Ergebnisse":
    st.subheader(f"📅 Detaillierte Ergebnisse für {tournament}")
    if st.session_state.match_results[tournament]:
        selected_matchday = st.selectbox("Wähle einen Spieltag", sorted(st.session_state.match_results[tournament].keys()))
        results_df = pd.DataFrame([st.session_state.match_results[tournament][selected_matchday]])
        st.table(results_df)
    else:
        st.info("Noch keine Ergebnisse eingetragen.")