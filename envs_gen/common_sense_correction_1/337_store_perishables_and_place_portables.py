from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 337_store_perishables_and_place_portables(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        - Containers: wooden_box, coaster
        - Objects: apple, bread, small-speaker, toycar
        - Distractors: pot-with-plant, shoe, book, tissue-box, dumbbell
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.coaster = self.add_actor("coaster", "coaster")

        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.toycar = self.add_actor("toycar", "toycar")

        # Add distractors
        distractor_list = ["pot-with-plant", "shoe", "book", "tissue-box", "dumbbell"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - Place apple and bread into wooden_box
        - Place small-speaker and toycar onto coaster
        - Include a recovery step for the small-speaker
        """
        # Place apple into wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Place apple into wooden_box:", success)
        if not success:
            return self.info

        # Place small-speaker into wooden_box (wrong action)
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("Place small-speaker into wooden_box (wrong):", success)
        if not success:
            return self.info

        # Recover: Place small-speaker onto coaster
        success = self.pick_and_place(self.small_speaker, self.coaster)
        print("Recover: Place small-speaker onto coaster:", success)
        if not success:
            return self.info

        # Place toycar onto coaster
        success = self.pick_and_place(self.toycar, self.coaster)
        print("Place toycar onto coaster:", success)
        if not success:
            return self.info

        # Place bread into wooden_box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Place bread into wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed.
        - Perishable edible items (apple, bread) are in wooden_box
        - Small portable electronics (small-speaker) and toys (toycar) are on coaster
        """
        if (self.check_on(self.apple, self.wooden_box) and
            self.check_on(self.bread, self.wooden_box) and
            self.check_on(self.small_speaker, self.coaster) and
            self.check_on(self.toycar, self.coaster)):
            return True
        return False
