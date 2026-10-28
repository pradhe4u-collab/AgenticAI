"""Pitch to the AI Sharks — Streamlit app.

Host-routed two-round panel from Session 09. Paste a pitch, run the tank,
and inspect round-1, debate, and host wrap-up without notebook magics.
"""

from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass
from typing import List, Optional, TypedDict

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from dotenv import find_dotenv, load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

load_dotenv(find_dotenv(usecwd=True))

st.set_page_config(
    page_title="SharkAI",
    page_icon="🦈",
    layout="wide",
    initial_sidebar_state="expanded",
)

os.environ.setdefault("CREWAI_TELEMETRY_ENABLED", "false")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

SAMPLE_PITCH = """GharSolar - rooftop solar subscriptions for middle-class Indian homes.

Problem: rooftop solar saves families 60% on power bills, but the Rs 2-3 lakh upfront cost
puts it out of reach for most.

Solution: GharSolar installs solar for zero upfront cost; households pay a fixed monthly
subscription lower than their old bill. We own the panels and the financing.

Traction: 2,100 homes installed across Jaipur and Indore in 14 months. Rs 1.1 crore monthly
recurring revenue. BUT gross margin is only 12% today because of hardware and install costs,
and each install costs us Rs 1.8 lakh to acquire, recovered over 4 years. Churn is under 2%.

Ask: raising Rs 25 crore for 15% to build install capacity and negotiate panel supply deals.
"""

DEFAULT_MODEL = "openai/gpt-oss-120b"
CHEAP_MODEL = "openai/gpt-oss-20b"
MAX_ROUNDS = 2
ORDER = ["numbers", "visionary", "skeptic", "customer_shark", "growth_shark"]


@dataclass
class Shark:
    name: str
    title: str
    system: str


SHARKS = [
    Shark(
        "Nikhil",
        "The Numbers Shark",
        "You are Nikhil, a ruthless numbers-first investor. You judge a startup on unit "
        "economics alone: margins, CAC vs LTV, burn rate, path to profit, and whether the "
        "valuation is sane. You are unmoved by vision or hype - show you the math or you pass. "
        "You speak bluntly and quote numbers.",
    ),
    Shark(
        "Veena",
        "The Visionary",
        "You are Veena, a visionary investor. You back bold founders and enormous markets. You "
        "look past today's messy numbers to the 10x outcome - the mission, the timing, the "
        "founder's ambition. You get genuinely excited by a big idea and are willing to bet early. "
        "You speak with warmth and conviction.",
    ),
    Shark(
        "Sameer",
        "The Skeptic",
        "You are Sameer, a sharp skeptic. Your job is to find why this startup will FAIL: crowded "
        "competition, no moat, weak differentiation, regulatory or execution risk, a founder gap. "
        "You are hard to convince and you probe the weakest point. You are fair but tough, and you "
        "say plainly what worries you.",
    ),
    Shark(
        "Priya",
        "Customer Shark",
        "You are Priya, a customer shark. You focus on customer pain points, willingness to pay, "
        "retention, and product-market fit. Your personality is customer-focused, empathetic, but "
        "demands evidence. You reject pitches that assume customers will buy without validating demand.",
    ),
    Shark(
        "Arjun",
        "Growth Shark",
        "You are Arjun, a Growth Shark. You focus on customer acquisition, distribution, scalability, "
        "and growth potential. Your personality is ambitious, data-driven, and commercially minded. "
        "You question unrealistic growth projections and unsustainable acquisition costs.",
    ),
]

HOST = (
    "You are the host of 'Pitch to the AI Sharks'. You are witty, fair and concise. In 3-4 "
    "sentences, summarise how the panel voted, note where the sharks agreed and where they "
    "clashed, and leave the founder with one clear, actionable takeaway."
)


class Verdict(BaseModel):
    shark: str = Field(description="the shark's name")
    stance: str = Field(description="INVEST or PASS")
    offer: Optional[str] = Field(
        default=None,
        description="an offer like 'Rs 50L for 10%', or null if passing",
    )
    reasoning: str = Field(
        description="2-3 sentences justifying the stance, in the shark's own voice"
    )


class RoomState(TypedDict):
    pitch: str
    round1: list[Verdict]
    final: list[Verdict]
    turn: str
    calls: int
    summary: str


def new_llm(model: str, temperature: float = 0.3) -> ChatGroq:
    return ChatGroq(model=model, temperature=temperature, max_retries=8, timeout=60)


def _format(verdicts: List[Verdict]) -> str:
    lines = []
    for v in verdicts:
        offer = f"  Offer: {v.offer}" if v.offer else ""
        lines.append(f"- {v.shark} - {v.stance}: {v.reasoning}{offer}")
    return "\n".join(lines)


