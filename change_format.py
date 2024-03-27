import os
from PIL import Image

def change_image_extension(folder_path, target_extension='jpg'):
    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)

    # Create a new folder called 'new_images' on the same level as the 'images_folder'
    new_folder_path = os.path.join(os.path.dirname(folder_path), 'jpg_images')
    os.makedirs(new_folder_path, exist_ok=True)

    # Iterate through each file
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)

        # Check if the file is an image (you can add more supported extensions if needed)
        if file_name.lower().endswith(('.png', '.jpeg', '.gif', '.bmp', '.tiff', "webp", ".heic", ".jpg")):
            # Open the image using PIL
            try:
                img = Image.open(file_path)

                # Save the image with the new extension in the 'new_images' folder
                new_file_name = os.path.splitext(file_name)[0] + '.' + target_extension
                new_file_path = os.path.join(new_folder_path, new_file_name)
                img.convert("RGB").save(new_file_path)

                # Close the image
                img.close()

                # Remove the old file if you want (use with caution!)
                # os.remove(file_path)

                print(f"Converted: {file_name} -> {new_file_name}")

            except Exception as e:
                print(f"Error converting {file_name}: {e}")

if __name__ == "__main__":
    folder_path = 'images_folder'
    change_image_extension(folder_path)
