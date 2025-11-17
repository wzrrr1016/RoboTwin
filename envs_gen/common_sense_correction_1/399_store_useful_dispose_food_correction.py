from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 399_store_useful_dispose_food_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Containers: wooden_box, dustbin
        Objects: drill, mouse, book, apple, hamburg
        Distractors: pet-collar, pot-with-plant, dumbbell, shoe, toycar
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add required objects
        self.drill = self.add_actor("drill", "drill")
        self.mouse = self.add_actor("mouse", "mouse")
        self.book = self.add_actor("book", "book")
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        
        # Add distractors
        distractor_list = ['pet-collar', 'pot-with-plant', 'dumbbell', 'shoe', 'toycar']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions to complete the task:
        1. Place drill in wooden_box
        2. Place hamburg in wooden_box (wrong action)
        3. Recover hamburg to dustbin
        4. Place book in wooden_box
        5. Place mouse in wooden_box
        6. Place apple in dustbin
        """
        # Step 1: Place drill in wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Pick and place drill:", success)
        if not success:
            return self.info

        # Step 2: Wrongly place hamburg in wooden_box
        success = self.pick_and_place(self.hamburg, self.wooden_box)
        print("Pick and place hamburg (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover hamburg to dustbin
        success = self.pick_and_place(self.hamburg, self.dustbin)
        print("Recover hamburg to dustbin:", success)
        if not success:
            return self.info

        # Step 4: Place book in wooden_box
        success = self.pick_and_place(self.book, self.wooden_box)
        print("Pick and place book:", success)
        if not success:
            return self.info

        # Step 5: Place mouse in wooden_box
        success = self.pick_and_place(self.mouse, self.wooden_box)
        print("Pick and place mouse:", success)
        if not success:
            return self.info

        # Step 6: Place apple in dustbin
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Pick and place apple:", success)
        if not success:
            return self.info

        return self.info  # All steps succeeded

    def check_success(self):
        """
        Verify if all objects are in their correct containers:
        - Reusable tools, electronics, and reading materials in wooden_box
        - Perishable and fast-food items in dustbin
        """
        # Check if all required objects are in their correct containers
        drill_in_wooden = self.check_on(self.drill, self.wooden_box)
        mouse_in_wooden = self.check_on(self.mouse, self.wooden_box)
        book_in_wooden = self.check_on(self.book, self.wooden_box)
        apple_in_dustbin = self.check_on(self.apple, self.dustbin)
        hamburg_in_dustbin = self.check_on(self.hamburg, self.dustbin)

        # Return True if all conditions are met
        if (drill_in_wooden and mouse_in_wooden and book_in_wooden and
            apple_in_dustbin and hamburg_in_dustbin):
            return True
        return False
