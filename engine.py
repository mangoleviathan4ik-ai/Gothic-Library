"""
Уровни игры.

Легенда тайлов:
  '#'  твёрдая стена/пол
  '~'  хрупкая стена (ломается только Гигантом)
  '^'  шипы (мгновенная смерть активного тела -> рестарт уровня)
  '.'  пусто
  'G' 'M' 'R'  точки старта Гиганта / Волшебницы / Плута
  'E'  точка спавна врага-патруля
  'B'  точка спавна босса
  'D'  дверь (конец уровня)

Уровни 1-9   — написаны вручную, учат по одной механике за раз.
Уровни 10/20/30 — боссы (тоже вручную).
Остальные (11-19, 21-29) — генерируются процедурно из проверенных
"сегментов", поэтому гарантированно проходимы, но каждый раз разные
(зависят от номера уровня, а не от случайного сида — чтобы уровень
всегда выглядел одинаково при повторном заходе).
"""

import random
import pygame
from . import constants as C


# ------------------------------------------------------------------
# Builder — удобный конструктор сетки уровня
# ------------------------------------------------------------------

class Builder:
    def __init__(self, width, height=C.ROWS):
        self.w = width
        self.h = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]

    def rect(self, x0, y0, x1, y1, ch='#'):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if 0 <= x < self.w and 0 <= y < self.h:
                    self.grid[y][x] = ch

    def set(self, x, y, ch):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.grid[y][x] = ch

    def floor(self, x0, x1, y=None, ch='#'):
        y = self.h - 1 if y is None else y
        self.rect(x0, y, x1, y, ch)

    def rows(self):
        return [''.join(r) for r in self.grid]


GROUND_ROW = C.ROWS - 1  # нижний ряд тайлов = земля по умолчанию


# ------------------------------------------------------------------
# Level — разобранная и готовая к игре карта
# ------------------------------------------------------------------

