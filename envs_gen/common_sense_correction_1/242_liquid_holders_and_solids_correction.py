from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 242_liquid_holders_and_solids_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Containers: coaster and plate
        - Objects: cup, can, blue_block, pot-with-plant
        - Distractors: calculator, screwdriver, hammer, alarm-clock, stapler
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.plate = self.add_actor("plate", "plate")

        # Add objects
        self.cup = self.add_actor("cup", "cup")
        self.can = self.add_actor("can", "can")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

        # Add distractors
        distractors = ["calculator", "screwdriver", "hammer", "alarm-clock", "stapler"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        - Place cup on coaster
        - Place can on plate (wrong action)
        - Recover can to coaster
        - Place blue_block on plate
        - Place pot-with-plant on plate
        """
        # Step 1: Place cup on coaster
        success = self.pick_and_place(self.cup, self.coaster)
        print("Place cup on coaster:", success)
        if not success:
            return self.info

        # Step 2: Place can on plate (wrong action)
        success = self.pick_and_place(self.can, self.plate)
        print("Place can on plate (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover can to coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Recover can to coaster:", success)
        if not success:
            return self.info

        # Step 4: Place blue_block on plate
        success = self.pick_and_place(self.blue_block, self.plate)
        print("Place blue block on plate:", success)
        if not success:
            return self.info

        # Step 5: Place pot-with-plant on plate
        success = self.pick_and_place(self.pot_with_plant, self.plate)
        print("Place pot-with-plant on plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Cup and can (liquid holders) are on the coaster
        - Blue_block and pot-with-plant (solid decorative or toy objects) are on the plate
        """
        if (
            self.check_on(self.cup, self.coaster) and
            self.check_on(self.can, self.coaster) and
            self.check_on(self.blue_block, self.plate) and
            self.check_on(self.pot_with_plant, self.plate)
        ):
            return True
        return False
