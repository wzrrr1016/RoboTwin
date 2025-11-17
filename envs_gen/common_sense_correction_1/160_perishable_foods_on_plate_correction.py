from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 160_perishable_foods_on_plate_correction(Imagine_Task):
    def load_actors(self):
        # Add the plate and required objects
        self.plate = self.add_actor("plate", "plate")
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.pink_block = self.add_actor("pink_block", "pink_block")

        # Add distractors
        distractor_list = ["calculator", "screwdriver", "toycar", "pot-with-plant", "alarm-clock", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # First, incorrectly place shampoo on plate
        success = self.pick_and_place(self.shampoo, self.plate)
        print("Pick and place shampoo on plate (wrong):", success)
        if not success:
            return self.info

        # Correct by moving shampoo to pink_block
        success = self.pick_and_place(self.shampoo, self.pink_block)
        print("Pick and place shampoo on pink_block (recovery):", success)
        if not success:
            return self.info

        # Place perishable edibles on plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Pick and place apple:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bread, self.plate)
        print("Pick and place bread:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.french_fries, self.plate)
        print("Pick and place french fries:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check all food items are on plate and shampoo is not on plate
        if (self.check_on(self.apple, self.plate) and
            self.check_on(self.bread, self.plate) and
            self.check_on(self.french_fries, self.plate) and
            not self.check_on(self.shampoo, self.plate)):
            return True
        return False
