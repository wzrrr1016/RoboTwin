from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 205_noisy_vs_silent_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (containers and objects) into the environment.
        """
        # Create containers
        self.tray = self.add_actor("tray", "tray")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Create target objects
        self.bell = self.add_actor("bell", "bell")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractor objects
        distractor_list = ['screwdriver', 'book', 'shoe', 'stapler', 'markpen']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions to complete the task.
        """
        # 1. Place bell (sound producer) on tray
        success = self.pick_and_place(self.bell, self.tray)
        print("Place bell on tray:", success)
        if not success:
            return self.info

        # 2. Place sand-clock on tray (wrong placement)
        success = self.pick_and_place(self.sand_clock, self.tray)
        print("Place sand-clock on tray (wrong):", success)
        if not success:
            return self.info

        # 3. Correct placement: move sand-clock to fluted_block
        success = self.pick_and_place(self.sand_clock, self.fluted_block)
        print("Move sand-clock to fluted_block:", success)
        if not success:
            return self.info

        # 4. Place alarm-clock (sound producer) on tray
        success = self.pick_and_place(self.alarm_clock, self.tray)
        print("Place alarm-clock on tray:", success)
        if not success:
            return self.info

        # 5. Place bread (perishable) in fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Place bread in fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if all objects are placed in their correct containers.
        """
        # Check if sound-producing items are on the tray
        sound_producers_on_tray = (
            self.check_on(self.bell, self.tray) and
            self.check_on(self.alarm_clock, self.tray)
        )
        
        # Check if silent/perishable items are in fluted_block
        silent_perishable_in_fluted = (
            self.check_on(self.sand_clock, self.fluted_block) and
            self.check_on(self.bread, self.fluted_block)
        )
        
        return sound_producers_on_tray and silent_perishable_in_fluted
