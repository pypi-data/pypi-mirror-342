def one():
    print('''
#Image Representation
import numpy as np
import matplotlib.pyplot as plt
from skimage import img_as_uint
from skimage.io import imshow, imread
from skimage.color import rgb2hsv
from skimage.color import rgb2gray
          
array_1 = np.array([[255, 0],  [0, 255]])
plt.imshow(array_1, cmap = 'gray')
plt.show()
          
array_2 = np.array([[255, 0, 255], [0, 255, 0],[255, 0, 255]])
plt.imshow(array_2, cmap = 'gray');
plt.show()
          
array_spectrum = np.array([np.arange(0,255,17),
np.arange(255,0,-17),np.arange(0,255,17),np.arange(255,0,-17)])
fig, ax = plt.subplots(1, 2, figsize=(12,4))
ax[0].imshow(array_spectrum, cmap = 'gray')
ax[0].set_title('Arange Generation')
ax[1].imshow(array_spectrum.T, cmap = 'gray')
ax[1].set_title('Transpose Generation')

array_colors = np.array([[[255, 0, 0], [0, 255, 0],[0, 0, 255]]])
plt.imshow(array_colors);
plt.show()
          
array_spectrum = np.array([np.arange(0,255,17),
np.arange(255,0,-17),np.arange(0,255,17),np.arange(255,0,-17)])
fig, ax = plt.subplots(1, 2, figsize=(12,4))
ax[0].imshow(array_spectrum, cmap = 'gray')
ax[0].set_title('Arange Generation')
ax[1].imshow(array_spectrum.T, cmap = 'gray')
ax[1].set_title('Transpose Generation')
          

#Manipulating an actual Image

from google.colab import files
uploaded = files.upload()
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from skimage import img_as_uint
from skimage.io import imshow, imread
from skimage.color import rgb2hsv
from skimage.color import rgb2gray
from skimage.color import rgba2rgb

image = imread('image.jpg')
plt.imshow(image)
plt.show()
image.shape
          
fig, ax = plt.subplots(1, 3, figsize=(6,4), sharey=True)
ax[0].imshow(image[:, 0:130])
ax[0].set_title('First Split')
ax[1].imshow(image[:, 130:260])
ax[1].set_title('Second Split')
ax[2].imshow(image[:, 260:390])
ax[2].set_title('Third Split')
plt.imshow(image[95:250, 130:275])
plt.show()
          
fig, ax = plt.subplots(1, 3, figsize=(12,4), sharey=True)
ax[0].imshow(image[:,:,0], cmap = 'Reds')
ax[0].set_title('Red')
ax[1].imshow(image[:,:,1], cmap = 'Greens')
ax[1].set_title('Green')
ax[2].imshow(image[:,:,2], cmap = 'Blues')
ax[2].set_title('Blue')
          
image_hsv = rgb2hsv(image)
fig, ax = plt.subplots(1, 3, figsize=(12,4), sharey=True)
ax[0].imshow(image_hsv[:,:,0], cmap = 'hsv')
ax[0].set_title('Hue')
ax[1].imshow(image_hsv[:,:,1], cmap = 'gray')
ax[1].set_title('Saturation')
ax[2].imshow(image_hsv[:,:,2], cmap = 'gray')
ax[2].set_title('Value')
          
image_gray = rgb2gray(image)
fig, ax = plt.subplots(1, 5, figsize=(17,6), sharey=True)
ax[0].imshow(image_gray, cmap = 'gray')
ax[0].set_title('Original Grayscale')
ax[1].imshow(img_as_uint(image_gray > 0.25),cmap = 'gray')
ax[1].set_title('Greater than 0.25')
ax[2].imshow(img_as_uint(image_gray > 0.50),cmap = 'gray')
ax[2].set_title('Greater than 0.50')
ax[3].imshow(img_as_uint(image_gray > 0.75),cmap = 'gray')
ax[3].set_title('Greater than 0.75')
ax[4].imshow(img_as_uint(image_gray > np.mean(image_gray)),cmap = 'gray')
ax[4].set_title('Greater than Mean')
          
#Reducing Quantization Values

import numpy as np
import matplotlib.pyplot as plt
img = np.random.rand(256, 256)
reduced_img_2bits = np.round(img * 3) / 3
reduced_img_1bit = np.round(img)
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
          
#Reducing Number of Samples

import numpy as np
import matplotlib.pyplot as plt
img = np.random.rand(256, 256)
reduced_img_half = img[::2, ::2]
reduced_img_quarter = img[::4, ::4]
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

#Reducing Both Quantization Values and Number of Samples

import numpy as np
import matplotlib.pyplot as plt
img = np.random.rand(256, 256)
reduced_img_2bits_half = np.round(img[::2, ::2] * 3) / 3
reduced_img_1bit_quarter = np.round(img[::4, ::4])
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
''')
    
