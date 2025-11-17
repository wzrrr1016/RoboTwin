from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 49_food_vs_nonfood_separation_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.can = self.add_actor("can", "can")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        
        # Add distractors
        distractor_list = ['calculator', 'pet-collar', 'table-tennis', 'roll-paper', 'battery']
        self.add_distractors(distractor_list)
        
        # Final scene check
        self.check_scene()

    def play_once(self):
        # Place food items in plate
        success = self.pick_and_place(self.apple, self.plate)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.french_fries, self.plate)
        if not success:
            return self.info
            
        # Wrong placement (can in plate) followed by recovery
        success = self.pick_and_place(self.can, self.plate)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.can, self.dustbin)
        if not success:
            return self.info
            
        # Place non-food items in dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.pink_block, self.dustbin)
        if not success:
            return self.info
            
        self.add_end()
        return self.info

    def check_success(self):
        # Verify all objects are in correct containers
        if (self.check_on(self.apple, self.plate) and
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.can, self.dustbin) and
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.pink_block, self.dustbin)):
            return True
        return False
