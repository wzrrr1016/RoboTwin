from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 64_tools_and_perishables_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.drill = self.add_actor("drill", "drill")
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add distractors
        distractor_list = ["calculator", "alarm-clock", "pot-with-plant", "toycar", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Pick bread and place into wooden_box (wrong)
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Place bread into wooden_box (wrong):", success)
        if not success:
            return self.info
        
        # 2. Pick bread from wooden_box and place onto fluted_block (recovery)
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Recover bread to fluted_block:", success)
        if not success:
            return self.info
        
        # 3. Pick hammer and place into wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Place hammer into wooden_box:", success)
        if not success:
            return self.info
        
        # 4. Pick drill and place into wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Place drill into wooden_box:", success)
        if not success:
            return self.info
        
        # 5. Pick french_fries and place onto fluted_block
        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Place french fries onto fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all required objects are in their correct locations
        if (self.check_on(self.hammer, self.wooden_box) and
            self.check_on(self.drill, self.wooden_box) and
            self.check_on(self.bread, self.fluted_block) and
            self.check_on(self.french_fries, self.fluted_block)):
            return True
        return False
