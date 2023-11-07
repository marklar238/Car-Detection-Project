import cv2


# Function to parse coordinates from a text file
def parse_coordinates(file_path):
    coordinates = {}
    with open(file_path, 'r') as file:
        for line in file:
            data = line.strip().split(',')
            if len(data) == 9:
                image_id = int(data[0])
                x_min, y_min, width, height = map(float, data[2:6])
                if image_id not in coordinates:
                    coordinates[image_id] = []
                coordinates[image_id].append((int(x_min), int(y_min), int(x_min + width), int(y_min + height)))
    return coordinates


# Path to the folder containing images
image_folder = 'M1401'

start_image_id = 100  # Change this to the starting image ID
end_image_id = 101


def open_and_print(file_path):
    with open(file_path, 'r') as file:
        coordinates = parse_coordinates(file_path)

        for target_image_id in range(start_image_id, end_image_id):
            if target_image_id in coordinates:
                image_path = f"{image_folder}/img{str(target_image_id).zfill(6)}.jpg"
                image = cv2.imread(image_path)

                for x_min, y_min, x_max, y_max in coordinates[target_image_id]:
                    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                cv2.imshow(f'Image {file_path}', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print(f"Image {target_image_id} not found in the text file.")


open_and_print('M1401.txt')

open_and_print('M1401_DET.txt')

open_and_print('M1401_DET_det_RON.txt')

open_and_print('M1401_DET_RFCN.txt')

open_and_print('M1401_DET_FRCNN.txt')