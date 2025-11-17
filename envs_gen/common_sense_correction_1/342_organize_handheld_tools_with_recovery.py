from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 342_organize_handheld_tools_with_recovery(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.stapler = self.add_actor("stapler", "stapler")
        self.apple = self.add_actor("apple", "apple")
        self.red_block = self.add_actor("red_block", "red_block")
        
        # Add distractors
        distractor_list = ["pot-with-plant", "shoe", "alarm-clock", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Wrong action: pick red_block and place into fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("pick place red_block into fluted_block (wrong):", success)
        if not success:
            return self.info

        # Recovery: pick red_block from fluted_block and place on table
        success = self.pick_and_place(self.red_block, self.table)
        print("pick place red_block on table (recovery):", success)
        if not success:
            return self.info

        # Correct actions
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("pick place hammer:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("pick place stapler:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.apple, self.table)
        print("pick place apple:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify that metal tools are in the organizer and non-tools are properly placed
        if (self.check_on(self.hammer, self.fluted_block) and
            self.check_on(self.stapler, self.fluted_block) and
            self.check_on(self.apple, self.table) and
            not self.check_on(self.red_block, self.fluted_block)):
            return True
        return False
