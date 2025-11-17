from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 289_utensils_and_heavy_tools_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add objects
        self.knife = self.add_actor("knife", "knife")
        self.fork = self.add_actor("fork", "fork")
        self.drill = self.add_actor("drill", "drill")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        
        # Add distractors
        distractor_list = ['pet-collar', 'alarm-clock', 'small-speaker', 'microphone', 'markpen']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place fork on coaster
        success = self.pick_and_place(self.fork, self.coaster)
        print("Place fork on coaster:", success)
        if not success:
            return self.info

        # Step 2: Wrong placement of knife into wooden_box
        success = self.pick_and_place(self.knife, self.wooden_box)
        print("Place knife into wooden_box (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover knife to coaster
        success = self.pick_and_place(self.knife, self.coaster)
        print("Recover knife to coaster:", success)
        if not success:
            return self.info

        # Step 4: Place drill into wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Place drill into wooden_box:", success)
        if not success:
            return self.info

        # Step 5: Place dumbbell into wooden_box
        success = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("Place dumbbell into wooden_box:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify final positions
        if (self.check_on(self.fork, self.coaster) and
            self.check_on(self.knife, self.coaster) and
            self.check_on(self.drill, self.wooden_box) and
            self.check_on(self.dumbbell, self.wooden_box)):
            return True
        return False
