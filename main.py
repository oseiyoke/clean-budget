from services.split_pdf import main as split_pdf
from services.convert_to_images import main as convert_to_images
from services.aws import upload_to_aws
from services.vision import main as write_projects
import time

def main(source_path, pages_per_pdf):
    split_pdf(source_path, pages_per_pdf)
    convert_to_images(source_path)
    upload_to_aws(source_path)
    write_projects(source_path)



file_path = input("What is the path to the file you want to convert? ")
pages_per_pdf = input("How many pages should each PDF have? ")

start_time = time.time()
print(f"Starting at {start_time}")
main(file_path, pages_per_pdf)

print(f"Finished in {time.time() - start_time} seconds")