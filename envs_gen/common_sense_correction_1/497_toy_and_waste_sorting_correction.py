from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 497_toy_and_waste_sorting_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes containers, objects, and distractors.
        """
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects to be manipulated
        self.green_block = self.add_actor("green_block", "green_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.can = self.add_actor("can", "can")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")

        # Add distractors
        distractor_list = ["calculator", "pot-with-plant", "hammer", "alarm-clock", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        This includes placing toys in the wooden_box and waste in the dustbin.
        """
        # Place green block into wooden box
        success = self.pick_and_place(self.green_block, self.wooden_box)
        print("Place green_block:", success)
        if not success:
            return self.info

        # Wrong placement of can into wooden box
        success = self.pick_and_place(self.can, self.wooden_box)
        print("Wrong can placement:", success)
        if not success:
            return self.info

        # Recovery: move can to dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        print("Recover can:", success)
        if not success:
            return self.info

        # Place tissue-box into dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Place tissue-box:", success)
        if not success:
            return self.info

        # Place red and blue blocks into wooden box
        success = self.pick_and_place(self.red_block, self.wooden_box)
        print("Place red_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.blue_block, self.wooden_box)
        print("Place blue_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        This includes verifying that all toys are in the wooden_box
        and all waste items are in the dustbin.
        """
        # Check if all toys are in the wooden_box
        toys_in_wooden = (
            self.check_on(self.green_block, self.wooden_box) and
            self.check_on(self.red_block, self.wooden_box) and
            self.check_on(self.blue_block, self.wooden_box)
        )

        # Check if all waste items are in the dustbin
        waste_in_dustbin = (
            self.check_on(self.can, self.dustbin) and
            self.check_on(self.tissue_box, self.dustbin)
        )

        return toys_in_wooden and waste_in_dustbin
