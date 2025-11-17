from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 271_drinkware_organizer_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the environment.
        - Containers: fluted_block
        - Objects: cup_with_handle, cup_without_handle, can, small-speaker
        - Distractors: calculator, shoe, book, markpen, dumbbell
        """
        # Add the organizer surface (fluted_block)
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add drinkware and sealed beverage containers
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.can = self.add_actor("can", "can")

        # Add the small-speaker (used for wrong placement and recovery)
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")

        # Add distractors to the environment
        distractor_list = ['calculator', 'shoe', 'book', 'markpen', 'dumbbell']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm.
        1. Wrongly place small-speaker on fluted_block
        2. Recover by placing small-speaker on the table
        3. Place all drinkware and sealed beverage containers on fluted_block
        """
        # Step 1: Wrong placement of small-speaker
        success = self.pick_and_place(self.small_speaker, self.fluted_block)
        print("Wrong place small speaker:", success)
        if not success:
            return self.info

        # Step 2: Recovery - place small-speaker on the table
        success = self.pick_and_place(self.small_speaker, self.table)
        print("Recover small speaker:", success)
        if not success:
            return self.info

        # Step 3: Place cup_with_handle on fluted_block
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Place cup with handle:", success)
        if not success:
            return self.info

        # Step 4: Place can on fluted_block
        success = self.pick_and_place(self.can, self.fluted_block)
        print("Place can:", success)
        if not success:
            return self.info

        # Step 5: Place cup_without_handle on fluted_block
        success = self.pick_and_place(self.cup_without_handle, self.fluted_block)
        print("Place cup without handle:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if all required objects are placed on the fluted_block.
        - cup_with_handle
        - can
        - cup_without_handle
        """
        return (
            self.check_on(self.cup_with_handle, self.fluted_block) and
            self.check_on(self.can, self.fluted_block) and
            self.check_on(self.cup_without_handle, self.fluted_block)
        )
