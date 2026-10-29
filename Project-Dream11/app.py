"""Streamlit UI for Dream11 Genie.

Run:  streamlit run app.py
Needs GROQ_API_KEY in your environment / .env (free Groq key).
"""
import streamlit as st
import os
from agent import pick_team
from data import SQUADS

st.set_page_config(page_title="Dream11 Genie", page_icon="🏏", layout="centered")

st.title("🏏 Dream11 Genie")
st.caption("An AI agent that reasons over live-style data to pick your fantasy XI.")


# Sidebar - Settings & Authentication
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input(
        "Groq API Key",
        value="",
        type="password",
        help="Uses GROQ_API_KEY from environment or .env if left blank.",
    )
    st.markdown("---")
    st.markdown(
        "Get a free API key at [Groq Console](https://console.groq.com/keys)."
    )

# Determine API Key
effective_api_key = api_key_input.strip() or os.getenv("GROQ_API_KEY")

match = st.selectbox("Pick a fixture", list(SQUADS.keys())) 

if st.button("Generate my XI", type="primary"):

    if not effective_api_key:
        st.error(
            "⚠️ Groq API key not found. Please provide it in the sidebar or set `GROQ_API_KEY` in your `.env` file."
        )
    else:
        # Set environment variable dynamically if provided via sidebar
        os.environ["GROQ_API_KEY"] = effective_api_key
            
        with st.spinner("The agent is calling tools and reasoning…"):
            team = pick_team(match)

        st.subheader(f"Your XI — {team.match}")
        c1, c2 = st.columns(2)
        c1.metric("Captain (2x)", team.captain)
        c2.metric("Vice-captain (1.5x)", team.vice_captain)

        st.table(
            [
                {
                    "": "⭐" if p.player == team.captain else ("🔸" if p.player == team.vice_captain else ""),
                    "Player": p.player,
                    "Role": p.role,
                    "Team": p.team,
                    "Why": p.reason,
                }
                for p in team.players
            ]
        )
        st.info(f"**Strategy:** {team.strategy}")
