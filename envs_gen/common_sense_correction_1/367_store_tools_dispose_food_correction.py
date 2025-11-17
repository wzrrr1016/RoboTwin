from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 367_store_tools_dispose_food_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        - Containers: shoe_box, dustbin
        - Objects: hammer, scanner, apple, french_fries, bottle
        - Distractors: pet-collar, toycar, sand-clock, bell, blue_block
        """
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.scanner = self.add_actor("scanner", "scanner")
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.bottle = self.add_actor("bottle", "bottle")

        # Add distractors
        distractor_list = ['pet-collar', 'toycar', 'sand-clock', 'bell', 'blue_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of robot actions to complete the task:
        1. Put reusable tools (hammer, scanner) into the shoe_box.
        2. Place recyclable bottles and perishable/oily food (apple, french_fries) into the dustbin.
        3. Correct a wrong action: initially placing the bottle in the shoe_box, then recovering by moving it to the dustbin.
        """
        # Correct action: hammer to shoe_box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Pick hammer to shoe_box:", success)
        if not success:
            return self.info

        # Wrong action: bottle to shoe_box
        success = self.pick_and_place(self.bottle, self.shoe_box)
        print("Pick bottle to shoe_box (wrong):", success)
        if not success:
            return self.info

        # Recovery: move bottle to dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Pick bottle to dustbin (recovery):", success)
        if not success:
            return self.info

        # Correct action: scanner to shoe_box
        success = self.pick_and_place(self.scanner, self.shoe_box)
        print("Pick scanner to shoe_box:", success)
        if not success:
            return self.info

        # Correct action: french_fries to dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Pick french_fries to dustbin:", success)
        if not success:
            return self.info

        # Correct action: apple to dustbin
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Pick apple to dustbin:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if all objects are placed in the correct containers:
        - hammer and scanner in shoe_box
        - apple, french_fries, and bottle in dustbin
        """
        if (self.check_on(self.hammer, self.shoe_box) and
            self.check_on(self.scanner, self.shoe_box) and
            self.check_on(self.apple, self.dustbin) and
            self.check_on(self.french_fries, self.dustbin) and
            self.check_on(self.bottle, self.dustbin)):
            return True
        return False
