from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 30_organize_heavy_and_living_items_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        
        # Add distractors
        self.add_distractors(["calculator", "battery", "toycar", "book", "red_block"])

    def play_once(self):
        # First wrong action: place pot-with-plant on fluted_block
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Wrong placement of pot-with-plant:", success)
        if not success:
            return self.info
        
        # Recovery action: move pot-with-plant to shoe_box
        success = self.pick_and_place(self.pot_with_plant, self.shoe_box)
        print("Recovery placement of pot-with-plant:", success)
        if not success:
            return self.info
        
        # Place dumbbell on fluted_block (heavy exercise item)
        success = self.pick_and_place(self.dumbbell, self.fluted_block)
        print("Placing dumbbell:", success)
        if not success:
            return self.info
        
        # Place screwdriver on fluted_block (hand tool)
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Placing screwdriver:", success)
        if not success:
            return self.info
        
        # Place shampoo in shoe_box (liquid personal-care item)
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("Placing shampoo:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        if (self.check_on(self.pot_with_plant, self.shoe_box) and
            self.check_on(self.dumbbell, self.fluted_block) and
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.shampoo, self.shoe_box)):
            return True
        return False
