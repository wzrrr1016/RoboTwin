from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 302_organize_play_and_natural_items_with_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.apple = self.add_actor("apple", "apple")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

        # Add distractors
        distractor_list = ["calculator", "screwdriver", "hammer", "stapler", "mouse"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place toycar into fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("pick place toycar:", success)
        if not success:
            return self.info

        # Place yellow_block into fluted_block
        success = self.pick_and_place(self.yellow_block, self.fluted_block)
        print("pick place yellow_block:", success)
        if not success:
            return self.info

        # Wrongly place apple into fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("pick place apple (wrong):", success)
        if not success:
            return self.info

        # Correct apple placement into shoe_box
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("pick place apple (correct):", success)
        if not success:
            return self.info

        # Place pot-with-plant into shoe_box
        success = self.pick_and_place(self.pot_with_plant, self.shoe_box)
        print("pick place pot-with-plant:", success)
        if not success:
            return self.info

    def check_success(self):
        if (self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.yellow_block, self.fluted_block) and
            self.check_on(self.apple, self.shoe_box) and
            self.check_on(self.pot_with_plant, self.shoe_box)):
            return True
        return False
