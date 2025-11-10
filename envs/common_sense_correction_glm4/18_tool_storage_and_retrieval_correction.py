from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class tool_storage_and_retrieval_correction(Imagine_Task):
    def load_actors(self):
        # Load the shoe_box and wooden_box
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Load all objects
        for tool in self.tools:
            self.add_actor("object", tool)
        for non_tool in self.non_tools:
            self.add_actor("object", non_tool)

    def play_once(self):
        # Pick and place tools into the shoe_box
        for tool in self.tools:
            object_actor = self.get_actor(tool)
            if object_actor:
                success = self.pick_and_place(object_actor, self.shoe_box)
                print(f"Placing {tool} into shoe_box: {success}")
                if not success:
                    return self.info

        # Pick and place non-tools into the wooden_box
        for non_tool in self.non_tools:
            object_actor = self.get_actor(non_tool)
            if object_actor:
                success = self.pick_and_place(object_actor, self.wooden_box)
                print(f"Placing {non_tool} into wooden_box: {success}")
                if not success:
                    return self.info

    def check_success(self):
        # Check if all tools are in the shoe_box and all non-tools are in the wooden_box
        for tool in self.tools:
            object_actor = self.get_actor(tool)
            if object_actor and not self.check_on(object_actor, self.shoe_box):
                return False

        for non_tool in self.non_tools:
            object_actor = self.get_actor(non_tool)
            if object_actor and not self.check_on(object_actor, self.wooden_box):
                return False

        return True

    def get_actor(self, object_name):
        # Helper function to get an actor by name
        for actor in self.actors:
            if actor.object_name == object_name:
                return actor
        return None

    def pick_and_place(self, object, container):
        # Use the provided pick_and_place function
        return self.pick_and_place(object, container)

    def check_on(self, object, container):
        # Use the provided check_on function
        return self.check_on(object, container)

    def check_grasp(self, object):
        # Use the provided check_grasp function
        return self.check_grasp(object)
