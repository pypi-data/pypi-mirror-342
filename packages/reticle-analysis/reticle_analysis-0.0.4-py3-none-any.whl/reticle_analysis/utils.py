import numpy as np
import tifffile as tiff
from scipy.ndimage import gaussian_filter
import cv2
from skimage.filters import threshold_triangle
import os
import tifffile
import argparse
from scipy.ndimage import median_filter
import time
import multiprocessing
from multiprocessing import Pool, cpu_count


# PARAMETROS
sigma1 = 1.0
sigma2 = 3.0
remove_outliers_filter_size = 3
roi_size = (25, 25)
frame_range = (1, 40)



#-------------------------------- PASO 1 DoG --------------------------------------

def process_dog(image_stack, sigma1, sigma2):
    if sigma1 > 0:
        blur1 = gaussian_filter(image_stack, sigma=sigma1)
    else:
        blur1 = image_stack

    blur2 = gaussian_filter(image_stack, sigma=sigma2)
    dog = blur1 - blur2
    return dog

def difference_of_gaussians(stack_path, sigma1, sigma2):
    image_stack = tiff.imread(stack_path)

    if image_stack.ndim == 3:
        frames, height, width = image_stack.shape
        channels = 1
        image_stack = image_stack[:, np.newaxis, :, :]
    elif image_stack.ndim == 4:
        frames, channels, height, width = image_stack.shape
    else:
        raise ValueError("Unexpected number of dimensions in the image stack")
    
    if channels > 1:
        channel_data = image_stack[:, 1, :, :].astype(np.float32)
    else:
        channel_data = image_stack[:, 0, :, :].astype(np.float32)

    dog_stack = process_dog(channel_data, sigma1, sigma2)

    return dog_stack.astype(np.float32)

#-------------------------------- PASO 2 Máscara Binaria --------------------------

def binary_mask(dog_stack_path):
    dog_stack = tiff.imread(dog_stack_path)
    frames, height, width = dog_stack.shape
    
    mask_stack = np.zeros_like(dog_stack)
    
    for frame in range(frames):
        image = dog_stack[frame, :, :]
        thresh_val = threshold_triangle(image)
        _, bin_mask = cv2.threshold(image, thresh_val, 65535, cv2.THRESH_BINARY)
        mask_stack[frame, :, :] = bin_mask
    
    return mask_stack.astype(np.uint16)
#-------------------------------- PASO 3 Remove Outliers --------------------------

def median_filt(stack_path,filter_size):
    stack_array = tiff.imread(stack_path)
    filtered_array = median_filter(stack_array, size=filter_size)

    return filtered_array.astype(np.uint16)

#-------------------------------- PASO 4 Normalizar -------------------------------

def normalize(mask_path, original_stack_path):
    mask_stack = tiff.imread(mask_path)
    max_value = np.iinfo(mask_stack.dtype).max
    normalizado = mask_stack / max_value

    original_stack = tiff.imread(original_stack_path)
    if original_stack.ndim == 3:
        channel_0_original_stack = original_stack
    elif original_stack.ndim == 4:
        channel_0_original_stack = original_stack[:, 0, :, :]
    else:
        raise ValueError("Unexpected number of dimensions in the original stack")

    stack_result = normalizado * channel_0_original_stack

    return stack_result.astype(np.float32)

#------------------ PASO 5 ROIs y log2(p/f0) --------------------------------------

def create_rectangle_roi(x, y, width, height, image_shape):
    img_height, img_width = image_shape
    width = min(width, img_width - x)
    height = min(height, img_height - y)
    return (x, y, width, height)

def create_mask_from_roi(roi, image_shape):
    x, y, width, height = roi
    mask = np.zeros(image_shape, dtype=bool)
    mask[y:y + height, x:x + width] = True
    return mask

def generate_rois(image_shape, roi_size):
    height, width = image_shape
    rois = []
    resto = width % roi_size[0]
    for y in range(0, height, roi_size[1]):
        for x in range(0, width, roi_size[0]):
            current_width = min(roi_size[0], width - x)
            current_height = min(roi_size[1], height - y)
            roi = create_rectangle_roi(x, y, roi_size[0], current_height, (height, width))
            rois.append(roi)
        if resto != 0:
            roi = create_rectangle_roi(x + current_width, y, current_width, current_height, (height, width))
            rois.append(roi)
    return rois

def get_neighbor_indices(roi_index, rois_per_row, rois_per_col):
    neighbors = []
    row = roi_index // rois_per_row
    col = roi_index % rois_per_row
    for d_row in [-1, 0, 1]:
        for d_col in [-1, 0, 1]:
            if d_row == 0 and d_col == 0:
                continue
            neighbor_row = row + d_row
            neighbor_col = col + d_col
            if 0 <= neighbor_row < rois_per_col and 0 <= neighbor_col < rois_per_row:
                neighbor_index = neighbor_row * rois_per_row + neighbor_col
                neighbors.append(neighbor_index)
    return neighbors

