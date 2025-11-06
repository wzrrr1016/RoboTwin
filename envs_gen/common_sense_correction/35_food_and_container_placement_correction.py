from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 35_food_and_container_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load the required containers and objects
        self.plate = self.add_actor("plate", "plate")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")

    def play_once(self):
        # Step 1: Pick and place french_fries into the plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("pick place french_fries:", success)
        if not success:
            return self.info

        # Step 2: Pick and place cup_without_handle into the plate (wrong action)
        success = self.pick_and_place(self.cup_without_handle, self.plate)
        print("pick place cup_without_handle (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick cup_without_handle from plate and place into fluted_block (recovery)
        success = self.pick_and_place(self.cup_without_handle, self.fluted_block)
        print("pick place cup_without_handle (recovery):", success)
        if not success:
            return self.info

        # Step 4: Pick and place dumbbell into fluted_block
        success = self.pick_and_place(self.dumbbell, self.fluted_block)
        print("pick place dumbbell:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if french_fries is on the plate
        # Check if cup_without_handle and dumbbell are on the fluted_block
        if (self.check_on(self.french_fries, self.plate) and
            self.check_on(self.cup_without_handle, self.fluted_block) and
            self.check_on(self.dumbbell, self.fluted_block)):
            return True
        return False
