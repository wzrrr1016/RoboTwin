from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 480_store_reusables_dispose_consumables_correction(Imagine_Task):
    def load_actors(self):
        """
        Load the required objects and distractors into the environment.
        - Required objects: alarm-clock, drill, shampoo, toycar
        - Distractors: shoe, book, apple, dumbbell, baguette
        Containers (wooden_box and dustbin) are assumed to be preloaded in the environment.
        """
        # Add required objects as actors
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock_0")
        self.drill = self.add_actor("drill", "drill_0")
        self.shampoo = self.add_actor("shampoo", "shampoo_0")
        self.toycar = self.add_actor("toycar", "toycar_0")

        # Add distractors to the environment
        distractor_list = ["shoe", "book", "apple", "dumbbell", "baguette"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm:
        1. Pick shampoo and place it into wooden_box (wrong action)
        2. Pick shampoo from wooden_box and place it into dustbin (recovery)
        3. Pick alarm-clock and place it into wooden_box
        4. Pick drill and place it into wooden_box
        5. Pick toycar and place it into wooden_box
        """
        # Step 1: Wrong action - Place shampoo into wooden_box
        success = self.pick_and_place(self.shampoo, self.wooden_box)
        print("Wrong: Shampoo to wooden_box:", success)
        if not success:
            return self.info

        # Step 2: Recovery - Place shampoo into dustbin
        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Recovery: Shampoo to dustbin:", success)
        if not success:
            return self.info

        # Step 3: Place alarm-clock into wooden_box
        success = self.pick_and_place(self.alarm_clock, self.wooden_box)
        print("Alarm-clock to wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Place drill into wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Drill to wooden_box:", success)
        if not success:
            return self.info

        # Step 5: Place toycar into wooden_box
        success = self.pick_and_place(self.toycar, self.wooden_box)
        print("Toycar to wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed:
        - alarm-clock, drill, and toycar are in wooden_box
        - shampoo is in dustbin
        """
        if (
            self.check_on(self.alarm_clock, self.wooden_box) and
            self.check_on(self.drill, self.wooden_box) and
            self.check_on(self.toycar, self.wooden_box) and
            self.check_on(self.shampoo, self.dustbin)
        ):
            return True
        return False
