import knime_extension as knext


# This defines the root CV Post Processing KNIME category that is displayed in the node repository
category = knext.category(
    path="/community",
    level_id="cv_postprocessing",
    name="Computer Vision Postprocessing Extension",
    description="Python Nodes for Computer Vision Postprocessing",
    icon="icons/icon.png",
)

import nodes.cat1
# import nodes.cat2