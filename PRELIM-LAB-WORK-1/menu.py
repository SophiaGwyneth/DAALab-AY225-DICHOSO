import time
import os

def bubble_sort_descending(arr):
    """Sorts an array in DESCENDING order using bubble sort."""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def insertion_sort_descending(arr):
    """Sorts an array in DESCENDING order using insertion sort."""
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] < key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort_descending(arr):
    """Sorts an array in DESCENDING order using merge sort."""
    def merge_sort_helper(array):
        if len(array) <= 1:
            return array
        mid = len(array) // 2
        left = merge_sort_helper(array[:mid])
        right = merge_sort_helper(array[mid:])
        return merge(left, right)

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] >= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:]) 
        return result
    return merge_sort_helper(arr)

def read_dataset(filename):
    """Reads numbers from a file and returns them as a list."""
    try:
        with open(filename, 'r') as file:
            numbers = []
            for line in file:
                line = line.strip()
                if line:
                    try:
                        if '.' in line:
                            numbers.append(float(line))
                        else:
                            numbers.append(int(line))
                    except ValueError:
                        if ',' in line:
                            nums = [float(x.strip()) if '.' in x.strip() else int(x.strip())
                                   for x in line.split(',') if x.strip()]
                            numbers.extend(nums)
                        else:
                            nums = [float(x.strip()) if '.' in x.strip() else int(x.strip())
                                   for x in line.split() if x.strip()]
                            numbers.extend(nums)
            return numbers
    except FileNotFoundError:
        print(f"Error: File not found at path: {filename}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def display_menu():
    """Display the sorting algorithm menu."""
    print("\n" + "="*50)
    print("         SORTING ALGORITHMS MENU")
    print("="*50)
    print("1. Bubble Sort (Descending)")
    print("2. Insertion Sort (Descending)")
    print("3. Merge Sort (Descending)")
    print("4. Exit")
    print("="*50)

def perform_sort(data, choice):
    """Perform the selected sorting algorithm and display results."""
    data_copy = data.copy()
    start_time = time.perf_counter()
    
    if choice == 1:
        sort_name = "Bubble Sort"
        sorted_data = bubble_sort_descending(data_copy)
    elif choice == 2:
        sort_name = "Insertion Sort"
        sorted_data = insertion_sort_descending(data_copy)
    elif choice == 3:
        sort_name = "Merge Sort"
        sorted_data = merge_sort_descending(data_copy)
    else:
        return
    
    end_time = time.perf_counter()
    time_taken = end_time - start_time
   
    print(f"\n{sort_name} - SORTING COMPLETE!\n")
    print("Sorted elements (descending order):")
    print(sorted_data)
   
    print(f"\n{'='*50}")
    print(f"Algorithm: {sort_name}")
    print(f"Time taken: {time_taken:.6f} seconds")
    print(f"Total elements sorted: {len(sorted_data)}")
   
    is_sorted = all(sorted_data[i] >= sorted_data[i+1] for i in range(len(sorted_data)-1))
    print(f"Verification: {'✓ CORRECT!' if is_sorted else '✗ FAILED!'}")
    print("="*50)

# Main program
if __name__ == "__main__":
    # DYNAMIC PATH RESOLUTION:
    # This finds the folder where menu.py lives and looks for dataset.txt there.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(base_dir, "dataset.txt")
    
    print(f"Attempting to read data from: {filename}")
   
    data = read_dataset(filename)
   
    if data:
        print(f"Dataset loaded: {len(data)} elements")
        while True:
            display_menu()
            try:
                choice = int(input("\nEnter your choice (1-4): "))
                if choice == 4:
                    print("\nExiting program...")
                    break
                elif choice in [1, 2, 3]:
                    perform_sort(data, choice)
                else:
                    print("\nInvalid choice! Please select 1-4.")
            except ValueError:
                print("\nInvalid input! Please enter a number.")
            except KeyboardInterrupt:
                break
    else:
        print("Failed to read data. Please ensure 'dataset.txt' is in the same folder as this script.")