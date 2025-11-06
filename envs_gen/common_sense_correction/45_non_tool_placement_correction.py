from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 45_non_tool_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")

        # Load objects
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.stapler = self.add_actor("stapler", "stapler")
        self.mug = self.add_actor("mug", "mug")
        self.microphone = self.add_actor("microphone", "microphone")
        self.orange_block = self.add_actor("orange_block", "orange_block")

    def play_once(self):
        # Place non-tool items into the plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("pick place french_fries:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mug, self.plate)
        print("pick place mug:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.microphone, self.plate)
        print("pick place microphone:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.orange_block, self.plate)
        print("pick place orange_block:", success)
        if not success:
            return self.info

        # Place stapler into the plate (wrong action)
        success = self.pick_and_place(self.stapler, self.plate)
        print("pick place stapler into plate:", success)
        if not success:
            pass  # Proceed regardless of success

        # Recover the stapler from the plate and place it on the table
        if self.check_on(self.stapler, self.plate):
            success = self.pick_and_place(self.stapler, self.table)
            print("pick place stapler on table:", success)
            if not success:
                return self.info

    def check_success(self):
        # Check if all non-tool items are on the plate and the stapler is not
        if (self.check_on(self.french_fries, self.plate) and
            self.check_on(self.mug, self.plate) and
            self.check_on(self.microphone, self.plate) and
            self.check_on(self.orange_block, self.plate) and
            not self.check_on(self.stapler, self.plate)):
            return True
        return False
