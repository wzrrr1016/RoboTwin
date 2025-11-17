from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 249_drinkware_on_organizer_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        Includes containers, objects, and distractors.
        """
        # Add containers to the environment
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects to be sorted
        self.cup = self.add_actor("cup", "cup")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.can = self.add_actor("can", "can")
        self.apple = self.add_actor("apple", "apple")
        self.mouse = self.add_actor("mouse", "mouse")

        # Add distractor objects
        distractor_list = ['calculator', 'alarm-clock', 'sand-clock', 'small-speaker', 'microphone']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's sorting actions in sequence.
        Includes error correction for initial wrong placement.
        """
        # Initial wrong placement (part of the task sequence)
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple on fluted_block (wrong):", success)
        if not success:
            return self.info

        # Recovery action - move apple to correct container
        if self.check_on(self.apple, self.fluted_block):
            success = self.pick_and_place(self.apple, self.wooden_box)
            print("Recover apple to wooden_box:", success)
            if not success:
                return self.info

        # Place drinkware items on organizer surface
        success = self.pick_and_place(self.cup, self.fluted_block)
        print("Place cup:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup_without_handle, self.fluted_block)
        print("Place cup without handle:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.can, self.fluted_block)
        print("Place can:", success)
        if not success:
            return self.info

        # Place non-drinkware item in storage box
        success = self.pick_and_place(self.mouse, self.wooden_box)
        print("Place mouse:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if all objects are placed in their correct containers.
        Returns True if all conditions are met, False otherwise.
        """
        # Check drinkware items are on fluted_block
        drinkware_correct = (
            self.check_on(self.cup, self.fluted_block) and
            self.check_on(self.cup_without_handle, self.fluted_block) and
            self.check_on(self.can, self.fluted_block)
        )

        # Check non-drinkware items are in wooden_box
        non_drinkware_correct = (
            self.check_on(self.apple, self.wooden_box) and
            self.check_on(self.mouse, self.wooden_box)
        )

        return drinkware_correct and non_drinkware_correct
