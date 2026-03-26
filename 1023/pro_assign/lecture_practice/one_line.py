from functools import reduce
import heapq

def top_k_frequent(arr,target):
    return set(sorted([x for x in arr if arr.count(x)>=target]))

def rotate_list_right(nums,k):
    #shift each element of arr to the right by k
    k %= len(nums)  # Fix for k larger than list length
    return nums[-k:] + nums[:-k]
    
def rotate_list_left(nums,k):
    #shift each element of arr to the left by k
    k %= len(nums)  
    return nums[k:] + nums[:k]

def merge_two_sorted_list(arr1,arr2):
    return list(heapq.merge(arr1, arr2))

def find_missing_number(arr):
    return sum([i for i in range(min(arr),max(arr)+1)])-sum(arr)

def group_by_length(arr:list[str]):
    return {length: [s for s in arr if len(s) == length] for length in set(len(s) for s in arr)}
 
def transpose(arr):
    #e.g [[1,2],[4,5]]-> [[1,4],[2,5]]
    return [[row[i] for row in arr] for i in range(len(arr[0]))]


def product_except_self(nums):
    return [reduce(lambda a,b: a*b, nums[:i] + nums[i+1:]) for i in range(len(nums))]

def is_valid_parentheses(s: str) -> bool:
    return len( reduce(
        lambda stack, c: stack[:-1] if stack and stack[-1] + c in {"()", "{}", "[]"} else stack + [c],
        s,
        []  # Initial value: empty stack
        ) ) == 0

def search_insert_position(arr,target):
    return next(
        (i for i in range(1, len(arr)) if arr[i-1] < target <= arr[i]),
        len(arr) if target > arr[-1] else 0
    )
'''
The generator looks for i where arr[i-1] < target <= arr[i] (your original condition).
If the generator finds such an i, next() returns it.
If not:
If target > arr[-1] → default to len(arr).
Else (target <= arr[0]) → default to 0.

'''

def reverse_words_in_str(s:str):
    return ''.join(s.split()[::-1])

def count_uppercase_letters(s: str) -> int:
    return sum(1 for c in s if c.isupper())

def remove_duplicates(arr):
    return [x for i,x in enumerate(arr) if x not in arr[:i]]

def main():
    sample_list=[4,2,1,2,1,3]
    two_d=[[1,2],[4,5]]
    print(transpose(two_d))
    print(list(zip(*two_d)))

    
if __name__=='__main__':
    main()

    

