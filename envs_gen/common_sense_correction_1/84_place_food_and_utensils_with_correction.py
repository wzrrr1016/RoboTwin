from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 84_place_food_and_utensils_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        Includes the plate, edible foods, eating utensils, and distractors.
        """
        # Add the plate as a container
        self.plate = self.add_actor("plate", "plate")

        # Add edible foods
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.french_fries = self.add_actor("french_fries", "french_fries")

        # Add eating utensil
        self.fork = self.add_actor("fork", "fork")

        # Add a non-edible object (screwdriver) that will be mistakenly placed and then removed
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

        # Add distractors to the environment
        distractor_list = ["calculator", "toycar", "book", "shoe", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        Includes placing edible foods and utensils on the plate,
        placing a wrong object on the plate and then recovering it.
        """
        # Place hamburg on the plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Pick hamburg:", success)
        if not success:
            return self.info

        # Place french_fries on the plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Pick french_fries:", success)
        if not success:
            return self.info

        # Place screwdriver on the plate (wrong action)
        success = self.pick_and_place(self.screwdriver, self.plate)
        print("Pick screwdriver (wrong):", success)
        if not success:
            return self.info

        # Recover screwdriver by placing it on the table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Recover screwdriver:", success)
        if not success:
            return self.info

        # Place fork on the plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Pick fork:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The success condition is:
        - hamburg is on the plate
        - french_fries is on the plate
        - fork is on the plate
        - screwdriver is NOT on the plate
        """
        if (
            self.check_on(self.hamburg, self.plate) and
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.fork, self.plate) and
            not self.check_on(self.screwdriver, self.plate)
        ):
            return True
        return False
