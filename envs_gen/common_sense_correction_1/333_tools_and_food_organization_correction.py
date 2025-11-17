from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 333_tools_and_food_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.tray = self.add_actor("tray", "tray")
        
        # Add objects
        self.drill = self.add_actor("drill", "drill")
        self.hammer = self.add_actor("hammer", "hammer")
        self.stapler = self.add_actor("stapler", "stapler")
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add distractors
        distractor_list = ["toycar", "book", "pot-with-plant", "alarm-clock", "calculator"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place tools in shoe_box
        success = self.pick_and_place(self.drill, self.shoe_box)
        print("Pick drill:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Pick hammer:", success)
        if not success:
            return self.info
            
        # Wrong placement of apple (needs recovery)
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Pick apple (wrong placement):", success)
        if not success:
            return self.info
            
        # Recovery: Move apple to tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Pick apple (recovery):", success)
        if not success:
            return self.info
            
        # Place remaining objects
        success = self.pick_and_place(self.stapler, self.shoe_box)
        print("Pick stapler:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Pick french fries:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all tools are in shoe_box and foods are on tray
        if (self.check_on(self.drill, self.shoe_box) and
            self.check_on(self.hammer, self.shoe_box) and
            self.check_on(self.stapler, self.shoe_box) and
            self.check_on(self.apple, self.tray) and
            self.check_on(self.french_fries, self.tray)):
            return True
        return False
