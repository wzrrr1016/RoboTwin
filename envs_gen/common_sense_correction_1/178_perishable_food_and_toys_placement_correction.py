from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 178_perishable_food_and_toys_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.plate = self.add_actor("plate", "plate")
        
        # Add objects
        self.bread = self.add_actor("bread", "bread")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add distractors
        distractor_list = ["calculator", "screwdriver", "alarm-clock", "pot-with-plant", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Pick pink_block and place it into fluted_block
        success = self.pick_and_place(self.pink_block, self.fluted_block)
        print("Place pink_block:", success)
        if not success:
            return self.info

        # 2. Pick bread and place it into fluted_block (wrong action)
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Wrong placement of bread:", success)
        if not success:
            return self.info

        # 3. Pick bread from fluted_block and place it onto plate (recovery)
        success = self.pick_and_place(self.bread, self.plate)
        print("Recover bread placement:", success)
        if not success:
            return self.info

        # 4. Pick purple_block and place it into fluted_block
        success = self.pick_and_place(self.purple_block, self.fluted_block)
        print("Place purple_block:", success)
        if not success:
            return self.info

        # 5. Pick yellow_block and place it into fluted_block
        success = self.pick_and_place(self.yellow_block, self.fluted_block)
        print("Place yellow_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify bread is on the plate and all blocks are in the fluted_block
        if (self.check_on(self.bread, self.plate) and
            self.check_on(self.pink_block, self.fluted_block) and
            self.check_on(self.purple_block, self.fluted_block) and
            self.check_on(self.yellow_block, self.fluted_block)):
            return True
        return False
