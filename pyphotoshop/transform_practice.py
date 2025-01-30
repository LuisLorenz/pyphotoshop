from image import Image
import numpy as np

def brighten(image, factor):    
    x_pixels, y_pixels, num_channels = image.array.shape 
        # extracting these 3 components from the im_array
        #   the array is created by the decoder of the png algo 
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    # # intuitive way
    # for x in range(x_pixels):
    #     for y in range(y_pixels):
    #         for c in range(num_channels):
    #             # iterating through all pixel 
    #             new_im.array[x, y, c] = image.array[x, y, c] * factor 
    #                 # the factor only changes the values for c 
    #                     # why not x,y in this code?
    #                         # x,y define just the position
    #                         # the value is given by c and this value is changed through the factor 
    #                 # num_channels: there are three
    #                     # so for each channel the value is adjusted 
            
    # vectorized version
    new_im.array = image.array * factor 
    # faster
    
    return new_im # none global var   

def adjust_contrast(image, factor, mid):
    # adjust the contrast by increasing the difference from the user-defined midpoint by factor amount
    x_pixels, y_pixels, num_channels = image.array.shape 
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    # slow way
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image.array[x, y, c] - mid) * factor + mid # not so clear so far

    # # fast way
    # new_im.array = (image.array - mid) * factor + mid 

    return new_im

def blur(image, kernel_size):
    # kernel size is the number of pixels to take into account when applying the blur
    # (ie kernel_size = 3 would be neighbors to the left/right, top/bottom, and diagonals)
    # kernel size should always be an *odd* number -> why is this important? 
    # making the pixel(s) more the same like the neighboring pixels
    x_pixels, y_pixels, num_channels = image.array.shape 
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    neighbor_range = kernel_size // 2 

    # slow way
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0 
                for x_i in range(max(0, x - neighbor_range), min(x_pixels, x + neighbor_range + 1)):
                    # old: for x_i in range(max(0, x - neighbor_range), min(x_pixels - 1, x + neighbor_range + 1)):
                    # border check: take at least 0 
                    #   do not go lower than 0 
                    for y_i in range(max(0, y - neighbor_range), min(y_pixels, y + neighbor_range + 1)):
                        # old: for y_i in range(max(0, y - neighbor_range), min(y_pixels - 1, y + neighbor_range + 1)):
                        # going into the other dimesion 
                        total += image.array[x_i, y_i, c]
                new_im.array[x,y,c] = total / (kernel_size ** 2) # average

    return new_im

def apply_kernel(image, kernel):
    # the kernel should be a 2D array that represents the kernel we'll use!
    # for the sake of simiplicity of this implementation, let's assume that the kernel is SQUARE
    # for example the sobel x kernel (detecting horizontal edges) is as follows:
    # [1 0 -1]
    # [2 0 -2]
    # [1 0 -1]
    x_pixels, y_pixels, num_channels = image.array.shape 
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    kernel_size = kernel.shape[0] 
    neighbor_range = kernel_size // 2 

    # slow way
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0 
                for x_i in range(max(0, x - neighbor_range), min(x_pixels, x + neighbor_range + 1)):
                    for y_i in range(max(0, y - neighbor_range), min(y_pixels, y + neighbor_range + 1)):
                        x_k = x_i + neighbor_range - x 
                        y_k = y_i + neighbor_range - y
                        kernel_val = kernel[x_k, y_k]
                        total += image.array[x_i, y_i, c] * kernel_val

                # new_im.array[x,y,c] = total 
                new_im.array[x, y, c] = np.clip(abs(total), 0, 255) 
                # it is amout the difference to zero (there is a sharp difference between e.g. left to right)
                # negative values are set to positive for avoiding a set to zero
                # near 0 means a very soft change/none from left to right

    return new_im


def combine_images(image1, image2):
    # let's combine two images using the squared sum of squares: value = sqrt(value_1**2, value_2**2)
    # size of image1 and image2 MUST be the same
    x_pixels, y_pixels, num_channels = image1.array.shape # or image2 because they should be the same shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x,y,c] = (image1.array[x,y,c]**2 + image2.array[x,y,c]**2)**0.5 
                    # x and y stay the same, c is averaged
                    # creating big square and take the square root out of it

    return new_im
    
