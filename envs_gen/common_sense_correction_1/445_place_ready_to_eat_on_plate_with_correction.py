from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 445_place_ready_to_eat_on_plate_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the environment.
        Includes the plate, edible items, utensils, and drink containers.
        Adds distractor objects to the environment.
        """
        self.plate = self.add_actor("plate", "plate")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.fork = self.add_actor("fork", "fork")
        self.bottle = self.add_actor("bottle", "bottle")
        distractor_list = ["calculator", "screwdriver", "toycar", "alarm-clock", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm.
        Includes placing edible items on the plate, and recovering from a wrong action.
        """
        # Place hamburg on the plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Place hamburg on plate:", success)
        if not success:
            return self.info

        # Place french_fries on the plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french_fries on plate:", success)
        if not success:
            return self.info

        # Place fork on the table (utensil should not be on the plate)
        success = self.pick_and_place(self.fork, self.table)
        print("Place fork on table:", success)
        if not success:
            return self.info

        # Wrong action: Place bottle on the plate (drink container should not be on the plate)
        success = self.pick_and_place(self.bottle, self.plate)
        print("Wrong: Place bottle on plate:", success)
        if not success:
            return self.info

        # Recovery: Place bottle on the table
        success = self.pick_and_place(self.bottle, self.table)
        print("Recover: Place bottle on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        Edible items must be on the plate, utensils and drink containers must not be on the plate.
        """
        hamburg_on_plate = self.check_on(self.hamburg, self.plate)
        french_fries_on_plate = self.check_on(self.french_fries, self.plate)
        fork_on_plate = self.check_on(self.fork, self.plate)
        bottle_on_plate = self.check_on(self.bottle, self.plate)

        return (
            hamburg_on_plate and
            french_fries_on_plate and
            not fork_on_plate and
            not bottle_on_plate
        )
