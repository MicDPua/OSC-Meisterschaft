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
        return {
            "players": {"Herren-Einzel": [], "Damen-Einzel": [], "Herren-Doppel": [], "Damen-Doppel": []},
            "matches": {"Herren-Einzel": [], "Damen-Einzel": [], "Herren-Doppel": [], "Damen-Doppel": []},
            "ranking": {"Herren-Einzel": {}, "Damen-Einzel": {}, "Herren-Doppel": {}, "Damen-Doppel": {}},
            "match_results": {"Herren-Einzel": {}, "Damen-Einzel": {}, "Herren-Doppel": {}, "Damen-Doppel": {}},
            "current_matchday": {"Herren-Einzel": 1, "Damen-Einzel": 1, "Herren-Doppel": 1, "Damen-Doppel": 1}
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
if "players" not in st.session_state:
    st.session_state.update(load_data())
    save_data()

# Titel der App
st.title("🏸 Badminton Meisterschaft")

# Seiten-Menü
menu = st.sidebar.radio("📌 Menü", ["Spielübersicht & Ergebnisse", "📊 Rangliste", "📅 Spieltag Ergebnisse"])

tournament = st.selectbox("🏆 Wähle ein Turnier", list(st.session_state.players.keys())) if st.session_state.players else None

if tournament:
    if menu == "Spielübersicht & Ergebnisse":
        st.subheader("📌 Spieler Registrierung")
        new_player = st.text_input("Spielername eingeben")
        if st.button("Hinzufügen") and new_player:
            if new_player not in st.session_state.players[tournament]:
                st.session_state.players[tournament].append(new_player)
                st.session_state.ranking[tournament][new_player] = {"Punkte": 0, "Spiele": 0}
                save_data()
                st.success(f"{new_player} wurde hinzugefügt!")
        
        st.subheader("❌ Spieler entfernen")
        if st.session_state.players[tournament]:
            remove_player = st.selectbox("Spieler auswählen", ["Keinen entfernen"] + st.session_state.players[tournament])
            if st.button("Entfernen") and remove_player != "Keinen entfernen":
                st.session_state.players[tournament].remove(remove_player)
                st.session_state.ranking[tournament].pop(remove_player, None)
                save_data()
                st.success(f"{remove_player} wurde entfernt!")
        
        def generate_matches():
            players = st.session_state.players[tournament]
            random.shuffle(players)
            return [(players[i], players[i + 1]) for i in range(0, len(players) - 1, 2)] + ([players[-1], "Freilos"] if len(players) % 2 else [])
        
        st.subheader("🎲 Spielplan")
        if st.button("Nächste Runde starten"):
            st.session_state.matches[tournament] = generate_matches()
            save_data()
        
        st.subheader("🏸 Aktuelle Matches")
        st.table(pd.DataFrame(st.session_state.matches[tournament], columns=["Spieler 1", "Spieler 2"]))
    
    elif menu == "📊 Rangliste" and tournament in st.session_state.ranking:
        st.subheader("🏆 Rangliste (Live-Aktualisierung)")
        if st.session_state.ranking[tournament]:
            df_rank = pd.DataFrame([{**{"Spieler": p}, **st.session_state.ranking[tournament][p]} for p in st.session_state.ranking[tournament]])
            if not df_rank.empty:
                df_rank = df_rank.sort_values(by="Punkte", ascending=False)
                st.table(df_rank)
            else:
                st.info("Noch keine Ranglisten-Daten vorhanden.")
        else:
            st.info("Noch keine Ranglisten-Daten vorhanden.")
    
    elif menu == "📅 Spieltag Ergebnisse" and tournament in st.session_state.match_results:
        st.subheader(f"📅 Detaillierte Ergebnisse für {tournament}")
        matchdays = st.session_state.match_results[tournament]
        if matchdays:
            selected_matchday = st.selectbox("Wähle einen Spieltag", sorted(matchdays.keys()))
            results_df = pd.DataFrame(matchdays[selected_matchday])
            st.table(results_df)
        else:
            st.info("Noch keine Ergebnisse eingetragen.")
else:
    st.warning("Es gibt noch keine Turniere. Bitte neue Spieler hinzufügen.")