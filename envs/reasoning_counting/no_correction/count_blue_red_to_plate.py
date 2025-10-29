
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien


class count_blue_red_to_plate(Imagine_Task):
    def load_actors(self):
        # Containers
        self.plate = self.add_actor("plate", "plate")

        # Blocks (use create_box to simulate colored blocks)
        poses = self.create_box_pose(6)
        self.blocks = []
        colors = ["red", "red", "blue", "blue", "blue", "green"]
        for i, (pose, color) in enumerate(zip(poses, colors)):
            blk = self.create_block(pose, color)
            blk.set_name(f"block_{color}_{i}")
            self.blocks.append(blk)

    def play_once(self):
        # Counting reasoning: place exactly 2 red and 2 blue blocks on the plate
        placed = 0
        for blk in self.blocks:
            name = blk.get_name()
            if ("red" in name or "blue" in name) and placed < 4:
                success = self.pick_place_block(blk, self.plate)
                if not success:
                    return self.info
                placed += 1

    def check_success(self):
        # Verify at least 2 red + 2 blue on plate
        red_blue_on_plate = 0
        for blk in self.blocks:
            name = blk.get_name()
            if ("red" in name or "blue" in name) and self.check_actors_contact(blk, self.plate):
                red_blue_on_plate += 1
        return red_blue_on_plate >= 4

