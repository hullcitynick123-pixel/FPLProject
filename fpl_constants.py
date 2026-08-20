# --- Manager to Team Name Mapping ---

MANAGER_TEAMS = {
    "Kirkman": "Squad",
    "Seargent": "Iraola Coaster",
    "Atkinson": "Kibosh FC",
    "Milner": "Milner's Maulers",
    "Conor": "Conor's Team",
    "Trapps": "Just Gimme de Ligt",
    "Robinson": "Sean's Long Staff",
    "Shaw": "Farke the Bus",
    "Browes": "Always Showtime",
    "Ryder": "Bad To The Bum",
}

# --- Transfer sheet row order (fixed) used to derive each gameweek's pick order ---
# The manager in position 0 gets 1st pick in Gameweek 1, the manager in position 1
# gets 1st pick in Gameweek 2, and so on, wrapping back to position 0 after Seargent.
TRANSFER_PICK_ORDER = [
    "Ryder",
    "Wilkinson",
    "Shaw",
    "Robinson",
    "Browes",
    "Atkinson",
    "Kirkman",
    "Trapps",
    "Milner",
    "Seargent",
]