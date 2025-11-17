from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 481_paper_and_non_sharp_grouping_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment"""
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.book = self.add_actor("book", "book")
        self.scanner = self.add_actor("scanner", "scanner")
        self.fork = self.add_actor("fork", "fork")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.knife = self.add_actor("knife", "knife")
        
        # Add distractors
        distractor_list = ['toycar', 'pot-with-plant', 'dumbbell', 'red_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of pick-and-place actions"""
        # Place tissue-box (non-sharp paper-based item) in fluted_block
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Place tissue-box:", success)
        if not success:
            return self.info

        # Wrong placement - book (paper-based) in shoe_box
        success = self.pick_and_place(self.book, self.shoe_box)
        print("Place book (wrong):", success)
        if not success:
            return self.info

        # Recovery - move book to correct container
        success = self.pick_and_place(self.book, self.fluted_block)
        print("Recover book:", success)
        if not success:
            return self.info

        # Place scanner (electronic) in shoe_box
        success = self.pick_and_place(self.scanner, self.shoe_box)
        print("Place scanner:", success)
        if not success:
            return self.info

        # Place knife (sharp) in shoe_box
        success = self.pick_and_place(self.knife, self.shoe_box)
        print("Place knife:", success)
        if not success:
            return self.info

        # Place fork (non-sharp) in fluted_block
        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Place fork:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if all objects are in their correct containers"""
        return (
            self.check_on(self.tissue_box, self.fluted_block) and  # Non-sharp paper-based
            self.check_on(self.book, self.fluted_block) and        # Non-sharp paper-based
            self.check_on(self.scanner, self.shoe_box) and         # Electronic
            self.check_on(self.knife, self.shoe_box) and           # Sharp
            self.check_on(self.fork, self.fluted_block)            # Non-sharp
        )
