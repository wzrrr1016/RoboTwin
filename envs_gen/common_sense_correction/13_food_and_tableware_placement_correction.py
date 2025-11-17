from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 13_food_and_tableware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("wooden_box", "fluted_block")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")
        
        # Add distractors
        distractor_list = ["calculator", "pet-collar", "table-tennis", "dumbbell"]
        self.add_distractors(distractor_list)
        
        # Final scene check
        self.check_scene()

    def play_once(self):
        # Place food and tableware in fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.bread, self.fluted_block)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.fork, self.fluted_block)
        if not success:
            return self.info
        
        # Wrong placement of shampoo (recovery needed)
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        if not success:
            return self.info
        
        # Recovery: Move shampoo to shoe_box
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        if not success:
            return self.info
        
        # Final placement of knife
        success = self.pick_and_place(self.knife, self.fluted_block)
        if not success:
            return self.info
        
        self.add_end()
        return self.info

    def check_success(self):
        # Verify all food/tableware are in fluted_block and hygiene item in shoe_box
        if (self.check_on(self.apple, self.fluted_block) and
            self.check_on(self.bread, self.fluted_block) and
            self.check_on(self.fork, self.fluted_block) and
            self.check_on(self.knife, self.fluted_block) and
            self.check_on(self.shampoo, self.shoe_box)):
            return True
        return False
