from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 485_drinkware_and_toy_blocks_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        - Containers: coaster and plate
        - Objects: can, cup, green_block, blue_block, purple_block
        - Distractors: alarm-clock, stapler, dumbbell, battery, pot-with-plant
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.plate = self.add_actor("plate", "plate")
        
        # Add objects
        self.can = self.add_actor("can", "can")
        self.cup = self.add_actor("cup", "cup")
        self.green_block = self.add_actor("green_block", "green_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        
        # Add distractors
        distractor_list = ['alarm-clock', 'stapler', 'dumbbell', 'battery', 'pot-with-plant']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task:
        1. Place the can on the coaster
        2. Place the cup on the coaster
        3. Place the green_block on the plate
        4. Place the blue_block on the plate
        5. Place the purple_block on the plate
        """
        # Place can on coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("pick place can:", success)
        if not success:
            return self.info

        # Place cup on coaster
        success = self.pick_and_place(self.cup, self.coaster)
        print("pick place cup:", success)
        if not success:
            return self.info

        # Place green_block on plate
        success = self.pick_and_place(self.green_block, self.plate)
        print("pick place green_block:", success)
        if not success:
            return self.info

        # Place blue_block on plate
        success = self.pick_and_place(self.blue_block, self.plate)
        print("pick place blue_block:", success)
        if not success:
            return self.info

        # Place purple_block on plate
        success = self.pick_and_place(self.purple_block, self.plate)
        print("pick place purple_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Can and cup are on the coaster
        - Green_block, blue_block, and purple_block are on the plate
        """
        return (
            self.check_on(self.can, self.coaster) and
            self.check_on(self.cup, self.coaster) and
            self.check_on(self.green_block, self.plate) and
            self.check_on(self.blue_block, self.plate) and
            self.check_on(self.purple_block, self.plate)
        )
