from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 251_delicate_vs_heavy_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add containers to the environment
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add required objects to the environment
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.mug = self.add_actor("mug", "mug")
        self.hammer = self.add_actor("hammer", "hammer")
        self.drill = self.add_actor("drill", "drill")
        
        # Add distractor objects to the environment
        distractor_list = ["apple", "baguette", "french_fries", "chips-tub", "hamburg"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Action 1: Place pot-with-plant on fluted_block
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Place pot-with-plant:", success)
        if not success:
            return self.info
        
        # Action 2: Place hammer in wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Place hammer:", success)
        if not success:
            return self.info
        
        # Action 3: Wrong placement of mug into wooden_box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Place mug (wrong):", success)
        if not success:
            return self.info
        
        # Action 4: Recovery: move mug to fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Recover mug:", success)
        if not success:
            return self.info
        
        # Action 5: Place sand-clock on fluted_block
        success = self.pick_and_place(self.sand_clock, self.fluted_block)
        print("Place sand-clock:", success)
        if not success:
            return self.info
        
        # Action 6: Place drill in wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Place drill:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        if (self.check_on(self.pot_with_plant, self.fluted_block) and
            self.check_on(self.sand_clock, self.fluted_block) and
            self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.hammer, self.wooden_box) and
            self.check_on(self.drill, self.wooden_box)):
            return True
        return False
