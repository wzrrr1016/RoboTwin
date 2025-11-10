from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class color_block_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Load the containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Load the blocks
        for block in self.blocks:
            self.blocks[block] = self.add_actor("block", block)

    def play_once(self):
        # Define the order of blocks to be placed
        block_order = ['red_block', 'blue_block', 'green_block', 'yellow_block', 'purple_block', 'orange_block']

        for block_name in block_order:
            block = self.blocks[block_name]

            # Pick the block
            success = self.pick_and_place(block, self.coaster if block_name in ['red_block', 'green_block', 'yellow_block'] else self.wooden_box)
            if not success:
                print(f"Failed to pick and place {block_name}")
                return self.info

            # Check if the block is on the correct container
            if block_name in ['red_block', 'green_block', 'yellow_block']:
                if not self.check_on(block, self.coaster):
                    print(f"Block {block_name} is not on the coaster")
                    return self.info
            else:
                if not self.check_on(block, self.wooden_box):
                    print(f"Block {block_name} is not on the wooden_box")
                    return self.info

        return self.info

    def check_success(self):
        # Check if all blocks are in the correct container
        for block_name, block in self.blocks.items():
            if block_name in ['red_block', 'green_block', 'yellow_block']:
                if not self.check_on(block, self.coaster):
                    return False
            else:
                if not self.check_on(block, self.wooden_box):
                    return False

        return True
