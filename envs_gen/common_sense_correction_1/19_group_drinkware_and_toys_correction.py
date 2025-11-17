from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 19_group_drinkware_and_toys_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.plate = self.add_actor("plate", "plate")
        
        # Add required objects
        self.cup = self.add_actor("cup", "cup")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.red_block = self.add_actor("red_block", "red_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        
        # Add distractors
        distractor_list = ["calculator", "pot-with-plant", "alarm-clock", "shoe", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place cup on coaster
        success = self.pick_and_place(self.cup, self.coaster)
        print("Place cup on coaster:", success)
        if not success:
            return self.info
            
        # Place red_block on coaster (wrong action)
        success = self.pick_and_place(self.red_block, self.coaster)
        print("Place red_block on coaster (wrong):", success)
        if not success:
            return self.info
            
        # Recovery: Move red_block to plate
        success = self.pick_and_place(self.red_block, self.plate)
        print("Move red_block to plate:", success)
        if not success:
            return self.info
            
        # Place blue_block on plate
        success = self.pick_and_place(self.blue_block, self.plate)
        print("Place blue_block on plate:", success)
        if not success:
            return self.info
            
        # Place cup_without_handle on coaster
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("Place cup_without_handle on coaster:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        # Verify all objects are in their correct final positions
        return (
            self.check_on(self.cup, self.coaster) and
            self.check_on(self.cup_without_handle, self.coaster) and
            self.check_on(self.red_block, self.plate) and
            self.check_on(self.blue_block, self.plate)
        )
