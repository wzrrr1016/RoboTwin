from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 287_store_tools_and_display_toys_with_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add required objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.green_block = self.add_actor("green_block", "green_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.drill = self.add_actor("drill", "drill")
        
        # Add distractors
        distractor_list = ["pot-with-plant", "microphone", "small-speaker", "sand-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place lightweight play items and blocks on tray
        success = self.pick_and_place(self.toycar, self.tray)
        print("Place toycar on tray:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.green_block, self.tray)
        print("Place green_block on tray:", success)
        if not success:
            return self.info
            
        # Wrong placement of tool (drill) on tray
        success = self.pick_and_place(self.drill, self.tray)
        print("Wrongly place drill on tray:", success)
        if not success:
            return self.info
            
        # Recovery: Move drill to shoe_box
        success = self.pick_and_place(self.drill, self.shoe_box)
        print("Move drill to shoe_box:", success)
        if not success:
            return self.info
            
        # Final placement
        success = self.pick_and_place(self.yellow_block, self.tray)
        print("Place yellow_block on tray:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in correct containers
        if (self.check_on(self.toycar, self.tray) and
            self.check_on(self.green_block, self.tray) and
            self.check_on(self.yellow_block, self.tray) and
            self.check_on(self.drill, self.shoe_box)):
            return True
        return False
