from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 6_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the coaster as a container
        self.coaster = self.add_actor("coaster", "coaster")
        # Load the drinkware items
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        # Load the green_block as a distractor
        self.green_block = self.add_actor("green_block", "green_block")
        # The book is not part of the task, but it's included in the scene
        self.book = self.add_actor("book", "book")

    def play_once(self):
        # Attempt to pick green_block and place into coaster (wrong action)
        success = self.pick_and_place(self.green_block, self.coaster)
        print("pick place green_block:", success)
        if not success:
            # Recovery: pick green_block from coaster and place on table
            success = self.pick_and_place(self.green_block, self.table)
            print("pick place green_block on table:", success)
            if not success:
                return self.info

        # Now place the correct drinkware items into the coaster
        # Pick and place cup_with_handle
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("pick place cup_with_handle:", success)
        if not success:
            return self.info

        # Pick and place cup_without_handle
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("pick place cup_without_handle:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if both cups are on the coaster
        if self.check_on(self.cup_with_handle, self.coaster) and self.check_on(self.cup_without_handle, self.coaster):
            return True
        return False
