from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 32_store_small_toys_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the shoe_box (container), the small play items (toycar, pink_block, blue_block),
        the incorrect item (dumbbell), and the distractor objects.
        """
        # Add the shoe_box as a container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add the small, lightweight play items
        self.toycar = self.add_actor("toycar", "toycar")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")

        # Add the incorrect (heavy) item
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")

        # Add distractor objects to the environment
        distractor_list = ["olive-oil", "baguette", "drill", "pot-with-plant", "shampoo"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        The robot will:
        1. Place the toycar into the shoe_box
        2. Place the pink_block into the shoe_box
        3. Place the dumbbell into the shoe_box (incorrect action)
        4. Remove the dumbbell from the shoe_box and place it on the table (recovery)
        5. Place the blue_block into the shoe_box
        """
        # Step 1: Place toycar into shoe_box
        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("Pick toycar and place into shoe_box:", success)
        if not success:
            return self.info

        # Step 2: Place pink_block into shoe_box
        success = self.pick_and_place(self.pink_block, self.shoe_box)
        print("Pick pink_block and place into shoe_box:", success)
        if not success:
            return self.info

        # Step 3: Place dumbbell into shoe_box (wrong action)
        success = self.pick_and_place(self.dumbbell, self.shoe_box)
        print("Pick dumbbell and place into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Step 4: Remove dumbbell from shoe_box and place on table (recovery)
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Pick dumbbell from shoe_box and place on table (recovery):", success)
        if not success:
            return self.info

        # Step 5: Place blue_block into shoe_box
        success = self.pick_and_place(self.blue_block, self.shoe_box)
        print("Pick blue_block and place into shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The task is considered successful if:
        - toycar, pink_block, and blue_block are all in the shoe_box
        - dumbbell is not in the shoe_box
        """
        if (
            self.check_on(self.toycar, self.shoe_box) and
            self.check_on(self.pink_block, self.shoe_box) and
            self.check_on(self.blue_block, self.shoe_box) and
            not self.check_on(self.dumbbell, self.shoe_box)
        ):
            return True
        return False