def _evaluate(shark: Shark, pitch: str, model: str, temperature: float, others: str = "") -> Verdict:
    prompt = (
        shark.system
        + '\n\nYou are judging this startup pitch:\n"""\n'
        + pitch
        + '\n"""\n'
    )
    if others:
        prompt += (
            "\nThe other sharks have given their takes:\n"
            + others
            + "\n\nReact to them where you disagree, then give YOUR verdict.\n"
        )
    prompt += (
        f"\nRespond as {shark.name}. Decide INVEST or PASS, make an offer only if you "
        "invest, and give your reasoning in your own voice."
    )
    verdict = (
        new_llm(model, temperature)
        .with_structured_output(Verdict, method="json_schema", strict=True)
        .invoke(prompt)
    )
    verdict.shark = shark.name
    return verdict


def _host(state: RoomState, model: str, temperature: float) -> dict:
    prompt = (
        HOST
        + "\n\nThe pitch:\n"
        + state["pitch"]
        + "\n\nThe panel's final verdicts:\n"
        + _format(state["final"])
        + "\n\nGive your wrap-up."
    )
    return {"summary": new_llm(model, temperature=max(temperature, 0.5)).invoke(prompt).content}


def build_room(model: str, temperature: float, max_rounds: int):
    def host_node(state: RoomState):
        calls = state.get("calls", 0)
        turn = ORDER[calls % len(ORDER)] if calls < max_rounds * len(ORDER) else "done"
        update = {"turn": turn}
        if turn == "done":
            update.update(_host(state, model, temperature))
        return update

    def route(state: RoomState):
        return state["turn"]

    def shark_node(index: int):
        def run(state: RoomState):
            round_number = state.get("calls", 0) // len(ORDER)
            others = ""
            if round_number:
                others = _format(
                    [v for v in state.get("round1", []) if v.shark != SHARKS[index].name]
                )
            verdict = _evaluate(SHARKS[index], state["pitch"], model, temperature, others)
            key = "final" if round_number else "round1"
            return {key: [*state.get(key, []), verdict], "calls": state.get("calls", 0) + 1}

        return run

    graph = StateGraph(RoomState)
    graph.add_node("host", host_node)
    for i, name in enumerate(ORDER):
        graph.add_node(name, shark_node(i))
    graph.set_entry_point("host")
    graph.add_conditional_edges(
        "host",
        route,
        {name: name for name in ORDER} | {"done": END},
    )
    for name in ORDER:
        graph.add_edge(name, "host")
    return graph.compile()


async def evaluate_async(shark: Shark, pitch: str, model: str, temperature: float) -> Verdict:
    prompt = shark.system + "\nPitch:\n" + pitch
    verdict = await (
        new_llm(model, temperature)
        .with_structured_output(Verdict, method="json_schema", strict=True)
        .ainvoke(prompt)
    )
    verdict.shark = shark.name
    return verdict


def verdicts_frame(verdicts: List[Verdict]) -> pd.DataFrame:
    rows = []
    for v in verdicts:
        rows.append(
            {
                "Shark": v.shark,
                "Stance": v.stance,
                "Offer": v.offer or "—",
                "Reasoning": v.reasoning,
            }
        )
    return pd.DataFrame(rows)


def stance_chart(verdicts: List[Verdict], title: str):
    counts = {"INVEST": 0, "PASS": 0}
    for v in verdicts:
        key = "INVEST" if str(v.stance).upper().startswith("INVEST") else "PASS"
        counts[key] += 1
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    colors = ["#2e7d32", "#c62828"]
    ax.bar(list(counts.keys()), list(counts.values()), color=colors)
    ax.set_title(title)
    ax.set_ylabel("Sharks")
    ax.set_ylim(0, max(len(verdicts), 1))
    fig.tight_layout()
    return fig


def ensure_api_key(sidebar_key: str) -> str:
    key = (sidebar_key or os.getenv("GROQ_API_KEY", "")).strip()
    if key:
        os.environ["GROQ_API_KEY"] = key
    return key


def render_sidebar():
    st.sidebar.header("Session")
    api_key = st.sidebar.text_input(
        "Groq API key",
        value="",
        type="password",
        help="Uses GROQ_API_KEY from the environment if left blank.",
    )
    model = st.sidebar.selectbox(
        "Model",
        [DEFAULT_MODEL, CHEAP_MODEL],
        index=0,
        help="Strict JSON structured output is enabled for openai/gpt-oss-* models.",
    )
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
    max_rounds = st.sidebar.slider("Debate rounds", 1, 2, MAX_ROUNDS)
    mode = st.sidebar.radio(
        "Run mode",
        (
            "Host-routed tank (2 rounds)",
            "Concurrent first looks",
        ),
        help="The tank is the Session 09 router. Concurrent mode is a cheaper first-round only.",
    )
    st.sidebar.caption(
        f"{len(SHARKS)} sharks × {max_rounds} round(s) = "
        f"{len(SHARKS) * max_rounds} specialist calls, plus the host wrap-up."
    )
    return api_key, model, temperature, max_rounds, mode


