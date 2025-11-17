from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 492_kitchen_utensils_and_tools_storage_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        - Containers: coaster, shoe_box
        - Objects: teanet, fork, drill, apple
        - Distractors: calculator, pet-collar, toycar, book, alarm-clock
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add required objects
        self.teanet = self.add_actor("teanet", "teanet")
        self.fork = self.add_actor("fork", "fork")
        self.drill = self.add_actor("drill", "drill")
        self.apple = self.add_actor("apple", "apple")

        # Add distractors
        distractor_list = ["calculator", "pet-collar", "toycar", "book", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Pick apple and place it on the coaster
        2. Pick teanet and place it on the coaster
        3. Pick drill and place it on the coaster (wrong action)
        4. Pick drill from the coaster and place it into the shoe_box (recovery)
        5. Pick fork and place it on the coaster
        """
        # Step 1: Place apple on coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple on coaster:", success)
        if not success:
            return self.info

        # Step 2: Place teanet on coaster
        success = self.pick_and_place(self.teanet, self.coaster)
        print("Place teanet on coaster:", success)
        if not success:
            return self.info

        # Step 3: Place drill on coaster (wrong action)
        success = self.pick_and_place(self.drill, self.coaster)
        print("Place drill on coaster (wrong):", success)
        if not success:
            return self.info

        # Step 4: Move drill to shoe_box (recovery)
        success = self.pick_and_place(self.drill, self.shoe_box)
        print("Move drill to shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place fork on coaster
        success = self.pick_and_place(self.fork, self.coaster)
        print("Place fork on coaster:", success)
        if not success:
            return self.info

        return self.info  # All steps completed successfully

    def check_success(self):
        """
        Check if the task was completed successfully:
        - Small kitchen utensils (fork) and tea accessories (teanet)
        - Perishable edible items (apple) are on the coaster
        - Heavy tools (drill) are in the shoe_box
        """
        if (
            self.check_on(self.apple, self.coaster) and
            self.check_on(self.teanet, self.coaster) and
            self.check_on(self.fork, self.coaster) and
            self.check_on(self.drill, self.shoe_box)
        ):
            return True
        return False
