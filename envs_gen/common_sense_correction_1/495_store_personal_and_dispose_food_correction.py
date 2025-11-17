from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 495_store_personal_and_dispose_food_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Containers: shoe_box, dustbin
        Objects: shoe, screwdriver, book, bread, french_fries
        Distractors: red_block, green_block, blue_block, yellow_block
        """
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.shoe = self.add_actor("shoe", "shoe")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.book = self.add_actor("book", "book")
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")

        # Add distractors
        distractor_list = ['red_block', 'green_block', 'blue_block', 'yellow_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        Actions:
        1. Pick shoe and place it into shoe_box
        2. Pick bread and place it into dustbin
        3. Pick book and place it into dustbin (wrong)
        4. Pick book from dustbin and place it into shoe_box (recovery)
        5. Pick screwdriver and place it into shoe_box
        6. Pick french_fries and place it into dustbin
        """
        # Step 1: Pick shoe and place in shoe_box
        success = self.pick_and_place(self.shoe, self.shoe_box)
        print("Pick shoe:", success)
        if not success:
            return self.info

        # Step 2: Pick bread and place in dustbin
        success = self.pick_and_place(self.bread, self.dustbin)
        print("Pick bread:", success)
        if not success:
            return self.info

        # Step 3: Wrong action - Pick book and place in dustbin
        success = self.pick_and_place(self.book, self.dustbin)
        print("Pick book (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recovery - Pick book from dustbin and place in shoe_box
        success = self.pick_and_place(self.book, self.shoe_box)
        print("Recover book:", success)
        if not success:
            return self.info

        # Step 5: Pick screwdriver and place in shoe_box
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Pick screwdriver:", success)
        if not success:
            return self.info

        # Step 6: Pick french_fries and place in dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Pick french fries:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions of all relevant objects.
        Success criteria:
        - Wearable items (shoe), small tools (screwdriver), and keepable belongings (book) are in the shoe_box
        - Perishable or oily foods (bread, french_fries) are in the dustbin
        """
        if (self.check_on(self.shoe, self.shoe_box) and
            self.check_on(self.screwdriver, self.shoe_box) and
            self.check_on(self.book, self.shoe_box) and
            self.check_on(self.bread, self.dustbin) and
            self.check_on(self.french_fries, self.dustbin)):
            return True
        return False
