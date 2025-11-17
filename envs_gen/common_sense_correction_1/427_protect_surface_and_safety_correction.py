from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 427_protect_surface_and_safety_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Containers: coaster, dustbin
        Objects: cup_with_handle, fork, cup, knife
        Distractors: toycar, book, alarm-clock, shoe, red_block
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.fork = self.add_actor("fork", "fork")
        self.cup = self.add_actor("cup", "cup")
        self.knife = self.add_actor("knife", "knife")

        # Add distractors
        distractor_list = ['toycar', 'book', 'alarm-clock', 'shoe', 'red_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        Actions:
        1. Place cup_with_handle on coaster
        2. Place fork into dustbin (wrong action)
        3. Recover fork from dustbin to coaster
        4. Place cup on coaster
        5. Place knife into dustbin
        """
        # Step 1: Place cup_with_handle on coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle on coaster:", success)
        if not success:
            return self.info

        # Step 2: Place fork into dustbin (wrong action)
        success = self.pick_and_place(self.fork, self.dustbin)
        print("Place fork into dustbin:", success)
        if not success:
            return self.info

        # Step 3: Recover fork from dustbin to coaster
        success = self.pick_and_place(self.fork, self.coaster)
        print("Recover fork to coaster:", success)
        if not success:
            return self.info

        # Step 4: Place cup on coaster
        success = self.pick_and_place(self.cup, self.coaster)
        print("Place cup on coaster:", success)
        if not success:
            return self.info

        # Step 5: Place knife into dustbin
        success = self.pick_and_place(self.knife, self.dustbin)
        print("Place knife into dustbin:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        Success conditions:
        - cup_with_handle and cup are on the coaster
        - fork is on the coaster (after recovery)
        - knife is in the dustbin
        """
        if (
            self.check_on(self.cup_with_handle, self.coaster) and
            self.check_on(self.cup, self.coaster) and
            self.check_on(self.fork, self.coaster) and
            self.check_on(self.knife, self.dustbin)
        ):
            return True
        return False
