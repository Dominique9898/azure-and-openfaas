from PIL import Image, ImageFilter
import io
import base64
import math
def RESIZE_IMAGE(image_data_b64, output_size):
    """
    图像缩放函数，接收base64编码的图像数据和输出尺寸，返回缩放后的图像字节流。
    """
    # Decode the base64 image data
    image_data = base64.b64decode(image_data_b64)

    # Read the image into a PIL Image object
    with Image.open(io.BytesIO(image_data)) as img:
        # Resize the image
        resized_image = img.resize(output_size)
        
        # Save the resized image to a byte stream
        with io.BytesIO() as output:
            resized_image.save(output, format="JPEG")
            # Get the byte data from the stream
            image_bytes = output.getvalue()
    
    # Encode the byte data back to base64 for HTTP response
    resized_image_b64 = base64.b64encode(image_bytes).decode('utf-8')
    return resized_image_b64

def APPLY_FILTER(image_data_b64, filter_type=ImageFilter.GaussianBlur(5)):
    """
    图像滤镜应用函数，接收图像字节流列表和滤镜类型，返回应用滤镜后的图像字节流列表。
    """
    image_data = base64.b64decode(image_data_b64)
    if not isinstance(filter_type, ImageFilter.Filter):
        raise ValueError("filter_type must be an instance of ImageFilter.Filter")
    
    with Image.open(io.BytesIO(image_data)) as img:
        filtered_image = img.filter(filter_type)
        with io.BytesIO() as output:
            filtered_image.save(output, format="JPEG")
            image_bytes = output.getvalue()

    filtered_image_b64 = base64.b64encode(image_bytes).decode('utf-8')
    return filtered_image_b64

def COMPOSITE_IMAGES(image_data_list):
    """
    图像合成函数，接收一个 base64 编码的图像数据列表，将它们合成为一个矩形，并返回合成图像的字节流。
    """
    # Decode base64-encoded image data and open as PIL images
    images = [Image.open(io.BytesIO(base64.b64decode(image_data))) for image_data in image_data_list]

    # Calculate the number of rows and columns
    num_images = len(images)
    num_columns = int(math.ceil(math.sqrt(num_images)))
    num_rows = int(math.ceil(num_images / num_columns))

    # Calculate the width and height of each cell
    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)
    cell_width = max_width
    cell_height = max_height

    # Calculate the total width and height of the composite image
    total_width = cell_width * num_columns
    total_height = cell_height * num_rows

    # Create a new blank image with the correct size
    composite_image = Image.new('RGB', (total_width, total_height))

    # Paste each image into the composite image
    row_index = 0
    col_index = 0
    for img in images:
        x_offset = col_index * cell_width
        y_offset = row_index * cell_height
        composite_image.paste(img, (x_offset, y_offset))

        # Move to the next cell
        col_index += 1
        if col_index >= num_columns:
            col_index = 0
            row_index += 1

    # Save the composite image to a byte stream
    with io.BytesIO() as output:
        composite_image.save(output, format="JPEG")
        image_bytes = output.getvalue()

    composited_image_b64 = base64.b64encode(image_bytes).decode('utf-8')
    return composited_image_b64