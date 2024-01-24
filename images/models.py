from django.db import models
from django.core.files.base import ContentFile
from django.contrib import admin
import PIL
import numpy as np
import cv2
from io import BytesIO
import os
from cvzone.SelfiSegmentationModule import SelfiSegmentation

class Image(models.Model):
    img = models.ImageField(upload_to='images')
    rmbg_img = models.ImageField(blank=True, upload_to='images_rmbg')

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        pil_img = PIL.Image.open(self.img)
        img = np.array(pil_img)
        # Convert image to BGR format (assuming it's in RGB format)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Assuming SelfiSegmentation is a class with a method removeBG
        segmentor = SelfiSegmentation()
        rmbg = segmentor.removeBG(img_bgr, (0, 255, 0), cutThreshold=0.4)

        # Convert the resulting image back to RGB format
        rmbg_rgb = cv2.cvtColor(rmbg, cv2.COLOR_BGR2RGB)

        buffer = BytesIO()
        output_img = PIL.Image.fromarray(rmbg_rgb)
        output_img.save(buffer, format='png')
        val = buffer.getvalue()

        # Split the filename into name and extension
        filename = os.path.basename(self.img.name)
        name, *extension = filename.split(".")
        
        # Handle cases where there are multiple dots in the filename
        extension = ".".join(extension)

        # Save the background-removed image with a modified filename
        self.rmbg_img.save(f"bgrm_{name}.{extension}", ContentFile(val), save=False)
        super().save(*args, **kwargs)


        


