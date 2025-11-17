from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 14_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the coaster container
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add main objects
        self.can = self.add_actor("can", "can")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.mouse = self.add_actor("mouse", "mouse")
        self.toycar = self.add_actor("toycar", "toycar")
        self.red_block = self.add_actor("red_block", "red_block")
        
        # Add distractors
        distractors = ["pet-collar", "table-tennis", "roll-paper", "battery", "shoe"]
        self.add_distractors(distractors)
        
        # Check if all actors are properly placed
        self.check_scene()

    def play_once(self):
        # Place drinkware on coaster
        success = self.pick_and_place(self.can, self.coaster)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        if not success:
            return self.info
            
        # Wrong placement (mouse on coaster)
        success = self.pick_and_place(self.mouse, self.coaster)
        if not success:
            return self.info
            
        # Recovery (mouse to table)
        success = self.pick_and_place(self.mouse, self.table)
        if not success:
            return self.info
            
        # Place non-drinkware items on table
        success = self.pick_and_place(self.toycar, self.table)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.red_block, self.table)
        if not success:
            return self.info
            
        self.add_end()
        return self.info

    def check_success(self):
        # Check drinkware on coaster
        drinkware_on_coaster = (
            self.check_on(self.can, self.coaster) and 
            self.check_on(self.cup_without_handle, self.coaster)
        )
        
        # Check non-drinkware on table
        non_drinkware_on_table = (
            self.check_on(self.mouse, self.table) and 
            self.check_on(self.toycar, self.table) and 
            self.check_on(self.red_block, self.table)
        )
        
        return drinkware_on_coaster and non_drinkware_on_table
