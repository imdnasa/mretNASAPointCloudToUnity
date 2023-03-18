import os

# specify the file path
file_path = r'D:\Unity\AzureKinect\Assets\PPTK Textures\img.png'


# check if file exists before deleting
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"The file {file_path} has been deleted.")
else:
    print(f"The file {file_path} does not exist.")
