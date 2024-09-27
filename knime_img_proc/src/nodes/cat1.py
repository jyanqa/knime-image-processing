import logging
import knime.extension as knext
from utils import knutils as kutil
from PIL import Image, ImageDraw
# TODO: Change the folder name, and subfolder name to be: computer vision postprocessing

LOGGER = logging.getLogger(__name__)

# Step 1: DEFINE THE CATEGORY AND ITS SUBCATEGORIES.
main_category = knext.category(
    path="/community/cv_postprocessing",
    level_id="cv_postprocessing",
    name="Computer Vision Postprocessing",
    description="Nodes that preprocess the output of Computer Vision tasks.",
    icon="icons/icon.png", 
)

object_dectection_category = knext.category(
    path=main_category,
    level_id="object_dectection",
    name="Object Detection",
    description="Nodes for Object Detection Tasks.",
    icon="icons/icon.png",
)

object_segmentation_category = knext.category(
    path=main_category,
    level_id="object_segmentation",
    name="Object Segmentation",
    description="Nodes for Object Segmentation Tasks.",
    icon="icons/icon.png",
)
#Step 2: DEFINE THE NODE OF THE EXTENTION.

############################################
##### Bounding Box for Object Detection
############################################

@knext.node(name="Object Detection Postprocess", 
            node_type=knext.NodeType.MANIPULATOR, 
            icon_path="icons/icon.png", 
            category = object_dectection_category)

@knext.input_table(
    name = "Image", 
    description = "The image is used to draw bounding boxes."
    )
# @knext.output_image(
#     name = "Image and Detected Objects",
#     description = "The image with bounding boxes of detected objects."
#     )
@knext.output_table(
    name ="Detected Objects",
    description = "A table of detected objects, the corresponding score of that prediction and the image with the bounding boxes."
    )

class BoundingBoxDraw:
    """Short one-line description of the node.
    Long description of the node.
    Can be multiple lines.
    """
    column_image = knext.ColumnParameter(
        label = "Image Column",
        description = "The column that contains the image to be processed.",
        column_filter = kutil.is_type_timestamp # Todo: is it correct?

    )
    column_prediction = knext.ColumnParameter(
        label = "Prediction Column",
        description = "The column that contains the prediction of the object detection model.",
        column_filter = kutil.is_type_timestamp #Todo: is it correct?
        )
    
    filter_objects_param = knext.StringParameter("Object Filter", "The objects that should be filtered out. In case there are multiple objects, each object should be separated by a comma and a space (, ).", "person")

    filter_score_param = knext.DoubleParameter(label = " Prediction Score Threshold", 
                                         description= "The minimum score for filtering out object detections.",
                                          default_value= 0.8,
                                          min_value= 0.0,
                                          max_value= 1.0,
                                          ) 

    # def configure(self, configure_context, input_schema_1):
    def configure(self, configure_context, input_schema_1):  
        self.column_image = kutil.column_exists_or_preset(
            configure_context,
            self.column_image,
            input_schema_1,
            kutil.is_type_timestamp,
        )
        self.column_prediction = kutil.column_exists_or_preset(
            configure_context,
            self.column_prediction,
            input_schema_1,
            kutil.is_type_timestamp,
        )   

        # return input_schema_1
        ## Tutorial step 12: Uncomment the following to adjust to the changes we do in this step in the execute method (and comment out the previous return statement)
        return None
        ## Tutorial step 13: Uncomment to set a warning for the configuration, which will be shown in the workflow
        configure_context.set_warning("This is a warning during configuration")

 
    def execute(self, exec_context, input_1): 
        ''''
        This function is the main function that is executed the post processing task.'''

        df = input_1.to_pandas()
        image = df["Image"].iloc[0]
        LOGGER.warning(image)
        draw = ImageDraw.Draw(image) #TODO:


        object_detection_output = df["Prediction"].iloc[0]

        # Add filter for object labels and scores
        filter_threshold = self.filter_score_param
        filter_labels = self.filter_objects_param.split(', ')

         # Lists to store label and score information
        labels = []
        scores = []

        # Draw all bounding boxes first.
        for obj in object_detection_output:
            # Get the values of the bounding box from the pretrained models outputs.
            box = obj['box']
            label = obj['label']
            score = obj['score']
            xmin, ymin, xmax, ymax = box['xmin'], box['ymin'], box['xmax'], box['ymax']

            # Append the detected objects to the dataframe.
            labels.append(label)
            scores.append(score)

            # Filter out objects based on the label and score threshold
            if label not in filter_labels or score <= filter_threshold:
                continue

            # Draw rectangle and text on the image.
            draw.rectangle([xmin, ymin, xmax, ymax], outline= "red", width= 5)
            draw.text((xmin, ymin), f'{label} : {round(score, 2)}', fill='white', stroke_fill='black', stroke_width=2)


        df['Object Labels'] = ', '.join(labels)
        df['Object Scores'] = ', '.join(map(str, scores))
        df['IMG w. Detected Objects'] = image
        return knext.Table.from_pandas(df)
        # return input_1
        # ## Tutorial step 12: Uncomment the following lines to work with the new port (and comment out the previous return statement)
        # input_1_pandas = input_1.to_pandas() # Transform the input table to some processable format (pandas or pyarrow)
        # input_2_pandas = input_2.to_pandas()
        # input_1_pandas['column2'] = input_1_pandas['column1'] + input_2_pandas['column1']
        # return knext.Table.from_pandas(input_1_pandas)
        # ## Tutorial step 13: Uncomment the following line to use the parameters from the configuration dialogue (and comment out the previous return statement)
        # input_1_pandas['column2'] = input_1_pandas['column2'] + self.double_param
        # LOGGER.warning(self.double_param) # Tutorial step 14: Logging some warning to the console
        # exec_context.set_warning("This is a warning") # Tutorial step 14: Set a warning to be shown in the workflow
        # return knext.Table.from_pandas(input_1_pandas) ### Tutorial step 13: Uncomment
