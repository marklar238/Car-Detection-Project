import os
from PIL import Image

def process_images(image_folder):
    # Create output image folder if it doesn't exist
    output_image_folder = f"{image_folder}_processed_images"
    os.makedirs(output_image_folder, exist_ok=True)

    # Process each image in the input folder
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg"):
            image_path = os.path.join(image_folder, filename)
            img = Image.open(image_path)

            # Format image name
            image_name = f"{image_folder}_formatted_{filename}"
            image_path_formatted = os.path.join(output_image_folder, image_name)

            # Check if the formatted image already exists, if not, save
            if not os.path.exists(image_path_formatted):
                img.save(image_path_formatted)


def process_text_file(image_folder, text_file):
    # Create output label folder if it doesn't exist
    output_label_folder = f"{image_folder}_processed_labels"
    os.makedirs(output_label_folder, exist_ok=True)

    # Read image dimensions
    with Image.open(os.path.join(image_folder, os.listdir(image_folder)[0])) as img:
        width, height = img.size

    # Read original text file content and store it in a dictionary
    original_data = {}
    with open(text_file, 'r') as original_txt_file:
        for line in original_txt_file:
            values = line.strip().split(',')
            image_name = f"{image_folder}_formatted_{values[0]}.jpg"
            coordinates = [
                round((int(values[2]) + int(values[4]) / 2) / width, 6),   # x_center = (x_min + width/2) / width
                round((int(values[3]) + int(values[5]) / 2) / height, 6),  # y_center = (y_min + height/2) / height
                round(int(values[4]) / width, 6),                          # normalize width
                round(int(values[5]) / height, 6)                          # normalize height
            ]

            if image_name in original_data:
                original_data[image_name].append(coordinates)
            else:
                original_data[image_name] = [coordinates]

    # Process corresponding text file
    for image_name, instances in original_data.items():
        txt_filename = f"{image_folder}_formatted_{os.path.splitext(image_name)[0]}.txt"
        txt_path = os.path.join(output_label_folder, txt_filename)

        # Check if the formatted label file already exists, if not, write content
        if not os.path.exists(txt_path):
            with open(txt_path, 'w') as txt_file:
                # Write the formatted coordinates to the new text file
                for coordinates in instances:
                    txt_file.write('0 ' + ' '.join(map(str, coordinates)) + '\n')


if __name__ == "__main__":
    image_folder = "M1303"  # Replace with your input image folder
    text_file = "M1303_gt.txt"  # Replace with your original text file

    # Process images
    process_images(image_folder)

    # Process text file
    process_text_file(image_folder, text_file)
