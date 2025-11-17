from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 177_place_small_toys_and_stationery_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Containers: fluted_block
        - Objects: dumbbell, red_block, purple_block, markpen
        - Distractors: pot-with-plant, shoe, shampoo, baguette, alarm-clock
        """
        # Add the organizer container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add small solid toys and stationery
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.red_block = self.add_actor("red_block", "red_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.markpen = self.add_actor("markpen", "markpen")
        
        # Add distractor objects
        distractor_list = ['pot-with-plant', 'shoe', 'shampoo', 'baguette', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the simulation:
        1. Wrong action: Place dumbbell into fluted_block
        2. Recovery: Remove dumbbell from fluted_block and place on table
        3. Correct actions: Place red_block, purple_block, and markpen into fluted_block
        """
        # Wrong action: Place dumbbell into fluted_block
        success = self.pick_and_place(self.dumbbell, self.fluted_block)
        print("Pick place dumbbell (wrong):", success)
        if not success:
            return self.info

        # Recovery: Place dumbbell back on table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Recover dumbbell:", success)
        if not success:
            return self.info

        # Correct action: Place red_block into fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Pick place red_block:", success)
        if not success:
            return self.info

        # Correct action: Place purple_block into fluted_block
        success = self.pick_and_place(self.purple_block, self.fluted_block)
        print("Pick place purple_block:", success)
        if not success:
            return self.info

        # Correct action: Place markpen into fluted_block
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Pick place markpen:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - red_block, purple_block, and markpen are in fluted_block
        - dumbbell is NOT in fluted_block
        """
        if (self.check_on(self.red_block, self.fluted_block) and
            self.check_on(self.purple_block, self.fluted_block) and
            self.check_on(self.markpen, self.fluted_block) and
            not self.check_on(self.dumbbell, self.fluted_block)):
            return True
        return False
