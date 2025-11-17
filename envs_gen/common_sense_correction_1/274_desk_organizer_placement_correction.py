from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 274_desk_organizer_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Distractors are added separately using the add_distractors method.
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add the main objects
        self.markpen = self.add_actor("markpen", "markpen")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.bottle = self.add_actor("bottle", "bottle")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")

        # Add distractors to the environment
        distractor_list = ['shoe', 'toycar', 'microphone', 'battery', 'french_fries']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot arm should perform.
        This includes placing objects into the organizer and correcting any misplaced items.
        """
        # Step 1: Place markpen into the organizer
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Pick place markpen:", success)
        if not success:
            return self.info

        # Step 2: Place sand-clock into the organizer
        success = self.pick_and_place(self.sand_clock, self.fluted_block)
        print("Pick place sand-clock:", success)
        if not success:
            return self.info

        # Step 3: Place bottle into the organizer (wrong action)
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Pick place bottle (wrong):", success)
        if not success:
            return self.info

        # Step 4: Correct the wrong action by placing the bottle on the table
        success = self.pick_and_place(self.bottle, self.table)
        print("Pick place bottle (recovery):", success)
        if not success:
            return self.info

        # Step 5: Place dumbbell on the table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Pick place dumbbell:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully by verifying the final positions of all relevant objects.
        """
        # Check if markpen and sand-clock are in the organizer
        markpen_in = self.check_on(self.markpen, self.fluted_block)
        sand_clock_in = self.check_on(self.sand_clock, self.fluted_block)

        # Check if bottle and dumbbell are on the table
        bottle_on_table = self.check_on(self.bottle, self.table)
        dumbbell_on_table = self.check_on(self.dumbbell, self.table)

        # Return True only if all conditions are met
        return markpen_in and sand_clock_in and bottle_on_table and dumbbell_on_table
