from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 151_drinkware_and_toys_on_coaster_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Add the coaster as a container.
        - Add the required objects: bottle, cup, purple_block, book, apple.
        - Add distractor objects as specified in the task.
        """
        # Add the coaster container
        self.coaster = self.add_actor("coaster", "coaster")

        # Add the main objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup = self.add_actor("cup", "cup")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.book = self.add_actor("book", "book")
        self.apple = self.add_actor("apple", "apple")

        # Add distractor objects
        distractor_list = ["hammer", "screwdriver", "alarm-clock", "shoe", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm.
        - Place purple_block, bottle, and cup on the coaster.
        - Attempt to place book on coaster (intentional mistake), then recover by placing it on the table.
        - Place apple on the table.
        """
        # Place purple_block on coaster
        success = self.pick_and_place(self.purple_block, self.coaster)
        print("Place purple_block on coaster:", success)
        if not success:
            return self.info

        # Place bottle on coaster
        success = self.pick_and_place(self.bottle, self.coaster)
        print("Place bottle on coaster:", success)
        if not success:
            return self.info

        # Intentionally place book on coaster (wrong action)
        success = self.pick_and_place(self.book, self.coaster)
        print("Wrongly place book on coaster:", success)
        if success:
            # Recovery: move book back to table
            success_recovery = self.pick_and_place(self.book, self.table)
            print("Recover book to table:", success_recovery)
            if not success_recovery:
                return self.info

        # Place cup on coaster
        success = self.pick_and_place(self.cup, self.coaster)
        print("Place cup on coaster:", success)
        if not success:
            return self.info

        # Place apple on table
        success = self.pick_and_place(self.apple, self.table)
        print("Place apple on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All drinkware (bottle, cup) and small toys (purple_block) must be on the coaster.
        - Book and apple must not be on the coaster.
        """
        if (
            self.check_on(self.bottle, self.coaster) and
            self.check_on(self.cup, self.coaster) and
            self.check_on(self.purple_block, self.coaster) and
            not self.check_on(self.book, self.coaster) and
            not self.check_on(self.apple, self.coaster)
        ):
            return True
        return False
