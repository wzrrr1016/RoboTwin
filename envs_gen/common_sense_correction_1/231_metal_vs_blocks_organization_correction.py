from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 231_metal_vs_blocks_organization_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Adds containers, target objects, and distractors as specified in the task.
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add target objects
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.stapler = self.add_actor("stapler", "stapler")
        self.bell = self.add_actor("bell", "bell")
        
        # Add distractors
        distractor_list = ["pot-with-plant", "shoe", "baguette", "apple"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions to complete the task:
        1. Place stapler (office item) in wooden_box
        2. Place bell (metal item) on fluted_block (wrong placement)
        3. Recover bell and place it in wooden_box
        4. Place all toy blocks on fluted_block
        """
        # Place stapler (office item) in wooden_box
        success = self.pick_and_place(self.stapler, self.wooden_box)
        print("Place stapler:", success)
        if not success:
            return self.info

        # Wrongly place bell (metal item) on fluted_block
        success = self.pick_and_place(self.bell, self.fluted_block)
        print("Wrong bell placement:", success)
        if not success:
            return self.info

        # Recover bell and place it in wooden_box
        success = self.pick_and_place(self.bell, self.wooden_box)
        print("Recover bell:", success)
        if not success:
            return self.info

        # Place toy blocks on fluted_block
        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Place blue block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Place green block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Place red block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Metal and office items are in wooden_box
        - Toy blocks are on fluted_block
        """
        # Check if metal and office items are in wooden_box
        # and toy blocks are on fluted_block
        if (self.check_on(self.stapler, self.wooden_box) and
            self.check_on(self.bell, self.wooden_box) and
            self.check_on(self.blue_block, self.fluted_block) and
            self.check_on(self.green_block, self.fluted_block) and
            self.check_on(self.red_block, self.fluted_block)):
            return True
        return False
