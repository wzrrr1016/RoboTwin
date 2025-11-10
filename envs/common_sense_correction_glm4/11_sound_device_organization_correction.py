from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class sound_device_organization_correction(Imagine_Task):
    def load_actors(self):
        # Load the tray and wooden box as containers
        self.tray = self.env.add_actor("tray", "tray")
        self.wooden_box = self.env.add_actor("wooden_box", "wooden_box")

        # Load the sound-producing devices (alarm-clock, microphone)
        self.alarm_clock = self.env.add_actor("alarm-clock", "alarm_clock")
        self.microphone = self.env.add_actor("microphone", "microphone")

        # Load the non-sound-producing items (fork, knife, mug)
        self.fork = self.env.add_actor("fork", "fork")
        self.knife = self.env.add_actor("knife", "knife")
        self.mug = self.env.add_actor("mug", "mug")

    def play_once(self):
        # Pick up the alarm-clock and place it into the tray
        success = self.env.pick_and_place(self.alarm_clock, self.tray)
        print("Pick and place alarm-clock:", success)

        # Pick up the microphone and place it into the tray (wrong action)
        success = self.env.pick_and_place(self.microphone, self.tray)
        print("Pick and place microphone (wrong):", success)

        # Pick up the microphone from the tray and place it into the wooden box (recovery)
        success = self.env.pick_and_place(self.microphone, self.wooden_box)
        print("Pick and place microphone (recovery):", success)

        # Pick up the fork and place it into the wooden box
        success = self.env.pick_and_place(self.fork, self.wooden_box)
        print("Pick and place fork:", success)

        # Pick up the knife and place it into the wooden box
        success = self.env.pick_and_place(self.knife, self.wooden_box)
        print("Pick and place knife:", success)

        # Pick up the mug and place it into the wooden box
        success = self.env.pick_and_place(self.mug, self.wooden_box)
        print("Pick and place mug:", success)

    def check_success(self):
        # Check if all sound-producing devices are in the tray
        success = self.env.check_on(self.alarm_clock, self.tray) and self.env.check_on(self.microphone, self.tray)
        # Check if all non-sound-producing items are in the wooden box
        success = success and self.env.check_on(self.fork, self.wooden_box) and self.env.check_on(self.knife, self.wooden_box) and self.env.check_on(self.mug, self.wooden_box)
        return success

# Example usage:
# env = YourEnvironmentClass()  # Replace with the actual environment class
# task = OrganizeItemsTask(env)
# task.load_actors()
# task.play_once()
# if task.check_success():
#     print("Task completed successfully!")
# else:
#     print("Task failed.")
