from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 306_place_reusable_and_disposable_items(Imagine_Task):
    def load_actors(self):
        # Add containers to the environment
        self.coaster = self.add_actor("coaster", "coaster")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add required objects to the environment
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.bottle = self.add_actor("bottle", "bottle")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add distractor objects to the environment
        distractor_list = ["red_block", "green_block", "blue_block", "yellow_block", "purple_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Place pot-with-plant on coaster
        success = self.pick_and_place(self.pot_with_plant, self.coaster)
        print("Place pot-with-plant:", success)
        if not success:
            return self.info

        # 2. Place bottle on coaster (wrong action)
        success = self.pick_and_place(self.bottle, self.coaster)
        print("Place bottle on coaster (wrong):", success)
        if not success:
            return self.info

        # 3. Recovery: Move bottle from coaster to dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Recover bottle to dustbin:", success)
        if not success:
            return self.info

        # 4. Place small-speaker on coaster
        success = self.pick_and_place(self.small_speaker, self.coaster)
        print("Place small-speaker:", success)
        if not success:
            return self.info

        # 5. Place french_fries in dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Place french fries:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        if (self.check_on(self.pot_with_plant, self.coaster) and
            self.check_on(self.small_speaker, self.coaster) and
            self.check_on(self.bottle, self.dustbin) and
            self.check_on(self.french_fries, self.dustbin)):
            return True
        return False