def two():
    print('''

from IPython import get_ipython
from IPython.display import display
import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow
from skimage import data
          
coins_image = data.coins()
coins_image_cv2 = cv2.cvtColor(coins_image, cv2.COLOR_GRAY2BGR)
astronaut_image = data.astronaut()
astronaut_image_cv2 = cv2.cvtColor(astronaut_image, cv2.COLOR_RGB2BGR)
print("Displaying images...")
cv2_imshow(coins_image_cv2)
cv2_imshow(astronaut_image_cv2)
          
# Store the data as images to be readable
cv2.imwrite('coins_image_cv2.jpg', coins_image_cv2)
cv2.imwrite('astronaut_image_cv2.jpg', astronaut_image_cv2)

# Read back the images
image1 = cv2.imread('coins_image_cv2.jpg')
image2 = cv2.imread('astronaut_image_cv2.jpg')

# Print the shapes of the images
print(f"Original Image 1 shape: {image1.shape}")
print(f"Original Image 2 shape: {image2.shape}")
          
# Resize image1 to match the dimensions of image2
image1_resized = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

# Perform arithmetic operations
added_image = cv2.add(image1_resized, image2)
subtracted_image = cv2.subtract(image1_resized, image2)
multiplied_image = cv2.multiply(image1_resized, 0.5)
divided_image = cv2.divide(image1_resized, 2)
# Create a figure and subplots
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Original and Resized Images
axes[0, 0].imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
axes[0, 0].set_title('Original Image 1')
axes[0, 0].axis('off')

axes[0, 1].imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
axes[0, 1].set_title('Original Image 2')
axes[0, 1].axis('off')

axes[0, 2].imshow(cv2.cvtColor(image1_resized, cv2.COLOR_BGR2RGB))
axes[0, 2].set_title('Resized Image 1')
axes[0, 2].axis('off')

# Operation Results
axes[1, 0].imshow(cv2.cvtColor(added_image, cv2.COLOR_BGR2RGB))
axes[1, 0].set_title('Added Image')
axes[1, 0].axis('off')

axes[1, 1].imshow(cv2.cvtColor(subtracted_image, cv2.COLOR_BGR2RGB))
axes[1, 1].set_title('Subtracted Image')
axes[1, 1].axis('off')

axes[1, 2].imshow(cv2.cvtColor(multiplied_image, cv2.COLOR_BGR2RGB))
axes[1, 2].set_title('Multiplied Image (x0.5)')
axes[1, 2].axis('off')

plt.tight_layout()
plt.show()
          
# Blending images (weighted addition)
blended_image = cv2.addWeighted(image1_resized, 0.7, image2, 0.3, 0)

# Display the blended image
plt.figure(figsize=(6, 6))
plt.imshow(cv2.cvtColor(blended_image, cv2.COLOR_BGR2RGB))
plt.title('Blended Image')
plt.axis('off')
plt.show()
          

#Discrete Cosine Transform - Inbuilt Image
from IPython import get_ipython 
from IPython.display import display 
 
import cv2 
import numpy as np 
import matplotlib.pyplot as plt 
from google.colab.patches import cv2_imshow 
from skimage import data 

coins_image = data.coins() 
coins_image_cv2 = coins_image 

dct_image = cv2.dct(np.float32(coins_image_cv2)) 
idct_image = cv2.idct(dct_image) 
plt.figure(figsize=(12, 6)) 
plt.subplot(1, 3, 1) 
plt.title('Original Image') 
plt.imshow((coins_image_cv2), cmap='gray') 
plt.axis('off') 
plt.subplot(1, 3, 2) 
plt.title('DCT Image') 
plt.imshow(np.log(abs(dct_image) + 1), cmap='gray') 
plt.axis('off') 
 
plt.subplot(1, 3, 3) 
plt.title('Reconstructed Image') 
plt.imshow(idct_image, cmap='gray')
plt.axis('off') 
plt.show() 
          

#Discrete Cosine Transform - Custom Image
import cv2 
import numpy as np 
import matplotlib.pyplot as plt 

im = cv2.imread('lena.jpg', cv2.IMREAD_GRAYSCALE) 
im = im.astype(np.float64) 
 
plt.figure(figsize=(12, 4)) 
 
plt.subplot(1, 3, 1) 
plt.imshow(im, cmap='gray') 
plt.title('Original') 

plt.axis('off') 
 
dct_image = cv2.dct(np.float32(im)) 
 
plt.subplot(1, 3, 2) 
plt.imshow(np.log(abs(dct_image) + 1), cmap='gray')  
plt.title('DCT Transform') 
plt.axis('off') 

dct_dct_image = cv2.dct(np.float32(dct_image)) 
 
plt.subplot(1, 3, 3) 
plt.imshow(dct_dct_image, cmap='gray') 
plt.title('DCT(DCT) Transform') 
plt.axis('off') 
 
plt.show()

''')
    
