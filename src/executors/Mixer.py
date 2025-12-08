
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

class Mixer(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.main_image_data = self.request.get_param("inputImage")
        self.overlay_image_data = self.request.get_param("overlayImage")

        self.outputImage = None
        self.outputInfo = ""

        self.load_parameters()

    def load_parameters(self):
        self.opacity_val = self.request.get_param("OpacityValue")
        self.method_sel = self.request.get_param("MethodSelection")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def process_mixing(self, main_img, overlay_img):
        h, w = main_img.shape[:2]
        overlay_resized = cv2.resize(overlay_img, (w, h))

        result = main_img

        if self.opacity_val is not None:
            alpha = 1.0 - self.opacity_val
            beta = self.opacity_val
            result = cv2.addWeighted(main_img, alpha, overlay_resized, beta, 0.0)
            self.outputInfo = f"Mixed with Opacity: {self.opacity_val}"

        elif self.method_sel == "Add":
            result = cv2.add(main_img, overlay_resized)
            self.outputInfo = "Method: Add"

        elif self.method_sel == "Multiply":
            result = cv2.multiply(main_img, overlay_resized, scale=1.0/255.0)
            result = cv2.convertScaleAbs(result, alpha=255)
            self.outputInfo = "Method: Multiply"

        return result

    def run(self):
        main_obj = Image.get_frame(img=self.main_image_data, redis_db=self.redis_db)
        main_img = main_obj.value
        if self.overlay_image_data is None:
            self.outputInfo = "Error: No overlay image provided"
            self.outputImage = Image.set_frame(img=main_obj, package_uID=self.uID, redis_db=self.redis_db)
            return build_response(context=self)

        overlay_obj = Image.get_frame(img=self.overlay_image_data, redis_db=self.redis_db)
        overlay_img = overlay_obj.value

        processed_image = self.process_mixing(main_img, overlay_img)
        main_obj.value = processed_image
        self.outputImage = Image.set_frame(img=main_obj, package_uID=self.uID, redis_db=self.redis_db)

        return build_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()