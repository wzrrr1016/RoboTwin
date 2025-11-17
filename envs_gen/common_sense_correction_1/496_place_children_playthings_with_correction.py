from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 496_place_children_playthings_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Containers: plate
        - Objects: red_block, green_block, toycar, cup
        - Distractors: hammer, book, apple, pot-with-plant, alarm-clock
        """
        # Add the plate container
        self.plate = self.add_actor("plate", "plate")
        
        # Add the target objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.toycar = self.add_actor("toycar", "toycar")
        self.cup = self.add_actor("cup", "cup")
        
        # Add distractor objects
        distractor_list = ["hammer", "book", "apple", "pot-with-plant", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of robot actions:
        1. Pick red_block and place on plate
        2. Pick cup and place on plate (wrong action)
        3. Pick cup from plate and place on table (recovery)
        4. Pick green_block and place on plate
        5. Pick toycar and place on plate
        """
        # Step 1: Place red_block on plate
        success = self.pick_and_place(self.red_block, self.plate)
        print("Pick red_block:", success)
        if not success:
            return self.info

        # Step 2: Place cup on plate (wrong action)
        success = self.pick_and_place(self.cup, self.plate)
        print("Pick cup (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing cup on table
        success = self.pick_and_place(self.cup, self.table)
        print("Recover cup:", success)
        if not success:
            return self.info

        # Step 4: Place green_block on plate
        success = self.pick_and_place(self.green_block, self.plate)
        print("Pick green_block:", success)
        if not success:
            return self.info

        # Step 5: Place toycar on plate
        success = self.pick_and_place(self.toycar, self.plate)
        print("Pick toycar:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was successfully completed by verifying:
        - red_block is on the plate
        - green_block is on the plate
        - toycar is on the plate
        """
        return (
            self.check_on(self.red_block, self.plate) and
            self.check_on(self.green_block, self.plate) and
            self.check_on(self.toycar, self.plate)
        )
