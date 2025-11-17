from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 252_organize_heavy_and_tool_items_with_correction(Imagine_Task):
    def load_actors(self):
        # Add container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add required objects
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.drill = self.add_actor("drill", "drill")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.bread = self.add_actor("bread", "bread")
        self.mug = self.add_actor("mug", "mug")
        
        # Add distractors
        distractor_list = ["book", "toycar", "alarm-clock", "tissue-box", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place heavy items and repair tools
        success = self.pick_and_place(self.dumbbell, self.fluted_block)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        if not success:
            return self.info
            
        # Wrong action (bread in fluted_block)
        success = self.pick_and_place(self.bread, self.fluted_block)
        if not success:
            return self.info
            
        # Recovery (bread on table)
        success = self.pick_and_place(self.bread, self.table)
        if not success:
            return self.info
            
        # Place remaining repair tool
        success = self.pick_and_place(self.drill, self.fluted_block)
        if not success:
            return self.info
            
        # Place mug on table
        success = self.pick_and_place(self.mug, self.table)
        if not success:
            return self.info

    def check_success(self):
        # Check if all required items are in the fluted_block
        if (self.check_on(self.dumbbell, self.fluted_block) and
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.drill, self.fluted_block)):
            return True
        return False
