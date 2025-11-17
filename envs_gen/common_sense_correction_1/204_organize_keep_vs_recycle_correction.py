from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 204_organize_keep_vs_recycle_correction(Imagine_Task):
    def load_actors(self):
        # Add containers to the environment
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add task-specific objects
        self.stapler = self.add_actor("stapler", "stapler")
        self.markpen = self.add_actor("markpen", "markpen")
        self.can = self.add_actor("can", "can")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractor objects
        distractor_list = ["pot-with-plant", "shoe", "dumbbell", "alarm-clock", "microphone"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # First wrong placement of can
        success = self.pick_and_place(self.can, self.fluted_block)
        print("Pick can into fluted_block:", success)
        if not success:
            return self.info
            
        # Recovery: move can to dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        print("Move can to dustbin:", success)
        if not success:
            return self.info
            
        # Place reusable office supplies and small toys
        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("Place stapler:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Place markpen:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        if (self.check_on(self.stapler, self.fluted_block) and
            self.check_on(self.markpen, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.can, self.dustbin)):
            return True
        return False
