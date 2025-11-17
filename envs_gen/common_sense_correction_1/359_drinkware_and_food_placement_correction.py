from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 359_drinkware_and_food_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load required containers and objects
        self.plate = self.add_actor("plate", "plate")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.mug = self.add_actor("mug", "mug")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.bottle = self.add_actor("bottle", "bottle")
        self.hamburg = self.add_actor("hamburg", "hamburg")

        # Add distractors
        distractor_list = ["calculator", "pet-collar", "hammer", "toycar", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Pick mug and place into fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("pick place mug:", success)
        if not success:
            return self.info

        # Step 2: Pick bottle and place into plate (wrong)
        success = self.pick_and_place(self.bottle, self.plate)
        print("pick place bottle to plate:", success)

        # Step 3: Recovery - Pick bottle from plate and place into fluted_block
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("recovery: pick place bottle to fluted_block:", success)
        if not success:
            return self.info

        # Step 4: Pick cup_without_handle and place into fluted_block
        success = self.pick_and_place(self.cup_without_handle, self.fluted_block)
        print("pick place cup_without_handle:", success)
        if not success:
            return self.info

        # Step 5: Pick hamburg and place into plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("pick place hamburg:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all drinkware is on fluted_block and food is on plate
        if (self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.bottle, self.fluted_block) and
            self.check_on(self.cup_without_handle, self.fluted_block) and
            self.check_on(self.hamburg, self.plate)):
            return True
        return False
