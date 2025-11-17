from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 45_sound_related_item_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.microphone = self.add_actor("microphone", "microphone")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.can = self.add_actor("can", "can")

        # Add distractors
        distractor_list = ["calculator", "pet-collar", "table-tennis", "roll-paper", "baguette", "battery"]
        self.add_distractors(distractor_list)

        # Finalize scene setup
        self.check_scene()

    def play_once(self):
        # Place sand-clock in wooden_box (non-sound-related)
        success = self.pick_and_place(self.sand_clock, self.wooden_box)
        if not success:
            return self.info

        # Place small-speaker in shoe_box (sound-related)
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        if not success:
            return self.info

        # Place microphone in shoe_box (sound-related)
        success = self.pick_and_place(self.microphone, self.shoe_box)
        if not success:
            return self.info

        # Place yellow_block in wooden_box (non-sound-related)
        success = self.pick_and_place(self.yellow_block, self.wooden_box)
        if not success:
            return self.info

        # Place can in wooden_box (non-sound-related)
        success = self.pick_and_place(self.can, self.wooden_box)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        # Check if all items are placed correctly
        if (self.check_on(self.small_speaker, self.shoe_box) and
            self.check_on(self.microphone, self.shoe_box) and
            self.check_on(self.sand_clock, self.wooden_box) and
            self.check_on(self.yellow_block, self.wooden_box) and
            self.check_on(self.can, self.wooden_box)):
            return True
        return False
