from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 416_store_reading_and_disposable_items_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        - Containers: fluted_block, shoe_box
        - Objects: book, markpen, tissue-box, bottle
        - Distractors: toycar, dumbbell, shoe, alarm-clock, red_block
        """
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.book = self.add_actor("book", "book")
        self.markpen = self.add_actor("markpen", "markpen")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.bottle = self.add_actor("bottle", "bottle")

        # Add distractors
        distractor_list = ["toycar", "dumbbell", "shoe", "alarm-clock", "red_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        Actions:
        1. Pick book and place it into shoe_box
        2. Pick bottle and place it into shoe_box (wrong)
        3. Pick bottle from shoe_box and place it onto fluted_block (recovery)
        4. Pick markpen and place it into shoe_box
        5. Pick tissue-box and place it onto fluted_block
        """
        # Step 1: Place book into shoe_box
        success = self.pick_and_place(self.book, self.shoe_box)
        print("Place book into shoe_box:", success)
        if not success:
            return self.info

        # Step 2: Wrongly place bottle into shoe_box
        success = self.pick_and_place(self.bottle, self.shoe_box)
        print("Place bottle into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover: Move bottle to fluted_block
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Move bottle to fluted_block:", success)
        if not success:
            return self.info

        # Step 4: Place markpen into shoe_box
        success = self.pick_and_place(self.markpen, self.shoe_box)
        print("Place markpen into shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place tissue-box onto fluted_block
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Place tissue-box onto fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Reading and writing materials (book, markpen) should be in shoe_box
        - Disposable or liquid-holding items (bottle, tissue-box) should be on fluted_block
        """
        if (self.check_on(self.book, self.shoe_box) and
            self.check_on(self.markpen, self.shoe_box) and
            self.check_on(self.bottle, self.fluted_block) and
            self.check_on(self.tissue_box, self.fluted_block)):
            return True
        return False
