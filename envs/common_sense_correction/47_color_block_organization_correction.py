from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class color_block_organization_correction_47(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Load objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.scanner = self.add_actor("scanner", "scanner")
        self.bottle = self.add_actor("bottle", "bottle")
        self.drill = self.add_actor("drill", "drill")

    def play_once(self):
        # Step 1: Pick red_block and place into wooden_box (wrong)
        success = self.pick_and_place(self.red_block, self.wooden_box)
        print("pick place red_block into wooden_box:", success)
        if not success:
            return self.info
        
        # Step 2: Pick red_block from wooden_box and place into fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("pick place red_block into fluted_block:", success)
        if not success:
            return self.info
        
        # Step 3: Pick orange_block and place into fluted_block (wrong)
        success = self.pick_and_place(self.orange_block, self.fluted_block)
        print("pick place orange_block into fluted_block:", success)
        if not success:
            return self.info
        
        # Step 4: Pick scanner and place into wooden_box
        success = self.pick_and_place(self.scanner, self.wooden_box)
        print("pick place scanner into wooden_box:", success)
        if not success:
            return self.info
        
        # Step 5: Pick bottle and place into wooden_box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("pick place bottle into wooden_box:", success)
        if not success:
            return self.info
        
        # Step 6: Pick drill and place into wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("pick place drill into wooden_box:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check red_block is in fluted_block (primary color)
        if not self.check_on(self.red_block, self.fluted_block):
            return False
        
        # Check orange_block is in wooden_box (secondary color)
        if not self.check_on(self.orange_block, self.wooden_box):
            return False
        
        # Check scanner, bottle, and drill are in wooden_box
        if not self.check_on(self.scanner, self.wooden_box):
            return False
        if not self.check_on(self.bottle, self.wooden_box):
            return False
        if not self.check_on(self.drill, self.wooden_box):
            return False
        
        return True
```
