from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 48_healthy_food_and_sound_device_placement(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.plate = self.add_actor("plate", "plate")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Load objects
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.mug = self.add_actor("mug", "mug")
        self.microphone = self.add_actor("microphone", "microphone")

    def play_once(self):
        # Place hamburg into plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("pick place hamburg:", success)
        if not success:
            return self.info

        # Place microphone into wooden_box
        success = self.pick_and_place(self.microphone, self.wooden_box)
        print("pick place microphone:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if hamburg is on the plate
        hamburg_on_plate = self.check_on(self.hamburg, self.plate)
        # Check if microphone is on the wooden_box
        microphone_on_wooden_box = self.check_on(self.microphone, self.wooden_box)

        return hamburg_on_plate and microphone_on_wooden_box
