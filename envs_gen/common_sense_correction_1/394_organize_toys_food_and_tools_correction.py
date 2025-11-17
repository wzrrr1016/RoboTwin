from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 394_organize_toys_food_and_tools_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.fork = self.add_actor("fork", "fork")
        
        # Add distractors
        distractor_list = ["pot-with-plant", "shoe", "book", "tissue-box", "markpen"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Put purple_block on tray
        success = self.pick_and_place(self.purple_block, self.tray)
        print("Pick purple_block and place into tray:", success)
        if not success:
            return self.info
        
        # Step 2: Put pink_block on tray
        success = self.pick_and_place(self.pink_block, self.tray)
        print("Pick pink_block and place into tray:", success)
        if not success:
            return self.info
        
        # Step 3: Put french_fries on tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Pick french_fries and place into tray:", success)
        if not success:
            return self.info
        
        # Step 4: Put small-speaker on tray (wrong placement)
        success = self.pick_and_place(self.small_speaker, self.tray)
        print("Pick small_speaker and place into tray (wrong):", success)
        if not success:
            return self.info
        
        # Step 5: Move small-speaker to fluted_block (recovery)
        success = self.pick_and_place(self.small_speaker, self.fluted_block)
        print("Pick small_speaker from tray and place into fluted_block (recovery):", success)
        if not success:
            return self.info
        
        # Step 6: Put fork in fluted_block
        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Pick fork and place into fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all required objects are in their correct containers
        if (self.check_on(self.purple_block, self.tray) and
            self.check_on(self.pink_block, self.tray) and
            self.check_on(self.french_fries, self.tray) and
            self.check_on(self.small_speaker, self.fluted_block) and
            self.check_on(self.fork, self.fluted_block)):
            return True
        return False
