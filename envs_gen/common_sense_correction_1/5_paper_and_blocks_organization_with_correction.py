from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 5_paper_and_blocks_organization_with_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.tray = self.add_actor("tray", "tray")
        
        # Add required objects
        self.book = self.add_actor("book", "book")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add distractors
        distractor_list = ["dumbbell", "microphone", "battery", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place book in shoe_box
        success = self.pick_and_place(self.book, self.shoe_box)
        print("Book to shoe_box:", success)
        if not success:
            return self.info

        # Step 2: Place purple_block on tray
        success = self.pick_and_place(self.purple_block, self.tray)
        print("Purple block to tray:", success)
        if not success:
            return self.info

        # Step 3: Wrong placement - tissue-box on tray
        success = self.pick_and_place(self.tissue_box, self.tray)
        print("Tissue-box to tray (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recovery - move tissue-box to shoe_box
        success = self.pick_and_place(self.tissue_box, self.shoe_box)
        print("Tissue-box to shoe_box (recovery):", success)
        if not success:
            return self.info

        # Step 5: Place green_block on tray
        success = self.pick_and_place(self.green_block, self.tray)
        print("Green block to tray:", success)
        if not success:
            return self.info

        # Step 6: Place yellow_block on tray
        success = self.pick_and_place(self.yellow_block, self.tray)
        print("Yellow block to tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify book and tissue-box are in shoe_box
        book_in_shoe = self.check_on(self.book, self.shoe_box)
        tissue_in_shoe = self.check_on(self.tissue_box, self.shoe_box)
        
        # Verify blocks are on tray
        purple_on_tray = self.check_on(self.purple_block, self.tray)
        green_on_tray = self.check_on(self.green_block, self.tray)
        yellow_on_tray = self.check_on(self.yellow_block, self.tray)
        
        # Return True if all conditions are met
        return all([book_in_shoe, tissue_in_shoe, purple_on_tray, green_on_tray, yellow_on_tray])
