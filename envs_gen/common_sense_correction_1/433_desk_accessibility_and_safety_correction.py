from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 433_desk_accessibility_and_safety_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        - Containers: tray and wooden_box
        - Objects: mouse, dumbbell, cup_without_handle, yellow_block, knife
        - Distractors: baguette, apple, shoe, pet-collar, chips-tub
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects
        self.mouse = self.add_actor("mouse", "mouse")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.knife = self.add_actor("knife", "knife")

        # Add distractors
        distractor_list = ['baguette', 'apple', 'shoe', 'pet-collar', 'chips-tub']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - First, place the dumbbell on the tray (wrong action), then move it to the wooden_box (recovery).
        - Place small, frequently-used desk items (mouse, cup_without_handle, yellow_block) on the tray.
        - Place heavy or dangerous items (dumbbell, knife) into the wooden_box.
        """
        # Step 1: Place dumbbell on tray (wrong action)
        success = self.pick_and_place(self.dumbbell, self.tray)
        print("Pick dumbbell and place on tray (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - Move dumbbell to wooden_box
        success = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("Pick dumbbell from tray and place into wooden_box (recovery):", success)
        if not success:
            return self.info

        # Step 3: Place mouse on tray
        success = self.pick_and_place(self.mouse, self.tray)
        print("Place mouse on tray:", success)
        if not success:
            return self.info

        # Step 4: Place cup_without_handle on tray
        success = self.pick_and_place(self.cup_without_handle, self.tray)
        print("Place cup_without_handle on tray:", success)
        if not success:
            return self.info

        # Step 5: Place yellow_block on tray
        success = self.pick_and_place(self.yellow_block, self.tray)
        print("Place yellow_block on tray:", success)
        if not success:
            return self.info

        # Step 6: Place knife into wooden_box
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("Place knife into wooden_box:", success)
        if not success:
            return self.info

        # All steps succeeded
        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All small, frequently-used items are on the tray.
        - All heavy or dangerous items are in the wooden_box.
        """
        if (
            self.check_on(self.mouse, self.tray) and
            self.check_on(self.cup_without_handle, self.tray) and
            self.check_on(self.yellow_block, self.tray) and
            self.check_on(self.dumbbell, self.wooden_box) and
            self.check_on(self.knife, self.wooden_box)
        ):
            return True
        return False
