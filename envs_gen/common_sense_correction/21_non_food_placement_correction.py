from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 21_non_food_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.plate = self.add_actor("plate", "plate")
        # Add objects
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.book = self.add_actor("book", "book")
        self.french_fries = self.add_actor("french_fries", "french_fries")

    def play_once(self):
        # Step 1: Pick tissue-box and place into tray (non-food)
        success = self.pick_and_place(self.tissue_box, self.tray)
        print("pick place tissue-box:", success)
        if not success:
            return self.info

        # Step 2: Pick book and place into tray (non-food)
        success = self.pick_and_place(self.book, self.tray)
        print("pick place book:", success)
        if not success:
            return self.info

        # Step 3: Pick french_fries and place into plate (food)
        success = self.pick_and_place(self.french_fries, self.plate)
        print("pick place french_fries:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all non-food items are in the tray and food item is in the plate
        if (self.check_on(self.tissue_box, self.tray) and
            self.check_on(self.book, self.tray) and
            self.check_on(self.french_fries, self.plate)):
            return True
        return False
