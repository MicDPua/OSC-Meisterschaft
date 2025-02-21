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

    # Spieler entfernen
    st.subheader("❌ Spieler entfernen")
    remove_player = st.selectbox("Spieler auswählen", ["Keinen entfernen"] + st.session_state.players[tournament])
    if st.button("Entfernen") and remove_player != "Keinen entfernen":
        st.session_state.players[tournament].remove(remove_player)
        del st.session_state.ranking[tournament][remove_player]
        st.success(f"{remove_player} wurde entfernt!")

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

        if len(players) % 2 == 1:
            pairs.append((players[-1], "Freilos"))

        return pairs

    st.subheader("🎲 Spielplan")
    if st.button("Nächste Runde starten"):
        st.session_state.matches[tournament] = generate_matches()

    # Spiele anzeigen
    st.subheader("🏸 Aktuelle Matches")
    table_data = []
    for match in st.session_state.matches[tournament]:
        player1, player2 = match
        table_data.append([player1, player2, ""])

    df_matches = pd.DataFrame(table_data, columns=["Spieler 1", "Spieler 2", "Ergebnis"])
    st.table(df_matches)

    # Ergebnisse eintragen in einer Zeile
    st.subheader("📝 Ergebnisse eintragen")
    for match in st.session_state.matches[tournament]:
        player1, player2 = match

        result = st.text_input(f"{player1} vs. {player2} (Format: 21-18, 15-21, 21-19)", key=f"{player1}_{player2}_result")

        if st.button(f"Speichern: {player1} vs. {player2}", key=f"save_{player1}_{player2}"):
            if result:
                sets = result.split(", ")
                wins_player1 = sum(1 for s in sets if int(s.split("-")[0]) > int(s.split("-")[1]))
                wins_player2 = sum(1 for s in sets if int(s.split("-")[1]) > int(s.split("-")[0]))

                if wins_player1 >= 2:
                    winner = player1
                elif wins_player2 >= 2:
                    winner = player2
                else:
                    st.