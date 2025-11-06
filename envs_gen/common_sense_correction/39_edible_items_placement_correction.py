from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 39_edible_items_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the plate (container)
        self.plate = self.add_actor("plate", "plate")
        # Load the microphone (non-edible, needs to be recovered)
        self.microphone = self.add_actor("microphone", "microphone")
        # Load the edible items
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.bread = self.add_actor("bread", "bread")
        # Load other objects (not required for the task)
        self.knife = self.add_actor("knife", "knife")
        self.mouse = self.add_actor("mouse", "mouse")

    def play_once(self):
        # Step 1: Recover the microphone if it's on the plate
        if self.check_on(self.microphone, self.plate):
            success = self.pick_and_place(self.microphone, self.table)
            print("pick place microphone:", success)
            if not success:
                return self.info

        # Step 2: Place the edible item 'hamburg' into the plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("pick place hamburg:", success)
        if not success:
            return self.info

        # Step 3: Place the edible item 'bread' into the plate
        success = self.pick_and_place(self.bread, self.plate)
        print("pick place bread:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if both hamburg and bread are on the plate
        if self.check_on(self.hamburg, self.plate) and self.check_on(self.bread, self.plate):
            return True
        return False
