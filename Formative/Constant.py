RootDir = "./Formative"

Participants = list(range(1, 16 + 1))
Postures = ["Standing", "Lying"]
Directions_num = ["0", "45", "90", "135", "180", "225", "270", "315"]
Directions = [
    "Right",
    "UpRight",
    "Up",
    "UpLeft",
    "Left",
    "DownLeft",
    "Down",
    "DownRight",
]
DirectionDict = {
    "0": "Right",
    "45": "UpRight",
    "90": "Up",
    "135": "UpLeft",
    "180": "Left",
    "225": "DownLeft",
    "270": "Down",
    "315": "DownRight",
}
Angles = ["HeadYaw", "HeadPitch", "TrunkYaw", "TrunkPitch"]

Colors = ["#52B4B4", "#d7658b"]
Colors_Alpha = ["#52B4B416", "#d7658b16"]

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
