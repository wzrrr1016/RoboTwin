from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 418_play_items_vs_personal_wear_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Containers: shoe_box, fluted_block
        Objects: shampoo, shoe, red_block, toycar, purple_block
        Distractors: calculator, book, hammer, pot-with-plant, mug
        """
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.shoe = self.add_actor("shoe", "shoe")
        self.red_block = self.add_actor("red_block", "red_block")
        self.toycar = self.add_actor("toycar", "toycar")
        self.purple_block = self.add_actor("purple_block", "purple_block")

        # Add distractors
        distractor_list = ["calculator", "book", "hammer", "pot-with-plant", "mug"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the simulation:
        1. Place shampoo into fluted_block (wrong action)
        2. Recover shampoo and place it into shoe_box
        3. Place shoe into shoe_box
        4. Place red_block, toycar, and purple_block into fluted_block
        """
        # Step 1: Place shampoo into fluted_block (wrong)
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Place shampoo into fluted_block (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recover shampoo and place into shoe_box
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("Recover shampoo to shoe_box:", success)
        if not success:
            return self.info

        # Step 3: Place shoe into shoe_box
        success = self.pick_and_place(self.shoe, self.shoe_box)
        print("Place shoe into shoe_box:", success)
        if not success:
            return self.info

        # Step 4: Place red_block into fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Place red_block:", success)
        if not success:
            return self.info

        # Step 5: Place toycar into fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar:", success)
        if not success:
            return self.info

        # Step 6: Place purple_block into fluted_block
        success = self.pick_and_place(self.purple_block, self.fluted_block)
        print("Place purple_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed:
        - shampoo and shoe are in shoe_box
        - red_block, toycar, and purple_block are in fluted_block
        """
        # Check shampoo and shoe are in shoe_box
        if (self.check_on(self.shampoo, self.shoe_box) and
            self.check_on(self.shoe, self.shoe_box)):

            # Check blocks and toycar are in fluted_block
            if (self.check_on(self.red_block, self.fluted_block) and
                self.check_on(self.toycar, self.fluted_block) and
                self.check_on(self.purple_block, self.fluted_block)):
                return True

        return False
