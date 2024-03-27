import cv2
import imutils
import os
from change_format import change_image_extension

folder_path = "images"
change_image_extension(folder_path)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def detect_and_resize(image, output_dir, output_filename):
    # Resize the image to a maximum width of 400 pixels
    image = imutils.resize(image, width=min(400, image.shape[1]))
    
    # Detect regions with humans using HOG (Histogram of Oriented Gradients) method
    (regions, _) = hog.detectMultiScale(image, winStride=(4, 4), padding=(4, 4), scale=1.05)
    
    if len(regions) > 0:
        # Calculate the enclosing region that includes all detected humans
        x_min = min(regions[:, 0])
        y_min = min(regions[:, 1])
        x_max = max(regions[:, 0] + regions[:, 2])
        y_max = max(regions[:, 1] + regions[:, 3])

        # Calculate the center of the enclosing region
        center_x = (x_min + x_max) // 2
        center_y = (y_min + y_max) // 2

        # Calculate the coordinates for cropping a 512x512 square around the center
        size = 256  # Half of the desired size (512/2)
        start_x = center_x - size
        end_x = center_x + size
        start_y = center_y - size
        end_y = center_y + size

        # Ensure the cropping region is within the image dimensions
        start_x = max(0, start_x)
        start_y = max(0, start_y)
        end_x = min(image.shape[1] - 1, end_x)
        end_y = min(image.shape[0] - 1, end_y)

        # Crop the image to the 512x512 region around the detected human
        cropped_image = image[start_y:end_y, start_x:end_x]

        # Resize the cropped image to 512x512
        resized_image = cv2.resize(cropped_image, (512, 512))
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)
        cv2.imwrite(output_path, resized_image)

        return resized_image

    else:
        print("No human detected in the image.")
        
        # Calculate the center of the image
        center_x = image.shape[1] // 2
        center_y = image.shape[0] // 2

        # Calculate the coordinates for cropping a 512x512 square around the center
        size = 256  # Half of the desired size (512/2)
        start_x = center_x - size
        end_x = center_x + size
        start_y = center_y - size
        end_y = center_y + size

        # Ensure the cropping region is within the image dimensions
        start_x = max(0, start_x)
        start_y = max(0, start_y)
        end_x = min(image.shape[1] - 1, end_x)
        end_y = min(image.shape[0] - 1, end_y)

        # Crop the image to the 512x512 region around the center of the image
        cropped_image = image[start_y:end_y, start_x:end_x]

        # Resize the cropped image to 512x512
        resized_image = cv2.resize(cropped_image, (512, 512))
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)
        cv2.imwrite(output_path, resized_image)

        return resized_image
    
# image_path = "images/wew.jpg"
# image = cv2.imread(image_path)
# output_filename = "resized_image.jpg"
# output_dir = "resized_images"
# resized_image = detect_and_resize(image)


#looping over folder

input_folder = "jpg_images"
output_dir = "resized_images"
no_humans_detected = []
os.makedirs(output_dir, exist_ok=True)


image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

for image_file in image_files:
    image_path = os.path.join(input_folder, image_file)
    image = cv2.imread(image_path)

    resized_image = detect_and_resize(image, output_dir, image_file)
    if resized_image is None:
        no_humans_detected.append(image_file)
    else:
        output_path = os.path.join(output_dir, image_file)
        _, file_extension = os.path.splitext(image_file)
        if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
            cv2.imwrite(output_path, resized_image)
        else:
            print(f"Skipping {image_file} - Unsupported file extension.")


# print("No humans detected in the following images: ", no_humans_detected)