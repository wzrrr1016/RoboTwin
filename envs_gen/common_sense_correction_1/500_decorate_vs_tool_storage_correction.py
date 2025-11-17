from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 500_decorate_vs_tool_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add required objects
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.drill = self.add_actor("drill", "drill")
        self.teanet = self.add_actor("teanet", "teanet")
        
        # Add distractors
        distractor_list = ["toycar", "shoe", "book", "markpen", "calculator"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place decorative/delicate items on tray
        success = self.pick_and_place(self.pot_with_plant, self.tray)
        print("Place pot-with-plant on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.sand_clock, self.tray)
        print("Place sand-clock on tray:", success)
        if not success:
            return self.info

        # Wrong placement of heavy tool (drill) on tray
        success = self.pick_and_place(self.drill, self.tray)
        print("Wrongly place drill on tray:", success)
        if not success:
            return self.info

        # Recovery: Move drill to wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Move drill to wooden_box:", success)
        if not success:
            return self.info

        # Place remaining delicate item on tray
        success = self.pick_and_place(self.teanet, self.tray)
        print("Place teanet on tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all decorative items are on tray and heavy tool is in wooden_box
        if (self.check_on(self.pot_with_plant, self.tray) and
            self.check_on(self.sand_clock, self.tray) and
            self.check_on(self.teanet, self.tray) and
            self.check_on(self.drill, self.wooden_box)):
            return True
        return False
```
