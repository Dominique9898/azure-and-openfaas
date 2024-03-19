import requests
import base64
import os
import concurrent.futures

# The local or deployed Azure Function endpoint
FUNCTION_URL = 'http://localhost:7071/api'

# Folder containing images
IMAGES_FOLDER = '/Users/dominikwei/Documents/test_set'
CONCURRENCY_LEVEL = 10  # Define how many concurrent requests you want to send
DEFAULT_IMAGES_PER_COMPOSITE = 100

def process_image(action, image_data):
    """
    Process the image with the specified action.
    """
    payload = {'action': action}
    if isinstance(image_data, str):
        payload['image_data'] = image_data
    elif isinstance(image_data, list):
        payload['image_data_list'] = image_data

    response = requests.post(f'{FUNCTION_URL}/{action}', json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to process image data with action '{action}'. "
              f"Status code: {response.status_code}, Response text: {response.text}")
        return None

def encode_image(image_path):
    """
    Encode the image to base64 and return the encoded string.
    """
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def perform_action(action, image_path):
    """
    Wrapper function to perform a specific action on an image.
    """
    encoded_image = encode_image(image_path)
    response_data = process_image(action, encoded_image)
    if response_data:
        processed_image_data = base64.b64decode(response_data.get('image_data'))
        save_processed_image(image_path, action, processed_image_data)

def save_processed_image(image_path, action, processed_image_data):
    """
    Save the processed image to a file for verification.
    """
    filename = os.path.basename(image_path)
    output_folder = os.path.join('processed_images', action)
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename)
    with open(output_path, 'wb') as f:
        f.write(processed_image_data)
    print(f"Image '{filename}' processed with action '{action}' and saved as '{output_path}'")

def test_resize():
    image_paths = [os.path.join(IMAGES_FOLDER, filename) for filename in os.listdir(IMAGES_FOLDER)
                   if filename.lower().endswith(('.jpeg', '.jpg'))][:CONCURRENCY_LEVEL]
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY_LEVEL) as executor:
        futures = [executor.submit(perform_action, 'resize', image_path) for image_path in image_paths]
        concurrent.futures.wait(futures)

def test_filter():
    image_paths = [os.path.join(IMAGES_FOLDER, filename) for filename in os.listdir(IMAGES_FOLDER)
                   if filename.lower().endswith(('.jpeg', '.jpg'))][:CONCURRENCY_LEVEL]
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY_LEVEL) as executor:
        futures = [executor.submit(perform_action, 'filter', image_path) for image_path in image_paths]
        concurrent.futures.wait(futures)

def perform_composite_action(batch_image_paths):
    """
    Performs a composite action on a batch of images.
    """
    encoded_images = [encode_image(image_path) for image_path in batch_image_paths]
    response_data = process_image('composite', encoded_images)
    if response_data:
        processed_image_data = base64.b64decode(response_data.get('image_data'))
        # Save the composited image. Here, a unique identifier is added to the filename.
        save_processed_image(batch_image_paths[0], f'composite_{len(batch_image_paths)}', processed_image_data)

def test_composite(concurrency_level=CONCURRENCY_LEVEL, images_per_composite=DEFAULT_IMAGES_PER_COMPOSITE):
    """
    Test the composite action by concurrently processing batches of images.
    """
    # Prepare a list of all image paths
    all_image_paths = [os.path.join(IMAGES_FOLDER, filename) for filename in os.listdir(IMAGES_FOLDER)
                       if filename.lower().endswith(('.jpeg', '.jpg'))]

    # Split the image paths into batches
    batches = [all_image_paths[i:i + images_per_composite] for i in range(0, len(all_image_paths), images_per_composite)]

    # Use ThreadPoolExecutor to concurrently process each batch
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency_level) as executor:
        futures = [executor.submit(perform_composite_action, batch) for batch in batches[:concurrency_level]]
        
        # Wait for all futures to complete
        concurrent.futures.wait(futures)
def main():
    test_resize()
    test_filter()
    test_composite()

if __name__ == "__main__":
    main()
