from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 172_audio_vs_drink_and_toy_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers to the environment
        self.coaster = self.add_actor("coaster", "coaster")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add required objects to the environment
        self.mug = self.add_actor("mug", "mug")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.microphone = self.add_actor("microphone", "microphone")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractor objects to the environment
        distractor_list = ["calculator", "book", "hammer", "shoe", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place small-speaker into wooden_box
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("Place small-speaker:", success)
        if not success:
            return self.info

        # Step 2: Place toycar into wooden_box (wrong action)
        success = self.pick_and_place(self.toycar, self.wooden_box)
        print("Place toycar (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover toycar to coaster
        success = self.pick_and_place(self.toycar, self.coaster)
        print("Place toycar (recovery):", success)
        if not success:
            return self.info

        # Step 4: Place microphone into wooden_box
        success = self.pick_and_place(self.microphone, self.wooden_box)
        print("Place microphone:", success)
        if not success:
            return self.info

        # Step 5: Place mug onto coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Place mug:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all required objects are in their correct final positions
        if (self.check_on(self.small_speaker, self.wooden_box) and
            self.check_on(self.microphone, self.wooden_box) and
            self.check_on(self.toycar, self.coaster) and
            self.check_on(self.mug, self.coaster)):
            return True
        return False
