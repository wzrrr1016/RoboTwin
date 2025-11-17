from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 248_store_safe_play_and_reading_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add the objects
        self.red_block = self.add_actor("red_block", "red_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.book = self.add_actor("book", "book")
        self.knife = self.add_actor("knife", "knife")
        
        # Add distractors
        distractor_list = ['pot-with-plant', 'alarm-clock', 'tissue-box', 'jam-jar']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Wrong action: Place knife into shoe_box
        success = self.pick_and_place(self.knife, self.shoe_box)
        print("Pick knife and place into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Recovery: Place knife back on table
        success = self.pick_and_place(self.knife, self.table)
        print("Pick knife from shoe_box and place on table (recovery):", success)
        if not success:
            return self.info

        # Place safe play items and reading materials into shoe_box
        success = self.pick_and_place(self.red_block, self.shoe_box)
        print("Pick red_block and place into shoe_box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.blue_block, self.shoe_box)
        print("Pick blue_block and place into shoe_box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.purple_block, self.shoe_box)
        print("Pick purple_block and place into shoe_box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.book, self.shoe_box)
        print("Pick book and place into shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all safe items are in shoe_box and knife is not
        if (self.check_on(self.red_block, self.shoe_box) and
            self.check_on(self.blue_block, self.shoe_box) and
            self.check_on(self.purple_block, self.shoe_box) and
            self.check_on(self.book, self.shoe_box) and
            not self.check_on(self.knife, self.shoe_box)):
            return True
        return False
