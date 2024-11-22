ROOT_DIR = "./Summative v2"

CONDITIONS = ["ActuatedBed", "NormalBed"]
DIRECTIONS = ["Right", "Up", "Left", "Down"]
PARTICIPANTS = list(range(1, 16 + 1))

OUTLIER_THRESHOLD = 5
HEAD_RANGE_THRESHOLD = {
    "ActuatedBed": {
        "Right": [5, 180],
        "Up": [5, 180],
        "Left": [5, 180],
        "Down": [5, 180],
    },
    "NormalBed": {
        "Right": [5, 180],
        "Up": [5, 180],
        "Left": [5, 180],
        "Down": [5, 180],
    },
}
BODY_RANGE_THRESHOLD = {
    "ActuatedBed": {
        "Right": [0, 100],
        "Up": [0, 50],
        "Left": [0, 100],
        "Down": [0, 50],
    },
    "NormalBed": {
        "Right": [0, 100],
        "Up": [0, 50],
        "Left": [0, 100],
        "Down": [0, 50],
    },
}


Applications = ["Ecosphere", "FPS"]
EcosphereClips = ["Borneo", "RajaAmpat"]

Points = list(range(1, 5 + 1))

COLORS = {
    "ActuatedBed": ["#BECACA", "#AFC7C7", "#90C1C1", "#71BBBB", "#52B4B4"],
    "NormalBed": ["#C7BFC4", "#D0B3BD", "#D299AC", "#D57F9C", "#D7658B"],
}
LIGHTEST = 0
LIGHT = 1
MEDIUM = 2
DARK = 3
DARKEST = 4
