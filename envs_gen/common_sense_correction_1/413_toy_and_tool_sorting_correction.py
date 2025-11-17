from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 413_toy_and_tool_sorting_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Adds containers, target objects, and distractors.
        """
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add required objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

        # Add distractors
        distractor_list = ["apple", "baguette", "tissue-box", "pot-with-plant", "shampoo"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm.
        Includes error handling for failed operations.
        """
        # 1. Place toycar into shoe_box
        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("Place toycar:", success)
        if not success:
            return self.info

        # 2. Place small-speaker into shoe_box (wrong placement)
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        print("Place small-speaker (wrong):", success)
        if not success:
            return self.info

        # 3. Recover: Place small-speaker into wooden_box
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("Recover small-speaker:", success)
        if not success:
            return self.info

        # 4. Place yellow_block into shoe_box
        success = self.pick_and_place(self.yellow_block, self.shoe_box)
        print("Place yellow_block:", success)
        if not success:
            return self.info

        # 5. Place screwdriver into wooden_box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("Place screwdriver:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if all objects are placed in the correct containers.
        Returns True if all conditions are met, False otherwise.
        """
        return (
            self.check_on(self.toycar, self.shoe_box) and
            self.check_on(self.yellow_block, self.shoe_box) and
            self.check_on(self.small_speaker, self.wooden_box) and
            self.check_on(self.screwdriver, self.wooden_box)
        )
