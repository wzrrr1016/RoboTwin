
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien


class mixed_container_logic_recover(Imagine_Task):
    def load_actors(self):
        # Containers
        self.bowl = self.add_actor("bowl", "bowl")
        self.plate = self.add_actor("plate", "plate")
        self.tray = self.add_actor("tray", "tray")

        # Objects
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.hammer = self.add_actor("hammer", "hammer")

    def play_once(self):
        # Mistake: place hammer on tray first, then recover to plate
        success = self.pick_and_place(self.hammer, self.tray)
        print("mistake hammer->tray:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.hammer, self.plate)
        print("recover hammer->plate:", success)
        if not success:
            return self.info

        # Reasoning: place apple into bowl (food), hamburg onto tray (main), hammer on plate (tool)
        success = self.pick_and_place(self.apple, self.bowl)
        print("place apple->bowl:", success)
        if not success:
            return self.info
        success = self.pick_and_place(self.hamburg, self.tray)
        print("place hamburg->tray:", success)
        if not success:
            return self.info

    def check_success(self):
        return (
            self.check_on(self.hammer, self.plate)
            and self.check_on(self.apple, self.bowl)
            and self.check_on(self.hamburg, self.tray)
        )

