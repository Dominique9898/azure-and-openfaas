import azure.functions as func
import logging
import base64
from image_utils import RESIZE_IMAGE, APPLY_FILTER, COMPOSITE_IMAGES
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="composite")
def composite_images(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f'Invoke Composite Images request.')
    
    # Parse the incoming JSON payload
    req_body = req.get_json()
    
    # Retrieve the base64-encoded image data list from the request
    image_data_list = req_body.get('image_data_list')
    
    # Process the image data
    composited_image_b64 = COMPOSITE_IMAGES(image_data_list)
    
    # Construct the response data
    response_data = {
        'image_data': composited_image_b64
    }

    # Return the response
    return func.HttpResponse(
        body=json.dumps(response_data),
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )



@app.route(route="filter")
def apply_filter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f'Invoke Apply Filter request.')
    
    # # Parse the incoming JSON payload
    req_body = req.get_json()
    
    # # Retrieve the image data and action from the request
    image_data_b64 = req_body.get('image_data')

    resized_image_b64 = APPLY_FILTER(image_data_b64)

    response_data = {
        'image_data': resized_image_b64
    }

    logging.info(f'Return Response. Resize Image response_json:{response_data}')

    return func.HttpResponse(
        body=json.dumps(response_data),
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )

@app.route(route="resize")
def resize_image(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f'Invoke Resize Image request.')
    
    # # Parse the incoming JSON payload
    req_body = req.get_json()
    
    # # Retrieve the image data and action from the request
    image_data_b64 = req_body.get('image_data')

    size = tuple(req_body.get('size', (256, 256))) 

    resized_image_b64 = RESIZE_IMAGE(image_data_b64, size)

    response_data = {
        'image_data': resized_image_b64
    }

    logging.info(f'Return Response. Resize Image response_json:{response_data}')

    return func.HttpResponse(
        body=json.dumps(response_data),
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )

@app.route(route="imageProcess")
def imageProcess(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    