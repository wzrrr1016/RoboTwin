from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 79_safe_storage_and_display_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Adds the containers (tray and shoe_box), the target objects (apple, bottle, knife, dumbbell),
        and the distractor objects as specified in the task description.
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add target objects
        self.apple = self.add_actor("apple", "apple")
        self.bottle = self.add_actor("bottle", "bottle")
        self.knife = self.add_actor("knife", "knife")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")

        # Add distractor objects
        distractor_list = ['calculator', 'toycar', 'pot-with-plant', 'book', 'markpen']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in one trial.
        The robot first places the apple in the shoe_box (wrong action), then recovers by
        placing it on the tray. It then places the bottle on the tray, and the knife and
        dumbbell into the shoe_box for safe storage.
        """
        # Step 1: Wrong action - Place apple in shoe_box
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Step 1 (Wrong): Place apple in shoe_box:", success)
        if not success:
            return self.info

        # Step 2: Recovery - Place apple on tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Step 2 (Recovery): Place apple on tray:", success)
        if not success:
            return self.info

        # Step 3: Place bottle on tray
        success = self.pick_and_place(self.bottle, self.tray)
        print("Step 3: Place bottle on tray:", success)
        if not success:
            return self.info

        # Step 4: Place knife in shoe_box
        success = self.pick_and_place(self.knife, self.shoe_box)
        print("Step 4: Place knife in shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place dumbbell in shoe_box
        success = self.pick_and_place(self.dumbbell, self.shoe_box)
        print("Step 5: Place dumbbell in shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions of all objects.
        - Edible and drinkable items (apple, bottle) should be on the tray.
        - Heavy or sharp items (knife, dumbbell) should be in the shoe_box.
        """
        if (self.check_on(self.apple, self.tray) and
            self.check_on(self.bottle, self.tray) and
            self.check_on(self.knife, self.shoe_box) and
            self.check_on(self.dumbbell, self.shoe_box)):
            return True
        return False
