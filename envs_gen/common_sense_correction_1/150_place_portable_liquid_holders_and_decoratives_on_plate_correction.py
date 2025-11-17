from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 150_place_portable_liquid_holders_and_decoratives_on_plate_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Adds the plate as a container.
        - Adds the relevant objects: bottle, cup, sand-clock, and dumbbell.
        - Adds distractor objects as specified in the task description.
        """
        # Add the plate as the target container
        self.plate = self.add_actor("plate", "plate")

        # Add the relevant objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup = self.add_actor("cup", "cup")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")

        # Add distractor objects as specified in the task
        distractor_list = ["calculator", "screwdriver", "mouse", "book", "apple"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        - First, the robot attempts to place the dumbbell on the plate (wrong action).
        - Then, it recovers by placing the dumbbell back on the table.
        - Finally, it places the correct objects (bottle, cup, sand-clock) on the plate.
        """
        # Wrong action: place dumbbell on plate
        success = self.pick_and_place(self.dumbbell, self.plate)
        print("Pick and place dumbbell on plate (wrong):", success)
        if not success:
            return self.info

        # Recovery: place dumbbell back on the table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Pick and place dumbbell back on table (recovery):", success)
        if not success:
            return self.info

        # Correct actions: place bottle, cup, and sand-clock on the plate
        success = self.pick_and_place(self.bottle, self.plate)
        print("Pick and place bottle:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup, self.plate)
        print("Pick and place cup:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.sand_clock, self.plate)
        print("Pick and place sand-clock:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All correct objects (bottle, cup, sand-clock) must be on the plate.
        - The dumbbell must not be on the plate (i.e., it must be back on the table).
        """
        correct_objects_on_plate = (
            self.check_on(self.bottle, self.plate) and
            self.check_on(self.cup, self.plate) and
            self.check_on(self.sand_clock, self.plate)
        )

        # Ensure the dumbbell is not on the plate (i.e., it was successfully recovered)
        dumbbell_not_on_plate = not self.check_on(self.dumbbell, self.plate)

        return correct_objects_on_plate and dumbbell_not_on_plate
