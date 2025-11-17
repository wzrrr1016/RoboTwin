from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 54_timepieces_and_consumables_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add objects
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.apple = self.add_actor("apple", "apple")
        
        # Add distractors
        distractor_list = ["screwdriver", "hammer", "toycar", "book", "markpen"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place alarm clock in organizer
        success = self.pick_and_place(self.alarm_clock, self.fluted_block)
        print("Place alarm clock:", success)
        if not success:
            return self.info

        # Step 2: Wrong placement of shampoo
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Place shampoo (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recovery - Move shampoo to coaster
        success = self.pick_and_place(self.shampoo, self.coaster)
        print("Recover shampoo:", success)
        if not success:
            return self.info

        # Step 4: Place sand clock in organizer
        success = self.pick_and_place(self.sand_clock, self.fluted_block)
        print("Place sand clock:", success)
        if not success:
            return self.info

        # Step 5: Place apple on coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all objects are in their correct final locations
        if (self.check_on(self.alarm_clock, self.fluted_block) and
            self.check_on(self.sand_clock, self.fluted_block) and
            self.check_on(self.shampoo, self.coaster) and
            self.check_on(self.apple, self.coaster)):
            return True
        return False
