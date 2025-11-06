from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 5_healthy_food_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the tray (container)
        self.tray = self.add_actor("tray", "tray")
        # Load the apple (healthy item)
        self.apple = self.add_actor("apple", "apple")
        # Load other objects present in the scene (not relevant for this task)
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.fork = self.add_actor("fork", "fork")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

    def play_once(self):
        # Attempt to pick the apple and place it into the tray
        success = self.pick_and_place(self.apple, self.tray)
        print("pick place apple:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the apple is on the tray
        return self.check_on(self.apple, self.tray)
