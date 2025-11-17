from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 68_place_play_items_with_tool_misplacement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Containers: tray
        - Objects: drill, hammer, red_block, toycar
        - Distractors: mug, apple, book, bottle, shoe
        """
        # Add the tray container
        self.tray = self.add_actor("tray", "tray")
        
        # Add the main objects involved in the task
        self.drill = self.add_actor("drill", "drill")
        self.hammer = self.add_actor("hammer", "hammer")
        self.red_block = self.add_actor("red_block", "red_block")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractor objects to the environment
        distractor_list = ['mug', 'apple', 'book', 'bottle', 'shoe']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Pick drill and place it into tray (wrong action)
        2. Pick drill from tray and place it onto table (recovery)
        3. Pick red_block and place it into tray
        4. Pick toycar and place it into tray
        """
        # Step 1: Wrong action - Place drill into tray
        success = self.pick_and_place(self.drill, self.tray)
        print("Pick and place drill into tray (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - Place drill back on table
        success = self.pick_and_place(self.drill, self.table)
        print("Recover drill to table:", success)
        if not success:
            return self.info

        # Step 3: Place red_block into tray
        success = self.pick_and_place(self.red_block, self.tray)
        print("Place red_block into tray:", success)
        if not success:
            return self.info

        # Step 4: Place toycar into tray
        success = self.pick_and_place(self.toycar, self.tray)
        print("Place toycar into tray:", success)
        if not success:
            return self.info

        return self.info  # All steps completed successfully

    def check_success(self):
        """
        Check if the task was successful by verifying:
        - red_block is on the tray
        - toycar is on the tray
        """
        # The task is to place play items (red_block and toycar) on the tray
        if self.check_on(self.red_block, self.tray) and self.check_on(self.toycar, self.tray):
            return True
        return False
