from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class office_and_fragile_storage_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the environment.
        - Add the shoe_box as the container.
        - Add the relevant objects: stapler, mouse, red_block, sand-clock, and bottle.
        - Add distractors as specified in the task description.
        """
        # Add the container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add the relevant objects
        self.stapler = self.add_actor("stapler", "stapler")
        self.mouse = self.add_actor("mouse", "mouse")
        self.red_block = self.add_actor("red_block", "red_block")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.bottle = self.add_actor("bottle", "bottle")

        # Add distractors
        distractor_list = ["dumbbell", "baguette", "pet-collar", "chips-tub"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        - Pick and place stapler, mouse, sand-clock, and bottle into the shoe_box.
        - Pick and place red_block into the shoe_box (wrong action).
        - Recover by picking red_block from the shoe_box and placing it back on the table.
        """
        # Step 1: Pick and place stapler into shoe_box
        success = self.pick_and_place(self.stapler, self.shoe_box)
        print("Pick place stapler:", success)
        if not success:
            return self.info

        # Step 2: Pick and place mouse into shoe_box
        success = self.pick_and_place(self.mouse, self.shoe_box)
        print("Pick place mouse:", success)
        if not success:
            return self.info

        # Step 3: Pick and place red_block into shoe_box (wrong action)
        success = self.pick_and_place(self.red_block, self.shoe_box)
        print("Pick place red_block (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover red_block by placing it back on the table
        success = self.pick_and_place(self.red_block, self.table)
        print("Recover red_block:", success)
        if not success:
            return self.info

        # Step 5: Pick and place sand-clock into shoe_box
        success = self.pick_and_place(self.sand_clock, self.shoe_box)
        print("Pick place sand-clock:", success)
        if not success:
            return self.info

        # Step 6: Pick and place bottle into shoe_box
        success = self.pick_and_place(self.bottle, self.shoe_box)
        print("Pick place bottle:", success)
        if not success:
            return self.info

        return self.info  # All actions completed successfully

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All small office accessories and fragile items are in the shoe_box.
        - The red_block is not in the shoe_box (it was removed in the recovery step).
        """
        # Check if all correct items are in the shoe_box
        stapler_on = self.check_on(self.stapler, self.shoe_box)
        mouse_on = self.check_on(self.mouse, self.shoe_box)
        sand_clock_on = self.check_on(self.sand_clock, self.shoe_box)
        bottle_on = self.check_on(self.bottle, self.shoe_box)

        # Check if red_block is not in the shoe_box
        red_block_not_on = not self.check_on(self.red_block, self.shoe_box)

        # Return True only if all conditions are met
        return stapler_on and mouse_on and sand_clock_on and bottle_on and red_block_not_on
