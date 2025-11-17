from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 46_heavy_item_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the tray container
        self.tray = self.add_actor("tray", "tray")
        
        # Add the main objects
        self.drill = self.add_actor("drill", "drill")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        
        # Add distractor objects
        distractor_list = ['calculator', 'pet-collar', 'table-tennis', 'stapler', 'sand-clock']
        self.add_distractors(distractor_list)
        
        # Check if all actors are placed correctly
        self.check_scene()

    def play_once(self):
        # Pick drill and place in tray
        success = self.pick_and_place(self.drill, self.tray)
        print("Pick drill into tray:", success)
        if not success:
            return self.info
        
        # Pick dumbbell and place in tray
        success = self.pick_and_place(self.dumbbell, self.tray)
        print("Pick dumbbell into tray:", success)
        if not success:
            return self.info
        
        # Wrong action: Pick cup and place in tray
        success = self.pick_and_place(self.cup_without_handle, self.tray)
        print("Pick cup into tray (wrong):", success)
        if not success:
            return self.info
        
        # Recovery: Pick cup from tray and place on table
        success = self.pick_and_place(self.cup_without_handle, self.table)
        print("Pick cup from tray to table:", success)
        if not success:
            return self.info
        
        # Pick french fries and place on table
        success = self.pick_and_place(self.french_fries, self.table)
        print("Pick french fries to table:", success)
        if not success:
            return self.info
        
        # Pick blue block and place on table
        success = self.pick_and_place(self.blue_block, self.table)
        print("Pick blue block to table:", success)
        if not success:
            return self.info
        
        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        # Check if heavy items are in the tray and light items are on the table
        if (self.check_on(self.drill, self.tray) and
            self.check_on(self.dumbbell, self.tray) and
            self.check_on(self.cup_without_handle, self.table) and
            self.check_on(self.french_fries, self.table) and
            self.check_on(self.blue_block, self.table)):
            return True
        return False