if __name__ == '__main__': # only when I am on this code space at the moment the flowing code runs
    # photo import 
    lake = Image(filename='lake.png')
    city = Image(filename='city.png')

    Italia1 = Image(filename='Italia1.png')
    Italia2 = Image(filename='Italia2.png')

    # brightened_im = brighten(lake, 1.7) # changing brightness level 
    # brightened_im.write_image('brightened2.png') # printing the image / writing it

    brightened_im = brighten(Italia1, 2.5)
    brightened_im.write_image('Italia1_brighthened_2.5.png')

    # brightened_im = brighten(Italia2, 1.7)
    # brightened_im.write_image('Italia2_brighthened_1.7.png')


    # brightened_im = brighten(Italia2, 2.5)
    # brightened_im.write_image('Italia2_brighthened_2.5.png')

    # # darken
    # darkened_im = brighten(lake, 0.3)
    # darkened_im.write_image('darkened2.jpg')

    # darkened_im = brighten(Italia2, 0.5)
    # darkened_im.write_image('Italia2_darkened_0.5.png')

    # # increase the contrast           
    # incr_contrast = adjust_contrast(lake, 2, 2)
    # incr_contrast.write_image('increased_contrast8.png')

    # incr_contrast = adjust_contrast(Italia1, 2, 0.3)
    # incr_contrast.write_image('Italia1_2_0.3.png')

    # incr_contrast = adjust_contrast(Italia1, 2, 0.5)
    # incr_contrast.write_image('Italia1_2.0.5.png')

    # incr_contrast = adjust_contrast(Italia1, 2, 0.7)
    # incr_contrast.write_image('Italia1_2_0.7.png')

    # # decrease the contrast           
    # decr_contrast = adjust_contrast(lake, 0.5, 0.5)
    # decr_contrast.write_image('decreased_contrast.png')

    # decr_contrast = adjust_contrast(Italia1, 0.5, 0.3)
    # decr_contrast.write_image('Italia1_0.5_0.3.png')

    # decr_contrast = adjust_contrast(Italia1, 0.5, 0.5)
    # decr_contrast.write_image('Italia1_0.5_0.5.png')

    # decr_contrast = adjust_contrast(Italia1, 0.5, 0.7)
    # decr_contrast.write_image('Italia1_0.5_0.7.png')
    

    # blue with kernel 3
    # blur_3 = blur(city, 3)
    # blur_3.write_image('blur_k3.png')

    # blur_3 = blur(Italia1, 3)
    # blur_3.write_image('Italia1_k3_-1.png')

    # blur_3 = blur(Italia1, 15)
    # blur_3.write_image('Italia1_k15_-1.png')

    # blur_3 = blur(Italia1, 3)
    # blur_3.write_image('Italia1_k3_.png')

    # blur_3 = blur(city, 15)
    # blur_3.write_image('city_k15_0.png')

    # blue with kernel 15
    # blur_15 = blur(city, 15)
    # blur_15.write_image('blur_k15.png')

    # sobel edge detection kernel
    sobel_x_kernel = np.array([
        [1,2,1], 
        [0,0,0], 
        [-1,-2,-1]
    ])
    sobel_y_kernel = np.array([
        [1,0,-1],    
        [2,0,-2], 
        [1,0,-1]
    ])

    # sobel_x = apply_kernel(city, sobel_x_kernel)
    # sobel_x.write_image('edge_x_new.png')
    # sobel_y = apply_kernel(city, sobel_y_kernel)
    # sobel_y.write_image('edge_y_new.png')

    # # the edges are highlighted 

    # sobel_x = apply_kernel(Italia1, sobel_x_kernel)
    # sobel_x.write_image('Italia1_x.png')
    # sobel_y = apply_kernel(Italia1, sobel_y_kernel)
    # sobel_y.write_image('Italia1_y.png')

    # sobel_xy = combine_images(sobel_x, sobel_y)
    # sobel_xy.write_image('edge_xy_new.png')

    # sobel_xy = combine_images(sobel_x, sobel_y)
    # sobel_xy.write_image('Italia1_xy.png')

    # # combination of those highlighting filters
    # # edge detection filter   