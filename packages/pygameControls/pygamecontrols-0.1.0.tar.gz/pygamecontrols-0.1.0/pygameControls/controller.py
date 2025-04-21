import pygame
from .controlsbase import ControlsBase
from .dualsense_controller import DualSenseController
from .dualsense_edge_controller import DualSenseEdgeController
from .logitech_f310_controller import LogitechF310Controller
from .logitech_f510_controller import LogitechF510Controller
from .logitech_f710_controller import LogitechF710Controller
from .xbox_series_x_controller import XboxSeriesXController
from .generic_controller import GenericController
from .logitech_dual_action_controller import LogitechDualActionController

__version__ = "0.1.0"

CONTROLLERS = {
    "DualSense Wireless Controller": DualSenseController,
    "DualSense Edge Wireless Controller": DualSenseEdgeController,
    "Logitech Gamepad F310": LogitechF310Controller,
    "Logitech Gamepad F510": LogitechF510Controller,
    "Logitech Gamepad F710": LogitechF710Controller,
    "Logitech Dual Action": LogitechDualActionController,
    "X box Series X Controller": XboxSeriesXController
    }

class Controllers:
    def __init__(self, joy):
        self.controllers = []
        if not joy.get_name() in CONTROLLERS:
            self.controllers.append(GenericController(joy))
        else:
            self.controllers.append(CONTROLLERS[joy.get_name()](joy))
        