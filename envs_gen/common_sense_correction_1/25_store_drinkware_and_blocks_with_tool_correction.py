from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 25_store_drinkware_and_blocks_with_tool_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        """
        # Add the wooden box container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add drinkware with handles
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.mug = self.add_actor("mug", "mug")
        
        # Add lightweight solid blocks
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        
        # Add the heavy power tool (should not be placed in the box)
        self.drill = self.add_actor("drill", "drill")
        
        # Add distractor objects
        distractor_list = ["calculator", "pet-collar", "chips-tub", "mouse", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of robot actions to complete the task.
        """
        # Place cup with handle in the wooden box
        success = self.pick_and_place(self.cup_with_handle, self.wooden_box)
        print("pick place cup_with_handle:", success)
        if not success:
            return self.info

        # Place blue block in the wooden box
        success = self.pick_and_place(self.blue_block, self.wooden_box)
        print("pick place blue_block:", success)
        if not success:
            return self.info

        # Attempt to place drill in the wooden box (this is a wrong action)
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("pick place drill (wrong):", success)
        
        # If placing drill in box fails (as expected), place it on the table instead
        if not success:
            success = self.pick_and_place(self.drill, self.table)
            print("pick place drill on table:", success)
            if not success:
                return self.info

        # Place mug in the wooden box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("pick place mug:", success)
        if not success:
            return self.info

        # Place purple block in the wooden box
        success = self.pick_and_place(self.purple_block, self.wooden_box)
        print("pick place purple_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        """
        # Check if all required items are in the wooden box
        all_in_box = (
            self.check_on(self.cup_with_handle, self.wooden_box) and
            self.check_on(self.blue_block, self.wooden_box) and
            self.check_on(self.mug, self.wooden_box) and
            self.check_on(self.purple_block, self.wooden_box)
        )
        
        # Check if the drill is NOT in the wooden box
        drill_not_in_box = not self.check_on(self.drill, self.wooden_box)
        
        return all_in_box and drill_not_in_box