def three():
    print('''
#Linear (Negative Transformation)
import cv2
import matplotlib.pyplot as plt
# Load the original image
original_image = cv2.imread("cameraman.jpg") # Replace with your image file
# Perform the negative transformation
negative_image = 256 - 1 - original_image
# Display the original and negative images side by side
plt.figure(figsize=(10, 5)) # Create a figure with a specified size
plt.subplot(1, 2, 1) # Subplot for the original image
plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off') # Turn off axis labels
plt.subplot(1, 2, 2) # Subplot for the negative image
plt.imshow(cv2.cvtColor(negative_image, cv2.COLOR_BGR2RGB))
plt.title("Negative Image")
plt.axis('off')
plt.show()
          
#Log Transformation (Logarithm Function) & inverse-Log Transformation (Exponential Function)
import cv2
import numpy as np

#Load an image
image = cv2.imread('cameraman.jpg', cv2.IMREAD_GRAYSCALE)

#Log Transformation
c = 30
log_transformed = c * (np.log(1 + image))

#Convert to 8-bit unsigned integer format
log_transformed = np.uint8(log_transformed)

# Inverse-Log Transformation
inverse_log_transformed = c * (np.exp(log_transformed / c) - 1)
# Convert to 8-bit unsigned integer format
inverse_log_transformed = np.uint8(inverse_log_transformed)
# Display the original and negative images side by side
plt.figure(figsize=(10, 5)) # Create a figure with a specified size
plt.subplot(1, 3, 1) # Subplot for the original image
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off') # Turn off axis labels
plt.subplot(1, 3, 2)
plt.imshow(cv2.cvtColor(log_transformed, cv2.COLOR_BGR2RGB))
plt.title("log_transformed")
plt.axis('off')
plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(inverse_log_transformed, cv2.COLOR_BGR2RGB))
plt.title("inverse_log_transformed")
plt.axis('off')
plt.show()
          
#Power Law Transformations
import cv2
import numpy as np
# Read an image
image = cv2.imread('cameraman.jpg', cv2.IMREAD_GRAYSCALE)
# Apply gamma correction (e.g., gamma = 1.5)
gamma = 2
gamma2=4
adjusted_image = np.power(image / 255.0, gamma) * 255.0
adjusted_image = adjusted_image.astype(np.uint8)
adjusted_image2 = np.power(image / 255.0, gamma2) * 255.0
adjusted_image2 = adjusted_image2.astype(np.uint8)
plt.figure(figsize=(10, 5)) # Create a figure with a specified size
plt.subplot(1, 3, 2) # Subplot for the original image
plt.imshow(cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB))
plt.title("adjusted_image gamma =2")
plt.subplot(1, 3, 1) # Subplot for the original image
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.subplot(1, 3, 3) # Subplot for the original image
plt.imshow(cv2.cvtColor(adjusted_image2, cv2.COLOR_BGR2RGB))
plt.title("Original Image gamma = 4")
plt.axis('off')
          
#Contrast Stretching
import cv2
import numpy as np
# Function to map each intensity level to output intensity level.
def pixelVal(pix, r1, s1, r2, s2):
 if (0 <= pix and pix <= r1):
  return (s1 / r1)*pix
 elif (r1 < pix and pix <= r2):
  return ((s2 - s1)/(r2 - r1)) * (pix - r1) + s1
 else:
  return ((255 - s2)/(255 - r2)) * (pix - r2) + s2
# Open the image.
img = cv2.imread('cameraman.jpg')
# Define parameters.
r1 = 85
s1 = 21
r2 = 14
s2 = 255
# Vectorize the function to apply it to each value in the Numpy array.
pixelVal_vec = np.vectorize(pixelVal)
# Apply contrast stretching.
contrast_stretched = pixelVal_vec(img, r1, s1, r2, s2)
# Save edited image.
cv2.imwrite('contrast_stretch.jpg', contrast_stretched)
# Display the original and contrast-stretched images side by side
plt.figure(figsize=(10, 5)) # Create a figure with a specified size
plt.subplot(1, 2, 1) # Subplot for the original image
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off') # Turn off axis labels
plt.subplot(1, 2, 2) # Subplot for the contrast-stretched image
plt.imshow(cv2.cvtColor(contrast_stretched.astype(np.uint8),
cv2.COLOR_BGR2RGB))
plt.title('Contrast Stretched Image')
plt.axis('off') # Turn off axis labels
plt.show()
          
#Thresholding
import cv2
import matplotlib.pyplot as plt
def threshold_image(image_path, threshold_value):
  # Load the image in grayscale
 img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
 # Apply thresholding
 ret, thresholded_img = cv2.threshold(img, threshold_value, 255,cv2.THRESH_BINARY)
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
threshold_image("cameraman.jpg",128)
          
#Intensity Level Slicing- Without BG
import numpy as np
import matplotlib.pyplot as plt
# Load the image
img = cv2.imread('cameraman.jpg')
# Define the intensity level slicing function
def intensityLevelSlicing(pixel_value):
 if 140 < pixel_value < 210:
  return 255 # Set to white
 else:
  return 0 # Set to black
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
plt.imshow(cv2.cvtColor(transformed_image.astype(np.uint8),
cv2.COLOR_BGR2RGB))
plt.title("Intensity Level Sliced Image")
plt.axis('off')
plt.show()
          
#Intensity Level Slicing- With BG
import cv2
import numpy as np
import matplotlib.pyplot as plt
# Load the image
img = cv2.imread('cameraman.jpg')
# Define the intensity level slicing function with background preservation
def intensityLevelSlicingWithBackground(pixel_value):
 if 140 < pixel_value < 210:
  return 255 # Set to white
 else:
  return pixel_value # Preserve original pixel value
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
          
#Bit Plane Slicing
import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow

def bit_plane_slicing(image_path):
    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Calculate the number of rows and columns for subplots
    num_rows = 2  # You can adjust this
    num_cols = 4  # You can adjust this

    # Create a figure and subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 6))  # Adjust figsize as needed
    fig.suptitle("Bit Plane Slicing", fontsize=16)

    # Iterate through each bit plane (0-7)
    for i in range(8):
        # Extract the bit plane
      bit_plane = (img >> i) & 1  # Right shift and bitwise AND

        # Calculate subplot index
      row_index = i // num_cols
      col_index = i % num_cols

        # Display the bit plane in the subplot
      axes[row_index, col_index].imshow(bit_plane * 255, cmap='gray')  # Scale for visibility, use gray colormap
      axes[row_index, col_index].set_title(f"Bit Plane {i}")
      axes[row_index, col_index].axis('off')  # Turn off axis labels

    # Adjust subplot spacing
    plt.tight_layout()
    plt.show()

# Example usage
bit_plane_slicing("cameraman.jpg")  # Replace with your image path


#Plotting Histogram and histogram Equalization
import cv2
import matplotlib.pyplot as plt
def plot_histogram_and_equalize(image_path):
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
plot_histogram_and_equalize("cameraman.jpg")

''')
    
