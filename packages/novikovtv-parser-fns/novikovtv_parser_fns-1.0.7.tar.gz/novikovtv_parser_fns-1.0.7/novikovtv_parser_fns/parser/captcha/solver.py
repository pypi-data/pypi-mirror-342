import os.path
import pickle
import warnings
from enum import Enum
from typing import Optional

import cv2
import numpy as np

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from keras.api.models import load_model

from novikovtv_parser_fns.parser.captcha.helpers import resize_to_fit


class CaptchaSolverType(Enum):
    AI = 1


class CaptchaSolver(object):
    def __init__(self, img: bytes, *, _solver_type: CaptchaSolverType = CaptchaSolverType.AI):
        image_np = np.frombuffer(img, np.uint8)
        img_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        self.image = img_np
        self.letter_images = []

        # if solver_type.value == CaptchaSolverType.AI.value:
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", category=UserWarning, module="keras")
        basedir: str = os.path.dirname(os.path.abspath(__file__))

        MODEL_FILENAME = os.path.join(basedir, "./ml_models/68_percents.keras")
        MODEL_LABELS_FILENAME = os.path.join(basedir, "./ml_models/68_percents.dat")

        with open(MODEL_LABELS_FILENAME, "rb") as f:
            self.lb = pickle.load(f)

        self.model = load_model(MODEL_FILENAME)

    def solve(self) -> Optional[str]:
        tr, image = cv2.threshold(self.image, 190, 230, cv2.THRESH_BINARY)
        image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.medianBlur(image, 3)
        image = cv2.fastNlMeansDenoising(image, None, 60, 10, 60)

        image = cv2.copyMakeBorder(image, 20, 20, 20, 20, cv2.BORDER_REPLICATE)

        thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contours = contours[0] if len(contours) == 2 else contours[1]

        letter_image_regions = []

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            if w / h > 0.7:
                half_width = int(w / 2)
                letter_image_regions.append((x, y, half_width, h))
                letter_image_regions.append((x + half_width, y, half_width, h))
            else:
                letter_image_regions.append((x, y, w, h))

        if len(letter_image_regions) != 6:
            return None

        letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])

        # output = cv2.merge([image] * 3)
        predictions = []
        for letter_bounding_box in letter_image_regions:
            x, y, w, h = letter_bounding_box

            letter_image = image[y - 2:y + h + 2, x - 2:x + w + 2]

            letter_image = resize_to_fit(letter_image, 20, 20)
            if letter_image is None:
                return None

            self.letter_images.append(letter_image)
            letter_image = np.expand_dims(letter_image, axis=2)
            letter_image = np.expand_dims(letter_image, axis=0)

            prediction = self.model.predict(letter_image, verbose=0)
            letter = self.lb.inverse_transform(prediction)[0]
            predictions.append(letter)

            # cv2.rectangle(output, (x - 2, y - 2), (x + w + 4, y + h + 4), (0, 255, 0), 1)
            # cv2.putText(output, letter, (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

        captcha_text = "".join(predictions)
        return captcha_text


if __name__ == '__main__':
    pass
