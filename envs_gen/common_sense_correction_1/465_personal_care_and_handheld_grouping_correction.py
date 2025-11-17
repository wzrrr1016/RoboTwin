from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 465_personal_care_and_handheld_grouping_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add target objects
        self.markpen = self.add_actor("markpen", "markpen")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractors
        distractor_list = ["chips-tub", "milk-box", "baguette", "apple"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Initial wrong action: markpen into shoe_box
        success = self.pick_and_place(self.markpen, self.shoe_box)
        print("Pick markpen into shoe_box (wrong):", success)
        if not success:
            return self.info
        
        # Recovery action: move markpen to fluted_block
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Recover markpen to fluted_block:", success)
        if not success:
            return self.info
        
        # Place personal-care items in shoe_box
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("Place shampoo into shoe_box:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.tissue_box, self.shoe_box)
        print("Place tissue-box into shoe_box:", success)
        if not success:
            return self.info
        
        # Place handheld objects on fluted_block
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Place cup_with_handle into fluted_block:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar into fluted_block:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        if (self.check_on(self.shampoo, self.shoe_box) and
            self.check_on(self.tissue_box, self.shoe_box) and
            self.check_on(self.markpen, self.fluted_block) and
            self.check_on(self.cup_with_handle, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block)):
            return True
        return False
