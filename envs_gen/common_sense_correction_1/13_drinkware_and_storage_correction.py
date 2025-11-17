from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 13_drinkware_and_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.mug = self.add_actor("mug", "mug")
        self.red_block = self.add_actor("red_block", "red_block")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        
        # Add distractors
        distractor_list = ["calculator", "pet-collar", "alarm-clock", "tissue-box", "microphone"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place cup_with_handle on tray
        success = self.pick_and_place(self.cup_with_handle, self.tray)
        print("Place cup_with_handle on tray:", success)
        if not success:
            return self.info

        # Step 2: Place mug on tray
        success = self.pick_and_place(self.mug, self.tray)
        print("Place mug on tray:", success)
        if not success:
            return self.info

        # Step 3: Place red_block on tray (wrong action)
        success = self.pick_and_place(self.red_block, self.tray)
        print("Place red_block on tray (wrong):", success)
        if not success:
            return self.info

        # Step 4: Move red_block from tray to shoe_box (recovery)
        success = self.pick_and_place(self.red_block, self.shoe_box)
        print("Move red_block to shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place dumbbell in shoe_box
        success = self.pick_and_place(self.dumbbell, self.shoe_box)
        print("Place dumbbell in shoe_box:", success)
        if not success:
            return self.info

        return self.info  # Task completed successfully

    def check_success(self):
        # Verify all objects are in their correct containers
        if (self.check_on(self.cup_with_handle, self.tray) and
            self.check_on(self.mug, self.tray) and
            self.check_on(self.red_block, self.shoe_box) and
            self.check_on(self.dumbbell, self.shoe_box)):
            return True
        return False
