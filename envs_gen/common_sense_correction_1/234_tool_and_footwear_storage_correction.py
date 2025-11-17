from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 234_tool_and_footwear_storage_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Create the wooden box as a container
        - Create the required objects: drill, shoe, bread, green_block
        - Add the specified distractor objects
        """
        # Create the wooden box container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Create the required objects
        self.drill = self.add_actor("drill", "drill")
        self.shoe = self.add_actor("shoe", "shoe")
        self.bread = self.add_actor("bread", "bread")
        self.green_block = self.add_actor("green_block", "green_block")
        
        # Add the specified distractor objects
        distractor_list = ["alarm-clock", "book", "pot-with-plant", "tissue-box", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Place drill inside wooden_box
        2. Place green_block inside wooden_box (wrong placement)
        3. Recover by placing green_block on top of wooden_box
        4. Place shoe inside wooden_box
        5. Place bread on top of wooden_box
        """
        # Place drill inside wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Place drill:", success)
        if not success:
            return self.info
            
        # Place green_block inside wooden_box (wrong placement)
        success = self.pick_and_place(self.green_block, self.wooden_box)
        print("Place green_block (wrong):", success)
        if not success:
            return self.info
            
        # Recover by placing green_block on top of wooden_box
        success = self.pick_and_place(self.green_block, self.wooden_box)
        print("Place green_block (recovery):", success)
        if not success:
            return self.info
            
        # Place shoe inside wooden_box
        success = self.pick_and_place(self.shoe, self.wooden_box)
        print("Place shoe:", success)
        if not success:
            return self.info
            
        # Place bread on top of wooden_box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Place bread:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully by checking:
        - Drill and shoe are inside the wooden_box
        - Green_block and bread are on top of the wooden_box
        """
        # Check if all required objects are on the wooden_box
        # Note: The API's check_on function is used for both inside and on-top placements
        return (
            self.check_on(self.drill, self.wooden_box) and
            self.check_on(self.shoe, self.wooden_box) and
            self.check_on(self.green_block, self.wooden_box) and
            self.check_on(self.bread, self.wooden_box)
        )
