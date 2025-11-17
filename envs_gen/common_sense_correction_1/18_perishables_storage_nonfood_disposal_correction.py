from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 18_perishables_storage_nonfood_disposal_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Containers (wooden_box and dustbin) are added as actors.
        Objects (apple, bread, shampoo, small-speaker) are added as actors.
        Distractors are added using the add_distractors API.
        """
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        
        # Add distractors
        distractor_list = ["toycar", "pot-with-plant", "book", "hammer", "red_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions defined in the task:
        1. Pick apple and place it into dustbin (wrong action)
        2. Pick apple and place it into wooden_box (recovery)
        3. Pick bread and place it into wooden_box
        4. Pick shampoo and place it into dustbin
        5. Pick small-speaker and place it into dustbin
        """
        # Wrong action: apple to dustbin
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Pick apple and place into dustbin (wrong):", success)
        if not success:
            return self.info

        # Recovery: apple to wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Pick apple and place into wooden_box (recovery):", success)
        if not success:
            return self.info

        # Place bread into wooden_box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Pick bread and place into wooden_box:", success)
        if not success:
            return self.info

        # Place shampoo into dustbin
        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Pick shampoo and place into dustbin:", success)
        if not success:
            return self.info

        # Place small-speaker into dustbin
        success = self.pick_and_place(self.small_speaker, self.dustbin)
        print("Pick small-speaker and place into dustbin:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if all objects are placed in the correct containers:
        - Perishable edible items (apple, bread) in wooden_box
        - Non-food items (shampoo, small-speaker) in dustbin
        """
        if (self.check_on(self.apple, self.wooden_box) and
            self.check_on(self.bread, self.wooden_box) and
            self.check_on(self.shampoo, self.dustbin) and
            self.check_on(self.small_speaker, self.dustbin)):
            return True
        return False
