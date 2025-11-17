from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 56_toy_and_fastfood_cleanup_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: shoe_box, dustbin
        - Objects: toycar, red_block, blue_block, french_fries, hamburg
        - Distractors: calculator, screwdriver, book, alarm-clock, dumbbell
        """
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.red_block = self.add_actor("red_block", "red_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.hamburg = self.add_actor("hamburg", "hamburg")

        # Add distractors
        distractor_list = ['calculator', 'screwdriver', 'book', 'alarm-clock', 'dumbbell']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        Steps:
        1. Place toycar into shoe_box
        2. Place hamburg into shoe_box (wrong action)
        3. Recover hamburg by placing it into dustbin
        4. Place red_block into shoe_box
        5. Place french_fries into dustbin
        6. Place blue_block into shoe_box
        """
        # Step 1: Place toycar into shoe_box
        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("Place toycar:", success)
        if not success:
            return self.info

        # Step 2: Place hamburg into shoe_box (wrong action)
        success = self.pick_and_place(self.hamburg, self.shoe_box)
        print("Place hamburg (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover hamburg by placing it into dustbin
        success = self.pick_and_place(self.hamburg, self.dustbin)
        print("Recover hamburg:", success)
        if not success:
            return self.info

        # Step 4: Place red_block into shoe_box
        success = self.pick_and_place(self.red_block, self.shoe_box)
        print("Place red_block:", success)
        if not success:
            return self.info

        # Step 5: Place french_fries into dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Place french_fries:", success)
        if not success:
            return self.info

        # Step 6: Place blue_block into shoe_box
        success = self.pick_and_place(self.blue_block, self.shoe_box)
        print("Place blue_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Toys and blocks (toycar, red_block, blue_block) should be in the shoe_box.
        - Fast food items (hamburg, french_fries) should be in the dustbin.
        """
        return (
            self.check_on(self.toycar, self.shoe_box) and
            self.check_on(self.red_block, self.shoe_box) and
            self.check_on(self.blue_block, self.shoe_box) and
            self.check_on(self.hamburg, self.dustbin) and
            self.check_on(self.french_fries, self.dustbin)
        )
