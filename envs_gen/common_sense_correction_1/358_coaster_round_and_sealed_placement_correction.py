from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 358_coaster_round_and_sealed_placement_correction(Imagine_Task):
    def load_actors(self):
        self.coaster = self.add_actor("coaster", "coaster")
        self.can = self.add_actor("can", "can")
        self.apple = self.add_actor("apple", "apple")
        self.book = self.add_actor("book", "book")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        distractors = ['calculator', 'hammer', 'shoe', 'toycar', 'stapler']
        self.add_distractors(distractors)

    def play_once(self):
        # Step 1: Place tissue-box on coaster (wrong action)
        success = self.pick_and_place(self.tissue_box, self.coaster)
        print("Place tissue-box on coaster (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recover by placing tissue-box on table
        success = self.pick_and_place(self.tissue_box, self.table)
        print("Recover tissue-box to table:", success)
        if not success:
            return self.info

        # Step 3: Place can on coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Place can on coaster:", success)
        if not success:
            return self.info

        # Step 4: Place apple on coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple on coaster:", success)
        if not success:
            return self.info

        # Step 5: Place book on table
        success = self.pick_and_place(self.book, self.table)
        print("Place book on table:", success)
        if not success:
            return self.info

    def check_success(self):
        if (
            self.check_on(self.apple, self.coaster) and
            self.check_on(self.can, self.coaster) and
            self.check_on(self.tissue_box, self.table) and
            self.check_on(self.book, self.table)
        ):
            return True
        return False
