from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 456_repair_and_everyday_items_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Create containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Create objects to be manipulated
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.markpen = self.add_actor("markpen", "markpen")
        self.fork = self.add_actor("fork", "fork")
        
        # Add distractor objects
        distractor_list = ["pot-with-plant", "toycar", "alarm-clock", "dumbbell", "red_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place repair tools in wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Hammer placed:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("Screwdriver placed:", success)
        if not success:
            return self.info
            
        # Initial incorrect placement of markpen
        success = self.pick_and_place(self.markpen, self.wooden_box)
        print("Markpen placed (wrong):", success)
        if not success:
            return self.info
            
        # Recovery - move markpen to correct container
        success = self.pick_and_place(self.markpen, self.shoe_box)
        print("Markpen recovered:", success)
        if not success:
            return self.info
            
        # Place everyday items in shoe_box
        success = self.pick_and_place(self.fork, self.shoe_box)
        print("Fork placed:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        if (self.check_on(self.hammer, self.wooden_box) and
            self.check_on(self.screwdriver, self.wooden_box) and
            self.check_on(self.markpen, self.shoe_box) and
            self.check_on(self.fork, self.shoe_box)):
            return True
        return False
