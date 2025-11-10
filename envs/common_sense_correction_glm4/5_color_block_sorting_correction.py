from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class color_block_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Load the wooden box and table actors
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.table = self.add_actor("table", "table")

        # Load the color blocks
        for block in self.blocks:
            self.add_actor("block", block)

    def play_once(self):
        # Define the sequence of actions to sort the blocks
        for block in self.blocks:
            # Pick the block
            success = self.pick_and_place(block, self.wooden_box if block in ["blue_block", "green_block"] else self.table)
            if not success:
                print(f"Failed to pick and place {block}.")
                return self.info

    def check_success(self):
        # Check if all primary color blocks are in the wooden box
        primary_blocks_in_box = all(self.check_on(block, self.wooden_box) for block in ["blue_block", "green_block"])
        # Check if all secondary color blocks are on the table
        secondary_blocks_on_table = all(self.check_on(block, self.table) for block in ["red_block", "yellow_block", "orange_block"])

        return primary_blocks_in_box and secondary_blocks_on_table

    def pick_and_place(self, object, container):
        # Check if the object is already on the container
        if self.check_on(object, container):
            return True

        # Pick the object
        if not self.check_grasp(object):
            print(f"Failed to grasp {object}.")
            return False

        # Place the object in the container
        success = self.play_once()
        if not success:
            print(f"Failed to place {object} in {container}.")
            return False

        return True

    def check_on(self, object, container):
        # Check if the object is on the container
        # This function should be implemented based on the available API
        pass

    def check_grasp(self, object):
        # Check if the object is grasped by the arm
        # This function should be implemented based on the available API
        pass
