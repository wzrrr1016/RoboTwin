from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 494_perishable_food_plate_placement_correction(Imagine_Task):
    def load_actors(self):
        self.plate = self.add_actor("plate", "plate")
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.toycar = self.add_actor("toycar", "toycar")
        distractors = ["pot-with-plant", "microphone", "dumbbell", "shoe", "sand-clock"]
        self.add_distractors(distractors)

    def play_once(self):
        # Place apple on plate
        success = self.pick_and_place(self.apple, self.plate)
        if not success:
            return self.info

        # Wrong action: place toycar on plate
        self.pick_and_place(self.toycar, self.plate)

        # Recovery: place toycar on table
        success = self.pick_and_place(self.toycar, self.table)
        if not success:
            return self.info

        # Place bread on plate
        success = self.pick_and_place(self.bread, self.plate)
        if not success:
            return self.info

        # Place hamburg on plate
        success = self.pick_and_place(self.hamburg, self.plate)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all edible items are on the plate
        if (self.check_on(self.apple, self.plate) and
            self.check_on(self.bread, self.plate) and
            self.check_on(self.hamburg, self.plate)):
            # Ensure toycar is not on the plate
            if not self.check_on(self.toycar, self.plate):
                return True
        return False
