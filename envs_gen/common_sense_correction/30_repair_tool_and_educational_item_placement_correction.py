from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 30_repair_tool_and_educational_item_placement_correction(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.tray = self.add_actor("tray", "tray")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Load objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.book = self.add_actor("book", "book")
        self.red_block = self.add_actor("red_block", "red_block")
        self.green_block = self.add_actor("green_block", "green_block")

    def play_once(self):
        # Step 1: Pick screwdriver and place into tray
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("pick place screwdriver:", success)
        if not success:
            return self.info

        # Step 2: Pick book and place into tray (wrong)
        success = self.pick_and_place(self.book, self.tray)
        print("pick place book into tray:", success)
        if not success:
            return self.info

        # Step 3: Pick book from tray and place into fluted_block (recovery)
        success = self.pick_and_place(self.book, self.fluted_block)
        print("pick place book into fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if screwdriver is on tray and book is on fluted_block
        if self.check_on(self.screwdriver, self.tray) and self.check_on(self.book, self.fluted_block):
            return True
        return False
