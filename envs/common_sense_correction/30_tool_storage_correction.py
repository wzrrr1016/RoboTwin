from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class tool_storage_correction_30(Imagine_Task):
    def load_actors(self):
        # Load containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Load objects
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.fork = self.add_actor("fork", "fork")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.scanner = self.add_actor("scanner", "scanner")

    def play_once(self):
        # Pick screwdriver from dustbin and place into wooden_box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("pick place screwdriver:", success)
        if not success:
            return self.info

        # Pick fork and place into wooden_box
        success = self.pick_and_place(self.fork, self.wooden_box)
        print("pick place fork:", success)
        if not success:
            return self.info

        # Pick tissue-box and place into dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("pick place tissue-box:", success)
        if not success:
            return self.info

        # Pick scanner and place into dustbin
        success = self.pick_and_place(self.scanner, self.dustbin)
        print("pick place scanner:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all metal tools (screwdriver, fork) are in wooden_box
        # Check if all non-metal objects (tissue-box, scanner) are in dustbin
        if (self.check_on(self.screwdriver, self.wooden_box) and
            self.check_on(self.fork, self.wooden_box) and
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.scanner, self.dustbin)):
            return True
        return False
