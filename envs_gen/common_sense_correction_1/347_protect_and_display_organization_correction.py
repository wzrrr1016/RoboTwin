from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 347_protect_and_display_organization_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        Adds containers, objects, and distractors as specified in the task description.
        """
        # Add containers to the environment
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects to the environment
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.apple = self.add_actor("apple", "apple")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.green_block = self.add_actor("green_block", "green_block")

        # Add distractors to the environment
        distractor_list = ['stapler', 'markpen', 'tissue-box', 'dumbbell']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of robot actions to complete the task.
        Includes both correct and recovery actions as specified in the task description.
        """
        # Place decorative living items and toys on the fluted_block (flat organizer)
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Place pot-with-plant on fluted_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Place blue_block on fluted_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Place green_block on fluted_block:", success)
        if not success:
            return self.info

        # Wrong placement of small-speaker on fluted_block (decorative items container)
        success = self.pick_and_place(self.small_speaker, self.fluted_block)
        print("Wrong placement of small-speaker on fluted_block:", success)
        if not success:
            return self.info

        # Recovery: Move small-speaker to shoe_box (small electronics container)
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        print("Recovery: Place small-speaker into shoe_box:", success)
        if not success:
            return self.info

        # Place apple (perishable food) into shoe_box
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Place apple into shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task is successfully completed by verifying the final positions of all objects.
        Returns True if all objects are in their correct containers, False otherwise.
        """
        # Check if decorative items and toys are on the fluted_block
        on_fluted_block = (
            self.check_on(self.pot_with_plant, self.fluted_block) and
            self.check_on(self.blue_block, self.fluted_block) and
            self.check_on(self.green_block, self.fluted_block)
        )

        # Check if small electronics and perishable food are in the shoe_box
        in_shoe_box = (
            self.check_on(self.small_speaker, self.shoe_box) and
            self.check_on(self.apple, self.shoe_box)
        )

        # Return True if all conditions are met
        return on_fluted_block and in_shoe_box
