#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import matplotlib.pyplot as plt
from skimage import img_as_uint
from skimage.io import imread, imshow
from skimage.color import rgb2hsv
from skimage.color import rgb2gray


# #### Creating Array 1

# In[6]:


array_1 = np.array([[255,0], [0,255]])
plt.imshow(array_1, cmap='gray')
plt.show()


# #### Creating Array 2

# In[7]:


array_2 = np.array([[255,0,255], [0,255,0], [255,0,255]])
plt.imshow(array_2, cmap='gray')    
plt.show()


# #### Creating a Array Spectrum

# In[17]:


array_spectrum = np.array([np.arange(0,255,17), np.arange(255,0,-17), np.arange(0,255,17), np.arange(255,0,-17)])
fig, ax = plt.subplots(1,2, figsize=(12,4))
ax[0].imshow(array_spectrum, cmap='gray')
ax[0].set_title('Arange Generation')
ax[1].imshow(array_spectrum.T, cmap='gray')
ax[1].set_title('Transpose Generation')


# #### Creating a RGB Array

# In[66]:


array_colors = np.array([[[255,0,0], [0,255,0], [0,0,255]]])
plt.imshow(array_colors, cmap='gray')
plt.show()


# #### Manipulating Actual Image

# In[20]:


image  = imread('../images/nobita.jpg')
plt.imshow(image)
print(image.shape)
plt.show()  


# #### Slice the image matix and represent each section as image

# In[43]:


fig, ax = plt.subplots(1,3, figsize=(8,4),sharey=True)
ax[0].imshow(image[:,0:600])
ax[0].set_title('First Split')

ax[1].imshow(image[:,130:275], cmap='gray')
ax[1].set_title('Second Split') 

ax[2].imshow(image[:,360:390], cmap='gray')
ax[2].set_title('Third Split')

plt.imshow(image[90:250, 130:275])
plt.show()


# #### Representaion of the images's Red, Green & Blue Components

# In[46]:


fig, ax = plt.subplots(1,3, figsize=(12,4),sharey=True)
ax[0].imshow(image[:,:,0],cmap='Reds')
ax[0].set_title('Red Channel')

ax[1].imshow(image[:,:,1],cmap='Greens')
ax[1].set_title('Green Channel')

ax[2].imshow(image[:,:,2],cmap='Blues')
ax[2].set_title('Blue Channel')
plt.show()


# #### Convert the image from RGB to HSV

# In[51]:


image_hsv = rgb2hsv(image)
fig, ax = plt.subplots(1,3, figsize=(12,4),sharey=True)

ax[0].imshow(image_hsv[:,:,1],cmap='hsv')
ax[0].set_title('Hue Channel')

ax[1].imshow(image_hsv[:,:,1],cmap='gray')
ax[1].set_title('Saturation Channel')

ax[2].imshow(image_hsv[:,:,2],cmap='gray')
ax[2].set_title('Value Channel')
plt.show()


# #### Convert Image Matrix to Grayscale

# In[53]:


image_gray = rgb2gray(image)
fig, ax = plt.subplots(1,5, figsize=(17,6),sharey=True)

ax[0].imshow(image_gray, cmap='gray')
ax[0].set_title('Grayscale Original')

ax[1].imshow(img_as_uint(image_gray > 0.25), cmap='gray')
ax[1].set_title('Greater than 0.25')

ax[2].imshow(img_as_uint(image_gray > 0.50), cmap='gray')
ax[2].set_title('Greater than 0.50')

ax[3].imshow(img_as_uint(image_gray > 0.75), cmap='gray')
ax[3].set_title('Greater than 0.75')

ax[4].imshow(img_as_uint(image_gray > np.mean(image_gray)), cmap='gray')
ax[4].set_title('Greater than Mean')


# ## Practical 1B

# ### Reducing Quantization Values

# In[54]:


# Create a sample image
img = np.random.rand(256, 256)

# Reduce the quantization values to 2 bits (4 levels)
reduced_img_2bits = np.round(img * 3) / 3

# Reduce the quantization values to 1 bit (2 levels)
reduced_img_1bit = np.round(img) 


# In[55]:


plt.subplot(1, 3, 1)
plt.imshow(img, cmap='gray')
plt.title('Original Image')

plt.subplot(1, 3, 2)
plt.imshow(reduced_img_2bits, cmap='gray')
plt.title('2 bits (4 levels)')

plt.subplot(1, 3, 3)
plt.imshow(reduced_img_1bit, cmap='gray')
plt.title('1 bit (2 levels)')
plt.show()


# #### Reducing the Number of Samples

# In[56]:


# Create a sample image
img = np.random.rand(256, 256)
# Reduce the number of samples to half
reduced_img_half = img[::2, ::2]
# Reduce the number of samples to quarter
reduced_img_quarter = img[::4, ::4] 


# In[ ]:





# In[57]:


plt.subplot(1, 3, 1)
plt.imshow(img, cmap='gray')
plt.title('Original Image')

plt.subplot(1, 3, 2)
plt.imshow(reduced_img_half, cmap='gray')
plt.title('Half Resolution')

plt.subplot(1, 3, 3)
plt.imshow(reduced_img_quarter, cmap='gray')
plt.title('Quarter Resolution')
plt.show()


# #### Reducing Both Quantization Values and Number of Samples:

# In[58]:


img = np.random.rand(256, 256)
# Reduce the quantization values to 2 bits (4 levels) and number of samples to half
reduced_img_2bits_half = np.round(img[::2, ::2] * 3) / 3
# Reduce the quantization values to 1 bit (2 levels) and number of samples to quarter
reduced_img_1bit_quarter = np.round(img[::4, ::4]) 


# In[63]:


# Display the images

plt.subplot(1, 3, 1)
plt.imshow(img, cmap='gray')
plt.title('Original Image')

plt.subplot(1, 3, 2)
plt.imshow(reduced_img_2bits_half, cmap='gray')
plt.title('2 bits (4 levels), Half Resolution')

plt.subplot(1, 3, 3)
plt.imshow(reduced_img_1bit_quarter, cmap='gray')
plt.title('1 bit (2 levels), Quarter Resolution')
plt.show()

