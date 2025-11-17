from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 391_organize_light_toys_keep_drinks_out_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Adds the fluted_block as the container, the three colorful blocks and the can as objects,
        and the specified distractors.
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add the objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.can = self.add_actor("can", "can")
        
        # Add distractors
        distractor_list = ["pot-with-plant", "book", "shoe", "baguette"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the environment:
        1. Attempt to place the can into the fluted_block (wrong action).
        2. If the can is in the fluted_block, recover by placing it on the table.
        3. Place the red, green, and pink blocks into the fluted_block.
        """
        # Step 1: Wrong action - place can into fluted_block
        success = self.pick_and_place(self.can, self.fluted_block)
        print("Wrong placement of can:", success)
        
        # Step 2: Recovery - place can on the table if it's in the fluted_block
        if self.check_on(self.can, self.fluted_block):
            success = self.pick_and_place(self.can, self.table)
            print("Recovery of can:", success)
            if not success:
                return self.info
        
        # Step 3: Place the blocks into the fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Place red_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Place green_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.pink_block, self.fluted_block)
        print("Place pink_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully:
        - All colorful blocks are in the fluted_block.
        - The can is not in the fluted_block.
        """
        # Check if all blocks are in the fluted_block
        blocks_in = (
            self.check_on(self.red_block, self.fluted_block) and
            self.check_on(self.green_block, self.fluted_block) and
            self.check_on(self.pink_block, self.fluted_block)
        )
        
        # Check if the can is not in the fluted_block
        can_not_in = not self.check_on(self.can, self.fluted_block)
        
        return blocks_in and can_not_in
