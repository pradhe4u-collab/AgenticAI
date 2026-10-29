"""Baked-in SAMPLE data for Dream11 Genie.

Illustrative sample data for multiple fixtures (CSK vs MI, CSK vs RCB) so the
project runs offline and deterministically — no third-party sports API needed.
The tool functions in tools.py read from here.
"""

VENUE = "MA Chidambaram Stadium, Chepauk"

# --- Pitch & conditions for the venue -------------------------------------
PITCH = {
    "MA Chidambaram Stadium, Chepauk": {
        "venue": "MA Chidambaram Stadium, Chepauk",
        "surface": "Dry, spin-friendly; grips and turns as the game wears on",
        "avg_first_innings": 165,
        "pace_vs_spin": "Spinners dominate; wrist-spin especially effective",
        "dew": "Light dew after 8:30 PM — a small edge to the chasing side",
        "recommendation": "Load up on quality spinners and in-form top-order batters; "
                          "medium-pace/cutters do better than express seam.",
    }
}

# --- Team form / news blurbs ----------------------------------------------
FORM = {
    "CSK": "CSK are in good rhythm at home. Ruturaj Gaikwad is in sublime touch at the top. "
           "Ravindra Jadeja provides key middle-overs spin and late balance. Matheesha Pathirana "
           "is sharp at the death, while Moeen Ali and Theekshana thrive on Chepauk's dry deck.",
    "MI": "MI are batting-heavy and explosive. Suryakumar Yadav is in red-hot form. "
          "Jasprit Bumrah is near-unplayable across all phases. Rohit Sharma has had mixed starts. "
          "Their spin depth remains thinner on sharp-turning tracks.",
    "RCB": "RCB lean heavily on their top-order engine. Virat Kohli is anchoring and scoring consistently. "
           "Faf du Plessis and Cameron Green offer aggressive intent, but spin attack depth "
           "remains a challenge on slow, turning surfaces away from Chinnaswamy.",
}

# --- Fixtures -------------------------------------------------------------
SQUADS = {
    "CSK vs MI": {
        "venue": VENUE,
        "teams": {"CSK": [], "MI": []},
    },
    "CSK vs RCB": {
        "venue": VENUE,
        "teams": {"CSK": [], "RCB": []},
    },
}

