from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 36_office_supplies_drinkware_separation_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects
        self.mouse = self.add_actor("mouse", "mouse")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.bottle = self.add_actor("bottle", "bottle")
        self.markpen = self.add_actor("markpen", "markpen")

        # Add distractors
        distractor_list = ["pet-collar", "table-tennis", "battery", "apple", "shoe", "dumbbell"]
        self.add_distractors(distractor_list)

        # Finalize scene setup
        self.check_scene()

    def play_once(self):
        # Step 1: Place mouse into wooden_box
        success = self.pick_and_place(self.mouse, self.wooden_box)
        print("Place mouse:", success)
        if not success:
            return self.info

        # Step 2: Place markpen into wooden_box
        success = self.pick_and_place(self.markpen, self.wooden_box)
        print("Place markpen:", success)
        if not success:
            return self.info

        # Step 3: Wrong placement of cup_with_handle into wooden_box
        success = self.pick_and_place(self.cup_with_handle, self.wooden_box)
        print("Wrong placement cup_with_handle:", success)
        if not success:
            return self.info

        # Step 4: Recovery - move cup_with_handle to fluted_block
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Recover cup_with_handle:", success)
        if not success:
            return self.info

        # Step 5: Place bottle into fluted_block
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Place bottle:", success)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        # Check if all objects are in their correct containers
        if (
            self.check_on(self.mouse, self.wooden_box) and
            self.check_on(self.markpen, self.wooden_box) and
            self.check_on(self.cup_with_handle, self.fluted_block) and
            self.check_on(self.bottle, self.fluted_block)
        ):
            return True
        return False
