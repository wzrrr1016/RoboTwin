from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 36_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the coaster as a container
        self.coaster = self.add_actor("coaster", "coaster")
        # Add the drinkware items
        self.bottle = self.add_actor("bottle", "bottle")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        # Add the toycar (wrong item)
        self.toycar = self.add_actor("toycar", "toycar")
        # Add other objects (optional, but included as per the task)
        self.scanner = self.add_actor("scanner", "scanner")
        self.stapler = self.add_actor("stapler", "stapler")

    def play_once(self):
        # Step 1: Pick toycar and place into coaster (wrong action)
        success = self.pick_and_place(self.toycar, self.coaster)
        print("pick place toycar:", success)
        if not success:
            return self.info

        # Step 2: Recovery: pick toycar from coaster and place on table
        success = self.pick_and_place(self.toycar, self.table)
        print("pick place toycar on table:", success)
        if not success:
            return self.info

        # Step 3: Pick bottle and place into coaster
        success = self.pick_and_place(self.bottle, self.coaster)
        print("pick place bottle:", success)
        if not success:
            return self.info

        # Step 4: Pick cup_with_handle and place into coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("pick place cup_with_handle:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if both drinkware items are on the coaster
        if self.check_on(self.bottle, self.coaster) and self.check_on(self.cup_with_handle, self.coaster):
            return True
        return False
