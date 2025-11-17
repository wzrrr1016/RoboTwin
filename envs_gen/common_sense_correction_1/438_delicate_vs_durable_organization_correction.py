from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 438_delicate_vs_durable_organization_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        - Containers: fluted_block, shoe_box
        - Objects: book, sand-clock, toycar, yellow_block, can
        - Distractors: apple, baguette, bread, hamburg
        """
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.book = self.add_actor("book", "book")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.toycar = self.add_actor("toycar", "toycar")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.can = self.add_actor("can", "can")

        # Add distractors
        distractor_list = ["apple", "baguette", "bread", "hamburg"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions as defined in the task.
        The sequence includes:
        1. Place toycar in fluted_block
        2. Place book in shoe_box
        3. Place can in shoe_box (wrong action)
        4. Recover can by placing it in fluted_block
        5. Place yellow_block in fluted_block
        """
        # 1. Place toycar in fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Pick toycar:", success)
        if not success:
            return self.info

        # 2. Place book in shoe_box
        success = self.pick_and_place(self.book, self.shoe_box)
        print("Pick book:", success)
        if not success:
            return self.info

        # 3. Place can in shoe_box (wrong action)
        success = self.pick_and_place(self.can, self.shoe_box)
        print("Pick can (wrong):", success)
        if not success:
            return self.info

        # 4. Recover can by placing it in fluted_block
        success = self.pick_and_place(self.can, self.fluted_block)
        print("Recover can:", success)
        if not success:
            return self.info

        # 5. Place yellow_block in fluted_block
        success = self.pick_and_place(self.yellow_block, self.fluted_block)
        print("Pick yellow_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if all objects are placed in the correct containers.
        - toycar and yellow_block in fluted_block
        - book and can in shoe_box (after recovery)
        """
        if (self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.book, self.shoe_box) and
            self.check_on(self.can, self.fluted_block) and
            self.check_on(self.yellow_block, self.fluted_block)):
            return True
        return False
