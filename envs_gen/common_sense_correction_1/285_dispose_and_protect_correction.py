from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 285_dispose_and_protect_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add required objects
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.bread = self.add_actor("bread", "bread")
        self.fork = self.add_actor("fork", "fork")
        self.green_block = self.add_actor("green_block", "green_block")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        
        # Add distractors
        distractor_list = ["pot-with-plant", "shoe", "pet-collar", "shampoo", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place tissue-box in dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Place tissue-box:", success)
        if not success:
            return self.info
        
        # Step 2: Place bread in dustbin
        success = self.pick_and_place(self.bread, self.dustbin)
        print("Place bread:", success)
        if not success:
            return self.info
        
        # Step 3: Place fork in dustbin (wrong action)
        success = self.pick_and_place(self.fork, self.dustbin)
        print("Place fork (wrong):", success)
        if not success:
            return self.info
        
        # Step 4: Recover fork to coaster
        success = self.pick_and_place(self.fork, self.coaster)
        print("Recover fork to coaster:", success)
        if not success:
            return self.info
        
        # Step 5: Place green_block on coaster
        success = self.pick_and_place(self.green_block, self.coaster)
        print("Place green_block:", success)
        if not success:
            return self.info
        
        # Step 6: Place hamburg in dustbin
        success = self.pick_and_place(self.hamburg, self.dustbin)
        print("Place hamburg:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Check if all disposable paper items and edible food are in dustbin
        # and all small hard reusable items are on coaster
        if (self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.bread, self.dustbin) and
            self.check_on(self.hamburg, self.dustbin) and
            self.check_on(self.fork, self.coaster) and
            self.check_on(self.green_block, self.coaster)):
            return True
        return False
