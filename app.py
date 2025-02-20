import streamlit as st
import pandas as pd
import random

# Заголовок страницы
st.title("Badminton Meisterschaft")

# Инициализация Session State для хранения данных
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

# Выбор турнира
tournament = st.selectbox("Wähle ein Turnier", ["Herren-Einzel", "Damen-Einzel", "Herren-Doppel", "Damen-Doppel"])

# Добавление игроков
st.subheader("Spieler Registrierung")
new_player = st.text_input("Spielername eingeben")
if st.button("Hinzufügen"):
    if new_player and new_player not in st.session_state.players[tournament]:
        st.session_state.players[tournament].append(new_player)
        st.session_state.ranking[tournament][new_player] = 0
        st.success(f"{new_player} wurde hinzugefügt!")

# Функция генерации пар для игр (швейцарская система)
def generate_matches():
    players = st.session_state.players[tournament]
    if len(players) < 2:
        st.warning("Mindestens zwei Spieler sind erforderlich, um eine Runde zu starten.")
        return []

    random.shuffle(players)
    pairs = []
    for i in range(0, len(players) - 1, 2):
        pairs.append((players[i], players[i + 1]))

    if len(players) % 2 == 1:  # Если нечетное количество игроков, один получает свободную победу
        pairs.append((players[-1], "Freilos"))

    return pairs

# Генерация новой пары для следующего раунда
st.subheader("Spielplan")
if st.button("Nächste Runde starten"):
    st.session_state.matches[tournament] = generate_matches()

# Отображение таблицы с играми
table_data = []
for match in st.session_state.matches[tournament]:
    player1, player2 = match
    table_data.append([player1, player2, ""])

df_matches = pd.DataFrame(table_data, columns=["Spieler 1", "Spieler 2", "Ergebnis"])
st.table(df_matches)

# Ввод результатов матчей
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

# Таблица с рейтингом игроков
st.subheader("Rangliste")
rank_df = pd.DataFrame(list(st.session_state.ranking[tournament].items()), columns=["Spieler", "Punkte"])
rank_df = rank_df.sort_values(by="Punkte", ascending=False)
st.table(rank_df)