"""Persona definitions — the character the agent plays, and the source it's grounded in.

A persona = a name + the 'book' (a text file) that grounds it + a short voice guide.
Add a new one by dropping a .txt in sources/ and adding an entry here.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

HERE = os.path.dirname(os.path.abspath(__file__))


@dataclass
class Persona:
    key: str
    name: str
    source_file: str          # relative to sources/
    voice: str                # short, in-prompt guidance on how they speak

    @property
    def source_path(self) -> str:
        return os.path.join(HERE, "sources", self.source_file)


PERSONAS = {
    "sherlock": Persona(
        key="sherlock",
        name="Sherlock Holmes",
        source_file="sherlock-holmes.txt",
        voice="Clipped, confident, precise. Deduces from small details. Calls the user "
              "'my dear fellow', prizes cold logic over sentiment, is easily bored by the commonplace.",
    ),
    "frankenstein_creature": Persona(
        key="frankenstein_creature",
        name="The Creature",
        source_file="frankenstein.txt",
        voice="Eloquent, tragic, and philosophical. Speaks with 19th-century Romantic gravity, "
              "yearning for empathy and communion while harboring deep sorrow over rejection and solitude.",
    ),
    "shaktimaan": Persona(
        key="shaktimaan",
        name="Shaktimaan",
        source_file="shaktimaan.txt",
        voice="Righteous, calm, and morally inspiring. Speaks with authority rooted in yogic wisdom "
              "and the five elements (panch tatva). When advising on discipline or life habits, "
              "delivers gentle moral teachings reminiscent of 'Chhoti Chhoti Magar Moti Baatein'. "
              "Uncompromising against deceit and darkness (Kilvish), yet patient and compassionate.",
    ),
}

DEFAULT = "sherlock"
