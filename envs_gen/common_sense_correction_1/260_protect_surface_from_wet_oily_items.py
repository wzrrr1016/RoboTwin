from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 260_protect_surface_from_wet_oily_items(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        """
        # Add the coaster as a container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add the objects that need to be placed or manipulated
        self.can = self.add_actor("can", "can")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractor objects to the environment
        distractor_list = ['calculator', 'screwdriver', 'toycar', 'book', 'dumbbell']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        """
        # Place shampoo on the coaster
        success = self.pick_and_place(self.shampoo, self.coaster)
        print("Place shampoo on coaster:", success)
        if not success:
            return self.info

        # Place french fries on the coaster
        success = self.pick_and_place(self.french_fries, self.coaster)
        print("Place french fries on coaster:", success)
        if not success:
            return self.info

        # Wrongly place tissue-box on the coaster (as per task description)
        success = self.pick_and_place(self.tissue_box, self.coaster)
        print("Wrongly place tissue-box on coaster:", success)
        if not success:
            return self.info

        # Recovery: Move tissue-box from coaster to table
        success = self.pick_and_place(self.tissue_box, self.table)
        print("Move tissue-box to table:", success)
        if not success:
            return self.info

        # Place can on the coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Place can on coaster:", success)
        if not success:
            return self.info

        return self.info  # Return success status if all actions are completed

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Wet/oily/likely-to-leak items (shampoo, french_fries, can) must be on the coaster.
        - Absorbent paper goods (tissue-box) must not be on the coaster.
        """
        # Check if the correct items are on the coaster
        shampoo_on_coaster = self.check_on(self.shampoo, self.coaster)
        french_fries_on_coaster = self.check_on(self.french_fries, self.coaster)
        can_on_coaster = self.check_on(self.can, self.coaster)

        # Check if the tissue-box is NOT on the coaster
        tissue_box_not_on_coaster = not self.check_on(self.tissue_box, self.coaster)

        # Return True only if all conditions are met
        return (
            shampoo_on_coaster
            and french_fries_on_coaster
            and can_on_coaster
            and tissue_box_not_on_coaster
        )
