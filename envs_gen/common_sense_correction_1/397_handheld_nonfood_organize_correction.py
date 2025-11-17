from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 397_handheld_nonfood_organize_correction(Imagine_Task):
    def load_actors(self):
        # Create the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Create the objects
        self.bread = self.add_actor("bread", "bread")
        self.red_block = self.add_actor("red_block", "red_block")
        self.fork = self.add_actor("fork", "fork")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractors
        distractors = ["pot-with-plant", "alarm-clock", "shoe", "dumbbell", "scanner"]
        self.add_distractors(distractors)

    def play_once(self):
        # Place red_block into fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Place red_block:", success)
        if not success:
            return self.info
        
        # Place toycar into fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar:", success)
        if not success:
            return self.info
        
        # Wrongly place bread into fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Place bread (wrong):", success)
        if not success:
            return self.info
        
        # Recover: place bread on the table
        success = self.pick_and_place(self.bread, self.table)
        print("Recover bread:", success)
        if not success:
            return self.info
        
        # Place fork into fluted_block
        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Place fork:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Verify correct items are in the container and bread is on the table
        if (
            self.check_on(self.red_block, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.fork, self.fluted_block) and
            self.check_on(self.bread, self.table)
        ):
            return True
        return False
