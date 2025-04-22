#Aim :  a. Basic Intensity Transformation on images.  b. Histogram Processing

# In[1]:


#1.	Linear (negative transformations)
import cv2
import matplotlib.pyplot as plt


# In[ ]:


# Load the original image
original_image = cv2.imread("../images/helmet.jpg")
# Replace with your image file # Check if the image was loaded successfully
# Perform the negative transformation
negative_image = 256 - 1 - original_image


# In[5]:


# Display the original and negative images side by side
plt.figure(figsize=(10, 5))
# Create a figure with a specified size
plt.subplot(1, 2, 1)
# Subplot for the original image
plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off')	# Turn off axis labels

plt.subplot(1, 2, 2)
# Subplot for the negative image
plt.imshow(cv2.cvtColor(negative_image, cv2.COLOR_BGR2RGB))
plt.title("Negative Image")
plt.axis('off')

plt.show()
# Show the figure with both images


# In[7]:


#2.	Log Transformation (Logarithm Function)&Inverse-Log Transformation (Exponential Function)
import cv2
import numpy as np

# Load an image
image = cv2.imread('../images/nobita2.jpg', cv2.IMREAD_GRAYSCALE) # Log Transformation
c = 45
log_transformed = c * (np.log(image + 1))

# Convert to 8-bit unsigned integer format
log_transformed = np.uint8(log_transformed)

# Inverse-Log Transformation
inverse_log_transformed = c * (np.exp(log_transformed / c) - 1)

# Convert to 8-bit unsigned integer format
inverse_log_transformed = np.uint8(inverse_log_transformed)
 # Display the original and negative images side by side
plt.figure(figsize=(10, 5))
# Create a figure with a specified size
plt.subplot(1, 3, 1)
# Subplot for the original image
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off')
# Turn off axis labels
plt.subplot(1, 3, 2)
plt.imshow(cv2.cvtColor(log_transformed, cv2.COLOR_BGR2RGB))
plt.title("log_transformed")
plt.axis('off')
plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(inverse_log_transformed, cv2.COLOR_BGR2RGB))
plt.title("inverse_log_transformed")
plt.axis('off')
plt.show()



# In[9]:


#POWER LAW TRANSFORMATIONS
import cv2
import numpy as np
import matplotlib.pyplot as plt  # Import matplotlib

# Read an image
image = cv2.imread('../images/nobita2.jpg', cv2.IMREAD_GRAYSCALE)

# Apply gamma correction (e.g., gamma = 1.5) gamma = 2
gamma = 2  # Define gamma
gamma2 = 4
adjusted_image = np.power(image / 255.0, gamma) * 255.0
adjusted_image = adjusted_image.astype(np.uint8)
adjusted_image2 = np.power(image / 255.0, gamma2) * 255.0
adjusted_image2 = adjusted_image2.astype(np.uint8)

plt.figure(figsize=(10, 5))
plt.subplot(1, 3, 2)
plt.imshow(cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB))  # Convert to RGB for display
plt.title("adjusted_image gamma =2")

plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # Convert to RGB for display
plt.title("Original Image")

plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(adjusted_image2, cv2.COLOR_BGR2RGB))  # Convert to RGB for display
plt.title("Original Image gamma = 4")
plt.axis('off')

plt.show()  # Add plt.show() to display the plot


# In[10]:


#CONSTRAST STRETCHING
import cv2
import numpy as np
import matplotlib.pyplot as plt
# Function to map each intensity level to output intensity level.
def pixelVal(pix, r1, s1, r2, s2):
  if (0 <= pix and pix <= r1):
    return (s1 / r1)*pix
  elif (r1 < pix and pix <= r2):
    return ((s2 - s1)/(r2 - r1)) * (pix - r1) + s1
  else:
      return ((255 - s2)/(255 - r2)) * (pix - r2) + s2
# Open the image.
img = cv2.imread('../images/nobita2.jpg')

# Check if the image was loaded successfully
if img is None:
    print("Error: Could not open or read the image file.")
    # You may want to exit or handle the error in a different way
    exit()

# Define parameters.
r1	=	70
s1	=	0
r2	=	140
s2	=	255
# Vectorize the function to apply it to each value in the Numpy array.
pixelVal_vec = np.vectorize(pixelVal)
# Apply contrast stretching.
contrast_stretched = pixelVal_vec(img, r1, s1, r2, s2)

# Save edited image.
cv2.imwrite('contrast_stretch.jpg', contrast_stretched)
# Display the original and contrast-stretched images side by side
plt.figure(figsize=(10, 5))
# Create a figure with a specified size
plt.subplot(1, 2, 1)
# Subplot for the original image
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off')
# Turn off axis labels
plt.subplot(1, 2, 2)
# Subplot for the contrast-stretched image
plt.imshow(cv2.cvtColor(contrast_stretched.astype(np.uint8), cv2.COLOR_BGR2RGB))
plt.title('Contrast Stretched Image')
plt.axis('off')
# Turn off axis labels
plt.show()


