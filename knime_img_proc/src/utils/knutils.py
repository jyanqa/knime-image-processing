############################################
# General Helper Class
############################################
import knime_extension as knext
from typing import Callable

# main_category = knext.category(
#     path="/community/cv_postprocessing",
#     level_id="cv_postprocessing",
#     name="Computer Vision Postprocessing",
#     description="Nodes that preprocess the output of Computer Vision tasks.",
#     icon="icons/icon.png", #todo: to change the icon
# )

# object_dectection_category = knext.category(
#     path=main_category,
#     level_id="object_dectection",
#     name="Object Detection",
#     description="Nodes for Object Detection Tasks.",
#     icon="icons/icon.png",
# )
# object_segmentation_category = knext.category(
#     path=main_category,
#     level_id="object_segmentation",
#     name="Object Segmentation",
#     description="Nodes for Object Segmentation Tasks.",
#     icon="icons/icon.png",
# )

def is_type_timestamp(column: knext.Column):
    """
    This function checks on all the supported timestamp columns supported in KNIME.
    Note that legacy date&time types are not supported.
    @return: True if date&time column is compatible with the respective logical types supported in KNIME.
    """

    return True #boolean_or(is_time, is_date, is_datetime, is_zoned_datetime)(column)
def column_exists_or_preset(
    context: knext.ConfigurationContext,
    column: str,
    schema: knext.Schema,
    func: Callable[[knext.Column], bool] = None,
    none_msg: str = "No compatible column found in input table",
) -> str:
    """
    Checks that the given column is not None and exists in the given schema. If none is selected it returns the
    first column that is compatible with the provided function. If none is compatible it throws an exception.
    """
    if column is None:
        for c in schema:
            if func(c):
                context.set_warning(f"Preset column to: {c.name}")
                return c.name
        raise knext.InvalidParametersError(none_msg)
    __check_col_and_type(column, schema, func)
    return column


def __check_col_and_type(
    column: str,
    schema: knext.Schema,
    check_type: Callable[[knext.Column], bool] = None,
) -> None:
    """
    Checks that the given column exists in the given schema and that it matches the given type_check function.
    """
    # Check that the column exists in the schema and that it has a compatible type
    try:
        existing_column = schema[column]
        if check_type is not None and not check_type(existing_column):
            raise knext.InvalidParametersError(
                f"Column '{str(column)}' has incompatible data type"
            )
    except IndexError:
        raise knext.InvalidParametersError(
            f"Column '{str(column)}' not available in input table"
        )