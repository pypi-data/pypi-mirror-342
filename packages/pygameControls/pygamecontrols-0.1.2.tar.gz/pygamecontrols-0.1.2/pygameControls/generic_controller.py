import pygame
from pygameControls.controlsbase import ControlsBase
        
class GenericController(ControlsBase):
    def __init__(self, joy):
        self.device = joy
        self.instance_id: int = self.device.get_instance_id()
        self.name = self.device.get_name()
        self.guid = self.device.get_guid()
        self.numaxis: int = self.device.get_numaxes()
        self.axis: list = [self.device.get_axis(a) for a in range(self.numaxis)]
        self.numhats: int = self.device.get_numhats()
        self.hats: list = [self.device.get_hat(h) for h in range(self.numhats)]
        self.numbuttons: int = self.device.get_numbuttons()
        self.buttons: list = [self.device.get_button(b) for b in range(self.numbuttons)]
        self.mapping = {
            "left stick x": self.axis[0],
            "left stick y": self.axis[1],
            "right stick x": self.axis[2],
            "right stick y": self.axis[3],
            "right trigger": self.buttons[7],
            "left trigger": self.buttons[6],
            "dhat x": self.hats[0][0],
            "dhat y": self.hats[0][1],
            "left button": self.buttons[4],
            "right button": self.buttons[5],
            "X button": self.buttons[0],
            "Y button": self.buttons[3],
            "A button": self.buttons[1],
            "B button": self.buttons[2],
            "left stick button": self.buttons[10],
            "right stick button": self.buttons[11],
            "back button": self.buttons[8],
            "start button": self.buttons[9],
            "logo button": None
            }
        print(f"{self.name} connected.")
    
    def handle_input(self, event):
        pass
    
    def left(self):
        pass
    
    def right(self):
        pass
    
    def up(self):
        pass
    
    def down(self):
        pass
    
    def pause(self):
        pass
    
    def rumble(self):
        pass
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        self._name = name
    