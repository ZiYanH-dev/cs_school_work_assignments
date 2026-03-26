import numpy as np

def analyze_array(arr:list):
    '''
    Write a function analyze_array that takes a list of numbers, converts it into a NumPy array, and returns a
    dictionary containing the array’s shape, mean, standard deviation, and maximum value. Use the following
    header:
    '''
    np_arr=np.array(arr)
    return {
        'shape':np_arr.shape,
        'mean':np_arr.mean(),
        'std':np_arr.std(),
        'max':np_arr.max()

    }

def replace_outliers(data:np.ndarray, threshold, replacement_value):
    '''
Write a function replace_outliers that takes a 1D NumPy array and two numbers: threshold and
replacement_value. The function should replace all elements in the array whose absolute value is greater than
the threshold with the replacement_value. Use NumPy’s boolean array indexing, not a Python loop. 
    '''
    result=data.copy()
    result[np.absolute(result)>threshold]=replacement_value
    return result

def reshape_and_sum(data:np.ndarray, rows, cols):
    '''
Write a function reshape_and_sum that takes a 1D NumPy array and two integers rows and cols.
The function should:
1. Reshape the array into a 2D array with the given rows and cols.
2. Return a 1D array where each element is the sum of the corresponding column in the reshaped
If the array cannot be reshaped to the specified dimensions 
(due to size mismatch), return None.
    '''
    if data.size!=rows*cols:
        return None
    print(data.reshape(rows,cols))
    return data.reshape(rows,cols).sum(axis=0)

def handle_special_values(data):
    '''
Write a function handle_special_values that takes a NumPy array and returns a modified version where:
1. All NaN (Not a Number) values are replaced with -1.
2. All infinite values (both positive and negative infinity) are replaced with the array’s maximum finite value
(ignoring infinites and NaNs)
3. If there are no finite values in the array, return an array of zeros with the same shape.
    '''
    result=np.copy(data)
    result[np.isnan(result)]=-1
    max_finite=np.max(result[np.isfinite(result)])
    result[np.isinf(result)]=max_finite
    if not np.isfinite(result).any():
        return np.zeros_like(data)
    return result

def create_border(data:np.ndarray, border_width):
    '''
Write a function create_border that takes a 2D NumPy array and an integer border_width. The function
should add a border of zeros around the array with the specified width. The output should be a new array with
the original array in the center, surrounded by zeros.
    '''
    rows,cols=data.shape
    ze=np.zeros((rows+border_width*2,cols+border_width*2))
    ze[border_width:border_width+cols,border_width:border_width+rows]=data
    return ze


def moving_average(arr:np.ndarray,window_size):
    '''
The function should apply a moving average to arr and return a new 1D NumPy array containing the average
values. For each position i from 0 to arr.size - window_size, the output should be mean of
arr[i:i+window_size]. The output array should have a length of arr.size - window_size + 1.
Note: arr.size is the number of elements in the array arr.
    '''
    # Step 1: Calculate number of windows (output length)
    num_windows = arr.size - window_size + 1
    
    # Step 2: Create starting indices for all windows using np.arange()
    # This gives [0, 1, 2, ..., num_windows-1], which is [0,1,2...,arr.size-window_size]
    start_indices = np.arange(num_windows)
    
    # Step 3: Create a 2D array where each row is a sliding window
    # For each start index i, we take arr[i:i+window_size]
    # We reshape start_indices to (num_windows, 1) to broadcast with window indices
    window_indices = start_indices.reshape(-1, 1) + np.arange(window_size)
    window_values = arr[window_indices]
    
    # Step 4: Calculate mean of each window (row) using np.mean()
    moving_avg = np.mean(window_values, axis=1)
    
    return moving_avg
'''
Input array: [1 2 3 4 5 6]

Window indices (each row = indices of one window):
[[0 1 2]
 [1 2 3]
 [2 3 4]
 [3 4 5]]

All windows (each row = one window):
[[1 2 3]
 [2 3 4]
 [3 4 5]
 [4 5 6]]

eventually , arr[[[0,1,2], [1,2,3], ...]]

Moving average (each value = average of a window):
[2. 3. 4. 5.]
'''


def find_closest_points(points_a:np.ndarray,points_b:np.ndarray)->tuple:
    '''
Write a function find_closest_points that takes two 2D NumPy arrays points_a and points_b, where each
row represents a point in n-dimensional space. The function should return two arrays:
closest_indices: For each point in points_a, the index of the closest point in points_b (using
Euclidean distance).
min_distances: The corresponding minimum distances for each point in points_a.
Use broadcasting to compute all pairwise distances efficiently without explicit loops.
    '''
    a_reshaped = points_a[:, np.newaxis, :]  # Same as points_a[:, None, :]
    b_reshaped = points_b[np.newaxis, :, :]  # Same as points_b[None, :, :]
    
    # Step 2: Compute squared differences (broadcasts to (m, k, n))
    squared_diff = (a_reshaped - b_reshaped) ** 2
    
    # Step 3: Sum over dimensions to get squared Euclidean distances (shape (m, k))
    squared_distances = np.sum(squared_diff, axis=2)
    
    # Step 4: Find indices of minimum squared distance (avoids sqrt for speed)
    closest_indices = np.argmin(squared_distances, axis=1)
    
    # Step 5: Compute actual Euclidean distances (sqrt of min squared distance)
    # Use advanced indexing to get min squared distance for each row
    min_squared_distances = squared_distances[np.arange(len(points_a)), closest_indices]
    min_distances = np.sqrt(min_squared_distances)
    
    return closest_indices, min_distances



oned=np.arange(10)
onere=oned.reshape(2,5)
a=np.array([[2,3],[2,1]])

aa=np.array([[2],[1]])

print(np.sort(a,axis=0))