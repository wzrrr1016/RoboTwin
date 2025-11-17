from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 16_desk_items_on_tray_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the environment.
        - Tray is the main container.
        - Objects: book, stapler, bottle, pink_block.
        - Distractors: shoe, dumbbell, battery, chips-tub, baguette.
        """
        # Add the tray container
        self.tray = self.add_actor("tray", "tray")
        
        # Add objects used for working/reading and other relevant items
        self.book = self.add_actor("book", "book")
        self.stapler = self.add_actor("stapler", "stapler")
        self.bottle = self.add_actor("bottle", "bottle")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        
        # Add distractors (items not relevant to the task)
        distractor_list = ["shoe", "dumbbell", "battery", "chips-tub", "baguette"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the environment:
        1. Place book and stapler on the tray (work/reading items).
        2. Place bottle on the tray (wrong action, then recover).
        3. Place pink_block on the table (not for the tray).
        """
        # Place book on the tray
        success = self.pick_and_place(self.book, self.tray)
        print("Pick book:", success)
        if not success:
            return self.info

        # Place stapler on the tray
        success = self.pick_and_place(self.stapler, self.tray)
        print("Pick stapler:", success)
        if not success:
            return self.info

        # Place bottle on the tray (wrong action)
        success = self.pick_and_place(self.bottle, self.tray)
        print("Pick bottle (wrong):", success)
        if not success:
            return self.info

        # Recover by placing bottle on the table
        success = self.pick_and_place(self.bottle, self.table)
        print("Recover bottle:", success)
        if not success:
            return self.info

        # Place pink_block on the table (not for the tray)
        success = self.pick_and_place(self.pink_block, self.table)
        print("Pick pink_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully:
        - Book and stapler are on the tray.
        - Bottle and pink_block are on the table (not on the tray).
        """
        # Check if book and stapler are on the tray
        book_on_tray = self.check_on(self.book, self.tray)
        stapler_on_tray = self.check_on(self.stapler, self.tray)
        
        # Check if bottle and pink_block are on the table
        bottle_on_table = self.check_on(self.bottle, self.table)
        pink_block_on_table = self.check_on(self.pink_block, self.table)
        
        # Return True only if all conditions are met
        return book_on_tray and stapler_on_tray and bottle_on_table and pink_block_on_table
