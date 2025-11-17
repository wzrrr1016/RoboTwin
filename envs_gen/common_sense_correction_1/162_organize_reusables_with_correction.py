from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 162_organize_reusables_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes containers (tray, dustbin), target objects (tools, cups, food),
        and distractors.
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add target objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.hamburg = self.add_actor("hamburg", "hamburg")

        # Add distractors
        distractor_list = ['toycar', 'alarm-clock', 'pot-with-plant', 'book', 'shoe']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions to complete the task:
        - Place reusable tools and drinkware on the tray.
        - Place processed food (hamburg) in the dustbin.
        """
        # Step 1: Place cup_with_handle on tray
        success = self.pick_and_place(self.cup_with_handle, self.tray)
        print("Place cup_with_handle on tray:", success)
        if not success:
            return self.info

        # Step 2: Place cup_without_handle on tray
        success = self.pick_and_place(self.cup_without_handle, self.tray)
        print("Place cup_without_handle on tray:", success)
        if not success:
            return self.info

        # Step 3: Place hammer on tray
        success = self.pick_and_place(self.hammer, self.tray)
        print("Place hammer on tray:", success)
        if not success:
            return self.info

        # Step 4: Place hamburg on tray (wrong action)
        success = self.pick_and_place(self.hamburg, self.tray)
        print("Place hamburg on tray (wrong):", success)
        if not success:
            return self.info

        # Step 5: Move hamburg from tray to dustbin (recovery)
        success = self.pick_and_place(self.hamburg, self.dustbin)
        print("Move hamburg to dustbin:", success)
        if not success:
            return self.info

        # Step 6: Place screwdriver on tray
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Place screwdriver on tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed by verifying:
        - All reusable tools and drinkware are on the tray.
        - Processed food (hamburg) is in the dustbin.
        """
        if (
            self.check_on(self.cup_with_handle, self.tray) and
            self.check_on(self.cup_without_handle, self.tray) and
            self.check_on(self.hammer, self.tray) and
            self.check_on(self.screwdriver, self.tray) and
            self.check_on(self.hamburg, self.dustbin)
        ):
            return True
        return False
