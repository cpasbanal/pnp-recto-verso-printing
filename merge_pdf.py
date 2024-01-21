##########
# How to #
##########

# Look for files in directory passed as argument
# into subfolders /recto and /verso
# will merge images into a pdf to enable recto verso printing


###########
# Imports #
###########

from fpdf import FPDF
from PIL import Image
import math
import os
import sys

#############
# Constants #
#############
DPI = 72
PAGE_WIDTH = 210
MARGIN_WIDTH = 1
PAGE_HEIGHT = 297
MARGIN_HEIGHT = 1

if len(sys.argv) > 2 and sys.argv[2] == 'board':
    # Market or characters
    CARD_WIDTH = 200 # 915
    CARD_HEIGHT = 135.3  # 619
else:
    # Standard playing cards
    CARD_WIDTH = 63 # 1238
    CARD_HEIGHT =  83.2  # 1829


#############
# Functions #
#############
def gather_images():
    # All the images should be in two folders recto & verso
    # you can have only 1 verso that will be replicated for all the recto
    path = os.getcwd() +  "/" + sys.argv[1]
    images_recto = [path + "/recto/" + f for f in os.listdir(path + "/recto") if os.path.isfile(os.path.join(path + "/recto", f)) and f.lower().endswith('.jpg')]
    images_verso = [path + "/verso/" + f for f in os.listdir(path + "/verso") if os.path.isfile(os.path.join(path + "/verso", f)) and f.lower().endswith('.jpg')]
    if len(images_verso) < len(images_recto):
        images_verso = images_verso * ((len(images_recto) + len(images_verso) - 1) // len(images_verso))
    return images_recto, images_verso

def create_pdf(images_recto, images_verso, output_pdf_path):
    # Open a new PDF document
    fpdf=FPDF()

    # Get the number of images per row and per column
    img_per_row = math.floor((PAGE_WIDTH - MARGIN_WIDTH * 2) / CARD_WIDTH)
    img_per_col = math.floor((PAGE_HEIGHT- MARGIN_HEIGHT * 2) / CARD_HEIGHT)
    if img_per_col == 0 or img_per_row == 0:
        raise Exception("Not enough space in the page to add the image with this size")
    
    while len(images_recto) > 0:
        # Add images to the pdf document (recto and verso on each page, verso should be right to left for printing)
        fpdf.add_page()
        images_recto = fill_images(fpdf, images_recto, img_per_row, img_per_col)
        fpdf.add_page()
        images_verso = fill_images(fpdf, images_verso, img_per_row, img_per_col, direction = -1)
        pass

    # Save the PDF document
    fpdf.output(output_pdf_path)


def fill_images(fpdf, images, img_per_row, img_per_col, direction = 1):
    for row_index in range(img_per_col):
        for col_index in range(img_per_row):
            if len(images) == 0:
                return []
            image_path = images.pop(0)
            if direction == 1:
                fpdf.image(image_path, MARGIN_WIDTH + (col_index) * CARD_WIDTH, MARGIN_HEIGHT + (row_index) * CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT)
            else:
                fpdf.image(image_path, PAGE_WIDTH - MARGIN_WIDTH - (col_index + 1) * CARD_WIDTH, MARGIN_HEIGHT + (row_index) * CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT)
    return images


##############
# Main calls #
##############
output_pdf_path = sys.argv[1] + '.pdf'
images_recto, images_verso = gather_images()
create_pdf(images_recto, images_verso, output_pdf_path)