from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 36_toys_and_liquids_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add required objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.can = self.add_actor("can", "can")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        
        # Add distractors
        self.add_distractors(["calculator", "stapler", "shoe", "pot-with-plant", "alarm-clock"])

    def play_once(self):
        # Place red block on plate
        success = self.pick_and_place(self.red_block, self.plate)
        print("Place red_block on plate:", success)
        if not success:
            return self.info

        # Wrong placement of can on plate
        success = self.pick_and_place(self.can, self.plate)
        print("Wrong: Place can on plate:", success)
        if not success:
            return self.info

        # Recovery: Move can to coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Recovery: Place can on coaster:", success)
        if not success:
            return self.info

        # Place purple block on plate
        success = self.pick_and_place(self.purple_block, self.plate)
        print("Place purple_block on plate:", success)
        if not success:
            return self.info

        # Place shampoo on coaster
        success = self.pick_and_place(self.shampoo, self.coaster)
        print("Place shampoo on coaster:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all required placements
        return (
            self.check_on(self.red_block, self.plate) and
            self.check_on(self.purple_block, self.plate) and
            self.check_on(self.can, self.coaster) and
            self.check_on(self.shampoo, self.coaster)
        )
