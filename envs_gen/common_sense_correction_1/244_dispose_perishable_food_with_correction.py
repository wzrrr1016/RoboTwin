from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 244_dispose_perishable_food_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        Includes the dustbin (container), food items (objects), and distractors.
        """
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add food items that are either perishable or greasy
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.bread = self.add_actor("bread", "bread")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.apple = self.add_actor("apple", "apple")
        self.can = self.add_actor("can", "can")

        # Add distractor objects to the environment
        distractor_list = ['calculator', 'screwdriver', 'toycar', 'book', 'shoe']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in one trial.
        Includes placing food items in the dustbin, a wrong action, and recovery.
        """
        # Step 1: Place greasy food (french fries) into dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Pick and place french fries:", success)
        if not success:
            return self.info

        # Step 2: Place apple into dustbin (wrong action)
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Pick and place apple (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover apple by placing it back on the table
        success = self.pick_and_place(self.apple, self.table)
        print("Recover apple:", success)
        if not success:
            return self.info

        # Step 4: Place perishable food (bread) into dustbin
        success = self.pick_and_place(self.bread, self.dustbin)
        print("Pick and place bread:", success)
        if not success:
            return self.info

        # Step 5: Place perishable food (hamburg) into dustbin
        success = self.pick_and_place(self.hamburg, self.dustbin)
        print("Pick and place hamburg:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The correct items should be in the dustbin, and the apple should not be.
        """
        # Check if the correct items are in the dustbin
        correct_items_in_dustbin = (
            self.check_on(self.french_fries, self.dustbin) and
            self.check_on(self.bread, self.dustbin) and
            self.check_on(self.hamburg, self.dustbin)
        )

        # Check if the apple is not in the dustbin (i.e., it was recovered)
        apple_not_in_dustbin = not self.check_on(self.apple, self.dustbin)

        # Return True only if all conditions are met
        return correct_items_in_dustbin and apple_not_in_dustbin
