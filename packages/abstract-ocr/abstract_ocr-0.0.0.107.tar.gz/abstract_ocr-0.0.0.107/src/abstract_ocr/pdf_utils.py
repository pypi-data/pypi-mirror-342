#!/usr/bin/env python3
from .functions import argparse,Image
def images_to_pdf(image_paths, output_pdf):
    if not image_paths:
        raise ValueError("No image files provided for conversion.")

    # Open the first image and convert to RGB if necessary
    first_image = Image.open(image_paths[0])
    if first_image.mode in ("RGBA", "P"):
        first_image = first_image.convert("RGB")

    # List to hold subsequent images
    image_list = []
    for img_path in image_paths[1:]:
        img = Image.open(img_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        image_list.append(img)

    # Save all images into a single PDF file
    first_image.save(output_pdf, "PDF", resolution=100.0, save_all=True, append_images=image_list)
    print(f"PDF saved as: {output_pdf}")
