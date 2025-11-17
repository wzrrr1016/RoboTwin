from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 379_store_reusables_and_dispose_disposables_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add objects to be sorted
        self.book = self.add_actor("book", "book")
        self.mug = self.add_actor("mug", "mug")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add distractor objects
        distractor_list = ["apple", "baguette", "chips-tub", "french_fries", "hamburg"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place book in shoe_box (durable item)
        success = self.pick_and_place(self.book, self.shoe_box)
        print("Book placement:", success)
        if not success:
            return self.info

        # Step 2: Place mug in shoe_box (durable item)
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("Mug placement:", success)
        if not success:
            return self.info

        # Step 3: Place tissue-box in dustbin (disposable item)
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Tissue-box placement:", success)
        if not success:
            return self.info

        # Step 4: Incorrect placement of bottle in dustbin (disposable)
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Bottle (wrong) placement:", success)
        if not success:
            return self.info

        # Step 5: Recovery - Move bottle to shoe_box (correct placement)
        success = self.pick_and_place(self.bottle, self.shoe_box)
        print("Bottle (recovery) placement:", success)
        if not success:
            return self.info

        return self.info  # All steps completed successfully

    def check_success(self):
        # Verify final positions match task requirements
        if (self.check_on(self.book, self.shoe_box) and
            self.check_on(self.mug, self.shoe_box) and
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.bottle, self.shoe_box)):
            return True
        return False
