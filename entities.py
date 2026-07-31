"""Ghost Squad: Vessel — константы и настройки игры."""

TILE = 28                # размер тайла в пикселях
COLS_VISIBLE = 24        # сколько тайлов видно по горизонтали (окно камеры)
ROWS = 12                # высота уровня в тайлах (фиксированная для всех уровней)
SCREEN_W = TILE * COLS_VISIBLE
UI_HEIGHT = 72
SCREEN_H = TILE * ROWS + UI_HEIGHT
FPS = 60

GRAVITY = 0.55
MAX_FALL_SPEED = 15

TOTAL_LEVELS = 30
BOSS_LEVELS = (10, 20, 30)

# --- палитра (пиксель-арт, ограниченная палитра) ---
BLACK = (10, 10, 14)
BG_TOP = (18, 14, 30)
BG_BOTTOM = (46, 24, 52)
WALL = (74, 60, 90)
WALL_EDGE = (104, 88, 128)
BREAKABLE = (124, 74, 62)
BREAKABLE_CRACK = (60, 30, 26)
SPIKE = (210, 46, 64)
SPIKE_DARK = (140, 20, 40)
DOOR = (250, 210, 90)
DOOR_GLOW = (255, 240, 175)
GIANT_COLOR = (156, 134, 112)
GIANT_DARK = (104, 86, 70)
MAGE_COLOR = (154, 92, 224)
MAGE_DARK = (100, 50, 172)
ROGUE_COLOR = (92, 204, 124)
ROGUE_DARK = (50, 142, 82)
GHOST_GLOW = (200, 240, 255)
ENEMY_COLOR = (224, 62, 62)
ENEMY_DARK = (142, 30, 30)
BOSS_COLOR = (232, 32, 142)
BOSS_DARK = (142, 12, 92)
BOSS_ACCENT = (255, 200, 60)
CORPSE_TINT = (46, 46, 54)
TEXT_COLOR = (240, 240, 250)
TEXT_DIM = (160, 160, 178)
UI_BG = (16, 12, 22)
WHITE = (255, 255, 255)
GOLD = (250, 210, 90)

# --- ввод (можно переназначить) ---
KEY_LEFT = "left"
KEY_RIGHT = "right"
KEY_JUMP = "jump"
KEY_DOWN = "down"
KEY_PREV_BODY = "prev_body"
KEY_NEXT_BODY = "next_body"
KEY_ACTION = "action"
KEY_RESTART = "restart"