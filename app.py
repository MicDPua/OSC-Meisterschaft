set2_p2 = st.selectbox(f"{player2} - 2. Satz", score_options, key=f"{player2}_set2")
        set3_p1 = st.selectbox(f"{player1} - 3. Satz (falls nötig)", score_options, key=f"{player1}_set3")
        set3_p2 = st.selectbox(f"{player2} - 3. Satz (falls nötig)", score_options, key=f"{player2}_set3")

        if st.button(f"Speichern: {player1} vs. {player2}", key=f"save_{player1}_{player2}"):
            sets = [(set1_p1, set1_p2), (set2_p1, set2_p2), (set3_p1, set3_p2)]
            wins_player1 = sum(1 for p1, p2 in sets if p1 > p2)
            wins_player2 = sum(1 for p1, p2 in sets if p2 > p1)

            if wins_player1 >= 2:
                winner = player1
            elif wins_player2 >= 2:
                winner = player2
            else:
                st.error("Mindestens zwei Gewinnsätze sind nötig.")
                continue

            st.session_state.ranking[tournament][winner] += 2
            st.success(f"{winner} erhält 2 Punkte")

elif menu == "📊 Rangliste":
    # Rangliste anzeigen
    st.subheader("🏆 Rangliste (Live-Aktualisierung)")
    rank_df = pd.DataFrame(list(st.session_state.ranking[tournament].items()), columns=["Spieler", "Punkte"])
    rank_df = rank_df.sort_values(by="Punkte", ascending=False)
    st.table(rank_df)