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