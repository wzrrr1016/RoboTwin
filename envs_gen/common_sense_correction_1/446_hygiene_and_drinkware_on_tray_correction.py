from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 446_hygiene_and_drinkware_on_tray_correction(Imagine_Task):
    def load_actors(self):
        # Load the tray and relevant objects
        self.tray = self.add_actor("tray", "tray")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.green_block = self.add_actor("green_block", "green_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")

        # Add distractors to the environment
        distractors = ["calculator", "hammer", "shoe", "book", "stapler"]
        self.add_distractors(distractors)

    def play_once(self):
        # Step 1: Wrongly place green_block on tray
        success = self.pick_and_place(self.green_block, self.tray)
        print("Pick green_block and place into tray (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - place green_block back on the table
        success = self.pick_and_place(self.green_block, self.table)
        print("Pick green_block from tray and place on table (recovery):", success)
        if not success:
            return self.info

        # Step 3: Place hygiene and drinkware items on the tray
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Pick shampoo and place into tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.tissue_box, self.tray)
        print("Pick tissue-box and place into tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup_with_handle, self.tray)
        print("Pick cup_with_handle and place into tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Task is successful if:
        # - All hygiene and drinkware items are on the tray
        # - No toy blocks are on the tray
        hygiene_on_tray = (
            self.check_on(self.shampoo, self.tray) and
            self.check_on(self.tissue_box, self.tray) and
            self.check_on(self.cup_with_handle, self.tray)
        )
        toys_off_tray = (
            not self.check_on(self.green_block, self.tray) and
            not self.check_on(self.purple_block, self.tray)
        )

        return hygiene_on_tray and toys_off_tray
