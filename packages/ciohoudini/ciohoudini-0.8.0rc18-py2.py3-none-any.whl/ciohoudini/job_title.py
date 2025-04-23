"""frame range section in the UI."""

import hou
from ciohoudini import utils

def resolve_payload(node, **kwargs):
    rop_path = kwargs.get("rop_path", None)
    title = node.parm("title").eval().strip()
    title = "{}  {}".format(title, rop_path)
    use_stage_cameras = utils.get_parameter_value(node, "use_multiple_cameras")
    if use_stage_cameras:
        override_camera = kwargs.get("override_camera", None)
        if override_camera:
            title = "{}  {}".format(title, override_camera)
    return {"job_title": title}

