from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 29_recyclable_item_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        # Add objects
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.mouse = self.add_actor("mouse", "mouse")
        self.fork = self.add_actor("fork", "fork")
        self.book = self.add_actor("book", "book")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")

    def play_once(self):
        # Step 1: Pick book and place into shoe_box
        success = self.pick_and_place(self.book, self.shoe_box)
        print("pick place book:", success)
        if not success:
            return self.info

        # Step 2: Pick tissue-box and place into shoe_box
        success = self.pick_and_place(self.tissue_box, self.shoe_box)
        print("pick place tissue-box:", success)
        if not success:
            return self.info

        # Step 3: Pick orange_block and place into shoe_box (wrong)
        success = self.pick_and_place(self.orange_block, self.shoe_box)
        print("pick place orange_block:", success)
        if not success:
            return self.info

        # Step 4: Pick orange_block and place into dustbin (recovery)
        success = self.pick_and_place(self.orange_block, self.dustbin)
        print("pick place orange_block into dustbin:", success)
        if not success:
            return self.info

        # Step 5: Pick mouse and place into dustbin
        success = self.pick_and_place(self.mouse, self.dustbin)
        print("pick place mouse:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if book and tissue-box are on shoe_box
        if self.check_on(self.book, self.shoe_box) and self.check_on(self.tissue_box, self.shoe_box):
            # Check if orange_block and mouse are on dustbin
            if self.check_on(self.orange_block, self.dustbin) and self.check_on(self.mouse, self.dustbin):
                return True
        return False
