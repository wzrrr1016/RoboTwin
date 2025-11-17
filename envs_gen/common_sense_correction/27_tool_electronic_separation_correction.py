from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 27_tool_electronic_separation_correction(Imagine_Task):
    def load_actors(self):
        # Add containers and objects to the scene
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.scanner = self.add_actor("scanner", "scanner")
        self.stapler = self.add_actor("stapler", "stapler")
        self.hammer = self.add_actor("hammer", "hammer")
        self.knife = self.add_actor("knife", "knife")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        
        # Add distractor objects
        distractor_list = ["pot-with-plant", "sand-clock", "tissue-box", "shampoo", "red_block"]
        self.add_distractors(distractor_list)
        
        # Final scene check
        self.check_scene()

    def play_once(self):
        # Initial wrong action: put scanner in wooden box
        success = self.pick_and_place(self.scanner, self.wooden_box)
        print("Put scanner in wooden_box (wrong):", success)
        if not success:
            return self.info
            
        # Recovery: put scanner on table
        success = self.pick_and_place(self.scanner, self.table)
        print("Put scanner on table (recovery):", success)
        if not success:
            return self.info
            
        # Put office/repair tools in wooden box
        success = self.pick_and_place(self.stapler, self.wooden_box)
        print("Put stapler in wooden_box:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Put hammer in wooden_box:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("Put knife in wooden_box:", success)
        if not success:
            return self.info
            
        # Put electronic device on table
        success = self.pick_and_place(self.small_speaker, self.table)
        print("Put small-speaker on table:", success)
        if not success:
            return self.info
            
        self.add_end()
        return self.info

    def check_success(self):
        # Verify all objects are in their correct locations
        if (self.check_on(self.stapler, self.wooden_box) and
            self.check_on(self.hammer, self.wooden_box) and
            self.check_on(self.knife, self.wooden_box) and
            self.check_on(self.scanner, self.table) and
            self.check_on(self.small_speaker, self.table)):
            return True
        return False
