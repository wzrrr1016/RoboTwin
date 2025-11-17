from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 255_metal_item_grouping_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add required objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.fork = self.add_actor("fork", "fork")
        self.can = self.add_actor("can", "can")
        self.bell = self.add_actor("bell", "bell")
        
        # Add distractors
        distractor_list = ["baguette", "apple", "tissue-box", "book", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place metal tools and eating utensils in wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Pick hammer:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.fork, self.wooden_box)
        print("Pick fork:", success)
        if not success:
            return self.info
            
        # Wrong placement of can (needs recovery)
        success = self.pick_and_place(self.can, self.wooden_box)
        print("Pick can (wrong):", success)
        if not success:
            return self.info
            
        # Recovery - move can to correct container
        success = self.pick_and_place(self.can, self.shoe_box)
        print("Pick can (recovery):", success)
        if not success:
            return self.info
            
        # Place lightweight hollow/ringing metal item
        success = self.pick_and_place(self.bell, self.shoe_box)
        print("Pick bell:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        if (self.check_on(self.hammer, self.wooden_box) and
            self.check_on(self.fork, self.wooden_box) and
            self.check_on(self.can, self.shoe_box) and
            self.check_on(self.bell, self.shoe_box)):
            return True
        return False