def calculate_f0_per_roi(avg_fluorescence_array, frame_range, rois_per_row, rois_per_col, num_rois, channel):
    f0_per_roi = np.zeros(num_rois)
    for roi_idx in range(num_rois):
        roi_fluorescence_values = []
        for frame in range(frame_range[0], frame_range[1] + 1):
            avg = avg_fluorescence_array[frame, channel, roi_idx]
            neighbors = get_neighbor_indices(roi_idx, rois_per_row, rois_per_col)
            neighbor_values = [avg_fluorescence_array[frame, channel, n] for n in neighbors]
            all_values = neighbor_values + [avg]
            all_values = np.where(np.array(all_values) == 0, np.nan, all_values)
            avg_with_neighbors = np.nanmean(all_values)
            roi_fluorescence_values.append(avg_with_neighbors)
        f0_per_roi[roi_idx] = np.mean(roi_fluorescence_values)
    return f0_per_roi

def process_frame_range(args):
    frame_start, frame_end, rois, stack, num_channels, height, width = args
    local_fluorescence = []
    for frame in range(frame_start, frame_end):
        if num_channels == 1:
            image = stack[frame]
        else:
            image = stack[frame, 0]
        roi_avg = []
        for roi in rois:
            mask = create_mask_from_roi(roi, (height, width))
            roi_pixels = image[mask]
            roi_pixels = roi_pixels[roi_pixels > 0]
            roi_avg.append(np.mean(roi_pixels) if roi_pixels.size > 0 else 0)
        for channel in range(num_channels):
            local_fluorescence.append((frame, channel, roi_avg))
    return local_fluorescence

def process_chunk(args):
    start, end, rois, stack, f0_per_roi, num_channels, height, width, channel = args
    result_chunk = np.empty((end - start, height, width), dtype=np.float32)

    for i, frame in enumerate(range(start, end)):
        result_frame = np.full((height, width), np.nan, dtype=np.float32)
        for roi_index, roi in enumerate(rois):
            f0 = f0_per_roi[roi_index]
            mask = create_mask_from_roi(roi, (height, width))
            if stack.ndim == 3:
                roi_pixels = stack[frame][mask]
            elif stack.ndim == 4:
                roi_pixels = stack[frame, channel][mask]

            if f0 > 0:
                safe_roi_pixels = np.where(roi_pixels != 0, roi_pixels / f0, np.nan)
                log_result = np.log2(safe_roi_pixels)
                result_frame[mask] = log_result
            else:
                result_frame[mask] = np.nan
        result_chunk[i] = result_frame

    return result_chunk


def process_stack_rois(input_tiff,roi_size, frame_range):
    with tiff.TiffFile(input_tiff) as tif:
        stack = tif.asarray()

    if stack.ndim == 3:
        num_frames, height, width = stack.shape
        num_channels = 1
    elif stack.ndim == 4:
        num_frames, num_channels, height, width = stack.shape
    else:
        raise ValueError("Unexpected number of dimensions in the stack")

    print(f"STACK SHAPE: {stack.shape} \n")
    rois = generate_rois((height, width), roi_size)
    rois_per_row = (width + roi_size[0] - 1) // roi_size[0]
    rois_per_col = (height + roi_size[1] - 1) // roi_size[1]
    num_rois = len(rois)

    num_workers = min(num_frames, multiprocessing.cpu_count())
    print(f"NUMERO DE WORKERS: {num_workers} \n") 
    chunk_size = (num_frames + num_workers - 1) // num_workers
    frame_ranges = [(i, min(i + chunk_size, num_frames)) for i in range(0, num_frames, chunk_size)]
    print(f"FRAME_RANGES: {frame_ranges} \n")

    args = [(start, end, rois, stack, num_channels, height, width) for start, end in frame_ranges]

    inicio = time.time()
    with multiprocessing.Pool(processes=num_workers) as pool:
        results = pool.map(process_frame_range, args)
    fin = time.time()
    print(f"Tiempo de ejecución paralelo: {fin - inicio:.4f} segundos")

    roi_fluorescence = [item for sublist in results for item in sublist]
    avg_fluorescence_array = np.zeros((num_frames, num_channels, num_rois), dtype=np.float32)

    for frame, channel, averages in roi_fluorescence:
        avg_fluorescence_array[frame, channel, :len(averages)] = averages

    channel = 0
    inicio = time.time()
    f0_per_roi = calculate_f0_per_roi(avg_fluorescence_array, frame_range, rois_per_row, rois_per_col, num_rois, channel)
    fin = time.time()
    print(f"Tiempo de ejecución funcion F0: {fin - inicio:.4f} segundos")

    args = [
        (start, end, rois, stack, f0_per_roi, num_channels, height, width, channel)
        for start, end in frame_ranges
    ]

    inicio = time.time()
    with multiprocessing.Pool(processes=num_workers) as pool:
        processed_chunks = pool.map(process_chunk, args)

    new_stack = np.concatenate(processed_chunks, axis=0)
    fin = time.time()
    print(f"Tiempo de ejecución calculo despues de F0: {fin - inicio:.4f} segundos")

    return new_stack
