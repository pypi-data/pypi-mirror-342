from pygameControls.controlsbase import ControlsBase
from pydualsense import *

BATTERY_STATE = {
    "0": "Discharging",
    "1": "Charging",
    "2": "Full",
    "11": "Not charging",
    "15": "Error",
    "10": "Temp or voltage out of range"
    }

class DualSenseController(ControlsBase):
    def __init__(self, joy):
        self.device = pydualsense()
        self.device.init()
        self.name = self.device.device.get_product_string()
        self.powerlevel = self.device.battery.Level
        self.batterystate = BATTERY_STATE[str(self.device.battery.State)]
        self.set_player_id(PlayerID.PLAYER_1)
        print(f"{self.name} connected")
        print(f"Power level: {self.powerlevel}")
        print(f"Battery state: {self.batterystate}")
    
    def handle_input(self, event):
        pass
    
    def set_led(self, red: int, green: int, blue: int):
        self.device.light.setColorI(red, green, blue)

    def set_player_id(self, playerid: PlayerID):
        self.device.light.setPlayerID(playerid)
        
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
    
    @property
    def powerlevel(self) -> str:
        return self._powerlevel
    
    @powerlevel.setter
    def powerlevel(self, lvl: str) -> None:
        self._powerlevel = lvl
    
    @property
    def batterystate(self) -> int:
        return self._batterystate
    
    @batterystate.setter
    def batterystate(self, state) -> None:
        self._batterystate = state