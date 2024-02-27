import os
import csv
import boto3

def upload_to_aws(folder_path):
    s3 = boto3.client('s3')
    count = 0
    for file in os.listdir(folder_path):
        if count == 5:
            break
        if file.endswith('.jpg'):
            s3.upload_file(os.path.join(folder_path, file), '2024-projects-images', file, ExtraArgs={'ACL': 'public-read'})
            print(f"Uploaded {file}")
            count += 1

def loop_through_bucket(bucket_name):
    s3 = boto3.client('s3')

    # List objects within the bucket
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name)

    # Loop through each page (in case of large number of files)
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                # Check if the file is an image based on its extension
                if key.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    image_url = f"https://{bucket_name}.s3.eu-central-1.amazonaws.com/{key}"
                    print(f"Found image: {key}")

loop_through_bucket("2024-projects-images")