from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 26_hygiene_and_food_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects to be manipulated
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.microphone = self.add_actor("microphone", "microphone")
        self.bread = self.add_actor("bread", "bread")

    def play_once(self):
        # Step 1: Pick shampoo and place into shoe_box
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("pick place shampoo:", success)
        if not success:
            return self.info

        # Step 2: Pick microphone and place into shoe_box (wrong)
        success = self.pick_and_place(self.microphone, self.shoe_box)
        print("pick place microphone:", success)
        if not success:
            return self.info

        # Step 3: Pick microphone from shoe_box and place into fluted_block
        success = self.pick_and_place(self.microphone, self.fluted_block)
        print("pick place microphone:", success)
        if not success:
            return self.info

        # Step 4: Pick bread and place into fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("pick place bread:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if shampoo is in shoe_box
        if not self.check_on(self.shampoo, self.shoe_box):
            return False

        # Check if bread is in fluted_block
        if not self.check_on(self.bread, self.fluted_block):
            return False

        # Check if microphone is in fluted_block
        if not self.check_on(self.microphone, self.fluted_block):
            return False

        return True
