from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 467_fast_food_and_recyclables_correction(Imagine_Task):
    def load_actors(self):
        # Add containers to the environment
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add required objects to the environment
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.can = self.add_actor("can", "can")
        self.bottle = self.add_actor("bottle", "bottle")
        self.book = self.add_actor("book", "book")
        
        # Add distractor objects to the environment
        distractor_list = ["calculator", "hammer", "toycar", "shoe", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place ready-to-eat fast foods on the tray
        success = self.pick_and_place(self.hamburg, self.tray)
        print("Place hamburg:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Place french fries:", success)
        if not success:
            return self.info
            
        # Wrong placement of can (needs recovery)
        success = self.pick_and_place(self.can, self.tray)
        print("Wrongly place can:", success)
        if not success:
            return self.info
            
        # Recovery: Move can to dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        print("Recover can:", success)
        if not success:
            return self.info
            
        # Place recyclables in dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Place bottle:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.book, self.dustbin)
        print("Place book:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        return (
            self.check_on(self.hamburg, self.tray) and
            self.check_on(self.french_fries, self.tray) and
            self.check_on(self.can, self.dustbin) and
            self.check_on(self.bottle, self.dustbin) and
            self.check_on(self.book, self.dustbin)
        )
