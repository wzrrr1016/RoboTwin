from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 124_sound_vs_disposable_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.bread = self.add_actor("bread", "bread")
        self.microphone = self.add_actor("microphone", "microphone")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.bell = self.add_actor("bell", "bell")
        
        # Add distractors
        distractors = ["calculator", "screwdriver", "pot-with-plant", "shoe", "book"]
        self.add_distractors(distractors)

    def play_once(self):
        # Place disposable/perishable items in shoe_box
        success = self.pick_and_place(self.tissue_box, self.shoe_box)
        print("tissue-box to shoe_box:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.bread, self.shoe_box)
        print("bread to shoe_box:", success)
        if not success:
            return self.info
            
        # Place sound-producing/handling items in wooden_box
        success = self.pick_and_place(self.microphone, self.wooden_box)
        print("microphone to wooden_box:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("small-speaker to wooden_box:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.bell, self.wooden_box)
        print("bell to wooden_box:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        # Verify all items are in correct containers
        if (self.check_on(self.tissue_box, self.shoe_box) and
            self.check_on(self.bread, self.shoe_box) and
            self.check_on(self.microphone, self.wooden_box) and
            self.check_on(self.small_speaker, self.wooden_box) and
            self.check_on(self.bell, self.wooden_box)):
            return True
        return False
