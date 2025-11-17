from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 17_perishable_food_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        # Add the edible items
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        # Add the non-edible items
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        # Add distractors
        distractor_list = ["calculator", "screwdriver", "shoe", "alarm-clock", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Pick apple and place into fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Pick apple:", success)
        if not success:
            return self.info

        # Pick hamburg and place into fluted_block
        success = self.pick_and_place(self.hamburg, self.fluted_block)
        print("Pick hamburg:", success)
        if not success:
            return self.info

        # Pick pot-with-plant and place on table
        success = self.pick_and_place(self.pot_with_plant, self.table)
        print("Pick pot-with-plant:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if apple and hamburg are in fluted_block
        apple_on = self.check_on(self.apple, self.fluted_block)
        hamburg_on = self.check_on(self.hamburg, self.fluted_block)

        # Check if pot-with-plant is on the table
        pot_on_table = self.check_on(self.pot_with_plant, self.table)

        # Ensure yellow_block is NOT in fluted_block
        yellow_not_in = not self.check_on(self.yellow_block, self.fluted_block)

        return apple_on and hamburg_on and pot_on_table and yellow_not_in
