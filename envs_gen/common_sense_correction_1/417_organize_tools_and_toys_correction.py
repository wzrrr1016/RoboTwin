from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 417_organize_tools_and_toys_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        This includes the organizer (fluted_block), the heavy repair tools,
        the small toy (toycar), and the distractor objects.
        """
        # Add the organizer container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the heavy repair tools
        self.drill = self.add_actor("drill", "drill")
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

        # Add the small toy
        self.toycar = self.add_actor("toycar", "toycar")

        # Add distractor objects to the environment
        distractor_list = ['book', 'apple', 'pot-with-plant', 'alarm-clock', 'tissue-box']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        The robot first makes a wrong action (placing the toy in the organizer),
        then recovers by placing it on the table, and finally places the heavy tools
        into the organizer.
        """
        # Wrong action: Place toycar into fluted_block (incorrect)
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar into fluted_block (wrong):", success)
        if not success:
            return self.info

        # Recovery: Place toycar on the table (correct)
        success = self.pick_and_place(self.toycar, self.table)
        print("Place toycar on table (recovery):", success)
        if not success:
            return self.info

        # Place heavy tools into the organizer
        success = self.pick_and_place(self.drill, self.fluted_block)
        print("Place drill into fluted_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Place hammer into fluted_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Place screwdriver into fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        The task is considered successful if:
        - All heavy tools are in the organizer (fluted_block)
        - The small toy (toycar) is on the table
        """
        if (
            self.check_on(self.drill, self.fluted_block) and
            self.check_on(self.hammer, self.fluted_block) and
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.toycar, self.table)
        ):
            return True
        return False
