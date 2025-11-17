from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 41_toy_and_footwear_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.tray = self.add_actor("tray", "tray")
        
        # Add required objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.shoe = self.add_actor("shoe", "shoe")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add distractors
        distractor_list = ['calculator', 'pet-collar', 'alarm-clock', 'dumbbell', 'book']
        self.add_distractors(distractor_list)
        
        # Final scene check
        self.check_scene()

    def play_once(self):
        # Step 1: Wrong placement of toycar into shoe_box
        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("Pick toycar into shoe_box:", success)
        if not success:
            return self.info
            
        # Step 2: Recovery - move toycar to tray
        success = self.pick_and_place(self.toycar, self.tray)
        print("Pick toycar into tray:", success)
        if not success:
            return self.info
            
        # Step 3: Place orange_block into tray
        success = self.pick_and_place(self.orange_block, self.tray)
        print("Pick orange_block into tray:", success)
        if not success:
            return self.info
            
        # Step 4: Place blue_block into tray
        success = self.pick_and_place(self.blue_block, self.tray)
        print("Pick blue_block into tray:", success)
        if not success:
            return self.info
            
        # Step 5: Place yellow_block into tray
        success = self.pick_and_place(self.yellow_block, self.tray)
        print("Pick yellow_block into tray:", success)
        if not success:
            return self.info
            
        # Step 6: Place shoe into shoe_box
        success = self.pick_and_place(self.shoe, self.shoe_box)
        print("Pick shoe into shoe_box:", success)
        if not success:
            return self.info
            
        self.add_end()
        return self.info

    def check_success(self):
        # Verify all toys are in tray and shoe is in shoe_box
        if (self.check_on(self.toycar, self.tray) and
            self.check_on(self.orange_block, self.tray) and
            self.check_on(self.blue_block, self.tray) and
            self.check_on(self.yellow_block, self.tray) and
            self.check_on(self.shoe, self.shoe_box)):
            return True
        return False
