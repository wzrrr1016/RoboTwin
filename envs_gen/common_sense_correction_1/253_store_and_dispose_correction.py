from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 253_store_and_dispose_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        """
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add useful household items
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.markpen = self.add_actor("markpen", "markpen")
        
        # Add edible/perishable item
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add distractors
        distractor_list = ['toycar', 'red_block', 'green_block', 'blue_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions to complete the task.
        Steps:
        1. Place cup_with_handle in shoe_box
        2. Place french_fries in shoe_box (wrong action)
        3. Recover by placing french_fries in dustbin
        4. Place small-speaker in shoe_box
        5. Place markpen in shoe_box
        """
        # Step 1: Place cup_with_handle in shoe_box
        success = self.pick_and_place(self.cup_with_handle, self.shoe_box)
        print("Place cup_with_handle:", success)
        if not success:
            return self.info

        # Step 2: Wrongly place french_fries in shoe_box
        success = self.pick_and_place(self.french_fries, self.shoe_box)
        print("Wrongly place french_fries:", success)
        if not success:
            return self.info

        # Step 3: Recover by placing french_fries in dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Recover french_fries:", success)
        if not success:
            return self.info

        # Step 4: Place small-speaker in shoe_box
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        print("Place small-speaker:", success)
        if not success:
            return self.info

        # Step 5: Place markpen in shoe_box
        success = self.pick_and_place(self.markpen, self.shoe_box)
        print("Place markpen:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        Criteria:
        - Useful items (cup_with_handle, small-speaker, markpen) are in shoe_box
        - Edible item (french_fries) is in dustbin
        """
        if (self.check_on(self.cup_with_handle, self.shoe_box) and
            self.check_on(self.small_speaker, self.shoe_box) and
            self.check_on(self.markpen, self.shoe_box) and
            self.check_on(self.french_fries, self.dustbin)):
            return True
        return False
