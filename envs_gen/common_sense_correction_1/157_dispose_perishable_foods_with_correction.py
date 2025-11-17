from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 157_dispose_perishable_foods_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        Includes containers, target objects, and distractors.
        """
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add target objects
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.can = self.add_actor("can", "can")
        self.book = self.add_actor("book", "book")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        
        # Add distractor objects
        distractor_list = ['calculator', 'alarm-clock', 'toycar', 'shoe', 'small-speaker']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of robot actions for the task.
        Follows the specified action plan including error recovery.
        """
        # 1. Put bread in dustbin
        success = self.pick_and_place(self.bread, self.dustbin)
        print("Bread to dustbin:", success)
        if not success:
            return self.info

        # 2. Wrong action: Put screwdriver in dustbin
        success = self.pick_and_place(self.screwdriver, self.dustbin)
        print("Screwdriver to dustbin (wrong):", success)
        if not success:
            return self.info

        # 3. Recovery: Move screwdriver from dustbin to book
        success = self.pick_and_place(self.screwdriver, self.book)
        print("Screwdriver to book (recovery):", success)
        if not success:
            return self.info

        # 4. Put french fries in dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("French fries to dustbin:", success)
        if not success:
            return self.info

        # 5. Put can on book
        success = self.pick_and_place(self.can, self.book)
        print("Can to book:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        Checks if food items are in dustbin and non-food items are on book.
        """
        # Check if food items are in dustbin
        food_in_dustbin = (
            self.check_on(self.bread, self.dustbin) and
            self.check_on(self.french_fries, self.dustbin)
        )
        
        # Check if non-food items are on book
        non_food_on_book = (
            self.check_on(self.screwdriver, self.book) and
            self.check_on(self.can, self.book)
        )
        
        return food_in_dustbin and non_food_on_book
