from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 174_place_food_and_nonfood_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        """
        # Create containers
        self.plate = self.add_actor("plate", "plate")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Create objects to be manipulated
        self.apple = self.add_actor("apple", "apple")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.stapler = self.add_actor("stapler", "stapler")
        
        # Add distractor objects to the environment
        distractor_list = ['pet-collar', 'toycar', 'pot-with-plant', 'dumbbell', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions to complete the task.
        Includes a recovery step for the shampoo placement.
        """
        # 1. Wrong action: Place shampoo on plate (incorrect placement)
        success = self.pick_and_place(self.shampoo, self.plate)
        print("Place shampoo on plate (wrong):", success)
        if not success:
            return self.info

        # 2. Recovery action: Move shampoo from plate to shoe_box
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("Move shampoo to shoe_box (recovery):", success)
        if not success:
            return self.info

        # 3. Place edible/perishable item on plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Place apple on plate:", success)
        if not success:
            return self.info

        # 4. Place personal care item in shoe_box
        success = self.pick_and_place(self.tissue_box, self.shoe_box)
        print("Place tissue-box in shoe_box:", success)
        if not success:
            return self.info

        # 5. Place office item in shoe_box
        success = self.pick_and_place(self.stapler, self.shoe_box)
        print("Place stapler in shoe_box:", success)
        if not success:
            return self.info

        return self.info  # Return final state if all actions succeed

    def check_success(self):
        """
        Verify if the task was completed successfully by checking object placements.
        """
        # Check if all required objects are in their correct containers
        if (self.check_on(self.apple, self.plate) and
            self.check_on(self.shampoo, self.shoe_box) and
            self.check_on(self.tissue_box, self.shoe_box) and
            self.check_on(self.stapler, self.shoe_box)):
            return True
        return False