class Level:
    def __init__(self, rows, number, boss_info=None, title=""):
        self.number = number
        self.title = title
        self.grid = [list(r) for r in rows]
        self.height = len(self.grid)
        self.width = max(len(r) for r in self.grid)
        for r in self.grid:  # выравниваем длину строк
            while len(r) < self.width:
                r.append('.')
        self.spawns = {}
        self.enemy_spawns = []
        self.boss_spawn = None
        self.door_rect = None
        self.boss_info = boss_info  # (hp, name) или None
        self._parse()

    def _parse(self):
        kind_map = {"G": "giant", "M": "mage", "R": "rogue"}
        for row in range(self.height):
            for col in range(self.width):
                ch = self.grid[row][col]
                if ch in kind_map:
                    self.spawns[kind_map[ch]] = (col, row)
                    self.grid[row][col] = '.'
                elif ch == 'D':
                    self.door_rect = pygame.Rect(col * C.TILE, row * C.TILE, C.TILE, C.TILE)
                    self.grid[row][col] = '.'
                elif ch == 'E':
                    self.enemy_spawns.append((col, row))
                    self.grid[row][col] = '.'
                elif ch == 'B':
                    self.boss_spawn = (col, row)
                    self.grid[row][col] = '.'

    def tile_at(self, col, row):
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return '.'

    def is_solid(self, col, row):
        if col < 0 or col >= self.width:
            return True
        if row < 0 or row >= self.height:
            return False
        return self.grid[row][col] in ('#', '~')

    def smash(self, rect):
        c0 = max(0, rect.left // C.TILE)
        c1 = min(self.width - 1, rect.right // C.TILE)
        r0 = max(0, rect.top // C.TILE)
        r1 = min(self.height - 1, rect.bottom // C.TILE)
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if self.grid[r][c] == '~':
                    self.grid[r][c] = '.'

    def pixel_width(self):
        return self.width * C.TILE

    def pixel_height(self):
        return self.height * C.TILE

    def spawn_point(self, kind, body_w, body_h):
        """Пиксельные координаты (x, y) для тела kind, стоящего на тайле спавна."""
        col, row = self.spawns[kind]
        x = col * C.TILE + (C.TILE - body_w) / 2
        y = (row + 1) * C.TILE - body_h
        return x, y


# ------------------------------------------------------------------
# Ручные уровни 1-9 — обучение механикам
# ------------------------------------------------------------------

def level_1():
    """Учит: движение, прыжок, переключение тела (Z/X) — узкий лаз только для Плута."""
    b = Builder(24)
    b.floor(0, 23)
    b.set(2, GROUND_ROW - 1, 'G')
    b.set(4, GROUND_ROW - 1, 'M')
    b.set(6, GROUND_ROW - 1, 'R')
    # низкий лаз: потолок на всю ширину прохода, кроме одного ряда над полом
    b.rect(10, GROUND_ROW - 2, 15, GROUND_ROW - 2, '#')
    b.set(20, GROUND_ROW - 1, 'D')
    return Level(b.rows(), 1, title="Первые шаги")


def level_2():
    """Учит левитацию Волшебницы над пропастью, и обычный прыжок Плута/Гиганта по краю."""
    b = Builder(26)
    b.floor(0, 8)
    b.floor(18, 25)
    # пропасть с шипами на дне
    b.rect(9, GROUND_ROW, 17, GROUND_ROW, '^')
    # пара опорных платформ для тех, кто не умеет левитировать
    b.set(11, GROUND_ROW - 3, '#')
    b.set(12, GROUND_ROW - 3, '#')
    b.set(15, GROUND_ROW - 3, '#')
    b.set(16, GROUND_ROW - 3, '#')
    b.set(2, GROUND_ROW - 1, 'G')
    b.set(4, GROUND_ROW - 1, 'M')
    b.set(6, GROUND_ROW - 1, 'R')
    b.set(22, GROUND_ROW - 1, 'D')
    return Level(b.rows(), 2, title="Пропасть шипов")


def level_3():
    """Учит: Гигант ломает хрупкую стену действием (C)."""
    b = Builder(22)
    b.floor(0, 21)
    b.rect(11, GROUND_ROW - 3, 11, GROUND_ROW - 1, '~')
    b.set(2, GROUND_ROW - 1, 'G')
    b.set(4, GROUND_ROW - 1, 'M')
    b.set(6, GROUND_ROW - 1, 'R')
    b.set(18, GROUND_ROW - 1, 'D')
    return Level(b.rows(), 3, title="Крушить стены")


def level_4():
    """Учит: маленькие тела забираются на Гиганта, чтобы достать высокий уступ."""
    b = Builder(24)
    b.floor(0, 23)
    b.rect(12, GROUND_ROW - 5, 23, GROUND_ROW - 5, '#')  # высокий уступ с дверью
    b.rect(12, GROUND_ROW - 4, 12, GROUND_ROW - 1, '#')  # стена под уступом
    b.set(2, GROUND_ROW - 1, 'G')
    b.set(4, GROUND_ROW - 1, 'M')
    b.set(6, GROUND_ROW - 1, 'R')
    b.set(20, GROUND_ROW - 6, 'D')
    return Level(b.rows(), 4, title="Плечи великана")


def level_5():
    """Учит: враги — убиваются действием любого тела."""
    b = Builder(24)
    b.floor(0, 23)
    b.set(2, GROUND_ROW - 1, 'G')
    b.set(4, GROUND_ROW - 1, 'M')
    b.set(6, GROUND_ROW - 1, 'R')
    b.set(13, GROUND_ROW - 1, 'E')
    b.set(20, GROUND_ROW - 1, 'D')
    return Level(b.rows(), 5, title="Первая кровь")


def level_6():
    """Комбо: лаз + шипы + враг."""
    b = Builder(30)
    b.floor(0, 29)
    b.rect(8, GROUND_ROW - 2, 12, GROUND_ROW - 2, '#')  # лаз для плута
    b.rect(15, GROUND_ROW, 19, GROUND_ROW, '^')
    b.set(16, GROUND_ROW - 3, '#')
    b.set(17, GROUND_ROW - 3, '#')
    b.set(24, GROUND_ROW - 1, 'E')
    b.set(2, GROUND_ROW - 1, 'G')
    b.set(4, GROUND_ROW - 1, 'M')
    b.set(6, GROUND_ROW - 1, 'R')
    b.set(27, GROUND_ROW - 1, 'D')
    return Level(b.rows(), 6, title="Три преграды")


def level_7():
    """Вертикальная шахта: Гигант — ступень для остальных, наверху шипы понизу."""
    b = Builder(20)
    b.floor(0, 19)
    b.rect(9, GROUND_ROW - 6, 19, GROUND_ROW - 6, '#')
    b.rect(9, GROUND_ROW - 6, 9, GROUND_ROW - 1, '#')
    b.set(2, GROUND_ROW - 1, 'G')
    b.set(4, GROUND_ROW - 1, 'M')
    b.set(6, GROUND_ROW - 1, 'R')
    b.set(16, GROUND_ROW - 7, 'D')
    b.set(14, GROUND_ROW - 1, 'E')
    return Level(b.rows(), 7, title="Шахта")


def level_8():
    """Комбо: стена + пропасть + лаз друг за другом."""
    b = Builder(34)
    b.floor(0, 33)
    b.rect(9, GROUND_ROW - 3, 9, GROUND_ROW - 1, '~')
    b.rect(14, GROUND_ROW, 18, GROUND_ROW, '^')
    b.set(15, GROUND_ROW - 3, '#')
    b.set(16, GROUND_ROW - 3, '#')
    b.rect(22, GROUND_ROW - 2, 27, GROUND_ROW - 2, '#')
    b.set(30, GROUND_ROW - 1, 'E')
    b.set(2, GROUND_ROW - 1, 'G')
    b.set(4, GROUND_ROW - 1, 'M')
    b.set(6, GROUND_ROW - 1, 'R')
    b.set(31, GROUND_ROW - 1, 'D')
    return Level(b.rows(), 8, title="Три испытания")


def level_9():
    """Уровень перед первым боссом — длинный гаунтлет из всего пройденного."""
    b = Builder(40)
    b.floor(0, 39)
    b.rect(8, GROUND_ROW - 3, 8, GROUND_ROW - 1, '~')
    b.rect(12, GROUND_ROW - 2, 16, GROUND_ROW - 2, '#')
    b.rect(20, GROUND_ROW, 24, GROUND_ROW, '^')
    b.set(21, GROUND_ROW - 3, '#')
    b.set(23, GROUND_ROW - 3, '#')
    b.set(18, GROUND_ROW - 1, 'E')
    b.set(30, GROUND_ROW - 1, 'E')
    b.rect(33, GROUND_ROW - 5, 39, GROUND_ROW - 5, '#')
    b.rect(33, GROUND_ROW - 4, 33, GROUND_ROW - 1, '#')
    b.set(2, GROUND_ROW - 1, 'G')
    b.set(4, GROUND_ROW - 1, 'M')
    b.set(6, GROUND_ROW - 1, 'R')
    b.set(37, GROUND_ROW - 6, 'D')
    return Level(b.rows(), 9, title="Перед вратами")


HAND_LEVELS = {1: level_1, 2: level_2, 3: level_3, 4: level_4, 5: level_5,
               6: level_6, 7: level_7, 8: level_8, 9: level_9}


# ------------------------------------------------------------------
# Боссы: 10, 20, 30
# ------------------------------------------------------------------

def boss_arena(number, hp, name):
    b = Builder(26)
    b.floor(0, 25)
    b.rect(0, 0, 0, GROUND_ROW, '#')
    b.rect(25, 0, 25, GROUND_ROW, '#')
    b.set(2, GROUND_ROW - 1, 'G')
    b.set(4, GROUND_ROW - 1, 'M')
    b.set(6, GROUND_ROW - 1, 'R')
    b.set(20, GROUND_ROW - 2, 'B')
    b.set(22, GROUND_ROW - 1, 'D')  # дверь открывается за боссом (симв. награда)
    return Level(b.rows(), number, boss_info=(hp, name), title=name)


BOSS_DEFS = {
    10: lambda: boss_arena(10, 30, "Курган, Страж Костей"),
    20: lambda: boss_arena(20, 55, "Мать Пустоты"),
    30: lambda: boss_arena(30, 85, "Король-под-Землёй"),
}


# ------------------------------------------------------------------
# Процедурная генерация уровней 11-19 / 21-29
# ------------------------------------------------------------------

SEG_W = 12


def seg_start():
    b = Builder(SEG_W)
    b.floor(0, SEG_W - 1)
    b.set(2, GROUND_ROW - 1, 'G')
    b.set(4, GROUND_ROW - 1, 'M')
    b.set(6, GROUND_ROW - 1, 'R')
    return b.grid


def seg_end():
    b = Builder(SEG_W)
    b.floor(0, SEG_W - 1)
    b.set(SEG_W - 3, GROUND_ROW - 1, 'D')
    return b.grid


def seg_flat(rng, with_enemy):
    b = Builder(SEG_W)
    b.floor(0, SEG_W - 1)
    if with_enemy:
        b.set(rng.randint(4, SEG_W - 4), GROUND_ROW - 1, 'E')
    return b.grid


def seg_gap(rng):
    b = Builder(SEG_W)
    gap = rng.randint(2, 3)
    start = rng.randint(2, SEG_W - gap - 2)
    b.floor(0, start - 1)
    b.floor(start + gap, SEG_W - 1)
    return b.grid


def seg_spikes(rng):
    b = Builder(SEG_W)
    b.floor(0, 1)
    b.floor(SEG_W - 2, SEG_W - 1)
    b.rect(2, GROUND_ROW, SEG_W - 3, GROUND_ROW, '^')
    mid = SEG_W // 2
    b.set(mid - 1, GROUND_ROW - 3, '#')
    b.set(mid, GROUND_ROW - 3, '#')
    return b.grid


def seg_gate_wall(rng):
    """Хрупкая стена — требует Гиганта, но после разрушения проходима всем."""
    b = Builder(SEG_W)
    b.floor(0, SEG_W - 1)
    x = SEG_W // 2
    b.rect(x, GROUND_ROW - 3, x, GROUND_ROW - 1, '~')
    return b.grid


def seg_gate_tunnel(rng):
    """Низкий лаз — проходит только Плут (низкий рост)."""
    b = Builder(SEG_W)
    b.floor(0, SEG_W - 1)
    x0 = SEG_W // 2 - 2
    b.rect(x0, GROUND_ROW - 2, x0 + 3, GROUND_ROW - 2, '#')
    return b.grid


OPEN_SEGMENTS = [
    lambda rng: seg_flat(rng, False),
    lambda rng: seg_flat(rng, True),
    seg_gap,
    seg_spikes,
]
GATE_SEGMENTS = [seg_gate_wall, seg_gate_tunnel]


def paste(dst_builder, seg_grid, offset_col):
    for row in range(C.ROWS):
        for col in range(SEG_W):
            dst_builder.grid[row][offset_col + col] = seg_grid[row][col]


def generated_level(number):
    rng = random.Random(number * 7919 + 13)  # детерминированный сид по номеру уровня
    tier = number % 10  # 1..9 внутри десятка (10 сам босс, обрабатывается отдельно)
    n_open = 4 + tier // 2          # больше сегментов на поздних уровнях десятка
    n_open = max(3, min(n_open, 7))
    use_gate = rng.random() < 0.6 + tier * 0.03

    segments = [seg_start()]
    for _ in range(n_open):
        seg_fn = rng.choice(OPEN_SEGMENTS)
        segments.append(seg_fn(rng))
    if use_gate:
        segments.append(rng.choice(GATE_SEGMENTS)(rng))
    segments.append(seg_end())

    total_w = SEG_W * len(segments)
    b = Builder(total_w)
    for i, seg in enumerate(segments):
        paste(b, seg, i * SEG_W)

    return Level(b.rows(), number, title=f"Глубина {number}")


# ------------------------------------------------------------------
# Публичный доступ
# ------------------------------------------------------------------

def build_level(number):
    """Строит (заново) уровень по номеру. Вызывать при входе на уровень и при рестарте."""
    if number in BOSS_DEFS:
        return BOSS_DEFS[number]()
    if number in HAND_LEVELS:
        return HAND_LEVELS[number]()
    return generated_level(number)