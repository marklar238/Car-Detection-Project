import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image


def yolo_to_pixel(image_size, box):
    width, height = image_size
    x, y, h, w = box
    x = int((x - w / 2) * width)
    y = int((y - h / 2) * height)
    w = int(w * width)
    h = int(h * height)
    return x, y, w, h


def visualize_bounding_boxes(image_file, label_file):
    # Read image
    img = Image.open(image_file)
    width, height = img.size

    # Read bounding box coordinates from the label file
    with open(label_file, 'r') as label_file:
        lines = label_file.readlines()
        bounding_boxes = [[float(coord) for coord in line.strip().split()[1:]] for line in lines]

    # Convert YOLO format to pixel coordinates
    pixel_boxes = [yolo_to_pixel((width, height), box) for box in bounding_boxes]

    # Create figure and axes
    fig, ax = plt.subplots(1)

    # Display the image
    ax.imshow(img)

    # Add bounding boxes to the image
    for box in pixel_boxes:
        x, y, w, h = box
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    plt.show()

if __name__ == "__main__":
    image_file = "M1303_processed_images/M1303_formatted_img000010.jpg"  # Replace with your image file
    label_file = "M1303_processed_labels/M1303_formatted_M1303_formatted_10.txt"  # Replace with your label file
    visualize_bounding_boxes(image_file, label_file)
