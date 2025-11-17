from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 412_safety_and_food_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        Adds the tray and shoe_box as containers, and the relevant objects.
        Adds distractors to the environment.
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.bottle = self.add_actor("bottle", "bottle")
        self.can = self.add_actor("can", "can")
        self.knife = self.add_actor("knife", "knife")
        self.toycar = self.add_actor("toycar", "toycar")

        # Add distractors
        distractors = ["book", "pot-with-plant", "alarm-clock", "tissue-box", "dumbbell"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        Includes a recovery step for the can that was initially placed in the wrong container.
        """
        # Place edible items and drink containers on the tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Place french fries on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bottle, self.tray)
        print("Place bottle on tray:", success)
        if not success:
            return self.info

        # Wrong placement of can into shoe_box
        success = self.pick_and_place(self.can, self.shoe_box)
        print("Place can into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Recovery step: move can from shoe_box to tray
        success = self.pick_and_place(self.can, self.tray)
        print("Recover can to tray:", success)
        if not success:
            return self.info

        # Place sharp or small loose items into the shoe_box
        success = self.pick_and_place(self.knife, self.shoe_box)
        print("Place knife into shoe_box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("Place toycar into shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions of all relevant objects.
        """
        # Check if edible items and drink containers are on the tray
        on_tray = (
            self.check_on(self.french_fries, self.tray) and
            self.check_on(self.bottle, self.tray) and
            self.check_on(self.can, self.tray)
        )

        # Check if sharp or small loose items are in the shoe_box
        in_shoe_box = (
            self.check_on(self.knife, self.shoe_box) and
            self.check_on(self.toycar, self.shoe_box)
        )

        # Return True if all conditions are met
        return on_tray and in_shoe_box
