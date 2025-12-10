
import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.utils.response import build_response
from components.DemoPackage.src.models.PackageModel import PackageModel

class Brightness(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.input_image_data = self.request.get_param("inputImage")
        self.outputImage = None
        self.outputInfo = ""
        self.load_parameters()

    def load_parameters(self):
        self.brightness_val = self.request.get_param("BrightnessValue")
        self.preset_sel = self.request.get_param("PresetSelection")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def process_brightness(self, image):
        factor = 1.0

        if self.brightness_val is not None:
            factor = self.brightness_val
            self.outputInfo = f"Manual Mode: {factor}"
        elif self.preset_sel == "Low":
            factor = 0.5
            self.outputInfo = "Preset: Low"
        elif self.preset_sel == "High":
            factor = 1.5
            self.outputInfo = "Preset: High"

        return cv2.convertScaleAbs(image, alpha=factor, beta=0)

    def run(self):
        img_obj = Image.get_frame(img=self.input_image_data, redis_db=self.redis_db)
        current_image = img_obj.value

        processed_image = self.process_brightness(current_image)

        img_obj.value = processed_image
        self.outputImage = Image.set_frame(img=img_obj, package_uID=self.uID, redis_db=self.redis_db)
        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()