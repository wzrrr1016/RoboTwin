from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class tool_organization_correction_28(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        # Add objects
        self.stapler = self.add_actor("stapler", "stapler")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.can = self.add_actor("can", "can")
        self.book = self.add_actor("book", "book")
        # Optional: Add hammer if it's part of the task
        # self.hammer = self.add_actor("hammer", "hammer")

    def play_once(self):
        # Step 1: Pick stapler and place into tray (correct)
        success = self.pick_and_place(self.stapler, self.tray)
        print("pick place stapler:", success)
        if not success:
            return self.info

        # Step 2: Pick screwdriver and place into tray (wrong)
        success = self.pick_and_place(self.screwdriver, self.tray)
        print("pick place screwdriver (wrong):", success)
        if not success:
            return self.info

        # Step 3: Pick screwdriver from tray and place into shoe_box (correct)
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("pick place screwdriver (correct):", success)
        if not success:
            return self.info

        # Step 4: Pick can and place into shoe_box (correct)
        success = self.pick_and_place(self.can, self.shoe_box)
        print("pick place can:", success)
        if not success:
            return self.info

        # Step 5: Pick book and place into shoe_box (correct)
        success = self.pick_and_place(self.book, self.shoe_box)
        print("pick place book:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check that stapler is in tray
        if not self.check_on(self.stapler, self.tray):
            return False
        # Check that screwdriver is in shoe_box
        if not self.check_on(self.screwdriver, self.shoe_box):
            return False
        # Check that can is in shoe_box
        if not self.check_on(self.can, self.shoe_box):
            return False
        # Check that book is in shoe_box
        if not self.check_on(self.book, self.shoe_box):
            return False
        return True
