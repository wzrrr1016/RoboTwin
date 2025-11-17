from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 441_desk_vs_drink_items_with_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add target objects
        self.scanner = self.add_actor("scanner", "scanner")
        self.mouse = self.add_actor("mouse", "mouse")
        self.can = self.add_actor("can", "can")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractors
        distractors = ["pet-collar", "toycar", "dumbbell", "shoe", "pot-with-plant"]
        self.add_distractors(distractors)

    def play_once(self):
        # 1. Place scanner on fluted_block
        success = self.pick_and_place(self.scanner, self.fluted_block)
        print("Place scanner:", success)
        if not success:
            return self.info
            
        # 2. Place mouse on coaster (wrong placement)
        success = self.pick_and_place(self.mouse, self.coaster)
        print("Place mouse on coaster (wrong):", success)
        if not success:
            return self.info
            
        # 3. Recover mouse to fluted_block
        success = self.pick_and_place(self.mouse, self.fluted_block)
        print("Recover mouse to fluted_block:", success)
        if not success:
            return self.info
            
        # 4. Place can on coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Place can on coaster:", success)
        if not success:
            return self.info
            
        # 5. Place tissue-box on coaster
        success = self.pick_and_place(self.tissue_box, self.coaster)
        print("Place tissue-box on coaster:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        # Verify all objects are in their correct final positions
        return (
            self.check_on(self.scanner, self.fluted_block) and
            self.check_on(self.mouse, self.fluted_block) and
            self.check_on(self.can, self.coaster) and
            self.check_on(self.tissue_box, self.coaster)
        )
