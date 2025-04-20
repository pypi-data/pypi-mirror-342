import os
import cv2
import supervision as sv
from skimage.io import imread
from PIL import Image
from skimage.measure import label
from tqdm import tqdm
import numpy as np
from utils import get_base_dir
from utils import SAM2_Model, MOLMO_Model, run_molmo_inference, extract_point_coordinates_from_molmo_response

def five_points(xy):
    leftmost = xy[np.argmin(xy[:, 0])] # Point le plus à gauche (max en y)
    rightmost = xy[np.argmax(xy[:, 0])] # Point le plus à droite (max en x)
    bottommost = xy[np.argmin(xy[:, 1])] # Point le plus bas (min en y)
    topmost = xy[np.argmax(xy[:, 1])] # Point le plus haut (max en y)
    extremes = np.array([leftmost, rightmost, bottommost, topmost])
    return extremes

TEXT = "detect tree foliage in center and give me all points coordinates"
def codes(rgb_data):
    image_pil = Image.fromarray(rgb_data)
    molmo_model, molmo_processor = MOLMO_Model()
    sam2_model = SAM2_Model()
    #Molmo

    molmo_response = run_molmo_inference(
        model=molmo_model,
        processor=molmo_processor,
        image=image_pil,
        text=TEXT
    )
    xy = extract_point_coordinates_from_molmo_response(molmo_response)
    if len(xy)==0:
      print('No tree detected')
    else:
      xy = xy * np.array(image_pil.size) / 100
      key_points = sv.KeyPoints(xy=xy[np.newaxis, ...])
      sv.VertexAnnotator(color=sv.Color.RED, radius=10).annotate(image_pil.copy(), key_points)

    #SAM2
    sam2_model.set_image(cv2.cvtColor(rgb_data, cv2.COLOR_BGR2RGB))
    detections_list = []
    point_coords_set = five_points(xy)
    point_labels_set = np.array([1]*len(point_coords_set))
    masks, scores, logits = sam2_model.predict(
            point_coords=point_coords_set,
            point_labels=point_labels_set,
            multimask_output=False,
        )
    detections = sv.Detections(
            xyxy=sv.mask_to_xyxy(masks=masks),
            mask=masks.astype(bool)
        )
    detections_list.append(detections)

    detections = sv.Detections.merge(detections_list=detections_list)

    if detections.mask is None:
      instance_mask = np.zeros((rgb_data.shape[0],rgb_data.shape[1]),dtype='uint8')
    else:
      mask_tensor = detections.mask.astype('uint8')
      n,height,width = mask_tensor.shape
      instance_mask = np.zeros((height,width),dtype='uint8')
      for i in range(n):
        instance_mask[:,:] = np.where(mask_tensor[i,:,:]!=0,i+1,instance_mask[:,:])

    # img = Image.fromarray(instance_mask)
    # img.save(os.path.join(output_path,os.path.basename(A[ik])))
    return instance_mask
image = imread(r'C:\Users\KiloO\Downloads\MOLMO+SAM2-20250419T065201Z-001\To_share_for_analysis-SUMMER\flower_samdal_B2_T4.JPG')
output_msk = codes(image)
img = Image.fromarray(output_msk)
img.save(os.path.join(r'C:\Users\KiloO\appletree\src\appletree','output.png'))