# --- Players Database -----------------------------------------------------
# role: WK / BAT / AR / BOWL ; credits: Dream11-style 7.0-11.0
PLAYERS = {
    # ---------------- CSK ----------------
    "Ruturaj Gaikwad": {"team": "CSK", "role": "BAT", "credits": 10.5, "recent": [92, 46, 71, 58, 27],
                        "batting_avg": 48.2, "strike_rate": 141, "avg_fantasy_points": 78,
                        "note": "In-form opener; anchors and accelerates. Strong captaincy pick."},
    "MS Dhoni": {"team": "CSK", "role": "WK", "credits": 9.0, "recent": [20, 14, 9, 27, 4],
                 "batting_avg": 22.0, "strike_rate": 190, "avg_fantasy_points": 34,
                 "note": "Bats only a few overs now but explosive finisher + keeper points."},
    "Devon Conway": {"team": "CSK", "role": "BAT", "credits": 9.5, "recent": [8, 56, 40, 12, 63],
                     "batting_avg": 41.0, "strike_rate": 139, "avg_fantasy_points": 58,
                     "note": "Reliable left-hand opener; can also keep."},
    "Shivam Dube": {"team": "CSK", "role": "AR", "credits": 9.0, "recent": [51, 34, 66, 8, 39],
                    "batting_avg": 38.5, "strike_rate": 162, "avg_fantasy_points": 61,
                    "note": "Powerful middle-order hitter vs spin; bowls occasional seam."},
    "Ravindra Jadeja": {"team": "CSK", "role": "AR", "credits": 9.5, "recent": [37, 24, 18, 41, 29],
                        "batting_avg": 30.0, "strike_rate": 148, "avg_fantasy_points": 72,
                        "note": "Genuine all-rounder; left-arm spin ideal for Chepauk + fielding points."},
    "Moeen Ali": {"team": "CSK", "role": "AR", "credits": 8.5, "recent": [12, 28, 3, 44, 19],
                  "batting_avg": 24.0, "strike_rate": 155, "avg_fantasy_points": 49,
                  "note": "Off-spin all-rounder; exploits turn on this deck."},
    "Deepak Chahar": {"team": "CSK", "role": "BOWL", "credits": 8.5, "recent": [2, 1, 3, 0, 2],
                      "bowling_econ": 8.1, "avg_fantasy_points": 47,
                      "note": "New-ball swing; wicket threat in the powerplay."},
    "Matheesha Pathirana": {"team": "CSK", "role": "BOWL", "credits": 9.0, "recent": [3, 2, 4, 1, 3],
                            "bowling_econ": 7.8, "avg_fantasy_points": 66,
                            "note": "Slingy yorkers at the death; lethal wicket-taker."},
    "Maheesh Theekshana": {"team": "CSK", "role": "BOWL", "credits": 8.5, "recent": [2, 3, 1, 2, 2],
                           "bowling_econ": 7.2, "avg_fantasy_points": 52,
                           "note": "Mystery spinner; tight and dangerous on turning tracks."},
    "Tushar Deshpande": {"team": "CSK", "role": "BOWL", "credits": 8.0, "recent": [1, 2, 0, 3, 1],
                         "bowling_econ": 9.4, "avg_fantasy_points": 40,
                         "note": "Hit-the-deck seamer; effective middle overs."},
    "Ajinkya Rahane": {"team": "CSK", "role": "BAT", "credits": 8.0, "recent": [29, 45, 11, 33, 7],
                       "batting_avg": 27.0, "strike_rate": 140, "avg_fantasy_points": 42,
                       "note": "Experienced No. 3; solid technical player."},
    "Daryl Mitchell": {"team": "CSK", "role": "AR", "credits": 8.5, "recent": [22, 39, 63, 17, 30],
                       "batting_avg": 35.0, "strike_rate": 138, "avg_fantasy_points": 50,
                       "note": "Middle-order stabilizer; handy seam option."},

    # ---------------- MI ----------------
    "Rohit Sharma": {"team": "MI", "role": "BAT", "credits": 10.0, "recent": [11, 43, 8, 26, 5],
                     "batting_avg": 24.5, "strike_rate": 148, "avg_fantasy_points": 44,
                     "note": "Match-winner on his day but has had mixed recent returns."},
    "Ishan Kishan": {"team": "MI", "role": "WK", "credits": 9.0, "recent": [42, 69, 18, 33, 55],
                     "batting_avg": 39.0, "strike_rate": 152, "avg_fantasy_points": 62,
                     "note": "Aggressive keeper-bat opener; keeper dismissal upside."},
    "Suryakumar Yadav": {"team": "MI", "role": "BAT", "credits": 10.5, "recent": [78, 43, 102, 31, 65],
                         "batting_avg": 52.0, "strike_rate": 176, "avg_fantasy_points": 88,
                         "note": "Sensational form; elite multiplier candidate."},
    "Tilak Varma": {"team": "MI", "role": "AR", "credits": 9.0, "recent": [46, 32, 57, 21, 40],
                    "batting_avg": 40.0, "strike_rate": 150, "avg_fantasy_points": 56,
                    "note": "Left-hander who plays spin well; part-time off-break."},
    "Hardik Pandya": {"team": "MI", "role": "AR", "credits": 9.5, "recent": [28, 19, 44, 33, 12],
                      "batting_avg": 28.0, "strike_rate": 145, "avg_fantasy_points": 58,
                      "note": "High points floor with death batting and seam bowling."},
    "Tim David": {"team": "MI", "role": "AR", "credits": 8.5, "recent": [37, 8, 46, 22, 30],
                  "batting_avg": 31.0, "strike_rate": 168, "avg_fantasy_points": 47,
                  "note": "Lower-order finisher."},
    "Jasprit Bumrah": {"team": "MI", "role": "BOWL", "credits": 9.5, "recent": [3, 4, 2, 3, 4],
                       "bowling_econ": 6.4, "avg_fantasy_points": 82,
                       "note": "Elite wicket-taker and miserly economy; premium bowler pick."},
    "Piyush Chawla": {"team": "MI", "role": "BOWL", "credits": 8.0, "recent": [2, 1, 3, 1, 2],
                      "bowling_econ": 7.9, "avg_fantasy_points": 45,
                      "note": "Leg-spin control; useful on grip surfaces."},
    "Gerald Coetzee": {"team": "MI", "role": "BOWL", "credits": 8.5, "recent": [2, 3, 1, 2, 1],
                       "bowling_econ": 9.1, "avg_fantasy_points": 43,
                       "note": "High pace and bounce."},
    "Nuwan Thushara": {"team": "MI", "role": "BOWL", "credits": 8.0, "recent": [3, 1, 2, 2, 0],
                       "bowling_econ": 8.6, "avg_fantasy_points": 41,
                       "note": "Slingy angle; early breakthroughs."},
    "Dewald Brevis": {"team": "MI", "role": "BAT", "credits": 8.0, "recent": [17, 46, 25, 8, 39],
                      "batting_avg": 27.0, "strike_rate": 158, "avg_fantasy_points": 44,
                      "note": "Aggressive spin attacker."},
    "Naman Dhir": {"team": "MI", "role": "AR", "credits": 7.5, "recent": [24, 12, 33, 9, 20],
                   "batting_avg": 22.0, "strike_rate": 149, "avg_fantasy_points": 36,
                   "note": "Flexible batting option with part-time overs."},

    # ---------------- RCB ----------------
    "Virat Kohli": {"team": "RCB", "role": "BAT", "credits": 10.5, "recent": [83, 77, 51, 67, 42],
                    "batting_avg": 54.0, "strike_rate": 147, "avg_fantasy_points": 84,
                    "note": "High-volume run-scorer and reliable anchor. Default multiplier option."},
    "Faf du Plessis": {"team": "RCB", "role": "BAT", "credits": 9.5, "recent": [35, 62, 19, 44, 56],
                       "batting_avg": 36.2, "strike_rate": 154, "avg_fantasy_points": 60,
                       "note": "Powerplay boundary hitter; high catch rate at long-off."},
    "Rajat Patidar": {"team": "RCB", "role": "BAT", "credits": 8.5, "recent": [52, 23, 48, 12, 50],
                      "batting_avg": 32.5, "strike_rate": 172, "avg_fantasy_points": 54,
                      "note": "Elite boundary scorer against spin; vital at Chepauk."},
    "Glenn Maxwell": {"team": "RCB", "role": "AR", "credits": 9.0, "recent": [28, 4, 31, 0, 16],
                      "batting_avg": 26.0, "strike_rate": 160, "avg_fantasy_points": 52,
                      "note": "High-ceiling disruptor; off-spin will be active on a turner."},
    "Cameron Green": {"team": "RCB", "role": "AR", "credits": 9.0, "recent": [41, 18, 37, 25, 46],
                      "batting_avg": 34.0, "strike_rate": 148, "avg_fantasy_points": 64,
                      "note": "Top/middle-order hitting plus 2-4 overs of pace bowling."},
    "Dinesh Karthik": {"team": "RCB", "role": "WK", "credits": 8.5, "recent": [28, 38, 53, 14, 21],
                       "batting_avg": 31.0, "strike_rate": 182, "avg_fantasy_points": 48,
                       "note": "Death-over specialist with rapid scoring rates + keeping points."},
    "Anuj Rawat": {"team": "RCB", "role": "WK", "credits": 8.0, "recent": [48, 11, 21, 8, 3],
                   "batting_avg": 22.0, "strike_rate": 128, "avg_fantasy_points": 32,
                   "note": "Backup keeper-batter."},
    "Mahipal Lomror": {"team": "RCB", "role": "AR", "credits": 7.5, "recent": [33, 17, 0, 26, 19],
                       "batting_avg": 23.5, "strike_rate": 158, "avg_fantasy_points": 35,
                       "note": "Southpaw middle-order slogger."},
    "Mohammed Siraj": {"team": "RCB", "role": "BOWL", "credits": 9.0, "recent": [2, 1, 3, 1, 2],
                       "bowling_econ": 8.4, "avg_fantasy_points": 55,
                       "note": "Lead pace bowler; effective with new ball seam and swing."},
    "Yash Dayal": {"team": "RCB", "role": "BOWL", "credits": 8.0, "recent": [1, 2, 2, 0, 2],
                   "bowling_econ": 8.8, "avg_fantasy_points": 42,
                   "note": "Left-arm angle; mixes wide yorkers and slower deliveries."},
    "Karn Sharma": {"team": "RCB", "role": "BOWL", "credits": 8.0, "recent": [2, 1, 3, 1, 0],
                    "bowling_econ": 8.7, "avg_fantasy_points": 44,
                    "note": "Leg-spinner; essential attacking weapon on spinning tracks."},
    "Lockie Ferguson": {"team": "RCB", "role": "BOWL", "credits": 8.5, "recent": [2, 0, 2, 3, 1],
                        "bowling_econ": 9.2, "avg_fantasy_points": 46,
                        "note": "Express speed; uses short balls and quick yorkers."},
}

# --- Dynamic squad population for all defined fixtures -------------------
for fixture, data in SQUADS.items():
    team_keys = list(data["teams"].keys())
    for player_name, player_info in PLAYERS.items():
        if player_info["team"] in team_keys:
            data["teams"][player_info["team"]].append(player_name)