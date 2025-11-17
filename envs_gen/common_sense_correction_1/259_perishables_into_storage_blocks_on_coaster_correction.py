from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 259_perishables_into_storage_blocks_on_coaster_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.coaster = self.add_actor("coaster", "coaster")

        # Add objects
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.green_block = self.add_actor("green_block", "green_block")

        # Add distractors
        distractor_list = ["calculator", "hammer", "stapler", "pot-with-plant", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place bread on coaster (wrong action)
        success = self.pick_and_place(self.bread, self.coaster)
        print("Place bread on coaster (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recover by placing bread into shoe_box
        success = self.pick_and_place(self.bread, self.shoe_box)
        print("Recover: Place bread into shoe_box:", success)
        if not success:
            return self.info

        # Step 3: Place french_fries into shoe_box
        success = self.pick_and_place(self.french_fries, self.shoe_box)
        print("Place french_fries into shoe_box:", success)
        if not success:
            return self.info

        # Step 4: Place blocks on coaster
        success = self.pick_and_place(self.pink_block, self.coaster)
        print("Place pink_block on coaster:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.red_block, self.coaster)
        print("Place red_block on coaster:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.green_block, self.coaster)
        print("Place green_block on coaster:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all soft perishable foods are in shoe_box
        # and all small toy blocks are on coaster
        if (
            self.check_on(self.bread, self.shoe_box) and
            self.check_on(self.french_fries, self.shoe_box) and
            self.check_on(self.pink_block, self.coaster) and
            self.check_on(self.red_block, self.coaster) and
            self.check_on(self.green_block, self.coaster)
        ):
            return True
        return False
