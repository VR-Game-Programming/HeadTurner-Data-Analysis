RootDir = "./Summative"

Participants = list(range(1, 16 + 1))
Conditions = ["NormalBed", "ActuatedBed"]
Directions = ["Right", "Up", "Left", "Down"]
Applications = ["Ecosphere", "Archery"]
Points = list(range(1, 5 + 1))
EcosphereClips = ["EcosphereBorneo", "EcosphereRajaAmpat"]
Colors = ["#54bebe", "#d7658b"]
LikertColors = [
    ["#e5f6ff", "#82cfff", "#33b1ff", "#0072c3", "#003a6d"],
    ["#ffd7d9", "#ff8389", "#fa4d56", "#da1e28", "#750e13"],
]

RangeRadarChartAngleLabels = {
    "LR": [
        "Right 90",
        "Right 60",
        "Right 30",
        "Front",
        "Left 30",
        "Left 60",
        "Left 90",
        "Left 120",
        "Left 150",
        "Back",
        "Right 150",
        "Right 120",
    ],
    "UD": [
        "Front",
        "Up 30",
        "Up 60",
        "Up 90",
        "Up 120",
        "Up 150",
        "Back",
        "Down 150",
        "Down 120",
        "Down 90",
        "Down 60",
        "Down 30",
    ],
}


def ColorText(text, color):
    if color == "green":
        return f"\033[92m{text}\033[0m"
    elif color == "yellow":
        return f"\033[93m{text}\033[0m"
    elif color == "red":
        return f"\033[91m{text}\033[0m"
    else:
        return text