def four():
    print('''
#Performing DFT (Discrete Fourier Transform) and IDFT (Inverse Discrete Fourier Transform)
import cv2
import numpy as np
import matplotlib.pyplot as plt
image = cv2.imread('cameraman.jpg', cv2.IMREAD_GRAYSCALE)
if image is None:
  print("Error: Image not found. Please ensure 'cameraman.jpg' is in the same directory.")
  exit()

dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)
magnitude = cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])
magnitude_spectrum = 20 * np.log(magnitude + 1)
dft_ishift = np.fft.ifftshift(dft_shift)
idft = cv2.idft(dft_ishift)
reconstructed_image = cv2.magnitude(idft[:, :, 0], idft[:, :, 1])
reconstructed_image = cv2.normalize(reconstructed_image, None, 0, 255, cv2.NORM_MINMAX)
reconstructed_image = reconstructed_image.astype(np.uint8)
reconstructed_image = cv2.resize(reconstructed_image, (image.shape[1], image.shape[0]))

plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(image, cmap='gray',aspect='equal')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(magnitude_spectrum, cmap='gray',aspect='equal')
plt.title('Magnitude Spectrum')
plt.axis('off')
plt.show()

cv2.imwrite('magnitude_spectrum.jpg', magnitude_spectrum)
cv2.imwrite('reconstructed_image.jpg', reconstructed_image)

#Ideal, Butterworth and Gaussian LPFs (Low Pass Filter)
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

image = cv2.imread('cameraman.jpg', cv2.IMREAD_GRAYSCALE)

if image is None:
  print("Error: Image not found. Please ensure 'cameraman.jpg' is in the same directory.")
  exit()

rows, cols = image.shape
crow, ccol = rows // 2, cols // 2

#Frequency grid
u = np.arange(-ccol, ccol)
v = np.arange(-crow, crow)
U, V = np.meshgrid(u, v)
D = np.sqrt(U**2 + V**2)

#Filter Functions
def ideal_lpf(D, cutoff):
  H = np.zeros_like(D)
  H[D <= cutoff] = 1
  return H

def butterworth_lpf(D, cutoff, order):
  H = 1 / (1 + (D / cutoff)**(2 * order))
  return H

def gaussian_lpf(D, cutoff):
  H = np.exp(-(D**2) / (2 * (cutoff**2)))
  return H

# Apply filters and visualize
def apply_filter(image, filter_function):
    dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shifted = np.fft.fftshift(dft)
    filter_mask = filter_function(D)
    filtered = dft_shifted * filter_mask[:, :, np.newaxis]
    dft_ishifted = np.fft.ifftshift(filtered)
    idft = cv2.idft(dft_ishifted)
    result = cv2.magnitude(idft[:, :, 0], idft[:, :, 1])
    return filter_mask, cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX)
cutoff = 50
order = 2

# Apply the three filters
ideal_mask, ideal_result = apply_filter(image, lambda D: ideal_lpf(D,
cutoff))
butter_mask, butter_result = apply_filter(image, lambda D:
butterworth_lpf(D, cutoff, order))
gaussian_mask, gaussian_result = apply_filter(image, lambda D:
gaussian_lpf(D, cutoff))

# Subplots for each filter
fig, axes = plt.subplots(3, 3, figsize=(18, 12))

# Plot for Ideal Low Pass Filter
axes[0, 0].imshow(image, cmap='gray')
axes[0, 0].set_title('Original Image')
axes[0, 0].axis('off')

axes[0, 1].imshow(np.uint8(ideal_result), cmap='gray')
axes[0, 1].set_title('Ideal LPF Result')
axes[0, 1].axis('off')

ax = fig.add_subplot(331 + 2, projection='3d')
ax.plot_surface(U, V, ideal_mask, cmap='viridis')
ax.set_title('Ideal LPF Transfer Function')
ax.set_xlabel('Frequency U')
ax.set_ylabel('Frequency V')
ax.set_zlabel('Magnitude')

# Plot for Butterworth Low Pass Filter
axes[1, 0].imshow(image, cmap='gray')
axes[1, 0].set_title('Original Image')
axes[1, 0].axis('off')

axes[1, 1].imshow(np.uint8(butter_result), cmap='gray')
axes[1, 1].set_title('Butterworth LPF Result')
axes[1, 1].axis('off')
ax = fig.add_subplot(331 + 5, projection='3d')
ax.plot_surface(U, V, butter_mask, cmap='viridis')
ax.set_title('Butterworth LPF Transfer Function')
ax.set_xlabel('Frequency U')
ax.set_ylabel('Frequency V')
ax.set_zlabel('Magnitude')

# Plot for Gaussian Low Pass Filter
axes[2, 0].imshow(image, cmap='gray')
axes[2, 0].set_title('Original Image')
axes[2, 0].axis('off')

axes[2, 1].imshow(np.uint8(gaussian_result), cmap='gray')
axes[2, 1].set_title('Gaussian LPF Result')
axes[2, 1].axis('off')

ax = fig.add_subplot(331 + 8, projection='3d')
ax.plot_surface(U, V, gaussian_mask, cmap='viridis')
ax.set_title('Gaussian LPF Transfer Function')
ax.set_xlabel('Frequency U')
ax.set_ylabel('Frequency V')
ax.set_zlabel('Magnitude')

plt.tight_layout()
plt.show()

#Ideal, Butterworth and Gaussian HPFs (High Pass Filter)
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def ideal_highpass_filter(shape, cutoff_frequency):
  rows, cols = shape
  crow, ccol = rows // 2, cols // 2
  mask = np.ones((rows, cols), np.uint8)
  cv2.circle(mask, (ccol, crow), cutoff_frequency, 0, -1)
  return mask

def butterworth_highpass_filter(shape, cutoff_frequency, order=2):
    """Creates a Butterworth high-pass filter."""
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows, cols), np.float32)
    for i in range(rows):
        for j in range(cols):
            dist = np.sqrt((i - crow)**2 + (j - ccol)**2)
            mask[i, j] = 1 / (1 + (cutoff_frequency / dist)**(2 * order))
    return mask

def gaussian_highpass_filter(shape, cutoff_frequency):
    """Creates a Gaussian high-pass filter."""
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows, cols), np.float32)
    for i in range(rows):
        for j in range(cols):
            dist = np.sqrt((i - crow)**2 + (j - ccol)**2)
            mask[i, j] = 1 - np.exp(-(dist**2) / (2 *
(cutoff_frequency**2)))
    return mask

# Load the image in grayscale
image = cv2.imread('cameraman.jpg', cv2.IMREAD_GRAYSCALE)
if image is None:
    print("Error: Image not found. Please ensure 'cameraman.jpg' is in the current directory.")
    exit()

# Compute the DFT
dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

# Compute the magnitude spectrum
magnitude = cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])
magnitude_spectrum = 20 * np.log(magnitude + 1)  # Add 1 to avoid log(0)

# Create the filters
cutoff_frequency = 30  # Adjust as needed
ideal_mask = ideal_highpass_filter(image.shape, cutoff_frequency)
butterworth_mask = butterworth_highpass_filter(image.shape,
cutoff_frequency)
gaussian_mask = gaussian_highpass_filter(image.shape, cutoff_frequency)

# Apply the filters
filtered_ideal = dft_shift * ideal_mask[:, :, np.newaxis]
filtered_butterworth = dft_shift * butterworth_mask[:, :, np.newaxis]
filtered_gaussian = dft_shift * gaussian_mask[:, :, np.newaxis]

# Compute the IDFT
ideal_ishift = np.fft.ifftshift(filtered_ideal)
butterworth_ishift = np.fft.ifftshift(filtered_butterworth)
gaussian_ishift = np.fft.ifftshift(filtered_gaussian)

ideal_back = cv2.idft(ideal_ishift)
butterworth_back = cv2.idft(butterworth_ishift)
gaussian_back = cv2.idft(gaussian_ishift)

# Reconstruct the images (using magnitude)
ideal_image = cv2.magnitude(ideal_back[:, :, 0], ideal_back[:, :, 1])
butterworth_image = cv2.magnitude(butterworth_back[:, :, 0],
butterworth_back[:, :, 1])
gaussian_image = cv2.magnitude(gaussian_back[:, :, 0], gaussian_back[:, :,
1])

# Normalize for display
ideal_image = cv2.normalize(ideal_image, None, 0, 255,
cv2.NORM_MINMAX).astype(np.uint8)
butterworth_image = cv2.normalize(butterworth_image, None, 0, 255,
cv2.NORM_MINMAX).astype(np.uint8)

gaussian_image = cv2.normalize(gaussian_image, None, 0, 255,
cv2.NORM_MINMAX).astype(np.uint8)

# Display the results
plt.figure(figsize=(18, 12))  # Adjusted figure size for more subplots

# Original Image and Magnitude Spectrum
plt.subplot(2, 4, 1), plt.imshow(image, cmap='gray'), plt.title('Original Image')
plt.subplot(2, 4, 2), plt.imshow(magnitude_spectrum, cmap='gray'),
plt.title('Magnitude Spectrum')

# Filtered Images
plt.subplot(2, 4, 3), plt.imshow(ideal_image, cmap='gray'),
plt.title('Ideal HPF')
plt.subplot(2, 4, 4), plt.imshow(butterworth_image, cmap='gray'),
plt.title('Butterworth HPF')
plt.subplot(2, 4, 5), plt.imshow(gaussian_image, cmap='gray'),
plt.title('Gaussian HPF')

# Perspective Plots of Transfer Functions
X, Y = np.meshgrid(np.arange(ideal_mask.shape[1]),
np.arange(ideal_mask.shape[0]))

ax1 = plt.subplot(2, 4, 6, projection='3d')
ax1.plot_surface(X, Y, ideal_mask, cmap='viridis')
ax1.set_title('Ideal HPF Transfer Function (3D)')

ax2 = plt.subplot(2, 4, 7, projection='3d')
ax2.plot_surface(X, Y, butterworth_mask, cmap='viridis')
ax2.set_title('Butterworth HPF Transfer Function (3D)')

ax3 = plt.subplot(2, 4, 8, projection='3d')
ax3.plot_surface(X, Y, gaussian_mask, cmap='viridis')
ax3.set_title('Gaussian HPF Transfer Function (3D)')
plt.show()          
         
''')
    
