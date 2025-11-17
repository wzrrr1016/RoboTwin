from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 351_office_items_organizing_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Adds the fluted_block container and the relevant objects (markpen, mouse, scanner, screwdriver).
        Adds distractors as specified in the task description.
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add required objects
        self.markpen = self.add_actor("markpen", "markpen")
        self.mouse = self.add_actor("mouse", "mouse")
        self.scanner = self.add_actor("scanner", "scanner")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        
        # Add distractors
        distractor_list = ["apple", "baguette", "toycar", "pot-with-plant", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Place markpen into fluted_block
        2. Place mouse into fluted_block
        3. Place screwdriver into fluted_block (wrong action)
        4. Place screwdriver on the table (recovery)
        5. Place scanner into fluted_block
        """
        # Place markpen into fluted_block
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("markpen placed:", success)
        if not success:
            return self.info

        # Place mouse into fluted_block
        success = self.pick_and_place(self.mouse, self.fluted_block)
        print("mouse placed:", success)
        if not success:
            return self.info

        # Wrong placement of screwdriver into fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("screwdriver wrong placement:", success)

        # Recovery: Place screwdriver on the table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("screwdriver recovery:", success)
        if not success:
            return self.info

        # Place scanner into fluted_block
        success = self.pick_and_place(self.scanner, self.fluted_block)
        print("scanner placed:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully:
        - markpen, mouse, and scanner are in the fluted_block
        - screwdriver is not in the fluted_block
        """
        markpen_in = self.check_on(self.markpen, self.fluted_block)
        mouse_in = self.check_on(self.mouse, self.fluted_block)
        scanner_in = self.check_on(self.scanner, self.fluted_block)
        screwdriver_not_in = not self.check_on(self.screwdriver, self.fluted_block)
        
        return markpen_in and mouse_in and scanner_in and screwdriver_not_in
