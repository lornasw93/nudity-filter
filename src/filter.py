import os
import cv2
import pydload
import numpy as np
import onnxruntime
from utils import preprocess_image
import json


def dummy(x):
    return x


FILE_URLS = {
    "default": {
        "checkpoint": "https://github.com/notAI-tech/NudeNet/releases/download/v0/detector_v2_default_checkpoint.onnx",
        "classes": "https://github.com/notAI-tech/NudeNet/releases/download/v0/detector_v2_default_classes",
    },
    "base": {
        "checkpoint": "https://github.com/notAI-tech/NudeNet/releases/download/v0/detector_v2_base_checkpoint.onnx",
        "classes": "https://github.com/notAI-tech/NudeNet/releases/download/v0/detector_v2_base_classes",
    },
}


class Filter:
    detection_model = None
    classes = None

    def __init__(self, model_name="default"):
        """
        model = Filter()
        """
        checkpoint_url = FILE_URLS[model_name]["checkpoint"]
        classes_url = FILE_URLS[model_name]["classes"]

        home = os.path.expanduser("~")
        model_folder = os.path.join(home, f".NudeNet/")
        if not os.path.exists(model_folder):
            os.makedirs(model_folder)

        checkpoint_name = os.path.basename(checkpoint_url)
        checkpoint_path = os.path.join(model_folder, checkpoint_name)
        classes_path = os.path.join(model_folder, "classes")

        if not os.path.exists(checkpoint_path):
            print("Downloading the checkpoint to", checkpoint_path)
            pydload.dload(checkpoint_url,
                          save_to_path=checkpoint_path, max_time=None)

        if not os.path.exists(classes_path):
            print("Downloading the classes list to", classes_path)
            pydload.dload(
                classes_url, save_to_path=classes_path, max_time=None)

        self.detection_model = onnxruntime.InferenceSession(checkpoint_path)

        self.classes = [c.strip()
                        for c in open(classes_path).readlines() if c.strip()]

    def detect(self, img_path, min_prob=None):
        image, scale = preprocess_image(img_path)
        if not min_prob:
            min_prob = 0.6

        outputs = self.detection_model.run(
            [s_i.name for s_i in self.detection_model.get_outputs()],
            {self.detection_model.get_inputs(
            )[0].name: np.expand_dims(image, axis=0)},
        )

        labels = [op for op in outputs if op.dtype == "int32"][0]
        scores = [op for op in outputs if isinstance(op[0][0], np.float32)][0]
        boxes = [op for op in outputs if isinstance(op[0][0], np.ndarray)][0]

        boxes /= scale
        processed_boxes = []

        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            if score < min_prob:
                continue

            box = box.astype(int).tolist()
            label = self.classes[label]
            processed_boxes.append(
                {"box": [int(c) for c in box], "score": float(score), "label": label})

        img_name = os.path.splitext(os.path.basename(img_path))[0]

        with open("/Users/lornn/Desktop/Nudity Filter/Results/flagged_"+img_name+".json", "w", encoding="utf-8") as f:
            json.dump(processed_boxes, f, ensure_ascii=False, indent=4)

        print("NSFW areas flagged: ((" + str(len(processed_boxes)) + ")) for image: "+os.path.basename(img_path))

        return processed_boxes

    def censor_folder(self, folder_path, out_folder_path, parts_to_blur=[]):
        for img_filename in os.listdir(folder_path):
            path = os.path.join(folder_path, img_filename)
            
            img = cv2.imread(path)
 
            if img is not None:
                image = cv2.imread(path)

                if image is not None:
                    boxes = self.detect(path)
 
                    if len(boxes) > 0: 
                        if parts_to_blur:
                            boxes = [i["box"]
                                    for i in boxes if i["label"] in parts_to_blur]
                        else:
                            boxes = [i["box"] for i in boxes]

                        for box in boxes:
                            x, y = box[0], box[1]
                            w, h = box[2] - box[0], box[3] - box[1]

                            ROI = image[y:y+h, x:x+w]
                            blur = cv2.blur(ROI, (51, 51), 0)

                            image[y:y+h, x:x+w] = blur

                        if out_folder_path:
                            fp = out_folder_path + "blurred_" + img_filename
                            cv2.imwrite(fp, image)
                    else:
                        print("# Ignored censorsing image " + img_filename)


if __name__ == "__main__":
    f = Filter()

    # Scan each image in X folder to see if needs NSFW censoring (i.e. blurring) and export censored version into a results folder. For each image we also generate an exported classes JSON file
    f.censor_folder("/Users/lornn/Desktop/Nudity Filter/Test Images/", "/Users/lornn/Desktop/Nudity Filter/Results/")