def render_roster():
    st.subheader("The panel")
    st.dataframe(
        pd.DataFrame(
            [{"Shark": s.name, "Lens": s.title} for s in SHARKS],
        ),
        hide_index=True,
        width="stretch",
    )


def render_verdict_section(title: str, verdicts: List[Verdict]):
    st.subheader(title)
    if not verdicts:
        st.info("No verdicts yet.")
        return
    left, right = st.columns([1.4, 1])
    with left:
        st.dataframe(verdicts_frame(verdicts), hide_index=True, width="stretch")
    with right:
        st.pyplot(stance_chart(verdicts, title), clear_figure=True)


def run_tank(pitch: str, model: str, temperature: float, max_rounds: int) -> dict:
    room = build_room(model, temperature, max_rounds)
    recursion_limit = max_rounds * len(ORDER) * 2 + 8
    last = {
        "pitch": pitch,
        "round1": [],
        "final": [],
        "calls": 0,
        "turn": "",
        "summary": "",
    }
    status = st.status("Opening the tank…", expanded=True)
    for chunk in room.stream(
        {"pitch": pitch, "round1": [], "final": [], "calls": 0},
        config={"recursion_limit": recursion_limit},
    ):
        node = next(iter(chunk))
        last.update(chunk[node])
        if node == "host":
            turn = last.get("turn", "")
            if turn == "done":
                status.write("Host is wrapping the panel.")
            else:
                status.write(f"Host sent the pitch to **{turn}**.")
        else:
            calls = last.get("calls", 0)
            status.write(f"**{node}** voted ({calls} specialist call(s) so far).")
    status.update(label="Panel complete", state="complete")
    expected_calls = max_rounds * len(ORDER)
    if last.get("calls") != expected_calls:
        st.warning(
            f"Expected {expected_calls} specialist calls; got {last.get('calls')}."
        )
    return last


def run_concurrent(pitch: str, model: str, temperature: float) -> tuple[list[Verdict], float]:
    started = time.perf_counter()

    async def _gather():
        return await asyncio.gather(
            *[evaluate_async(s, pitch, model, temperature) for s in SHARKS]
        )

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        verdicts = asyncio.run(_gather())
    else:
        # Streamlit may already own an event loop; isolate asyncio.run.
        from concurrent.futures import ThreadPoolExecutor

        with ThreadPoolExecutor(max_workers=1) as pool:
            verdicts = pool.submit(asyncio.run, _gather()).result()

    elapsed = round(time.perf_counter() - started, 3)
    return list(verdicts), elapsed


def main():
    st.title("SharkAI")
    st.caption("Pitch to the AI Sharks — host-routed panel with independent specialist lenses.")

    api_key, model, temperature, max_rounds, mode = render_sidebar()
    if not ensure_api_key(api_key):
        st.warning("Add a Groq API key in the sidebar or set GROQ_API_KEY, then rerun.")
        st.stop()

    render_roster()
    pitch = st.text_area("Startup pitch", value=SAMPLE_PITCH, height=260)
    run = st.button("Pitch to the sharks", type="primary", disabled=not pitch.strip())

    if run:
        try:
            if mode.startswith("Host-routed"):
                st.session_state.result = {
                    "mode": "tank",
                    "data": run_tank(pitch.strip(), model, temperature, max_rounds),
                }
            else:
                with st.spinner("Sharks are reading the pitch in parallel…"):
                    verdicts, elapsed = run_concurrent(pitch.strip(), model, temperature)
                st.session_state.result = {
                    "mode": "concurrent",
                    "data": {"verdicts": verdicts, "elapsed": elapsed},
                }
        except Exception as exc:
            st.session_state.result = None
            st.error(f"The panel could not finish: {exc}")

    result = st.session_state.get("result")
    if not result:
        return

    if result["mode"] == "tank":
        data = result["data"]
        invest = sum(
            1 for v in data.get("final", []) if str(v.stance).upper().startswith("INVEST")
        )
        m1, m2, m3 = st.columns(3)
        m1.metric("Specialist calls", data.get("calls", 0))
        m2.metric("Final INVEST", invest)
        m3.metric("Final PASS", len(data.get("final", [])) - invest)
        if data.get("summary"):
            st.subheader("Host wrap-up")
            st.info(data["summary"])
        render_verdict_section("Round 1 — independent takes", data.get("round1", []))
        render_verdict_section("Final — after the debate", data.get("final", []))
        return

    data = result["data"]
    st.metric("Elapsed seconds", data["elapsed"])
    render_verdict_section("Concurrent first looks", data["verdicts"])


if __name__ == "__main__":
    main()
