# # import the libs ##

import torch, os
import pandas as pd
from transformers import pipeline, BertForSequenceClassification, BertTokenizerFast
from torch.utils.data import Dataset
from torch import cuda
from transformers import TrainingArguments, Trainer

from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from tqdm import tqdm

# !pip install accelerate -U


def predict(text):
    """
    Predicts the class label for a given input text

    Args:
        text (str): The input text for which the class label needs to be predicted.

    Returns:
        probs (torch.Tensor): Class probabilities for the input text.
        pred_label_idx (torch.Tensor): The index of the predicted class label.
        pred_label (str): The predicted class label.
    """
    # Tokenize the input text and move tensors to the GPU if available
    inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt").to("cuda")

    # Get model output (logits)
    outputs = model(**inputs)

    probs = outputs[0].softmax(1)
    """ Explanation outputs: The BERT model returns a tuple containing the output logits (and possibly other elements depending on the model configuration). In this case, the output logits are the first element in the tuple, which is why we access it using outputs[0].

    outputs[0]: This is a tensor containing the raw output logits for each class. The shape of the tensor is (batch_size, num_classes) where batch_size is the number of input samples (in this case, 1, as we are predicting for a single input text) and num_classes is the number of target classes.

    softmax(1): The softmax function is applied along dimension 1 (the class dimension) to convert the raw logits into class probabilities. Softmax normalizes the logits so that they sum to 1, making them interpretable as probabilities. """

    # Get the index of the class with the highest probability
    # argmax() finds the index of the maximum value in the tensor along a specified dimension.
    # By default, if no dimension is specified, it returns the index of the maximum value in the flattened tensor.
    pred_label_idx = probs.argmax()

    # Now map the predicted class index to the actual class label
    # Since pred_label_idx is a tensor containing a single value (the predicted class index),
    # the .item() method is used to extract the value as a scalar
    pred_label = model.config.id2label[pred_label_idx.item()]

    return probs, pred_label_idx, pred_label



# # load the model from the local and do prediction ##
model_path = "/mnt/g/Users/Manish/Desktop/interview_prep/parspec/parspec_assignment/code/finetuned_model"

model = BertForSequenceClassification.from_pretrained(model_path).to('cpu')
tokenizer = BertTokenizerFast.from_pretrained(model_path)

text = """NORDIC LIGHTS® NORDIC LIGHTS Ltd. P.O. Box 36, Bennäsvägen 155 FI-68601 Jakobstad, FINLAND Tel. +358 20 1345 100 www.nordiclights.com BUMBLEBEE The Bumblebee headlight module delivers an even, streak-free light pattern that greatly improves the driver’s vision. This ECE-approved headlight module comes in high beam and low beam versions, specifically designed and optimized for heavy-duty vehicles. Thanks to the well-balanced color temperature, the driver will stay alert longer. The Bumblebee’s exceptional light output in combination with the long light range places it among the top of the currently available options on the market. Not all products are available in all markets. During continuous improvement specifications and design are changing. All values are nominal values. Illustrations do not necessarily show the design of every version and some features are version specific. The lumens output varies depending on lens colour. TECHNICAL DATA Colour Temperature 5800 K Nominal Voltage DC 12 V 24 V Input Voltage DC 9 - 32 V Power Consumption High Beam 18W, Low Beam 18W Nominal Current at High/Low Beam 1.5 A@12V, 0.75 A@24V Connector Built-in Deutsch DT-2 (2-pin) Mount 3 pcs M6 screw Shock 60G Vibration 6Grms 24-1000Hz Lens Glass Body / Housing Aluminum Weight 0.95 kg IP Rating IP68, IP6K9K Salt Spray Test ISO 9227 240H EMC CISPR 25 Class 5, ISO 13766, ISO 14982, ISO 7637-2, ISO 10605, ISO 11452, EN 61000-4-2, EN 13309 ECE Approvals High Beam: ECE R149, Low Beam RHT: ECE R149, Low Beam LHT: ECE R149, Low Beam Symmetric: ECE R149 Operating Temperatures -40°C... +85°C (Full Power -40°C... +50°C) Electronics Isolated Part Numbers High Beam: 960-432B (ECE R149), Low Beam Symmetric: 960-434B (ECE R149), Low Beam LHT: 960-435B (ECE NORDIC LIGHTS® NORDIC LIGHTS Ltd. P.O. Box 36, Bennäsvägen 155 FI-68601 Jakobstad, FINLAND Tel. +358 20 1345 100 www.nordiclights.com R149), Low Beam RHT: 960-433B (ECE R149) NORDIC LIGHTS® NORDIC LIGHTS Ltd. P.O. Box 36, Bennäsvägen 155 FI-68601 Jakobstad, FINLAND Tel. +358 20 1345 100 www.nordiclights.com CONNECTORS Built-in Deutsch DT-2 (2-pin) KEY FEATURES ECE-approved module Easily adapted to your custom design Light pattern optimized for heavy-duty vehicles LIGHT PATTERNS DRAWINGS NORDIC LIGHTS® NORDIC LIGHTS Ltd. P.O. Box 36, Bennäsvägen 155 FI-68601 Jakobstad, FINLAND Tel. +358 20 1345 100 www.nordiclights.com NORDIC LIGHTS® NORDIC LIGHTS Ltd. P.O. Box 36, Bennäsvägen 155 FI-68601 Jakobstad, FINLAND Tel. +358 20 1345 100 www.nordiclights.com """

print(predict(text))
