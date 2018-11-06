#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0111

import argparse

from snake.game import Game, GameConf, GameMode

conf = GameConf()
conf.solver_name = dict_solver[args.s]
conf.mode = dict_mode[args.m]
print("Solver: %s    Mode: %s" % (conf.solver_name, conf.mode))

Game(conf).run()
