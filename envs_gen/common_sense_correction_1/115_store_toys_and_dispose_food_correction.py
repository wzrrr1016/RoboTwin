from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 115_store_toys_and_dispose_food_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Adds containers, target objects, and distractors.
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add target objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.book = self.add_actor("book", "book")
        self.can = self.add_actor("can", "can")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractors
        distractor_list = ["calculator", "screwdriver", "alarm-clock", "pot-with-plant", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions to complete the task.
        The robot will:
        1. Place toys and reading materials in the wooden_box
        2. Place perishable/disposable food items in the dustbin
        3. Correct any initial misplacements
        """
        # Place toys and reading materials in wooden_box
        success = self.pick_and_place(self.toycar, self.wooden_box)
        print("Place toycar:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.blue_block, self.wooden_box)
        print("Place blue_block:", success)
        if not success:
            return self.info

        # Place bread in wooden_box (wrong action)
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Wrongly place bread:", success)
        if not success:
            return self.info

        # Correct the bread placement to dustbin
        success = self.pick_and_place(self.bread, self.dustbin)
        print("Correctly place bread:", success)
        if not success:
            return self.info

        # Place book in wooden_box
        success = self.pick_and_place(self.book, self.wooden_box)
        print("Place book:", success)
        if not success:
            return self.info

        # Place can in dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        print("Place can:", success)
        if not success:
            return self.info

        return self.info  # Return info if all actions succeed

    def check_success(self):
        """
        Verify if the task was completed successfully by checking:
        - Toys and reading materials are in the wooden_box
        - Perishable/disposable food items are in the dustbin
        """
        return (
            self.check_on(self.toycar, self.wooden_box) and
            self.check_on(self.blue_block, self.wooden_box) and
            self.check_on(self.book, self.wooden_box) and
            self.check_on(self.bread, self.dustbin) and
            self.check_on(self.can, self.dustbin)
        )
