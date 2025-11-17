from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 158_keep_natural_vs_dispose_greasy_tools(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add main objects
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.hammer = self.add_actor("hammer", "hammer")
        
        # Add distractors
        distractor_list = ["calculator", "alarm-clock", "toycar", "shoe", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Put pot-with-plant in wooden_box
        success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
        print("Put pot-with-plant:", success)
        if not success:
            return self.info
        
        # Step 2: Put apple in wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Put apple:", success)
        if not success:
            return self.info
        
        # Step 3: Put bread in dustbin (wrong action)
        success = self.pick_and_place(self.bread, self.dustbin)
        print("Put bread in dustbin (wrong):", success)
        if not success:
            return self.info
        
        # Step 4: Recover bread to wooden_box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Recover bread:", success)
        if not success:
            return self.info
        
        # Step 5: Put french_fries in dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Put french_fries:", success)
        if not success:
            return self.info
        
        # Step 6: Put hammer in dustbin
        success = self.pick_and_place(self.hammer, self.dustbin)
        print("Put hammer:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        if (self.check_on(self.pot_with_plant, self.wooden_box) and
            self.check_on(self.apple, self.wooden_box) and
            self.check_on(self.bread, self.wooden_box) and
            self.check_on(self.french_fries, self.dustbin) and
            self.check_on(self.hammer, self.dustbin)):
            return True
        return False
