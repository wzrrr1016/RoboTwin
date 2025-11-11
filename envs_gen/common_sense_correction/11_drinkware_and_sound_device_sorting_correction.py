from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 11_drinkware_and_sound_device_sorting_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes containers, target objects, and distractors.
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add target objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")

        # Add distractors as specified in the task description
        distractor_list = ['pot-with-plant', 'tissue-box', 'dumbbell', 'markerpen', 'book']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        This includes placing objects on the correct containers and correcting
        any wrong placements.
        """
        # Step 1: Place cup_with_handle on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle on coaster:", success)
        if not success:
            return self.info

        # Step 2: Wrongly place small-speaker on coaster
        success = self.pick_and_place(self.small_speaker, self.coaster)
        print("Wrongly place small-speaker on coaster:", success)
        if not success:
            return self.info

        # Step 3: Recovery - move small-speaker to dustbin
        success = self.pick_and_place(self.small_speaker, self.dustbin)
        print("Recover: place small-speaker into dustbin:", success)
        if not success:
            return self.info

        # Step 4: Place cup_without_handle on coaster
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("Place cup_without_handle on coaster:", success)
        if not success:
            return self.info

        # Step 5: Place alarm-clock into dustbin
        success = self.pick_and_place(self.alarm_clock, self.dustbin)
        print("Place alarm-clock into dustbin:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions
        of all relevant objects.
        """
        if (
            self.check_on(self.cup_with_handle, self.coaster) and
            self.check_on(self.cup_without_handle, self.coaster) and
            self.check_on(self.small_speaker, self.dustbin) and
            self.check_on(self.alarm_clock, self.dustbin)
        ):
            return True
        return False
