from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 72_place_liquid_and_personalcare_on_plate_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Containers: plate
        - Objects: shampoo, bottle, knife, scanner
        - Distractors: apple, bread, red_block, markpen, bell
        """
        # Add the plate (container)
        self.plate = self.add_actor("plate", "plate")

        # Add required objects
        self.shampoo = self.add_actor("shampoo", "shampoo_0")
        self.bottle = self.add_actor("bottle", "bottle_0")
        self.knife = self.add_actor("knife", "knife_0")
        self.scanner = self.add_actor("scanner", "scanner_0")

        # Add distractors
        distractor_list = ["apple", "bread", "red_block", "markpen", "bell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm:
        1. Place shampoo on the plate
        2. Place bottle on the plate
        3. (Incorrectly) place knife on the plate
        4. Recover by placing knife on the table
        5. Place scanner on the table
        """
        # Place shampoo on the plate
        success = self.pick_and_place(self.shampoo, self.plate)
        print("Place shampoo on plate:", success)
        if not success:
            return self.info

        # Place bottle on the plate
        success = self.pick_and_place(self.bottle, self.plate)
        print("Place bottle on plate:", success)
        if not success:
            return self.info

        # Incorrectly place knife on the plate
        success = self.pick_and_place(self.knife, self.plate)
        print("Place knife on plate (wrong):", success)
        if not success:
            return self.info

        # Recovery: place knife on the table
        success = self.pick_and_place(self.knife, self.table)
        print("Recover knife to table:", success)
        if not success:
            return self.info

        # Place scanner on the table
        success = self.pick_and_place(self.scanner, self.table)
        print("Place scanner on table:", success)
        if not success:
            return self.info

        return self.info  # All actions completed successfully

    def check_success(self):
        """
        Check if the task was completed successfully:
        - Shampoo and bottle are on the plate
        - Knife and scanner are NOT on the plate
        """
        # Check if shampoo and bottle are on the plate
        shampoo_on_plate = self.check_on(self.shampoo, self.plate)
        bottle_on_plate = self.check_on(self.bottle, self.plate)

        # Check if knife and scanner are NOT on the plate
        knife_not_on_plate = not self.check_on(self.knife, self.plate)
        scanner_not_on_plate = not self.check_on(self.scanner, self.plate)

        # Return True if all conditions are met
        return all([shampoo_on_plate, bottle_on_plate, knife_not_on_plate, scanner_not_on_plate])
