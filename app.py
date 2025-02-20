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

elif menu == "📊 Rangliste":
    # Rangliste anzeigen
    st.subheader("🏆 Rangliste (Live-Aktualisierung)")
    rank_df = pd.DataFrame(list(st.session_state.ranking[tournament].items()), columns=["Spieler", "Punkte"])
    rank_df = rank_df.sort_values(by="Punkte", ascending=False)
    st.table(rank_df)