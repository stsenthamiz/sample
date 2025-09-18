import cv2
import numpy as np
import os

def process_image(img_path, model):
    img = cv2.imread(img_path)
    orig = img.copy()

    # Draw sample trait lines (replace with real logic if needed)
    height, width = img.shape[:2]
    cv2.line(img, (0,0), (width,height), (0,255,0), 3)
    cv2.line(img, (0,height//2), (width,height//2), (255,0,0), 3)
    cv2.line(img, (width//2,0), (width//2,height), (0,0,255), 3)

    # Model prediction
    img_rgb = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (224,224))
    img_array = np.expand_dims(img_resized/255.0, axis=0)
    pred = model.predict(img_array)
    pred_class = np.argmax(pred, axis=1)[0]
    class_map = {0: "Buffalo Type A", 1: "Buffalo Type B"}
    result = class_map.get(pred_class, "Unknown")

    # Save processed image
    processed_file_name = 'processed_' + os.path.basename(img_path)
    processed_file_path = os.path.join('static/uploads', processed_file_name)
    cv2.imwrite(processed_file_path, img)

    return processed_file_path, result