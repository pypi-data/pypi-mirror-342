
import torchvision.models as models
from torch import nn
import torch
from torchvision.models import vgg19
# Define VGG Loss
class VGGLoss(nn.Module):
    def __init__(self, weights_path=None,device =None):
        super().__init__()
        self.vgg = models.vgg19(pretrained=False).features[:35].eval().to(device)
        if weights_path:
            pretrained_weights = torch.load(weights_path)
            self.vgg.load_state_dict(pretrained_weights, strict=False)
        self.vgg[0] = nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1).to(device)
        for param in self.vgg.parameters():
            param.requires_grad = False
        self.loss = nn.MSELoss()
    def forward(self, input, target):
        input_features = self.vgg(input)
        target_features = self.vgg(target)
        return self.loss(input_features, target_features)
"""
vgg_loss = VGGLoss(weights_path="/mnt/wtx_weather_forecast/scx/stat/sat/sat2radar/vgg19-dcbb9e9d.pth").to(device)
""" 
 
import torch
import torch.nn as nn
import torch.nn.functional as F
from segment_anything import sam_model_registry

class SAMLoss(nn.Module):
    def __init__(self, model_type='vit_b', checkpoint_path=None, input_size=1024):
        """
        SAM-based perceptual loss with resolution handling
        
        Args:
            model_type (str): SAM model type (vit_b, vit_l, vit_h)
            checkpoint_path (str): Path to SAM checkpoint weights
            input_size (int): Target input size for SAM (default 1024)
        """
        super().__init__()
        self.input_size = input_size        
        # Initialize SAM model
        self.sam = sam_model_registry[model_type](checkpoint=None)        
        # Load pretrained weights if provided
        if checkpoint_path:
            state_dict = torch.load(checkpoint_path)
            self.sam.load_state_dict(state_dict)        
        # Use image encoder only and freeze parameters
        self.image_encoder = self.sam.image_encoder.eval()
        for param in self.image_encoder.parameters():
            param.requires_grad = False            
        # Define loss function
        self.loss = nn.MSELoss()        
        # Normalization parameters
        self.register_buffer('mean', torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1))
        self.register_buffer('std', torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1))
        
    def preprocess(self, x):
        """
        Preprocess input to match SAM requirements:
        1. Convert to 3-channel if needed
        2. Normalize using ImageNet stats
        3. Resize to target size
        """
        if x.shape[1] == 1:
            x = x.expand(-1, 3, -1, -1)  # More memory efficient than repeat        
        # Normalize
        x = (x - self.mean) / self.std        
        # Resize
        if x.shape[-2:] != (self.input_size, self.input_size):
            x = F.interpolate(x, size=(self.input_size, self.input_size), 
                             mode='bilinear', align_corners=False)        
        return x        
    def forward(self, input, target):
        # Preprocess
        input = self.preprocess(input)
        target = self.preprocess(target)        
        # Process in batches if needed
        batch_size = 4  # Adjust based on your GPU memory
        input_features = []
        target_features = []        
        with torch.no_grad():
            for i in range(0, input.size(0), batch_size):
                input_batch = input[i:i+batch_size]
                target_batch = target[i:i+batch_size]                
                input_features.append(self.image_encoder(input_batch))
                target_features.append(self.image_encoder(target_batch))        
        return self.loss(torch.cat(input_features), torch.cat(target_features))

