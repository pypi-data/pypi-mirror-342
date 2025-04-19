import hou
from pxr import Usd
import collections # Import collections for deque

def find_stage_cameras(rop_path):
    """
    Finds all prims of type 'Camera' on the USD stage connected upstream
    of the specified ROP node.
    """
    camera_list = []
    rop_node = hou.node(rop_path)
    if not rop_node:
        print(f"Error: Could not find ROP node at path: {rop_path}")
        return camera_list

    # print(f"Starting search for USD stage upstream from: {rop_node.path()}")
    stage_node = find_usd_stage_node(rop_node)

    if not stage_node:
        print(f"Error: Could not find an upstream node with a USD stage for {rop_node.path()}")
        return camera_list

    # print(f"Found USD stage provided by node: {stage_node.path()}")

    try:
        stage = stage_node.stage()
        if not stage:
             print(f"Error: Node {stage_node.path()} has a 'stage' attribute, but it returned None.")
             return camera_list

        print(f"Traversing stage from {stage_node.path()}...")
        for prim in stage.Traverse():
            # Check if the prim is defined and is of type Camera
            if prim.IsValid() and prim.GetTypeName() == "Camera":
                prim_path = str(prim.GetPath())
                # print(f"  Found camera: {prim_path}")
                camera_list.append(prim_path)

        if not camera_list:
            print("  No prims of type 'Camera' found on the stage.")

    except Exception as e:
        print(f"Error accessing stage or traversing prims for node {stage_node.path()}: {e}")

    return camera_list


def find_usd_stage_node(start_node):
    """
    Traverses upstream from the start_node to find the first node
    that has a valid USD stage attribute. Uses breadth-first search.

    Args:
        start_node (hou.Node): The node to start the upstream search from.

    Returns:
        hou.Node or None: The first upstream node with a valid stage, or None if not found.
    """
    if not start_node:
        return None

    # Use a deque for efficient queue operations (breadth-first search)
    queue = collections.deque(start_node.inputs())
    visited = set(start_node.inputs()) # Keep track of visited nodes to prevent cycles

    while queue:
        current_node = queue.popleft() # Get the next node from the front of the queue

        if not current_node: # Skip if the input connection is broken
            continue

        # Check if the current node has a 'stage' attribute and it's not None
        if hasattr(current_node, "stage"):
            try:
                # Accessing .stage() might throw an error in some cases
                stage_obj = current_node.stage()
                if stage_obj is not None:
                    print(f"  -> Found node with stage: {current_node.path()}")
                    return current_node # Found the first node with a valid stage
                else:
                    print(f"  -> Node {current_node.path()} has .stage but it's None. Continuing search...")
            except Exception as e:
                 print(f"  -> Error accessing .stage() on {current_node.path()}: {e}. Continuing search...")


        # Add the inputs of the current node to the queue if they haven't been visited
        for input_node in current_node.inputs():
            if input_node and input_node not in visited:
                visited.add(input_node)
                queue.append(input_node)

    print("  -> Reached top of hierarchy without finding a node with a stage.")
    return None # No node with a stage found in the upstream hierarchy

# --- Example Usage ---
def main():
    # Example usage of the find_stage_cameras function
    rop_path = "/stage/usdrender_rop1" # Make sure this path is correct in your scene
    cameras = find_stage_cameras(rop_path)

    print("\n--- Summary ---")
    if cameras:
        print("Cameras found on stage:")
        for cam in cameras:
            print(f"- {cam}")
    else:
        print("No cameras were found on the identified stage (or no stage was found).")

if __name__ == "__main__":
    main()