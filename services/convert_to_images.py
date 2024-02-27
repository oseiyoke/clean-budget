import os
from pytesseract import image_to_string
from pdf2image import convert_from_path

def get_sorted_files(folder_path):
    files = os.listdir(folder_path)
    full_paths = [os.path.join(folder_path, file) for file in files if file.endswith('.pdf')]
    sorted_files = sorted(full_paths, key=os.path.getmtime)
    return sorted_files

def main(file_path):
    """
    Function to process a PDF file and split it into individual images.
    :param file_path: The path to the PDF file to be processed.
    """
    count = 1
    project_pages = 0
    folder_path = file_path.replace('.pdf', '_split')

    if os.path.exists(folder_path):
        print("Gotten to the Folder with splits, Containing pdfs")
        images_folder = os.path.join(folder_path, 'images')
        pages_without_project_folder = os.path.join(images_folder, 'pages_without_project')

        # Create a folder to store the images
        if not os.path.exists(images_folder):
            print("Creating Images folder that didnt exist before...")
            os.makedirs(images_folder)
        
        # Create a folder to store the images that dont have projects
        if not os.path.exists(pages_without_project_folder):
            print("Creating Images Without Projects folder that didnt exist before...")
            os.makedirs(pages_without_project_folder)

        sorted_files = get_sorted_files(folder_path)

        # Convert each PDF File to images
        for file in sorted_files:
            print("Converting: ", file.split('/')[-1], " to images")
            file_path = os.path.join(folder_path, file)
            images = convert_from_path(file_path)

            # Loop through and save all images created using convert_from_path
            for i, image in enumerate(images):
                ocr_text = image_to_string(image)
                print(f"\nConverted image: {count} to text")

                if ("ERGP" in ocr_text) or ("ZIP2024" in ocr_text):
                    print(f"Found Project Code in Image {count}. Saving as page_{count}.jpg...")
                    name = os.path.join(images_folder, f'page_{count}.jpg')
                    image.save(name, 'JPEG')
                    project_pages += 1
                else:
                    print(f"Did not find Project Code in Image {count}. Saving in Pages without projects folder...")
                    name = os.path.join(pages_without_project_folder, f'page_{count}.jpg')
                    image.save(name, 'JPEG')
                
                count += 1
            print("Converted: ", count-1, " pages to images \n\n")


# main("/Users/oseiyoke/Documents/2024_APPROPRIATION.pdf")