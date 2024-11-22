from enum import Enum


class cshade(Enum):
    LIGHTEST = 0
    LIGHT = 1
    MEDIUM = 2
    DARK = 3
    DARKEST = 4


ROOT_DIR = "./Summative v2 test"

CONDITIONS = ["ActuatedBed", "NormalBed"]
DIRECTIONS = ["Right", "Up", "Left", "Down"]
PARTICIPANTS = list(range(1, 16 + 1))


Applications = ["Ecosphere", "FPS"]
EcosphereClips = ["Borneo", "RajaAmpat"]

Points = list(range(1, 5 + 1))


COLORS = {
    CONDITIONS[0]: {
        cshade.LIGHTEST: "#BECACA",
        cshade.LIGHT: "#AFC7C7",
        cshade.MEDIUM: "#90C1C1",
        cshade.DARK: "#71BBBB",
        cshade.DARKEST: "#52B4B4",
    },
    CONDITIONS[1]: {
        cshade.LIGHTEST: "#C7BFC4",
        cshade.LIGHT: "#D0B3BD",
        cshade.MEDIUM: "#D299AC",
        cshade.DARK: "#D57F9C",
        cshade.DARKEST: "#D7658B",
    },
}
