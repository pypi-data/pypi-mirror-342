#!/usr/bin/env python
# coding: utf-8

# # Practical 2A

# In[1]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import data


# # Practical 2B

# In[7]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import data
# Load a sample image (e.g., coins)
coins_image = data.coins()
# Convert the image from scikit-image to an OpenCV format
# The original code converted to BGR, causing the error
# Instead, keep it as grayscale for DCT
coins_image_cv2 = coins_image


# In[8]:


dct_image = cv2.dct(np.float32(coins_image_cv2))
 # Apply Inverse DCT (optional, for reconstruction)
idct_image = cv2.idct(dct_image)
 # Plotting the original, DCT, and IDCT (reconstructed) images
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.title('Original Image')

plt.imshow((coins_image_cv2), cmap='gray') # Original image is grayscale
plt.axis('off')
plt.subplot(1, 3, 2)
plt.title('DCT Image')
plt.imshow(np.log(abs(dct_image) + 1), cmap='gray') # Log scale for better visibility
plt.axis('off')
plt.subplot(1, 3, 3)
plt.title('Reconstructed Image')
plt.imshow(idct_image, cmap='gray') # Reconstructed image is grayscale
plt.axis('off')
plt.show()


# In[9]:


im = cv2.imread('../images/nobita.jpg', cv2.IMREAD_GRAYSCALE) # Read as grayscale
im = im.astype(np.float64) # Convert to double precision (like MATLAB's double)
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.imshow(im, cmap='gray')
plt.title('Original')
plt.axis('off')

# Apply DCT (Discrete Cosine Transform) - Using OpenCV
dct_image = cv2.dct(np.float32(im))
plt.subplot(1, 3, 2)
plt.imshow(np.log(abs(dct_image) + 1), cmap='gray') # Log scale for better visibility
plt.title('DCT Transform')
plt.axis('off')

# Apply DCT again to the DCT result
dct_dct_image = cv2.dct(np.float32(dct_image))
plt.subplot(1, 3, 3)
plt.imshow(dct_dct_image, cmap='gray') # You might need to adjust scaling here
plt.title('DCT(DCT) Transform')
plt.axis('off')
plt.show()


# In[6]:


# arthimetic Operations on Images
nobita = cv2.imread('../images/nobita.jpg')
helmet = cv2.imread('../images/helmet.jpg')
# Resize helmet to match nobita's dimensions
helmet_resized = cv2.resize(helmet, (nobita.shape[1], nobita.shape[0]))
# Perform arithmetic operations 
added_image = cv2.add(nobita, helmet_resized)
subtracted_image = cv2.subtract(nobita, helmet_resized)
multiplied_image = cv2.multiply(nobita, helmet_resized)
divided_image = cv2.divide(nobita, 2)
# Create a figure and subplots (adjust figsize if needed)
fig, axes = plt.subplots(3, 3, figsize=(15, 15))
# --- Display images in subplots ---
# Original Images
axes[0, 0].imshow(cv2.cvtColor(nobita, cv2.COLOR_BGR2RGB))
axes[0, 0].set_title(f'Original Image 1({nobita.shape[1]}x{nobita.shape[0]})') # Add size to title
axes[0, 0].axis('off')

axes[0, 1].imshow(cv2.cvtColor(helmet_resized, cv2.COLOR_BGR2RGB))
axes[0, 1].set_title(f"Original Image 2({helmet_resized.shape[1]}x{helmet_resized.shape[0]})")
axes[0, 1].axis('off')  

axes[0, 2].axis('off') # Empty subplot for better layout

axes[1, 0].imshow(cv2.cvtColor(added_image, cv2.COLOR_BGR2RGB))
axes[1, 0].set_title(f'Added Image ({added_image.shape[1]}x{added_image.shape[0]})') # Add size to title
axes[1, 0].axis('off')


axes[1, 1].imshow(cv2.cvtColor(subtracted_image, cv2.COLOR_BGR2RGB))
axes[1, 1].set_title(f'Subtracted Image({subtracted_image.shape[1]}x{subtracted_image.shape[0]})') # Add size totitle
axes[1, 1].axis('off')
axes[1, 2].axis('off') # Empty subplot for better layout

axes[2, 0].imshow(cv2.cvtColor(multiplied_image, cv2.COLOR_BGR2RGB))
axes[2, 0].set_title(f'Multiplied Image (x0.5)({multiplied_image.shape[1]}x{multiplied_image.shape[0]})') # Add size totitle
axes[2, 0].axis('off')

axes[2, 1].imshow(cv2.cvtColor(divided_image, cv2.COLOR_BGR2RGB))
axes[2, 1].set_title(f'Divided Image (/2) ({divided_image.shape[1]}x{divided_image.shape[0]})') # Add size to title
axes[2, 1].axis('off')
axes[2, 2].axis('off')
plt.tight_layout()
plt.show()

