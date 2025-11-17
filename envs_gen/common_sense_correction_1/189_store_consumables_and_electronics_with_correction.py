from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 189_store_consumables_and_electronics_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.bread = self.add_actor("bread", "bread")
        self.bottle = self.add_actor("bottle", "bottle")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")

        # Add distractors
        distractor_list = ["pet-collar", "dumbbell", "book", "markpen"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of robot actions to complete the task.
        Includes a wrong action followed by a recovery step.
        """
        # Wrong action: Place bottle into shoe_box (incorrect)
        success = self.pick_and_place(self.bottle, self.shoe_box)
        print("Place bottle into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Recovery: Pick bottle from shoe_box and place into tray
        success = self.pick_and_place(self.bottle, self.tray)
        print("Recover: Place bottle into tray:", success)
        if not success:
            return self.info

        # Place consumable foods on the tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Place french_fries on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bread, self.tray)
        print("Place bread on tray:", success)
        if not success:
            return self.info

        # Place small electronic/fragile item in shoe_box
        success = self.pick_and_place(self.alarm_clock, self.shoe_box)
        print("Place alarm-clock in shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if all objects are in their correct final positions.
        """
        if (
            self.check_on(self.bottle, self.tray) and
            self.check_on(self.french_fries, self.tray) and
            self.check_on(self.bread, self.tray) and
            self.check_on(self.alarm_clock, self.shoe_box)
        ):
            return True
        return False
