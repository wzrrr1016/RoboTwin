from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 454_access_vs_protection_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the environment.
        Containers (tray and wooden_box) are added as actors.
        Objects (stapler, screwdriver, mouse, cup_with_handle) are added as actors.
        Distractors are added using the add_distractors API.
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add objects
        self.stapler = self.add_actor("stapler", "stapler")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.mouse = self.add_actor("mouse", "mouse")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        
        # Add distractors
        distractor_list = ["tissue-box", "dumbbell", "book", "apple"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions as specified in the task.
        The sequence includes:
        1. Place stapler on tray
        2. Place screwdriver on tray
        3. Place mouse on tray (wrong action)
        4. Move mouse from tray to wooden_box (recovery)
        5. Place cup_with_handle in wooden_box
        """
        # Step 1: Place stapler on tray
        success = self.pick_and_place(self.stapler, self.tray)
        print("Pick place stapler:", success)
        if not success:
            return self.info

        # Step 2: Place screwdriver on tray
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Pick place screwdriver:", success)
        if not success:
            return self.info

        # Step 3: Place mouse on tray (wrong action)
        success = self.pick_and_place(self.mouse, self.tray)
        print("Pick place mouse (wrong):", success)
        if not success:
            return self.info

        # Step 4: Move mouse to wooden_box (recovery)
        success = self.pick_and_place(self.mouse, self.wooden_box)
        print("Pick place mouse (recovery):", success)
        if not success:
            return self.info

        # Step 5: Place cup_with_handle in wooden_box
        success = self.pick_and_place(self.cup_with_handle, self.wooden_box)
        print("Pick place cup_with_handle:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the final arrangement meets the task requirements:
        - stapler and screwdriver on tray
        - mouse and cup_with_handle in wooden_box
        """
        if (self.check_on(self.stapler, self.tray) and
            self.check_on(self.screwdriver, self.tray) and
            self.check_on(self.mouse, self.wooden_box) and
            self.check_on(self.cup_with_handle, self.wooden_box)):
            return True
        return False
