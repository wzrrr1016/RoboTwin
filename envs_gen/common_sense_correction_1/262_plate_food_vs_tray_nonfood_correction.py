from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 262_plate_food_vs_tray_nonfood_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Containers: plate and tray
        - Objects: apple, french_fries, bottle, screwdriver
        - Distractors: calculator, pet-collar, pot-with-plant, alarm-clock, shoe
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.tray = self.add_actor("tray", "tray")

        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.bottle = self.add_actor("bottle", "bottle")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

        # Add distractors
        distractor_list = ["calculator", "pet-collar", "pot-with-plant", "alarm-clock", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm:
        1. Place apple on the plate
        2. Place french_fries on the plate
        3. Place screwdriver on the tray
        4. (Wrong action) Place bottle on the plate
        5. (Recovery action) Move bottle from plate to tray
        """
        # Place apple on the plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Place apple on plate:", success)
        if not success:
            return self.info

        # Place french_fries on the plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french_fries on plate:", success)
        if not success:
            return self.info

        # Place screwdriver on the tray
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("Place screwdriver on tray:", success)
        if not success:
            return self.info

        # Wrong action: Place bottle on the plate
        success = self.pick_and_place(self.bottle, self.plate)
        print("Wrong: Place bottle on plate:", success)
        if not success:
            return self.info

        # Recovery action: Move bottle to the tray
        success = self.pick_and_place(self.bottle, self.tray)
        print("Recovery: Place bottle on tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed:
        - Perishable and ready-to-eat foods (apple, french_fries) are on the plate
        - Tools and drink containers (screwdriver, bottle) are on the tray
        """
        if (
            self.check_on(self.apple, self.plate) and
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.screwdriver, self.tray) and
            self.check_on(self.bottle, self.tray)
        ):
            return True
        return False
