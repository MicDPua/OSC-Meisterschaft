import streamlit as st
import pandas as pd
import random

# Titel der App
st.title("🏸 Badminton Meisterschaft")

# Initialisierung der Session-Variablen mit vorgegebenen Spielern
if "players" not in st.session_state:
    st.session_state.players = {
        "Herren-Einzel": [
            "Alexander Ott", "Yong-Hwan Noh", "Sebastian Ferdinand", "Jannik Senss",
            "Christian Hackstein", "Misha Kovalov", "Christian Becker", "Manuel Menzel"
        ],
        "Damen-Einzel": [],
        "Herren-Doppel": [],
        "Damen-Doppel": []
    }
if "matches" not in st.session_state:
    st.session_state.matches = {t: [] for t in st.session_state.players}
if "ranking" not in st.session_state:
    st.session_state.ranking = {
        t: {p: {"Punkte": 0, "Spiele": 0} for p in st.session_state.players[t]} 
        for t in st.session_state.players
    }
if "match_results" not in st.session_state:
    st.session_state.match_results = {t: [] for t in st.session_state.players}

# Seiten-Menü
menu = st.sidebar.radio("📌 Menü", ["Spielübersicht & Ergebnisse", "📊 Rangliste", "📅 Spieltag Ergebnisse"])

# Turnier Auswahl
tournament = st.selectbox("🏆 Wähle ein Turnier", ["Herren-Einzel", "Damen-Einzel", "Herren-Doppel", "Damen-Doppel"])

if menu == "Spielübersicht & Ergebnisse":
    # Spieler hinzufügen
    st.subheader("📌 Spieler Registrierung")
    new_player = st.text_input("Spielername eingeben")
    if st.button("Hinzufügen"):
        if new_player and new_player not in st.session_state.players[tournament]:
            st.session_state.players[tournament].append(new_player)
            st.session_state.ranking[tournament][new_player] = {"Punkte": 0, "Spiele": 0}
            st.success(f"{new_player} wurde hinzugefügt!")
error("Mindestens zwei Gewinnsätze sind nötig.")
                    continue

                st.session_state.ranking[tournament][winner]["Punkte"] += 2
                st.session_state.ranking[tournament][player1]["Spiele"] += 1
                st.session_state.ranking[tournament][player2]["Spiele"] += 1

                st.session_state.match_results[tournament].append({"Spieler 1": player1, "Spieler 2": player2, "Ergebnis": result})
                st.success(f"{winner} erhält 2 Punkte")

elif menu == "📊 Rangliste":
    # Rangliste anzeigen mit Spiele-Anzahl
    st.subheader("🏆 Rangliste (Live-Aktualisierung)")
    rank_data = [
        [spieler, info["Punkte"], max(1, info["Spiele"])]  # Startet bei 1 statt 0
        for spieler, info in st.session_state.ranking[tournament].items()
    ]
    rank_df = pd.DataFrame(rank_data, columns=["Spieler", "Punkte", "Spiele"])
    rank_df = rank_df.sort_values(by="Punkte", ascending=False)
    st.table(rank_df)

elif menu == "📅 Spieltag Ergebnisse":
    # Ergebnisse aller Spieltage anzeigen
    st.subheader(f"📅 Detaillierte Ergebnisse für {tournament}")
    if not st.session_state.match_results[tournament]:
        st.info("Noch keine Ergebnisse eingetragen.")
    else:
        results_df = pd.DataFrame(st.session_state.match_results[tournament])
        st.table(results_df)
