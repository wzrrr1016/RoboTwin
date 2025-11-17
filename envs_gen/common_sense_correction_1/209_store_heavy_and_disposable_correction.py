from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 209_store_heavy_and_disposable_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: shoe_box, dustbin
        - Objects: hammer, knife, dumbbell, markpen
        - Distractors: toycar, pot-with-plant, alarm-clock, book, apple
        """
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.knife = self.add_actor("knife", "knife")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.markpen = self.add_actor("markpen", "markpen")

        # Add distractors
        distractor_list = ['toycar', 'pot-with-plant', 'alarm-clock', 'book', 'apple']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task:
        1. Pick hammer and place it into shoe_box
        2. Pick markpen and place it into shoe_box (wrong action)
        3. Pick markpen from shoe_box and place it into dustbin (recovery)
        4. Pick knife and place it into shoe_box
        5. Pick dumbbell and place it into shoe_box
        """
        # Step 1: Place hammer in shoe_box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Pick hammer and place in shoe_box:", success)
        if not success:
            return self.info

        # Step 2: Place markpen in shoe_box (wrong action)
        success = self.pick_and_place(self.markpen, self.shoe_box)
        print("Pick markpen and place in shoe_box (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing markpen in dustbin
        success = self.pick_and_place(self.markpen, self.dustbin)
        print("Pick markpen from shoe_box and place in dustbin:", success)
        if not success:
            return self.info

        # Step 4: Place knife in shoe_box
        success = self.pick_and_place(self.knife, self.shoe_box)
        print("Pick knife and place in shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place dumbbell in shoe_box
        success = self.pick_and_place(self.dumbbell, self.shoe_box)
        print("Pick dumbbell and place in shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully:
        - Hammer, knife, and dumbbell are in the shoe_box
        - Markpen is in the dustbin
        """
        if (
            self.check_on(self.hammer, self.shoe_box) and
            self.check_on(self.knife, self.shoe_box) and
            self.check_on(self.dumbbell, self.shoe_box) and
            self.check_on(self.markpen, self.dustbin)
        ):
            return True
        return False
