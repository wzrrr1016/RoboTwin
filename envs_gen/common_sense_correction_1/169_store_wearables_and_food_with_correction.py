from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 169_store_wearables_and_food_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        - Containers: fluted_block, shoe_box
        - Objects: apple, bread, bottle, shoe
        - Distractors: calculator, screwdriver, book, pot-with-plant, toycar
        """
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.bottle = self.add_actor("bottle", "bottle")
        self.shoe = self.add_actor("shoe", "shoe")

        # Add distractors
        distractor_list = ["calculator", "screwdriver", "book", "pot-with-plant", "toycar"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of robot actions to complete the task:
        1. Place shoe into shoe_box
        2. Place bottle into shoe_box (wrong action)
        3. Move bottle from shoe_box to fluted_block (recovery)
        4. Place apple onto fluted_block
        5. Place bread onto fluted_block
        """
        # Step 1: Place shoe into shoe_box
        success = self.pick_and_place(self.shoe, self.shoe_box)
        print("Place shoe into shoe_box:", success)
        if not success:
            return self.info

        # Step 2: Place bottle into shoe_box (wrong action)
        success = self.pick_and_place(self.bottle, self.shoe_box)
        print("Place bottle into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Step 3: Move bottle from shoe_box to fluted_block (recovery)
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Move bottle to fluted_block:", success)
        if not success:
            return self.info

        # Step 4: Place apple onto fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple onto fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Place bread onto fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Place bread onto fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task is successfully completed:
        - Shoe is in shoe_box
        - Apple, bread, and bottle are on fluted_block
        """
        if (self.check_on(self.shoe, self.shoe_box) and
            self.check_on(self.apple, self.fluted_block) and
            self.check_on(self.bread, self.fluted_block) and
            self.check_on(self.bottle, self.fluted_block)):
            return True
        return False
