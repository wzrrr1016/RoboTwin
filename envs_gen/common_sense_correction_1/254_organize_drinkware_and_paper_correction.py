from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 254_organize_drinkware_and_paper_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.mug = self.add_actor("mug", "mug")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.book = self.add_actor("book", "book")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractors
        distractors = ["screwdriver", "toycar", "shoe", "dumbbell", "small-speaker"]
        self.add_distractors(distractors)

    def play_once(self):
        # Initial wrong action: Place book in fluted_block
        success = self.pick_and_place(self.book, self.fluted_block)
        print("Place book into fluted_block (wrong):", success)
        if not success:
            return self.info

        # Recovery action: Move book to plate
        success = self.pick_and_place(self.book, self.plate)
        print("Recover: Place book on plate:", success)
        if not success:
            return self.info

        # Place drinkware in fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Place mug into fluted_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup_without_handle, self.fluted_block)
        print("Place cup into fluted_block:", success)
        if not success:
            return self.info

        # Place paper-based item on plate
        success = self.pick_and_place(self.tissue_box, self.plate)
        print("Place tissue-box on plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify drinkware is in fluted_block
        mug_in_fluted = self.check_on(self.mug, self.fluted_block)
        cup_in_fluted = self.check_on(self.cup_without_handle, self.fluted_block)
        
        # Verify paper-based items are on plate
        book_on_plate = self.check_on(self.book, self.plate)
        tissue_on_plate = self.check_on(self.tissue_box, self.plate)
        
        return all([mug_in_fluted, cup_in_fluted, book_on_plate, tissue_on_plate])