def five():
    print('''
#Image Deblurring using Inverse and Wiener Filter
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

def motion_blur(image, kernel_size, angle):
  kernel = np.zeros((kernel_size, kernel_size))
  kernel[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
  kernel = cv2.warpAffine(kernel, cv2.getRotationMatrix2D((kernel_size / 2 - 0.5, kernel_size / 2 - 0.5), angle, 1.0), (kernel_size, kernel_size))
  kernel = kernel / np.sum(kernel)
  blurred = convolve2d(image, kernel, mode='same', boundary='wrap')
  return blurred

def inverse_filter(blurred, kernel, eps):
  blurred_fft = np.fft.fft2(blurred)
  kernel_fft = np.fft.fft2(kernel, s=blurred.shape)
  deblured_fft = blurred_fft / (kernel_fft + eps)
  deblured = np.fft.ifft2(deblured_fft).real
  return deblured

def wiener_filter(blurred, kernel, k):
    blurred_fft = np.fft.fft2(blurred)
    kernel_fft = np.fft.fft2(kernel, s=blurred.shape)
    kernel_fft_conj = np.conj(kernel_fft)
    deblurred_fft = (kernel_fft_conj / (np.abs(kernel_fft)**2 + k)) * blurred_fft
    deblurred = np.fft.ifft2(deblurred_fft).real
    return deblurred
          
# Load image and apply motion blur
img = cv2.imread('cameraman.jpg', cv2.IMREAD_GRAYSCALE)
kernel_size = 21
angle = 11
blurred = motion_blur(img, kernel_size, angle)
          
# Create blur kernel
kernel = np.zeros((kernel_size, kernel_size))
kernel[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
kernel = cv2.warpAffine(kernel, cv2.getRotationMatrix2D((kernel_size / 2 - 0.5, kernel_size / 2 - 0.5), angle, 1.0), (kernel_size, kernel_size))
kernel = kernel / np.sum(kernel)
          
# Deblur using inverse filtering
deblurred_inverse = inverse_filter(blurred, kernel, 0.01)

# Deblur using Wiener filtering
deblurred_wiener = wiener_filter(blurred, kernel, 0.01)

# Display results
plt.figure(figsize=(12, 6))
plt.subplot(131), plt.imshow(img, cmap='gray'), plt.title('Original Image')
plt.subplot(132), plt.imshow(blurred, cmap='gray'), plt.title('Blurred Image')
plt.subplot(133), plt.imshow(deblurred_inverse, cmap='gray'),
plt.title('Inverse Filtered')
plt.show()

plt.figure(figsize=(12, 6))
plt.subplot(131), plt.imshow(img, cmap='gray'), plt.title('Original Image')
plt.subplot(132), plt.imshow(blurred, cmap='gray'), plt.title('Blurred Image')
plt.subplot(133), plt.imshow(deblurred_wiener, cmap='gray'),
plt.title('Wiener Filtered')
plt.show()

''')
    
