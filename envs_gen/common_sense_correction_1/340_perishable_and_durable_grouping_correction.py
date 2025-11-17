from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 340_perishable_and_durable_grouping_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        - Containers: tray and wooden_box
        - Objects: apple, hamburg, orange_block, cup_with_handle, mug
        - Distractors: calculator, screwdriver, pot-with-plant, alarm-clock, book
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.mug = self.add_actor("mug", "mug")

        # Add distractors
        distractor_list = ['calculator', 'screwdriver', 'pot-with-plant', 'alarm-clock', 'book']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - Place perishable ready-to-eat foods and fresh fruit on the tray
        - Place durable toys and drinkware into the wooden_box
        - Correct any wrong placements (e.g., cup_with_handle initially placed on tray)
        """
        # 1. Place apple on tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Place apple on tray:", success)
        if not success:
            return self.info

        # 2. Place cup_with_handle on tray (wrong action)
        success = self.pick_and_place(self.cup_with_handle, self.tray)
        print("Wrongly place cup_with_handle on tray:", success)
        if not success:
            return self.info

        # 3. Correct the wrong placement: move cup_with_handle to wooden_box
        success = self.pick_and_place(self.cup_with_handle, self.wooden_box)
        print("Recover cup_with_handle to wooden_box:", success)
        if not success:
            return self.info

        # 4. Place hamburg on tray
        success = self.pick_and_place(self.hamburg, self.tray)
        print("Place hamburg on tray:", success)
        if not success:
            return self.info

        # 5. Place orange_block into wooden_box
        success = self.pick_and_place(self.orange_block, self.wooden_box)
        print("Place orange_block into wooden_box:", success)
        if not success:
            return self.info

        # 6. Place mug into wooden_box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Place mug into wooden_box:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        - Perishable ready-to-eat foods and fresh fruit (apple, hamburg) are on the tray
        - Durable toys and drinkware (orange_block, cup_with_handle, mug) are in the wooden_box
        """
        if (
            self.check_on(self.apple, self.tray) and
            self.check_on(self.hamburg, self.tray) and
            self.check_on(self.orange_block, self.wooden_box) and
            self.check_on(self.cup_with_handle, self.wooden_box) and
            self.check_on(self.mug, self.wooden_box)
        ):
            return True
        return False
