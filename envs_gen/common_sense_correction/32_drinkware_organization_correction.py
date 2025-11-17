from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 32_drinkware_organization_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes containers (coaster, tray) and objects (mug, can, cup_without_handle, stapler, shoe).
        Distractors are also added to simulate a realistic environment.
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.tray = self.add_actor("tray", "tray")

        # Add objects
        self.mug = self.add_actor("mug", "mug")
        self.can = self.add_actor("can", "can")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.stapler = self.add_actor("stapler", "stapler")
        self.shoe = self.add_actor("shoe", "shoe")

        # Add distractors
        distractor_list = ['fluted_block', 'alarm-clock', 'tissue-box', 'dumbbell', 'toycar', 'pot-with-plant']
        self.add_distractors(distractor_list)

        # Final check to ensure all actors are placed correctly
        self.check_scene()

    def play_once(self):
        """
        Define the sequence of actions the robot arm should perform.
        This includes a wrong action and a recovery step, followed by correct placements.
        """
        # Wrong action: Place mug into tray (incorrect)
        success = self.pick_and_place(self.mug, self.tray)
        print("Wrong: mug to tray:", success)
        if not success:
            return self.info

        # Recovery: Move mug from tray to coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Recovery: mug to coaster:", success)
        if not success:
            return self.info

        # Correct actions
        success = self.pick_and_place(self.can, self.coaster)
        print("can to coaster:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("cup_without_handle to coaster:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.stapler, self.tray)
        print("stapler to tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.shoe, self.tray)
        print("shoe to tray:", success)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        All drinkware (mug, can, cup_without_handle) should be on the coaster.
        All non-drinkware (stapler, shoe) should be on the tray.
        """
        if (self.check_on(self.mug, self.coaster) and
            self.check_on(self.can, self.coaster) and
            self.check_on(self.cup_without_handle, self.coaster) and
            self.check_on(self.stapler, self.tray) and
            self.check_on(self.shoe, self.tray)):
            return True
        return False
