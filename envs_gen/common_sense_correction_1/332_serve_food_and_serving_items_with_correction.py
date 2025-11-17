from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 332_serve_food_and_serving_items_with_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required objects and distractors in the environment."""
        # Create the plate container
        self.plate = self.add_actor("plate", "plate")
        
        # Create edible and serving items
        self.bread = self.add_actor("bread", "bread")
        self.mug = self.add_actor("mug", "mug")
        self.teanet = self.add_actor("teanet", "teanet")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add distractor objects
        distractor_list = ["calculator", "screwdriver", "toycar", "alarm-clock", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of actions to complete the task."""
        # Wrong action: place yellow_block on plate
        success = self.pick_and_place(self.yellow_block, self.plate)
        print("Pick yellow_block and place on plate (wrong):", success)
        if not success:
            return self.info

        # Recovery: move yellow_block back to table
        success = self.pick_and_place(self.yellow_block, self.table)
        print("Pick yellow_block from plate and place on table (recovery):", success)
        if not success:
            return self.info

        # Place edible items on plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Pick bread and place on plate:", success)
        if not success:
            return self.info

        # Place serving items on plate
        success = self.pick_and_place(self.mug, self.plate)
        print("Pick mug and place on plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.teanet, self.plate)
        print("Pick teanet and place on plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully."""
        # Check if all required items are on the plate
        # and the incorrect item is not on the plate
        if (self.check_on(self.bread, self.plate) and
            self.check_on(self.mug, self.plate) and
            self.check_on(self.teanet, self.plate) and
            not self.check_on(self.yellow_block, self.plate)):
            return True
        return False
