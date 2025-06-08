#Constants

# Generals
#------------------------------------------------------------------------
DEBUG = False

FRAMES = 60
CAPTION = "Fighter Game"
CENTER = (0, 0)
SCROLL_SPEED = 2
GRAVITY = 2
GROUND = 100
MIN_X = -200
REQUIRED_KILL_LEVEL = 5

#Entities
#------------------------------------------------------------------------

#Player
#------------------------------------------

PLAYER_OFFSET = [72, 56]
PLAYER_SCALE  = 4
JUMP_STRENGTH = -50
MAX_FALL_SPEED = 20
FAST_FALL_SPEED = 40
MOVE_SPEED = 5
FRAME_DURATION = 70

# Player position
PLAYER_X = MIN_X + 400
PLAYER_Y = 100
PLAYER_SIZE = 162

# Player rect
PLAYER_RECT_W = 94
PLAYER_RECT_H = 174
PLAYER_ATK_RECT_W = 100
# PLAYER_ATK_RECT_H = 100


# Enemies
#------------------------------------------
ENEMY_OFFSCREEN = 500
ENEMY_OFFSET_RANDOM = 100
ENEMY_MAXIMUM_VELOCITY = 30
ENEMY_MINIMUM_VELOCITY = 5
ENEMY_BASE_VELOCITY = 4

ENEMY_DEFAULT_SCORE = 1

# Wizard
#----------------------
WIZARD_SIZE   = 250
WIZARD_SCALE  = 3

# Move the Box
WIZARD_OFFSET = [300, 320]

# Screen Start
WIZARD_X = 1200
WIZARD_Y = 520

# Size of the Box
WIZARD_RECT_W = 180
WIZARD_RECT_H = 180


# Pig
#----------------------
PIG_SIZE   = (100, 100)
PIG_SCALE  = 3
PIG_SCORE  = 5

# Move the Box
PIG_OFFSET = [10, 10]

# Screen Start
PIG_X = 1600
PIG_Y = 30

# Size of the Box
PIG_RECT_W = 80
PIG_RECT_H = 80


#Frames
PLAYER_PER_ACTION = [10, 8, 1, 7, 7, 3, 7]
WIZARD_PER_ACTION = [8, 8, 1, 8, 8, 3, 7]


# States
#------------------------------------------------------------------------

#MainMenu
#------------------------------------------

MM_FONT_SIZE = 74
MM_TITLE = "Main Menu"
MM_OPTIONS = ["Start Game", "Instructions", "Quit"]
MM_Y_OFFSET = 50
MM_OPTIONS_Y_OFFSET = 150
MM_OPTIONS_DISTANCE = 60

#Instructions
#------------------------------------------
INST_FONT_SIZE     = 80
INST_MARGIN_X      = 50
INST_MARGIN_Y      = 50
INST_LINE_SPACING  = 100

INSTRUCTION_LINES = [
    "Instructions:",
    "ALI ZAVARI GAME DEVELOP",
    "Use arrow keys to move the character.",
    "Avoid the wizard and the pig.",
    "Press A and D to Attack.",
    "pig +5, wizard +1",
]

# Playing
#------------------------------------------
LEVEL_FONT_SIZE = 24
LEVEL_MARGIN_X = 10

# Game Over
#------------------------------------------


#------------------------------------------------------------------------
# Record
# File & size defaults
DEFAULT_RECORD_PATH = "records.json"
DEFAULT_MAX_RECORDS = 10


#------------------------------------------------------------------------
#Colors

WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
BLACK = (0, 0, 0)


#------------------------------------------------------------------------
# Encoding
UTF_8 = "utf-8"


#------------------------------------------------------------------------
# Fonts
ARIAL = "Arial"
