from PIL import Image, ImageFilter
import base64
import io
import json

# Your existing OpenFaaS image processing functions
from .image_utils import RESIZE_IMAGE, APPLY_FILTER, COMPOSITE_IMAGES

def handle(req):
    """
    Handle function for OpenFaaS to process image with specified action.
    """
    # Parse the incoming request data
    try:
        req_data = json.loads(req)
        action = req_data.get('action')
        image_data_b64 = req_data.get('image_data')
        image_data_list_b64 = req_data.get('image_data_list')

        if action == 'resize' and image_data_b64:
            # Call the resize function
            output_size = (256, 256)  # Example size, you would get this from the request as well
            result_b64 = RESIZE_IMAGE(image_data_b64, output_size)
            return json.dumps({"image_data": result_b64})

        elif action == 'filter' and image_data_b64:
            # Call the filter function
            result_b64 = APPLY_FILTER(image_data_b64)
            return json.dumps({"image_data": result_b64})

        elif action == 'composite' and image_data_list_b64:
            # Call the composite function
            result_b64 = COMPOSITE_IMAGES(image_data_list_b64)
            return json.dumps({"image_data": result_b64})

        else:
            return json.dumps({"error": "Invalid action or data"})
    except Exception as e:
        return json.dumps({"error": str(e)})
