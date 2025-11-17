from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 129_drinkware_on_plate_correction(Imagine_Task):
    def load_actors(self):
        # Add required containers and objects
        self.plate = self.add_actor("plate", "plate")
        self.mug = self.add_actor("mug", "mug")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractors as specified in the task description
        distractor_list = ['dumbbell', 'microphone', 'alarm-clock', 'shoe', 'calculator']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Pick and place mug on plate
        success = self.pick_and_place(self.mug, self.plate)
        print("Pick and place mug:", success)
        if not success:
            return self.info
            
        # Pick and place cup_without_handle on plate
        success = self.pick_and_place(self.cup_without_handle, self.plate)
        print("Pick and place cup_without_handle:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if both drinkware items are on the plate
        if self.check_on(self.mug, self.plate) and self.check_on(self.cup_without_handle, self.plate):
            return True
        return False
