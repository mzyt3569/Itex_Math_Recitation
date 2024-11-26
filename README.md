# Itex_Math_Recitation

# Installation

for windows....

conda create -n itex python=3.12

pip install -r requirements.txt

We use tessaract.

https://github.com/UB-Mannheim/tesseract/wiki

visit this page and install. make path so we can use tesseract in command.

# How to Use

python Inference.py -i /source_directory -o /output_directory -d /database_directory_for_rag 

if you want to use rag while translate, add --rag

if you want to know the steps add --debug. it will make some csv file.

if you want to make voices add --full. then it will create to mp3.

web demo

python web_launcher.py 

this web demo does not use rag, and does not make voices.

if you want to use rag, change false to true in line 16.

# Other information

OCR -> get image and make json-struct file.

parser -> seperate fraction and inequalities.

translator -> translate latex

merger -> merge latex.
