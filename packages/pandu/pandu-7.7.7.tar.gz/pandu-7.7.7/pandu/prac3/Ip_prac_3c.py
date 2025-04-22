#3c.Smoothing and Sharpening Filters
#Apply and display the results of mean, Gaussian, and median filters on the image.

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image with error handling
try:
    image = cv2.imread('../images/helmet.jpg', cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image file 'ghost.png' not found.") # Changed 'camera.jpg' to 'ghost.png'
except FileNotFoundError:
    print("Image file not found.")  # Handle the exception

# 1. Mean Filter
kernel_size = (5, 5)
mean_filtered = cv2.blur(image, kernel_size)

# 2. Gaussian Filter
gaussian_filtered = cv2.GaussianBlur(image, kernel_size, 0)

# 3. Median Filter
median_kernel_size = 5	# Must be odd
median_filtered = cv2.medianBlur(image, median_kernel_size)

# Display Results
plt.figure(figsize=(15, 5))

plt.subplot(1, 4, 1)
plt.imshow(image, cmap='gray')
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 4, 2)
plt.imshow(mean_filtered, cmap='gray')
plt.title("Mean Filtered")
plt.axis('off')

plt.subplot(1, 4, 3)
plt.imshow(gaussian_filtered, cmap='gray')
plt.title("Gaussian Filtered")
plt.axis('off')

plt.subplot(1, 4, 4)
plt.imshow(median_filtered, cmap='gray')
plt.title("Median Filtered")
plt.axis('off')

plt.tight_layout()
plt.show()


# In[5]:


#Sharpening (HIGH PASS FIlters) Filters:
#Using the Laplacian operator and using a kernel to emphasize high frequencies.
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image with error handling
try:
    image = cv2.imread('../images/helmet.jpg', cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image file 'lena.jpg' not found.")
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

# --- Spatial High-Pass Filters ---
# 1. Laplacian Filter
laplacian_filtered = cv2.Laplacian(image, cv2.CV_64F)
laplacian_filtered = np.uint8(np.absolute(laplacian_filtered))
# Convert to uint8
# 2. High-Pass Kernel Filter
kernel = np.array([[-1, -1, -1],
                   [-1, 8, -1],
                   [-1, -1, -1]])
high_pass_filtered = cv2.filter2D(image, -1, kernel)


# --- Display Results ---
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(image, cmap='gray')
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(laplacian_filtered, cmap='gray')
plt.title("Laplacian Filtered")
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(high_pass_filtered, cmap='gray')
plt.title("High-Pass Kernel Filtered")
plt.axis('off')

plt.tight_layout()
plt.show()

