from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class decorative_item_sorting_correction_36(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Load objects to be placed
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.scanner = self.add_actor("scanner", "scanner")
        self.can = self.add_actor("can", "can")
        self.stapler = self.add_actor("stapler", "stapler")
        self.book = self.add_actor("book", "book")

    def play_once(self):
        # Place pot-with-plant into coaster
        success = self.pick_and_place(self.pot_with_plant, self.coaster)
        print("pick place pot_with_plant:", success)
        if not success:
            return self.info

        # Place tissue-box into coaster
        success = self.pick_and_place(self.tissue_box, self.coaster)
        print("pick place tissue_box:", success)
        if not success:
            return self.info

        # Place scanner into wooden_box
        success = self.pick_and_place(self.scanner, self.wooden_box)
        print("pick place scanner:", success)
        if not success:
            return self.info

        # Place can into wooden_box
        success = self.pick_and_place(self.can, self.wooden_box)
        print("pick place can:", success)
        if not success:
            return self.info

        # Place stapler into wooden_box
        success = self.pick_and_place(self.stapler, self.wooden_box)
        print("pick place stapler:", success)
        if not success:
            return self.info

        # Place book into wooden_box
        success = self.pick_and_place(self.book, self.wooden_box)
        print("pick place book:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all decorative items are on the coaster
        if (self.check_on(self.pot_with_plant, self.coaster) and
            self.check_on(self.tissue_box, self.coaster)):

            # Check if all office items are on the wooden_box
            if (self.check_on(self.scanner, self.wooden_box) and
                self.check_on(self.can, self.wooden_box) and
                self.check_on(self.stapler, self.wooden_box) and
                self.check_on(self.book, self.wooden_box)):

                return True

        return False
