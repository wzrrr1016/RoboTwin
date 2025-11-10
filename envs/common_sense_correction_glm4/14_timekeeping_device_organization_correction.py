from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class timekeeping_device_organization_correction(Imagine_Task):
    def load_actors(self):
        # Load the actors into the environment
        self.coaster = self.add_actor("coaster", "coaster")
        self.tray = self.add_actor("tray", "tray")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.bell = self.add_actor("bell", "bell")
        self.microphone = self.add_actor("microphone", "microphone")

    def play_once(self):
        # Pick up the sand-clock and place it into the coaster
        success = self.pick_and_place(self.sand_clock, self.coaster)
        print("Pick and place sand-clock:", success)
        if not success:
            return self.info

        # Attempt to pick up the bell and place it into the tray (this should fail)
        success = self.pick_and_place(self.bell, self.tray)
        print("Pick and place bell (should fail):", success)
        if not success:
            # Pick up the bell from the tray and place it into the coaster (recovery)
            success = self.pick_and_place(self.bell, self.coaster)
            print("Pick and place bell (recovery):", success)
            if not success:
                return self.info

        # Pick up the microphone and place it into the tray
        success = self.pick_and_place(self.microphone, self.tray)
        print("Pick and place microphone:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if the sand-clock is on the coaster
        if self.check_on(self.sand_clock, self.coaster):
            # Check if the bell is on the coaster
            if self.check_on(self.bell, self.coaster):
                # Check if the microphone is on the tray
                if self.check_on(self.microphone, self.tray):
                    return True
        return False

# Example usage:
# task = OrganizeTask()
# task.load_actors()
# task.play_once()
# if task.check_success():
#     print("Task completed successfully.")
# else:
#     print("Task failed.")
