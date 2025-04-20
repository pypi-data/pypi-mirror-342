#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.signal import convolve2d


# In[3]:


def motion_blur(image, kernel_size, angle):
    """Applies motion blur to an image.

    Args:
        image (numpy.ndarray): The input image.
        kernel_size (int): The size of the motion blur kernel.
        angle (float): The angle of the motion blur in degrees.

    Returns:
        numpy.ndarray: The blurred image.
    """
    # Create the motion blur kernel
    kernel = np.zeros((kernel_size, kernel_size))
    kernel[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)

    # Rotate the kernel to the specified angle
    rotation_matrix = cv2.getRotationMatrix2D(
        (kernel_size / 2 - 0.5, kernel_size / 2 - 0.5), angle, 1.0
    )
    kernel = cv2.warpAffine(kernel, rotation_matrix, (kernel_size, kernel_size))

    # Normalize the kernel
    kernel = kernel / np.sum(kernel)

    # Apply the blur using convolution
    blurred = convolve2d(image, kernel, mode='same', boundary='wrap')

    return blurred


def inverse_filter(blurred_image, kernel, eps=1e-6):
    """Applies inverse filtering to deblur an image.

    Args:
        blurred_image (numpy.ndarray): The blurred image.
        kernel (numpy.ndarray): The blur kernel.
        eps (float, optional): A small value to avoid division by zero. Defaults to 1e-6.

    Returns:
        numpy.ndarray: The deblurred image.
    """
    # Perform Fourier Transform on the blurred image and kernel
    blurred_fft = np.fft.fft2(blurred_image)
    kernel_fft = np.fft.fft2(kernel, s=blurred_image.shape)

    # Apply inverse filtering in the frequency domain
    deblurred_fft = blurred_fft / (kernel_fft + eps)

    # Perform Inverse Fourier Transform to get the deblurred image
    deblurred_image = np.fft.ifft2(deblurred_fft).real

    return deblurred_image


def wiener_filter(blurred_image, kernel, k=0.01):
    """Applies Wiener filtering to deblur an image.

    Args:
        blurred_image (numpy.ndarray): The blurred image.
        kernel (numpy.ndarray): The blur kernel.
        k (float, optional): The noise-to-signal ratio. Defaults to 0.01.

    Returns:
        numpy.ndarray: The deblurred image.
    """
    # Perform Fourier Transform on the blurred image and kernel
    blurred_fft = np.fft.fft2(blurred_image)
    kernel_fft = np.fft.fft2(kernel, s=blurred_image.shape)

    # Calculate the Wiener filter
    kernel_fft_conj = np.conj(kernel_fft)  # Complex conjugate of the kernel
    wiener_filter = kernel_fft_conj / (np.abs(kernel_fft)**2 + k)

    # Apply the Wiener filter in the frequency domain
    deblurred_fft = wiener_filter * blurred_fft

    # Perform Inverse Fourier Transform to get the deblurred image
    deblurred_image = np.fft.ifft2(deblurred_fft).real

    return deblurred_image


# Load image and apply motion blur
img = cv2.imread('../images/helmet.jpg', cv2.IMREAD_GRAYSCALE)
kernel_size = 21
angle = 11
blurred = motion_blur(img, kernel_size, angle)

# Create blur kernel
kernel = np.zeros((kernel_size, kernel_size))
kernel[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
kernel = cv2.warpAffine(kernel, cv2.getRotationMatrix2D((kernel_size / 2 -
0.5, kernel_size / 2 - 0.5), angle, 1.0), (kernel_size, kernel_size))
kernel = kernel / np.sum(kernel)

# Deblur using inverse filtering
deblurred_inverse = inverse_filter(blurred, kernel, 0.01)

# Deblur using Wiener filtering
deblurred_wiener = wiener_filter(blurred, kernel, 0.01)

# Display results
plt.figure(figsize=(12, 6))
plt.subplot(131),
plt.imshow(img, cmap='gray'),
plt.title('Original Image')
plt.subplot(132), plt.imshow(blurred, cmap='gray'),
plt.title('Blurred Image')
plt.subplot(133),
plt.imshow(deblurred_inverse, cmap='gray'),
plt.title('Inverse Filtered')
plt.show()

plt.figure(figsize=(12, 6))
plt.subplot(131),
plt.imshow(img, cmap='gray'),
plt.title('Original Image')
plt.subplot(132),
plt.imshow(blurred, cmap='gray'),
plt.title('Blurred Image')
plt.subplot(133),
plt.imshow(deblurred_wiener, cmap='gray'),
plt.title('Wiener Filtered')
plt.show()

