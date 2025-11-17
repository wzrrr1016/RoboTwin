from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 473_portable_electronics_to_plate_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the plate as the container
        self.plate = self.add_actor("plate", "plate")
        # Add the required objects
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.microphone = self.add_actor("microphone", "microphone")
        self.mouse = self.add_actor("mouse", "mouse")
        # Add distractors to the environment
        distractor_list = ["pot-with-plant", "dumbbell", "shoe", "sand-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place small-speaker on the plate
        success = self.pick_and_place(self.small_speaker, self.plate)
        print("Place small-speaker:", success)
        if not success:
            return self.info

        # Step 2: Place microphone on the table (wrong action)
        success = self.pick_and_place(self.microphone, self.table)
        print("Place microphone on table (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover microphone to the plate
        success = self.pick_and_place(self.microphone, self.plate)
        print("Recover microphone to plate:", success)
        if not success:
            return self.info

        # Step 4: Place mouse on the plate
        success = self.pick_and_place(self.mouse, self.plate)
        print("Place mouse:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all required objects are on the plate
        return (
            self.check_on(self.small_speaker, self.plate) and
            self.check_on(self.microphone, self.plate) and
            self.check_on(self.mouse, self.plate)
        )
