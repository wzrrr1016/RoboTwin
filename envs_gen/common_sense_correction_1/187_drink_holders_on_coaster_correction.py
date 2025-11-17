from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 187_drink_holders_on_coaster_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Add the coaster as a container.
        - Add the objects used for holding or serving drinks.
        - Add distractor objects to the environment.
        """
        # Add the coaster container
        self.coaster = self.add_actor("coaster", "coaster")

        # Add objects used for holding or serving drinks
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.can = self.add_actor("can", "can")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")

        # Add distractor objects
        self.add_distractors(["calculator", "screwdriver", "shoe", "book", "toycar"])

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        - First, place shampoo on the coaster (wrong action).
        - Then, recover by placing shampoo back on the table.
        - Finally, place the correct drink-holding items on the coaster.
        """
        # Wrong action: place shampoo on the coaster
        success = self.pick_and_place(self.shampoo, self.coaster)
        print("Place shampoo on coaster (wrong):", success)
        if not success:
            return self.info

        # Recovery: place shampoo back on the table
        success = self.pick_and_place(self.shampoo, self.table)
        print("Recover shampoo to table:", success)
        if not success:
            return self.info

        # Place correct items on the coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Place can on coaster:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle on coaster:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("Place cup_without_handle on coaster:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All correct drink-holding items must be on the coaster.
        - Shampoo must not be on the coaster.
        """
        correct_items_on_coaster = (
            self.check_on(self.can, self.coaster) and
            self.check_on(self.cup_with_handle, self.coaster) and
            self.check_on(self.cup_without_handle, self.coaster)
        )
        shampoo_not_on_coaster = not self.check_on(self.shampoo, self.coaster)

        return correct_items_on_coaster and shampoo_not_on_coaster
