from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 200_office_organizer_with_recovery(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Add the container (fluted_block).
        - Add the objects (cup_with_handle, book, scanner, pot-with-plant, mouse).
        - Add distractors (baguette, shoe, dumbbell, shampoo, toycar).
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.book = self.add_actor("book", "book")
        self.scanner = self.add_actor("scanner", "scanner")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.mouse = self.add_actor("mouse", "mouse")

        # Add distractors
        distractor_list = ["baguette", "shoe", "dumbbell", "shampoo", "toycar"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        - First, perform a wrong action (place pot-with-plant into fluted_block).
        - Then, recover by placing it on top of fluted_block.
        - Place office electronics (scanner, mouse) into the organizer (fluted_block).
        - Place living or paper items (cup_with_handle, book) on top of the organizer.
        """
        # Wrong action: place pot-with-plant into fluted_block
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Wrong place pot-with-plant:", success)
        if not success:
            return self.info

        # Recovery: place pot-with-plant on top of fluted_block
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Recovery place pot-with-plant:", success)
        if not success:
            return self.info

        # Place office electronics into the organizer
        success = self.pick_and_place(self.scanner, self.fluted_block)
        print("Place scanner:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mouse, self.fluted_block)
        print("Place mouse:", success)
        if not success:
            return self.info

        # Place living or paper items on top of the organizer
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Place cup_with_handle:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.book, self.fluted_block)
        print("Place book:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Office electronics (scanner, mouse) should be in the organizer (fluted_block).
        - Living or paper items (cup_with_handle, book, pot_with_plant) should be on top of the organizer.
        """
        if (
            self.check_on(self.scanner, self.fluted_block) and
            self.check_on(self.mouse, self.fluted_block) and
            self.check_on(self.cup_with_handle, self.fluted_block) and
            self.check_on(self.book, self.fluted_block) and
            self.check_on(self.pot_with_plant, self.fluted_block)
        ):
            return True
        return False
