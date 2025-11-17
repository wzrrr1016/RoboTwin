from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 378_store_light_toys_and_sound_items_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Create the shoe_box container.
        - Add the relevant objects: toycar, small-speaker, bell, and hammer.
        - Add distractor objects to the environment.
        """
        # Create the shoe box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add the relevant objects
        self.toycar = self.add_actor("toycar", "toycar_0")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker_0")
        self.bell = self.add_actor("bell", "bell_0")
        self.hammer = self.add_actor("hammer", "hammer_0")

        # Add distractor objects
        self.add_distractors(["calculator", "baguette", "olive-oil", "milk-box", "tissue-box"])

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        - Place the toycar, small-speaker, and bell into the shoe_box.
        - Place the hammer into the shoe_box (wrong action).
        - Correct the wrong action by placing the hammer on the table.
        """
        # Place correct items into the shoe_box
        success = self.pick_and_place(self.toycar, self.shoe_box)
        if not success:
            return self.info

        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        if not success:
            return self.info

        success = self.pick_and_place(self.bell, self.shoe_box)
        if not success:
            return self.info

        # Wrong action: place hammer into the shoe_box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        if not success:
            return self.info

        # Recovery: place hammer on the table (not in the shoe_box)
        success = self.pick_and_place(self.hammer, self.table)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All correct items (toycar, small-speaker, bell) are in the shoe_box.
        - The hammer is not in the shoe_box (i.e., it was corrected).
        """
        correct_items_in_shoe_box = (
            self.check_on(self.toycar, self.shoe_box) and
            self.check_on(self.small_speaker, self.shoe_box) and
            self.check_on(self.bell, self.shoe_box)
        )

        hammer_not_in_shoe_box = not self.check_on(self.hammer, self.shoe_box)

        return correct_items_in_shoe_box and hammer_not_in_shoe_box
