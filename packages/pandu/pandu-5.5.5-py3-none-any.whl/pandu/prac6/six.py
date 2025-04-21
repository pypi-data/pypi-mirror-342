#!/usr/bin/env python
# coding: utf-8

# In[6]:


#Edge detection using Sobel, Prewitt, Canny, and Laplacian operators.
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read and convert the image to grayscale
image = cv2.imread('../images/nobita2.jpg', cv2.IMREAD_GRAYSCALE)

# Sobel operator (Horizontal and Vertical)
sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)  # Horizontal
sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)  # Vertical

# Prewitt operator (Horizontal and Vertical)
kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
prewitt_x = cv2.filter2D(image, -1, kernel_x)  # Horizontal
prewitt_y = cv2.filter2D(image, -1, kernel_y)  # Vertical

# Canny operator
canny_edges = cv2.Canny(image, 100, 200)

# Laplacian operator
laplacian = cv2.Laplacian(image, cv2.CV_64F)

# Display results
titles = ['Original', 'Sobel X', 'Sobel Y', 'Prewitt X', 'Prewitt Y',
'Canny', 'Laplacian']
images = [image, sobel_x, sobel_y, prewitt_x, prewitt_y, canny_edges,
laplacian]

plt.figure(figsize=(15, 10))
for i in range(len(images)):
    plt.subplot(3, 3, i + 1)
    plt.imshow(images[i], cmap='gray')
    plt.title(titles[i])
    plt.axis('off')

plt.tight_layout()
plt.show()

