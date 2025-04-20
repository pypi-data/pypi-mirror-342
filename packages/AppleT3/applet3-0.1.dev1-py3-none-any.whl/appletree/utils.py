import os.path

# CONF = config.get_conf_dict()
homedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# base_dir = CONF['general']['base_directory']
base_dir = "."

def get_base_dir():
    return os.path.abspath(os.path.join(homedir, base_dir))

import re
import numpy as np
import xml.etree.ElementTree as ET

def run_molmo_inference(model, processor, image, text):
    inputs = processor.process(
        images=[image],
        text=text
    )

    inputs = {k: v.to(model.device).unsqueeze(0) for k, v in inputs.items()}

    output = model.generate_from_batch(
        inputs,
        GenerationConfig(max_new_tokens=1024, stop_strings="<|endoftext|>"),
        tokenizer=processor.tokenizer
    )

    generated_tokens = output[0, inputs['input_ids'].size(1):]
    generated_text = processor.tokenizer.decode(generated_tokens, skip_special_tokens=True)

    return generated_text


def extract_point_coordinates_from_molmo_response(text):
    pattern = r'x(\d+)\s*=\s*"([\d.]+)"\s*y(\d+)\s*=\s*"([\d.]+)"'
    matches = re.findall(pattern, text)
    print(text)
    coordinates = [(float(x), float(y)) for _, x, _, y in matches]
    return np.array(coordinates)

# molmo_response = ' <points x1=”93.5″ y1=”29.8″ x2=”93.5″ y2=”38.1″ x3=”93.5″ y3=”45.4″ x4=”93.5″ y4=”53.1″ x5=”93.5″ alt=”person”>person</points>'
# molmo_response =  ' <point x="51.0" y="78.6" alt="tree">tree</point>'
def extract_point_coordinates_from_molmo_response(text):
  assert type(text)==str
  I = text.split(' ')
  X_ = []
  Y_ = []
  dico_X_ = {}
  dico_Y_ = {}
  for i_ in I:
    if 'x' in i_:
      val_ = i_.split('=')
      # print(val_)
      if len(val_[0])==1:
        key_ = 1
      else:
        key_ = int(val_[0].replace('x',''))
      dat_ = float(val_[1].strip("'").strip('"').replace('”','').replace('″','').replace(',','.'))
      X_.append([key_,dat_])
      dico_X_[key_] = dat_
    if 'y' in i_:
      val_ = i_.split('=')
      if len(val_[0])==1:
        key_ = 1
      else:
        key_ = int(val_[0].replace('y',''))

      dat_ = float(val_[1].strip("'").strip('"').replace('”','').replace('″','').replace(',','.'))
      Y_.append([key_,dat_])
      dico_Y_[key_] = dat_

  dico_X_ = dict(sorted(dico_X_.items()))
  dico_Y_ = dict(sorted(dico_Y_.items()))

  common_key = []
  for ix,iy in zip(dico_X_,dico_Y_):
    common_key.append(ix)

  coordinates = [(float(dico_X_[key_i]), float(dico_Y_[key_i])) for key_i in common_key]
  return np.array(coordinates)


def check_file():
    appletree_pth = os.path.join(get_base_dir(),"appletree")
    A = [ix for ix in os.listdir(appletree_pth) if ix.endswith(".pt")]
    if 'sam2.1_hiera_base_plus.pt' in A:
        pass
    else:
        import requests
        sam2p1_hq_hiera_l_url="https://huggingface.co/facebook/sam2.1-hiera-base-plus/blob/3bade67c3413cf3227203293b1ec3e530e45d48b/sam2.1_hiera_base_plus.pt"
        save_path = os.path.join(get_base_dir(),"appletree","sam2.1_hiera_base_plus.pt")
        response = requests.get(sam2p1_hq_hiera_l_url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Download completed successfully.")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")

import torch

from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
SAM2_CHECKPOINT = os.path.join(get_base_dir(),"appletree","sam2.1_hiera_base_plus.pt")

print('SAM2_CHECKPOINT',DEVICE)
if not os.path.exists(SAM2_CHECKPOINT):
    check_file()
    # raise FileNotFoundError(f"Checkpoint file not found: {SAM2_CHECKPOINT}")

SAM2_CONFIG = os.path.join(get_base_dir(),"appletree","sam2.1_hiera_b+.yaml")
sam2_model = build_sam2(
    config_file=SAM2_CONFIG,
    ckpt_path=SAM2_CHECKPOINT,
    device=DEVICE,
    apply_postprocessing=False
)
def SAM2_Model():
    return SAM2ImagePredictor(sam2_model)

from transformers import AutoModelForCausalLM, AutoProcessor, GenerationConfig

MOLMO_CHECKPOINT = 'allenai/Molmo-7B-D-0924'
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(DEVICE)
molmo_processor = AutoProcessor.from_pretrained(
    MOLMO_CHECKPOINT,
    trust_remote_code=True,
    torch_dtype='auto',
    device_map=DEVICE
)
molmo_model =  AutoModelForCausalLM.from_pretrained(
    MOLMO_CHECKPOINT,
    trust_remote_code=True,
    torch_dtype='auto',
    device_map=DEVICE
)
def MOLMO_Model():
    return molmo_model, molmo_processor
