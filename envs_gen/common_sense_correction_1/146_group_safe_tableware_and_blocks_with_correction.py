from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 146_group_safe_tableware_and_blocks_with_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors in the environment"""
        # Create the tray container
        self.tray = self.add_actor("tray", "tray")
        
        # Create the required objects
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.green_block = self.add_actor("green_block", "green_block")
        
        # Add distractor objects to the environment
        distractor_list = ["calculator", "alarm-clock", "shoe", "battery", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions"""
        # Place safe tableware (fork) on tray
        success = self.pick_and_place(self.fork, self.tray)
        print("Pick fork:", success)
        if not success:
            return self.info
            
        # Place purple block on tray
        success = self.pick_and_place(self.purple_block, self.tray)
        print("Pick purple_block:", success)
        if not success:
            return self.info
            
        # Place knife on tray (wrong action)
        success = self.pick_and_place(self.knife, self.tray)
        print("Pick knife (wrong):", success)
        if not success:
            return self.info
            
        # Recovery: Move knife back to table
        success = self.pick_and_place(self.knife, self.table)
        print("Recover knife:", success)
        if not success:
            return self.info
            
        # Place green block on tray
        success = self.pick_and_place(self.green_block, self.tray)
        print("Pick green_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if safe items are on the tray
        safe_items_on_tray = (
            self.check_on(self.fork, self.tray) and
            self.check_on(self.purple_block, self.tray) and
            self.check_on(self.green_block, self.tray)
        )
        
        # Check if sharp tool (knife) is NOT on the tray
        sharp_tool_off_tray = not self.check_on(self.knife, self.tray)
        
        return safe_items_on_tray and sharp_tool_off_tray
