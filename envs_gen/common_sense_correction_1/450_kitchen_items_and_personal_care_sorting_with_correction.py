from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 450_kitchen_items_and_personal_care_sorting_with_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors in the environment"""
        # Create containers
        self.plate = self.add_actor("plate", "plate")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Create required objects
        self.mug = self.add_actor("mug", "mug")
        self.teanet = self.add_actor("teanet", "teanet")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.knife = self.add_actor("knife", "knife")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        
        # Add distractor objects
        distractor_list = ['calculator', 'pet-collar', 'toycar', 'pot-with-plant', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of pick-and-place actions"""
        # Place eating/drinking items on plate
        success = self.pick_and_place(self.mug, self.plate)
        print("Place mug on plate:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.teanet, self.plate)
        print("Place teanet on plate:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french fries on plate:", success)
        if not success:
            return self.info
            
        # Initial incorrect placement of knife (needs recovery)
        success = self.pick_and_place(self.knife, self.plate)
        print("Place knife on plate (wrong):", success)
        if not success:
            return self.info
            
        # Recovery: Move knife to proper container
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("Move knife to wooden box:", success)
        if not success:
            return self.info
            
        # Place personal care items in wooden box
        success = self.pick_and_place(self.shampoo, self.wooden_box)
        print("Place shampoo in wooden box:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        """Verify if all items are in their correct final positions"""
        # Check food and kitchen items on plate
        plate_check = (
            self.check_on(self.mug, self.plate) and
            self.check_on(self.teanet, self.plate) and
            self.check_on(self.french_fries, self.plate)
        )
        
        # Check personal care and sharp items in wooden box
        box_check = (
            self.check_on(self.knife, self.wooden_box) and
            self.check_on(self.shampoo, self.wooden_box)
        )
        
        return plate_check and box_check
