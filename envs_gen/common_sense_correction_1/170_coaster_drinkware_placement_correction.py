from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 170_coaster_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the coaster as a container
        self.coaster = self.add_actor("coaster", "coaster")
        # Add the objects
        self.mug = self.add_actor("mug", "mug")
        self.bottle = self.add_actor("bottle", "bottle")
        self.can = self.add_actor("can", "can")
        self.book = self.add_actor("book", "book")
        # Add distractors
        distractor_list = ["calculator", "toycar", "alarm-clock", "small-speaker", "red_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place mug on coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Place mug on coaster:", success)
        if not success:
            return self.info

        # Wrongly place bottle on coaster
        success = self.pick_and_place(self.bottle, self.coaster)
        print("Wrongly place bottle on coaster:", success)
        if not success:
            return self.info

        # Recover: move bottle to table
        success = self.pick_and_place(self.bottle, self.table)
        print("Recover bottle to table:", success)
        if not success:
            return self.info

        # Place can on table
        success = self.pick_and_place(self.can, self.table)
        print("Place can on table:", success)
        if not success:
            return self.info

        # Place book on table
        success = self.pick_and_place(self.book, self.table)
        print("Place book on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check that mug is on the coaster
        if not self.check_on(self.mug, self.coaster):
            return False
        # Check that other items are not on the coaster
        if self.check_on(self.bottle, self.coaster):
            return False
        if self.check_on(self.can, self.coaster):
            return False
        if self.check_on(self.book, self.coaster):
            return False
        return True
