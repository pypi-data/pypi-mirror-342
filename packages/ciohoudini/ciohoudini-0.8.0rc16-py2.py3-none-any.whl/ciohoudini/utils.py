import hou
import os
import ciocore.loggeria

logger = ciocore.loggeria.get_conductor_logger()

def get_parameter_value(node, parm_name, string_value=False):
    """
    Retrieves the value of a parameter on a given Houdini node.

    Args:
        node (hou.Node): The Houdini node containing the parameter.
        parm_name (str): The name of the parameter to retrieve.

    Returns:
        str: The value of the parameter if found, otherwise an empty string.
    """
    try:
        parm = node.parm(parm_name)
        if parm:
            if string_value:
                return parm.evalAsString()
            else:
                return parm.eval()
        #else:
        #   logger.debug(f"Parameter not found: {parm_name}")
    except Exception as e:
        logger.error(f"Error getting parameter value: {e}")

    return None


def set_parameter_value(node, parm_name, value):
    """
    Sets the value of a parameter on a given Houdini node.

    Args:
        node (hou.Node): The Houdini node containing the parameter.
        parm_name (str): The name of the parameter to set.
        value (str): The value to set on the parameter.
    """
    try:
        if node:
            parm = node.parm(parm_name)
            if parm:
                parm.set(value)
        else:
            logger.debug(f"Node not found.")
    except Exception as e:
        logger.error(f"Error setting parameter value: {e}")

def evaluate_houdini_parameter(parm):
    """
    Evaluates a Houdini parameter, resolving any channel references (ch(), chs()),
    Houdini expressions (e.g., $HIP), or direct string values.
    If the parameter is 'output_folder' and the result is a file path, returns the directory of the path.

    Args:
        parm (hou.Parm): The Houdini parameter to evaluate.

    Returns:
        str: The resolved value of the parameter, or the folder if it's an 'output_folder' parameter with a file path.
    """

    try:
        if parm is not None:
            # Get the parameter name
            parm_name = parm.name()

            # Evaluate the parameter to get the resolved value or expression
            parm_value = parm.evalAsString()

            # Check if the value contains a channel reference (ch(), chs())
            if parm_value.startswith(('ch(', 'chs(', 'ch("', 'chs("')):
                # Extract the referenced parameter's path, remove 'ch()', 'chs()', fancy quotes, and spaces
                referenced_parm_path = parm_value[parm_value.index('(') + 1:-1].strip().replace('“', '"').replace('”', '"').strip('\"')

                # Separate the node path and parameter name
                node_path, ref_parm_name = referenced_parm_path.rsplit("/", 1)

                # Get the node that contains the referenced parameter
                referenced_node = hou.node(node_path)

                if referenced_node is not None:
                    # Get the parameter on the referenced node
                    referenced_parm = referenced_node.parm(ref_parm_name)

                    if referenced_parm is not None:
                        # Evaluate the referenced parameter's value
                        resolved_value = referenced_parm.eval()
                    else:
                        logger.debug(f"Could not find parameter: {ref_parm_name} on node {node_path}")
                        return None
                else:
                    logger.debug(f"Could not find node: {node_path}")
                    return None
            else:
                # If it's not a channel reference, evaluate and return the value
                resolved_value = parm.eval()

            # Special handling if the parameter is 'output_folder'
            if parm_name == "output_folder":
                # Check if the resolved value is a file path (i.e., contains a file extension)
                if os.path.isfile(resolved_value) or os.path.splitext(resolved_value)[1]:
                    # Return the folder of the file path
                    return os.path.dirname(resolved_value)

            # Return the evaluated value (or folder if applicable)
            return resolved_value
    except Exception as e:
        logger.error(f"Error evaluating Houdini parameter: {e}")

    return None



def evaluate_houdini_path(path_value):
    """
    Evaluates a Houdini path value, resolving any channel references (ch(), chs()),
    Houdini expressions (e.g., $HIP), or direct string values.
    If the result is a file path, returns the directory of the path.

    Args:
        path_value (str): The value of the path, which may be a channel reference, file path, folder path, or expression.

    Returns:
        str: The resolved path, or the folder if it's a file path.
    """
    if path_value is None:
        return None
    try:

        # Check if the value contains a channel reference (ch(), chs())
        if path_value.startswith(('ch(', 'chs(', 'ch("', 'chs("')):
            # Extract the referenced parameter's path, remove 'ch()', 'chs()', fancy quotes, and spaces
            referenced_parm_path = path_value[path_value.index('(') + 1:-1].strip().replace('“', '"').replace('”', '"').strip('\"')

            # Separate the node path and parameter name
            node_path, ref_parm_name = referenced_parm_path.rsplit("/", 1)

            # Get the node that contains the referenced parameter
            referenced_node = hou.node(node_path)

            if referenced_node is not None:
                # Get the parameter on the referenced node
                referenced_parm = referenced_node.parm(ref_parm_name)

                if referenced_parm is not None:
                    # Evaluate the referenced parameter's value
                    resolved_value = referenced_parm.eval()
                else:
                    logger.debug(f"Could not find parameter: {ref_parm_name} on node {node_path}")
                    return None
            else:
                logger.debug(f"Could not find node: {node_path}")
                return None
        else:
            # If it's not a channel reference, evaluate and return the value directly (handles $HIP, etc.)
            resolved_value = hou.expandString(path_value)

        # Special handling if the resolved value is a file path
        if os.path.isfile(resolved_value) or os.path.splitext(resolved_value)[1]:
            # Return the folder of the file path
            return os.path.dirname(resolved_value)

        # Return the evaluated value (which might already be a folder)
        return resolved_value

    except Exception as e:
        logger.error(f"Error evaluating Houdini path: {e}")
        return None
