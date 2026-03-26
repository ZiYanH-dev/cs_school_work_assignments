import random

sample_list=[4,2,1,2,1,3]


def printnum(n=0,upper=42):
    if n>upper:
        return
    print(n)
    printnum(n+1)

def printnum_reverse(n=0):
    #print from 0 to 42
    #then from 42 to 0
    if n>42:
        print()
        return
    print(n)
    printnum_reverse(n+1)
    print(n)

def sum_of_digits(n):
    if n<=0:
        return 0
    return n%10+sum_of_digits(n//10)

def super_digit(n:int):
    '''
    Given a number as a string, compute its super digit (sum of digits recursively until a single digit remains). 
    For example, super digit of "9875" is 9+8+7+5=29 → 2+9=11 → 1+1=2.
    '''

    if n<10:
        return n
    n=sum(int(c) for c in str(n))
    return super_digit(n)

def gcd(a, b):
    '''
    By definition, a % b is the remainder when a is divided by b. Mathematically, we can express a as:a = q * b + r

    suppose d is a common divisor of a and b. This means:
    a = d * k for some integer k (since d | a),
    b = d * m for some integer m (since d | b).
    Substitute these into the equation a = q * b + r: d * k = q * (d * m) + r
    Rearrange to solve for r:r = d * k - q * d * mr = d * (k - q * m)
    Since k, q, and m are integers, (k - q * m) is also an integer. This means r is a multiple of d, so d | r (i.e., d divides a % b).
    Thus, if d divides a and b, it must also divide b and r = a % b.
    Proof Step 2: If d divides b and a % b, then d divides a
    Now, let’s reverse it. Suppose d divides b and 
    '''
    #greatest common divisor
    # Base case: if b is 0, return a

    if b == 0:
        return a
    # Recursive step: gcd(a, b) = gcd(b, a % b)
    else:
        return gcd(b, a % b)

def handshake(n: int) -> int:
    if n <= 1: # Base case
        return 0 # No one to shake hands
    return handshake(n-1) + (n-1) # General case

def reverse_str(s:str)->str:
    if len(s)==1:
        return s
    return s[-1]+reverse_str(s[:-1])

def reverse_str_another(s):
    if len(s)==0:
        return ''
    remain=reverse_str_another(s[1:])
    return remain+s[0]

def reverse_arr(arr,left=0,right=None):
    if right==None:
        right=len(arr)-1
    if left>right:
        return arr
    
    arr[left],arr[right]=arr[right],arr[left]
    left+=1
    right-=1
    arr=reverse_arr(arr,left,right)
    return arr

def check_palidrome(s:str):
    if len(s)<=1:
        return True
    return s[0]==s[-1]and check_palidrome(s[1:-1])

def check_sorted(arr):
    if len(arr)<=1:
        return True
    return arr[0]<=arr[1] and check_sorted(arr[1:])

def remove_all_occurences(s:str,target:str)->str:
    #remove occurence of target is equal to concatenate
    #ones that are unequal to target
    if len(s)==1:
        return s[0]if s[0]!=target else ''
    if s[0]==target:
        return remove_all_occurences(s[1:],target)
    else:
        return s[0]+remove_all_occurences(s[1:],target)
    
def find_max(arr:list[int]):
    if not arr:
        return 0
    return max(arr[0],find_max(arr[1:]))

def find_smallest(numbers):
    # Base case: list with one element
    if len(numbers) == 1:
        return numbers[0]
    # Recursive case: compare first element with smallest of the rest
    else:
        smallest_of_rest = find_smallest(numbers[1:])
        return numbers[0] if numbers[0] < smallest_of_rest else smallest_of_rest

def Floor_Division(a,b):
    #find a//b
    #count the number of times we substract the divisor
    if a>=b:
        remain=a-b
        return 1+ Floor_Division(remain,b)
    else:
        return 0

def power_calculation(a,b):
    #equivalent to a^b
    if b>0:
        return a*power_calculation(a,b-1)
    else:
        return 1 

def number_guess(secret=random.randint(1,100)):
    guess=int(input('guess a number\n'))
    if guess==secret:
        print('u win')
        return
    elif guess<secret:
        print('low')
    else:
        print('high')
    number_guess(secret)

def calculator(s:str=None)->int:
    '''
    The program receives a user input, which is essentially a string with the following interleave elements,
    separated by a space ( ):
    a non-negative integer (e.g., 0, 1, 2),
    an operator (+ and *),
    For example, valid inputs are:

    1 + 1  # = 2
    1 + 2 * 3  # = 7
    1 + 2 * 3 + 4  # = 11
    1 * 2 * 3 + 4 * 5 * 6  # = 126
    1 + 2 + 3 * 4 + 5 + 6  # = 26
    Write a program that calculates the correct result by respecting the order of operations (calculate + after *).
    '''
    
    if not s:
        s=input('enter a str that is math quzz\n')
    if ' 'in s:
        s=s.replace(' ','')
    if s.isdigit():
        return int(s)

    index=-1
    result=0
    # * first then +
    if '*' in s:
        index=s.index('*')
    elif '+' in s:
        index=s.index('+')

    if index!=-1:
        #get the index to the left and right of our symbol
        #which we use to get the actual number we then use to calculate
        i,j=index-1,index+1
        match s[index]:
            case '*':
                result=int(s[i])*int(s[j])
            case '+':
                result=int(s[i])+int(s[j])
        result=str(result)
        #str is immutable,it cannot be modifyed in place
        #so we can only assign value to it
        s=s.replace(s[i:j+1],result)
    return calculator(s)

def calculator2(s:str):
    '''
    another version of the above one
    '''
    if s.isdigit():
        return int(s)
    
    if s.find('+')!=-1:
        parts=s.split('+')
        return sum(calculator2(part)for part in parts)
    if s.find('*')!=-1:
        result=1
        parts=s.split('*')
        for part in parts:
            result*=calculator2(part)
        return result
    
def count_occurence(arr,target):
    #count number of times target appears in arr
    if not arr:
        return 0
    if arr[0]==target:
        return 1+count_occurence(arr[1:],target)
    else:
        return count_occurence(arr[1:],target)
    
def binary_search_exisits(arr:list[int],target:int):
    #arr is sorted
    #if element exisits
    if not arr:
        return False
    
    mid=len(arr)//2
    if arr[mid]==target:
        return True
    elif arr[mid]<target:
        return binary_search_exisits(arr[mid+1:],target)
    else:
        return binary_search_exisits(arr[:mid],target)

def binary_search(arr,target,left=0,right=None,):
    #return the index of target
    if right==None:
        right=len(arr)-1
    if left >right:
        return -1
    
    mid=(right+left)//2
    if arr[mid]==target:
        return mid
    elif arr[mid]<target:
        left=mid+1
        return binary_search(arr,target,left,right)
    else:
        right=mid-1
        return binary_search(arr,target,left,right)

def check_substr(target: str, sub: str, n: int) -> bool:
    '''
    Write a recursive program that checks if a substring sub appears in a string target at least n
    times. You can assume target and sub are non-empty, and n is non-negative.
    '''
    #each time we compare the first substring of target of len n with sub
    if n==0:
        return True
    elif len(target)<len(sub):
        return False
    if target.startswith(sub):
        return check_substr(target[1:],sub,n-1)
    return check_substr(target[1:],sub,n)

def find_int(n:int)->list[int]:
    '''
A strictly-increasing integer means every digit in the number is greater than its preceding digit.
Write a recursive program find_int() that creates all strictly increasing integers with digits 1
to 9 of length n. You can assume n is always positive.
    '''
    if n<1 or n>9:
        return []
    result=[]

    def backtrack(current_num,numOfDigits_used=1):
        if numOfDigits_used==n:
            result.append(current_num)
            return
        
        last_digit=current_num%10
        start=last_digit+1
        for new_digit in range(start,10):
            new_num=current_num*10+new_digit
            backtrack(new_num,numOfDigits_used+1)
    for i in range(1,10):
        backtrack(i)
    return result

def permutation(arr):
    result=[]
    n=len(arr)
    used=[False]*n
    def backtrack(current,used):
        if len(current)==n:
            result.append(current.copy())
            return 
        for i in range(n):
            if not used[i]:
                current.append(arr[i])
                used[i]=True
                backtrack(current,used)
                current.pop()
                used[i]=False

    backtrack([],used=used)
    return result

def power_set(arr):
    'All Subsets of a Set'
    re=[]

    def backtrack(index=0,temp=[]):
        if index>=len(arr):
            re.append(temp.copy())
            return
        temp.append(arr[index])
        backtrack(index+1,temp)
        temp.pop()
        backtrack(index+1,temp)

    backtrack()
    return re

def main():
    sample_str='abcdbbbabc'
    sorted_list=[1,2,2,3,4]
    sample_string='wewewsa'
    print(permutation(sorted_list))


if __name__=='__main__':
    main()