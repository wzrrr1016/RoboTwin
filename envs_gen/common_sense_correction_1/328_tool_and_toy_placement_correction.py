from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 328_tool_and_toy_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add task objects
        self.drill = self.add_actor("drill", "drill")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractors
        distractor_list = ["calculator", "apple", "book", "pot-with-plant", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Wrong action: Place toycar into wooden_box (should be on coaster)
        success = self.pick_and_place(self.toycar, self.wooden_box)
        print("Place toycar into wooden_box (wrong):", success)
        if not success:
            return self.info

        # Recovery: Move toycar to coaster
        success = self.pick_and_place(self.toycar, self.coaster)
        print("Recover toycar to coaster:", success)
        if not success:
            return self.info

        # Place maintenance tools in wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Place drill into wooden_box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("Place screwdriver into wooden_box:", success)
        if not success:
            return self.info

        # Place small play item on coaster
        success = self.pick_and_place(self.blue_block, self.coaster)
        print("Place blue_block onto coaster:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify maintenance tools in wooden_box and play items on coaster
        if (self.check_on(self.drill, self.wooden_box) and
            self.check_on(self.screwdriver, self.wooden_box) and
            self.check_on(self.toycar, self.coaster) and
            self.check_on(self.blue_block, self.coaster)):
            return True
        return False
