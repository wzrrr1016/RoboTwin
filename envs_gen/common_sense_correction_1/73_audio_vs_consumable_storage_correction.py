from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 73_audio_vs_consumable_storage_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors and distractors in the environment."""
        # Create the wooden box container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Create the main objects for the task
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.microphone = self.add_actor("microphone", "microphone")
        self.bread = self.add_actor("bread", "bread")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractor objects to the environment
        distractor_list = ["calculator", "screwdriver", "toycar", "book", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robotic actions for the task."""
        # Place audio devices on top of the wooden box
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("Place small-speaker:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.microphone, self.wooden_box)
        print("Place microphone:", success)
        if not success:
            return self.info

        # Place consumable item inside the wooden box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Place bread:", success)
        if not success:
            return self.info

        # Initial incorrect placement of tissue box (on top)
        success = self.pick_and_place(self.tissue_box, self.wooden_box)
        print("Place tissue-box (wrong):", success)
        if not success:
            return self.info

        # Recovery: Move tissue box from top to inside the wooden box
        success = self.pick_and_place(self.tissue_box, self.wooden_box)
        print("Recover tissue-box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if all task requirements are successfully completed."""
        # Check if all required objects are properly placed on/into the wooden box
        if (self.check_on(self.small_speaker, self.wooden_box) and
            self.check_on(self.microphone, self.wooden_box) and
            self.check_on(self.bread, self.wooden_box) and
            self.check_on(self.tissue_box, self.wooden_box)):
            return True
        return False
