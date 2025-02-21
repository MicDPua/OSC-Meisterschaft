import streamlit as st
import pandas as pd
import random

# Titel der App
st.title("\U0001F3F8 Badminton Meisterschaft")

# Initialisierung der Session-Variablen
if "players" not in st.session_state:
    st.session_state.players = {"Herren-Einzel": [], "Damen-Einzel": [], "Herren-Doppel": [], "Damen-Doppel": []}
if "matches" not in st.session_state:
    st.session_state.matches = {t: [] for t in st.session_state.players}
if "ranking" not in st.session_state:
    st.session_state.ranking = {t: {} for t in st.session_state.players}
if "match_results" not in st.session_state:
    st.session_state.match_results = {t: {} for t in st.session_state.players}
if "current_matchday" not in st.session_state:
    st.session_state.current_matchday = {t: 1 for t in st.session_state.players}

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
            st.success(f"{new_player} wurde hinzugefügt!")

    # Spieler entfernen
    remove_player = st.selectbox("Spieler entfernen", ["Keinen entfernen"] + st.session_state.players[tournament])
    if st.button("Entfernen") and remove_player != "Keinen entfernen":
        st.session_state.players[tournament].remove(remove_player)
        del st.session_state.ranking[tournament][remove_player]
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
        if st.button(f"Speichern: {player1} vs. {player2}"):
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
                if matchday not in st.session_state.match_results[tournament]:st.session_state.match_results[tournament][matchday] = []
                
                st.session_state.match_results[tournament][matchday].append({"Spieler 1": player1, "Spieler 2": player2, "Ergebnis": result})
                st.success(f"{winner} erhält 2 Punkte")
            except ValueError:
                st.error("Falsches Format. Beispiel: '21-18, 15-21, 21-19'")

elif menu == "\U0001F3C6 Rangliste":
    st.subheader("\U0001F3C6 Rangliste")
    rank_data = [[p, d["Punkte"], d["Spiele"]] for p, d in st.session_state.ranking[tournament].items()]
    df_rank = pd.DataFrame(rank_data, columns=["Spieler", "Punkte", "Spiele"]).sort_values(by="Punkte", ascending=False)
    st.table(df_rank)

elif menu == "\U0001F4C5 Spieltage":
    st.subheader(f"\U0001F4C5 Ergebnisse für {tournament}")
    matchdays = st.session_state.match_results[tournament]
    if not matchdays:
        st.info("Noch keine Ergebnisse eingetragen.")
    else:
        selected_matchday = st.selectbox("Wähle einen Spieltag", sorted(matchdays.keys()))
        results_df = pd.DataFrame(matchdays[selected_matchday])
        st.table(results_df)