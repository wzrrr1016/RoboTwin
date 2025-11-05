from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class container_usage_correction_35(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Load objects
        self.fork = self.add_actor("fork", "fork")
        self.stapler = self.add_actor("stapler", "stapler")
        self.knife = self.add_actor("knife", "knife")

    def play_once(self):
        # Pick fork and place into coaster
        success = self.pick_and_place(self.fork, self.coaster)
        print("pick place fork:", success)
        if not success:
            return self.info
        
        # Pick stapler and place into dustbin
        success = self.pick_and_place(self.stapler, self.dustbin)
        print("pick place stapler:", success)
        if not success:
            return self.info
        
        # Pick knife and place into coaster
        success = self.pick_and_place(self.knife, self.coaster)
        print("pick place knife:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if fork and knife are on the coaster
        if not (self.check_on(self.fork, self.coaster) and self.check_on(self.knife, self.coaster)):
            return False
        
        # Check if stapler is on the dustbin
        if not self.check_on(self.stapler, self.dustbin):
            return False
        
        return True
