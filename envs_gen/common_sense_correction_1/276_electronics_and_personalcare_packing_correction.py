from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 276_electronics_and_personalcare_packing_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Add the wooden_box as the container.
        - Add the required objects: shampoo, microphone, mouse, hammer.
        - Add distractors as specified in the task description.
        """
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.microphone = self.add_actor("microphone", "microphone")
        self.mouse = self.add_actor("mouse", "mouse")
        self.hammer = self.add_actor("hammer", "hammer")
        distractor_list = ['baguette', 'apple', 'book', 'shoe', 'red_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - Pick and place the microphone into the wooden_box.
        - Pick and place the hammer into the wooden_box (this is a wrong action).
        - Recover by picking the hammer from the wooden_box and placing it on the table.
        - Pick and place the mouse into the wooden_box.
        - Pick and place the shampoo into the wooden_box.
        - Return early if any step fails.
        """
        success = self.pick_and_place(self.microphone, self.wooden_box)
        print("Pick microphone:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Pick hammer (wrong):", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.hammer, self.table)
        print("Recover hammer:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mouse, self.wooden_box)
        print("Pick mouse:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.shampoo, self.wooden_box)
        print("Pick shampoo:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All small electronic gadgets (microphone, mouse) and personal-care bottles (shampoo) must be in the wooden_box.
        - The hammer must be on the table (not in the wooden_box).
        """
        if (
            self.check_on(self.shampoo, self.wooden_box) and
            self.check_on(self.microphone, self.wooden_box) and
            self.check_on(self.mouse, self.wooden_box) and
            self.check_on(self.hammer, self.table)
        ):
            return True
        return False