def six():
    print('''
#Edge detction using Sobel,pewitt,Canny, and Laplacian operations
import cv2
import numpy as np
import matplotlib.pyplot as plt

image =cv2.imread('lena.jpg',cv2.IMREAD_GRAYSCALE)     
sobel_x = cv2.Sobel(image,cv2.CV_64F,1,0,ksize=3)
sobel_y = cv2.Sobel(image,cv2.CV_64F,0,1,ksize=3)

kernel_x = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
kernel_y = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
prewitt_x = cv2.filter2D(image,-1,kernel_x)
prewitt_y = cv2.filter2D(image,-1,kernel_y)

canny_edges = cv2.Canny(image,100,200)
laplacian=cv2.Laplacian(image,cv2.CV_64F)

titles= ['Original','Sobel X','Sobel Y','Prewitt X','Prewitt Y','Canny','Laplacian']
images=[image,sobel_x,sobel_y,prewitt_x,prewitt_y,canny_edges,laplacian]

plt.figure(figsize=(15,10))
for i in range(len(images)):
  plt.subplot(3,3,i+1)
  plt.imshow(images[i],cmap='gray')
  plt.title(titles[i])
  plt.axis('off')
plt.tight_layout()
plt.show()
    
''')

def seven():
    print('''
#Application of Morphological Operations on image
import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('blobs.png',cv2.IMREAD_GRAYSCALE)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(image,kernel,iterations = 1)
dilation = cv2.dilate(image,kernel,iterations = 1)
opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
plt.subplot(2,3,1),
plt.imshow(image, cmap = 'gray')
plt.title('Original Image')      
         
plt.subplot(2,3,2),
plt.imshow(erosion, cmap = 'gray')
plt.title('Erosion')
          
plt.subplot(2,3,3),
plt.imshow(dilation, cmap = 'gray')
plt.title('Dilation')
          
plt.subplot(2,3,4),
plt.imshow(opening, cmap = 'gray')
plt.title('Opening')
          
plt.subplot(2,3,5),
plt.imshow(closing, cmap = 'gray')
plt.title('Closing')
plt.tight_layout()
plt.show()
''')

def help():
    print('''
one() = Image Representation, Sampling & Quantization
two() = Arthemetic Operations and Discrete Cosine Transform (DCT)
three() = Intensity Transformation, Histogram Processing, Spatial Filtering: 1. Smoothing (Low Pass Filter), 2. Sharpening (High Pass Filter)
four() = Discrete Fourier transformation (DFT) & Inverse DiscreteFourier Transformation (IDFT), Low Pass Filters- Ideal, Gaussian & Butterworth, High  Pass Filters- Ideal, Gaussian & Butterworth
five() = Image Deblurring Using Inverse Filters, Image Deblurring Using Wiener Filters
six() = Edge Detection using sobel, prewitt,canny & Laplacian Operators
seven() = Apply Erosion, Dilation, Opening and Closing operations on images
''')