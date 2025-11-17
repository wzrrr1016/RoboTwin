from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 194_dispose_recover_reusable(Imagine_Task):
    def load_actors(self):
        # Create main containers and objects
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.can = self.add_actor("can", "can")
        self.mouse = self.add_actor("mouse", "mouse")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        
        # Add distractor objects
        distractor_list = ['pet-collar', 'sand-clock', 'red_block', 'green_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Correct placements
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Pick tissue-box and place into dustbin:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Pick french_fries and place into dustbin:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.can, self.dustbin)
        print("Pick can and place into dustbin:", success)
        if not success:
            return self.info
        
        # Wrong action: place mouse into dustbin
        success = self.pick_and_place(self.mouse, self.dustbin)
        print("Pick mouse and place into dustbin (wrong):", success)
        if not success:
            return self.info
        
        # Recovery: move mouse from dustbin to cup_with_handle
        success = self.pick_and_place(self.mouse, self.cup_with_handle)
        print("Pick mouse from dustbin and place into cup_with_handle (recovery):", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Verify all correct items are in dustbin and mouse is properly recovered
        if (self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.french_fries, self.dustbin) and
            self.check_on(self.can, self.dustbin) and
            self.check_on(self.mouse, self.cup_with_handle) and
            not self.check_on(self.mouse, self.dustbin)):
            return True
        return False
