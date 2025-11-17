from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 229_organize_play_and_electronics_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.small_speaker = self.add_actor("small-speaker", "small_speaker")
        self.microphone = self.add_actor("microphone", "microphone")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        
        # Add distractors
        distractor_list = ["apple", "baguette", "mug", "shampoo", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place toycar on fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar:", success)
        if not success:
            return self.info
        
        # Place small-speaker in wooden_box
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("Place small-speaker:", success)
        if not success:
            return self.info
        
        # Wrong placement: microphone on fluted_block
        success = self.pick_and_place(self.microphone, self.fluted_block)
        print("Wrong placement of microphone:", success)
        if not success:
            return self.info
        
        # Recovery: move microphone to wooden_box
        success = self.pick_and_place(self.microphone, self.wooden_box)
        print("Recover microphone:", success)
        if not success:
            return self.info
        
        # Place orange_block on fluted_block
        success = self.pick_and_place(self.orange_block, self.fluted_block)
        print("Place orange_block:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Verify all required placements
        if (
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.small_speaker, self.wooden_box) and
            self.check_on(self.microphone, self.wooden_box) and
            self.check_on(self.orange_block, self.fluted_block)
        ):
            return True
        return False
