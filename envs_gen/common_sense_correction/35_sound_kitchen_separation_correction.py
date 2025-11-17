from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 35_sound_kitchen_separation_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.plate = self.add_actor("plate", "plate")

        # Add objects
        self.teanet = self.add_actor("teanet", "teanet")
        self.bell = self.add_actor("bell", "bell")
        self.microphone = self.add_actor("microphone", "microphone")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")

        # Add distractors
        distractor_list = [
            "calculator", "pet-collar", "table-tennis", "battery", "sand-clock", "shoe"
        ]
        self.add_distractors(distractor_list)

        # Finalize scene setup
        self.check_scene()

    def play_once(self):
        # Step 1: Wrong placement of teanet into shoe_box
        success = self.pick_and_place(self.teanet, self.shoe_box)
        print("Wrong placement of teanet:", success)
        if not success:
            return self.info

        # Step 2: Recovery - move teanet to plate
        success = self.pick_and_place(self.teanet, self.plate)
        print("Recovery of teanet:", success)
        if not success:
            return self.info

        # Step 3: Place bell into shoe_box
        success = self.pick_and_place(self.bell, self.shoe_box)
        print("Placing bell:", success)
        if not success:
            return self.info

        # Step 4: Place microphone into shoe_box
        success = self.pick_and_place(self.microphone, self.shoe_box)
        print("Placing microphone:", success)
        if not success:
            return self.info

        # Step 5: Place cup_with_handle into plate
        success = self.pick_and_place(self.cup_with_handle, self.plate)
        print("Placing cup_with_handle:", success)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        # Check if all objects are in the correct containers
        if (
            self.check_on(self.teanet, self.plate) and
            self.check_on(self.cup_with_handle, self.plate) and
            self.check_on(self.bell, self.shoe_box) and
            self.check_on(self.microphone, self.shoe_box)
        ):
            return True
        return False
