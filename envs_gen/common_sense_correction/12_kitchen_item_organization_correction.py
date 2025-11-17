from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 12_kitchen_item_organization_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        This includes containers, target objects, and distractors.
        """
        # Add containers to the environment
        self.tray = self.add_actor("tray", "tray")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add kitchen and non-kitchen objects
        self.knife = self.add_actor("knife", "knife")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.mug = self.add_actor("mug", "mug")
        self.bread = self.add_actor("bread", "bread")
        self.mouse = self.add_actor("mouse", "mouse")
        
        # Add distractor objects to the environment
        distractor_list = ['drill', 'dumbbell', 'fluted_block', 'teanet', 'tissue-box', 'battery']
        self.add_distractors(distractor_list)
        
        # Final check to ensure all actors are properly placed
        self.check_scene()

    def play_once(self):
        """
        Execute the robot's task sequence:
        1. Place kitchen items in the tray
        2. Place mouse in tray (wrong action)
        3. Correct by placing mouse in wooden box
        """
        # Place kitchen items in tray
        success = self.pick_and_place(self.knife, self.tray)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.cup_with_handle, self.tray)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.mug, self.tray)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.bread, self.tray)
        if not success:
            return self.info
            
        # Wrong placement - mouse in tray
        success = self.pick_and_place(self.mouse, self.tray)
        if not success:
            return self.info
            
        # Recovery - move mouse to correct container
        success = self.pick_and_place(self.mouse, self.wooden_box)
        if not success:
            return self.info
            
        # Mark task completion
        self.add_end()
        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - All kitchen items in tray
        - Mouse in wooden box
        """
        # Check kitchen items in tray
        kitchen_items_in_tray = (
            self.check_on(self.knife, self.tray) and
            self.check_on(self.cup_with_handle, self.tray) and
            self.check_on(self.mug, self.tray) and
            self.check_on(self.bread, self.tray)
        )
        
        # Check mouse in wooden box
        mouse_in_wooden_box = self.check_on(self.mouse, self.wooden_box)
        
        # Return overall success status
        return kitchen_items_in_tray and mouse_in_wooden_box
