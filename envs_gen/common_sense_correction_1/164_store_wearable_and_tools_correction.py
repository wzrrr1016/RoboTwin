from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 164_store_wearable_and_tools_correction(Imagine_Task):
    def load_actors(self):
        # Create containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Create objects to be manipulated
        self.shoe = self.add_actor("shoe", "shoe")
        self.hammer = self.add_actor("hammer", "hammer")
        self.mouse = self.add_actor("mouse", "mouse")
        self.stapler = self.add_actor("stapler", "stapler")
        
        # Add distractors to the environment
        distractor_list = ['baguette', 'pot-with-plant', 'book', 'red_block', 'apple']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Initial wrong placement of shoe in wooden_box
        success = self.pick_and_place(self.shoe, self.wooden_box)
        print("Wrong placement of shoe:", success)
        if not success:
            return self.info
            
        # Recovery: Move shoe to correct container (shoe_box)
        success = self.pick_and_place(self.shoe, self.shoe_box)
        print("Recovery placement of shoe:", success)
        if not success:
            return self.info
            
        # Place tools and office items in wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Place hammer:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.mouse, self.wooden_box)
        print("Place mouse:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.stapler, self.wooden_box)
        print("Place stapler:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        shoe_in_shoe_box = self.check_on(self.shoe, self.shoe_box)
        hammer_in_wooden = self.check_on(self.hammer, self.wooden_box)
        mouse_in_wooden = self.check_on(self.mouse, self.wooden_box)
        stapler_in_wooden = self.check_on(self.stapler, self.wooden_box)
        
        return all([shoe_in_shoe_box, hammer_in_wooden, mouse_in_wooden, stapler_in_wooden])
