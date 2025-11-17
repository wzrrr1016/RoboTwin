from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 93_consumables_vs_disposables_correction(Imagine_Task):
    def load_actors(self):
        # Add required containers
        self.plate = self.add_actor("plate", "plate")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add target objects
        self.apple = self.add_actor("apple", "apple")
        self.can = self.add_actor("can", "can")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractor objects from the task description
        distractor_list = ['calculator', 'screwdriver', 'toycar', 
                          'alarm-clock', 'pot-with-plant', 'dumbbell']
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Pick can and place it into dustbin (wrong action)
        success = self.pick_and_place(self.can, self.dustbin)
        print("Pick can to dustbin (wrong):", success)
        if not success:
            return self.info

        # 2. Pick can from dustbin and place it onto plate (recovery)
        success = self.pick_and_place(self.can, self.plate)
        print("Recover can to plate:", success)
        if not success:
            return self.info

        # 3. Pick apple and place it onto plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Pick apple to plate:", success)
        if not success:
            return self.info

        # 4. Pick tissue-box and place it into dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Pick tissue-box to dustbin:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all required conditions are met
        apple_on_plate = self.check_on(self.apple, self.plate)
        can_on_plate = self.check_on(self.can, self.plate)
        tissue_in_dustbin = self.check_on(self.tissue_box, self.dustbin)
        
        return apple_on_plate and can_on_plate and tissue_in_dustbin
