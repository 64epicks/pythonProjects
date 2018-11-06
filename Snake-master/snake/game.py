#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0111,W0201,W0703

import errno
import os
import traceback
from enum import Enum, unique

from snake.base import Direc, Map, PointType, Pos, Snake
from snake.gui import GameWindow
from snake.solver import DQNSolver, GreedySolver, HamiltonSolver


@unique
class GameMode(Enum):
    NORMAL = 0         # AI with GUI
    BENCHMARK = 1      # Run benchmarks without GUI
    TRAIN_DQN = 2      # Train DQNSolver without GUI
    TRAIN_DQN_GUI = 3  # Train DQNSolver with GUI


class GameConf:

    def __init__(self):
        """Initialize a default configuration."""

        # Game mode
        self.mode = GameMode.NORMAL

        # Solver
        self.solver_name = 'HamiltonSolver'  # Class name of the solver

        # Size
        self.map_rows = 8
        self.map_cols = self.map_rows
        self.map_width = 160  # pixels
        self.map_height = self.map_width
        self.info_panel_width = 155  # pixels
        self.window_width = self.map_width + self.info_panel_width
        self.window_height = self.map_height
        self.grid_pad_ratio = 0.25

        # Switch
        self.show_grid_line = False
        self.show_info_panel = True

        # Delay
        self.interval_draw = 50       # ms
        self.interval_draw_max = 200  # ms

        # Color
        self.color_bg = '#000000'
        self.color_txt = '#F5F5F5'
        self.color_line = '#424242'
        self.color_wall = '#F5F5F5'
        self.color_food = '#FFF59D'
        self.color_head = '#F5F5F5'
        self.color_body = '#F5F5F5'

        # Initial snake
        self.init_direc = Direc.RIGHT
        self.init_bodies = [Pos(1, 4), Pos(1, 3), Pos(1, 2), Pos(1, 1)]
        self.init_types = [PointType.HEAD_R] + [PointType.BODY_HOR] * 3

        # Font
        self.font_info = ('Arial', 9)

        # Info
        self.info_str = (
            "<w/a/s/d>: snake direction\n"
            "<space>: pause/resume\n"
            "<r>: restart    <esc>: exit\n"
            "-----------------------------------\n"
            "status: %s\n"
            "episode: %d   step: %d\n"
            "length: %d/%d (" + str(self.map_rows) + "x" + str(self.map_cols) + ")\n"
            "-----------------------------------"
        )
        self.info_status = ['eating', 'dead', 'full']

class Game:

    def __init__(self, conf):
        self._conf = conf
        self._map = Map(conf.map_rows + 2, conf.map_cols + 2)
        self._snake = Snake(self._map, conf.init_direc,
                            conf.init_bodies, conf.init_types)
        self._pause = False
        self._solver = globals()[self._conf.solver_name](self._snake)
        self._episode = 1
        self._init_log_file()

    @property
    def snake(self):
        return self._snake

    @property
    def episode(self):
        return self._episode

    def run(self):
        window = GameWindow("Snake", self._conf, self._map, self, self._on_exit, (
            ('<w>', lambda e: self._update_direc(Direc.UP)),
            ('<a>', lambda e: self._update_direc(Direc.LEFT)),
            ('<s>', lambda e: self._update_direc(Direc.DOWN)),
            ('<d>', lambda e: self._update_direc(Direc.RIGHT)),
            ('<r>', lambda e: self._reset()),
            ('<space>', lambda e: self._toggle_pause())
        ))
    def _toggle_pause(self):
        self._pause = not self._pause