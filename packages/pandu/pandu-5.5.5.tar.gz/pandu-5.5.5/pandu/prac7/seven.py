#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Applications of Morphological Operations on image
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('blobs.png', cv2.IMREAD_GRAYSCALE)

# Check if image loading was successful
if image is None:
    print("Error: Could not load image. Please check the file path and ensure the image exists.")
    exit() # or handle the error appropriately

# Create a structuring element
kernel = np.ones((5,5), np.uint8)

# Perform erosion
erosion = cv2.erode(image, kernel, iterations = 1)

# Perform dilation
dilation = cv2.dilate(image, kernel, iterations = 1)

# Perform opening
opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# Perform closing
closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

# Display the results in subplots
plt.figure(figsize=(12, 8))

plt.subplot(2, 3, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')

plt.subplot(2, 3, 2)
plt.imshow(erosion, cmap='gray')
plt.title('Erosion')

plt.subplot(2, 3, 3)
plt.imshow(dilation, cmap='gray')
plt.title('Dilation')

plt.subplot(2, 3, 4)
plt.imshow(opening, cmap='gray')
plt.title('Opening')
plt.subplot(2, 3, 5)
plt.imshow(closing, cmap='gray')
plt.title('Closing')
plt.tight_layout()
plt.show()

