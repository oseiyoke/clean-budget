import base64
import requests
import ast
import csv
import os
import boto3

# OpenAI API Key
api_key = "sk-xxx"


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_text_from_image_using_vision(image_url):
  # Path to your image

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }

  payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": """
            This is an image containing various information, including project line items. Project line items begin with a project code(ERGP...).
            Extract the project code(ERGP...), project name, budget amount and type for each line item that you discover in this image, 
            and when you're done with discovery, return all line items to me in a list like the example below:
            projects=[["ERGP123455", "Project 1", "Fixed", "1000"], ["ERGP123456", "Project 2", "Variable", "2000"]]
            """
          },
          {
          "type": "image_url",
          "image_url": {
            "url": image_url
          }
          }
        ]
      }
    ],
    "max_tokens": 4096
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

  data = response.json()
  print(data)
  content = data['choices'][0]['message']['content']
  print(content)
  start_idx = content.find('[')
  end_idx = content.rfind(']') + 1

  list_of_projects = ast.literal_eval(content[start_idx:end_idx])
  return list_of_projects

def main(folder_path):
  count = 0
  s3 = boto3.client('s3')

  # List objects within the bucket
  bucket_name = "2024-projects-images"
  paginator = s3.get_paginator('list_objects_v2')
  page_iterator = paginator.paginate(Bucket=bucket_name)

  # Loop through each page (in case of large number of files)
  for page in page_iterator:
      if count == 1:
        break
      if 'Contents' in page:
          for obj in page['Contents']:
              key = obj['Key']
              # Check if the file is an image based on its extension
              if key.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                  print(f"Found image {key}")
                  image_url = f"https://{bucket_name}.s3.eu-central-1.amazonaws.com/{key}"
                  list_of_projects = get_text_from_image_using_vision(image_url)

                  with open(os.path.join(folder_path, 'projects.csv'), 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(list_of_projects)
                  count+=1