# In[11]:


#Thresholding
import cv2
import matplotlib.pyplot as plt

def threshold_image(image_path, threshold_value):
    """
    Applies thresholding to an image and displays the results.

    Args:
    image_path: The path to the input image. threshold_value: The threshold value to use.
    """

    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding
    ret, thresholded_img = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)
    # Display the original and thresholded images
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title("Original Image")
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(thresholded_img, cmap='gray')
    plt.title("Thresholded Image")
    plt.axis('off')
    plt.show()
# Example usage
threshold_image("../images/helmet.jpg", 128)
# Replace with your image path and desired threshold value


# In[12]:


#Intensity Level Slicing without BG
import cv2
import numpy as np
import matplotlib.pyplot as plt
# Load the image
img = cv2.imread('../images/helmet.jpg')
# Define the intensity level slicing function
def intensityLevelSlicing(pixel_value):
  if 140 < pixel_value < 210:
    return 255
  else:
    return 0
# Apply the function to each pixel in the image
intensityLevelSlicing_vec = np.vectorize(intensityLevelSlicing)
transformed_image = intensityLevelSlicing_vec(img)
# Display the original and transformed images
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off')
plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(transformed_image.astype(np.uint8), cv2.COLOR_BGR2RGB))
plt.title("Intensity Level Sliced Image")
plt.axis('off')
plt.show()


# In[23]:


#WITH BG
import cv2
import numpy as np
import matplotlib.pyplot as plt


# Load the image
img = cv2.imread('../images/helmet.jpg')

# Define the intensity level slicing function with background preservation
def intensityLevelSlicingWithBackground(pixel_value):
	if 140 < pixel_value < 210:
		return 255	# Set to white
	else:
		return pixel_value	# Preserve original pixel value
# Apply the function to each pixel in the image
intensityLevelSlicing_vec = np.vectorize(intensityLevelSlicingWithBackground)
transformed_image = intensityLevelSlicing_vec(img)

# Display the original and transformed images
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(transformed_image.astype(np.uint8),
cv2.COLOR_BGR2RGB))
plt.title("Intensity Level Sliced Image with Background")
plt.axis('off')
plt.show()
# Display the original and transformed images




# In[ ]:


#Bit plane Slicing
import cv2
import numpy as np
import matplotlib.pyplot as plt


# In[19]:


def bit_plane_slicing(image_path):
    """
    Performs bit-plane slicing on an image and displays the bit planes
    using subplots.

    Args:
        image_path: The path to the input image.
    """

    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Calculate the number of rows and columns for subplots
    num_rows = 2  # You can adjust this
    num_cols = 4  # You can adjust this

    # Create a figure and subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 6))
    fig.suptitle("Bit Plane Slicing", fontsize=16)

    # Iterate through each bit plane (0-7)
    for i in range(8):
        # Extract the bit plane
        bit_plane = (img >> i) & 1  # Right shift and bitwise AND

        # Calculate subplot index
        row_index = i // num_cols
        col_index = i % num_cols

        # Display the bit plane in the subplot
        axes[row_index, col_index].imshow(bit_plane * 255, cmap='gray')
        axes[row_index, col_index].set_title(f"Bit Plane {i}")
        axes[row_index, col_index].axis('off')  # Turn off axis labels

    plt.tight_layout()  # Adjust subplot spacing
    plt.show()

# Example usage
bit_plane_slicing("../Prac2/astronaut_image_cv2.jpg")  # Replace with your image path


# In[21]:


#3B. Plotting Histogram and histogram Equalization
import cv2
import matplotlib.pyplot as plt

def plot_histogram_and_equalize(image_path):
    """
    Plots the histogram of an image and performs histogram equalization.

    Args:
        image_path: The path to the input image.
    """

    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Calculate and plot the histogram
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.hist(img.ravel(), 256, [0, 256])
    plt.title("Original Histogram")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")

    # Perform histogram equalization
    equalized_img = cv2.equalizeHist(img)

    # Calculate and plot the histogram of the equalized image
    plt.subplot(1, 2, 2)
    plt.hist(equalized_img.ravel(), 256, [0, 256])
    plt.title("Equalized Histogram")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()

    # Display the original and equalized images  (These lines were moved inside the function)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title("Original Image")
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(equalized_img, cmap='gray')
    plt.title("Equalized Image")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Example usage
plot_histogram_and_equalize("../images/nobita2.jpg")  # Replace with your image path

