from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 136_reusable_vs_disposable_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        Adds the main objects and distractors as specified in the task description.
        """
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add main objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.book = self.add_actor("book", "book")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractors
        distractor_list = ["red_block", "green_block", "blue_block", "yellow_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot to complete the task.
        The task involves:
        1. Initial incorrect placement of bottle in dustbin
        2. Recovery of bottle to wooden_box
        3. Correct placement of other objects in appropriate containers
        """
        # 1. Initial incorrect placement of bottle in dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Place bottle into dustbin (wrong):", success)
        if not success:
            return self.info

        # 2. Recovery: Move bottle from dustbin to wooden_box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("Recover bottle to wooden_box:", success)
        if not success:
            return self.info

        # 3. Place book (reusable/recyclable) in wooden_box
        success = self.pick_and_place(self.book, self.wooden_box)
        print("Place book into wooden_box:", success)
        if not success:
            return self.info

        # 4. Place french_fries (food waste) in dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Place french fries into dustbin:", success)
        if not success:
            return self.info

        # 5. Place tissue-box (disposable) in dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Place tissue-box into dustbin:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if all objects are in their correct final positions according to the task requirements.
        Returns True if all conditions are met, False otherwise.
        """
        # Check if recyclable/reusable items are in wooden_box
        bottle_in_wooden_box = self.check_on(self.bottle, self.wooden_box)
        book_in_wooden_box = self.check_on(self.book, self.wooden_box)
        
        # Check if disposable/food-waste items are in dustbin
        fries_in_dustbin = self.check_on(self.french_fries, self.dustbin)
        tissue_in_dustbin = self.check_on(self.tissue_box, self.dustbin)
        
        # Return True only if all conditions are satisfied
        return all([
            bottle_in_wooden_box,
            book_in_wooden_box,
            fries_in_dustbin,
            tissue_in_dustbin
        ])
