from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 461_tools_and_drinkware_organize_correction(Imagine_Task):
    def load_actors(self):
        # Add the organizer container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add hand tools and drinkware
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add distractors
        distractor_list = ['calculator', 'pet-collar', 'toycar', 'book', 'apple']
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Pick hammer and place into fluted_block
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Pick place hammer:", success)
        if not success:
            return self.info

        # 2. Pick bottle and place onto table (wrong)
        success = self.pick_and_place(self.bottle, self.table)
        print("Pick place bottle onto table (wrong):", success)
        if not success:
            return self.info

        # 3. Pick bottle from table and place into fluted_block (recovery)
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Pick place bottle into fluted_block (recovery):", success)
        if not success:
            return self.info

        # 4. Pick screwdriver and place into fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Pick place screwdriver:", success)
        if not success:
            return self.info

        # 5. Pick cup_with_handle and place into fluted_block
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Pick place cup_with_handle:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all hand tools and drinkware are in the organizer
        if (self.check_on(self.hammer, self.fluted_block) and
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.cup_with_handle, self.fluted_block) and
            self.check_on(self.bottle, self.fluted_block)):
            return True
        return False
