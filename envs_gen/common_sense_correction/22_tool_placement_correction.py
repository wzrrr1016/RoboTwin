from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 22_tool_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the environment.
        - Containers: plate and wooden_box
        - Objects: scanner, hammer, dumbbell, sand-clock, bell
        - Distractors: cup_with_handle, battery, cup-with-liquid, blue_block, toycar, book
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add main objects
        self.scanner = self.add_actor("scanner", "scanner")
        self.hammer = self.add_actor("hammer", "hammer")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.bell = self.add_actor("bell", "bell")

        # Add distractors
        distractor_list = [
            "cup_with_handle", "battery", "cup-with-liquid", "blue_block", "toycar", "book"
        ]
        self.add_distractors(distractor_list)

        # Final check to ensure all actors are placed correctly
        self.check_scene()

    def play_once(self):
        """
        Define the sequence of robot arm actions to complete the task.
        - First, place scanner into wooden_box (wrong action)
        - Then, recover by placing scanner into plate
        - Place hammer and dumbbell into wooden_box
        - Place sand-clock and bell into plate
        """
        # Step 1: Wrong placement of scanner into wooden_box
        success = self.pick_and_place(self.scanner, self.wooden_box)
        print("Pick scanner to wooden_box (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - move scanner to plate
        success = self.pick_and_place(self.scanner, self.plate)
        print("Pick scanner to plate (recovery):", success)
        if not success:
            return self.info

        # Step 3: Place hammer into wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Pick hammer to wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Place dumbbell into wooden_box
        success = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("Pick dumbbell to wooden_box:", success)
        if not success:
            return self.info

        # Step 5: Place sand-clock into plate
        success = self.pick_and_place(self.sand_clock, self.plate)
        print("Pick sand-clock to plate:", success)
        if not success:
            return self.info

        # Step 6: Place bell into plate
        success = self.pick_and_place(self.bell, self.plate)
        print("Pick bell to plate:", success)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Tools (hammer, dumbbell) must be in wooden_box
        - Non-tools (scanner, sand-clock, bell) must be in plate
        """
        # Check if tools are in the correct container
        tools_in_wooden_box = (
            self.check_on(self.hammer, self.wooden_box) and
            self.check_on(self.dumbbell, self.wooden_box)
        )

        # Check if non-tools are in the correct container
        non_tools_in_plate = (
            self.check_on(self.scanner, self.plate) and
            self.check_on(self.sand_clock, self.plate) and
            self.check_on(self.bell, self.plate)
        )

        # Return True only if all conditions are met
        return tools_in_wooden_box and non_tools_in_plate
