'''
A Car Door	8
A Car Wheel	5.8
A Tire	5
A Set of lights	10.5
An Engine	20
A Steering Wheel	12.7
'''

def main():
    num=int(input('Enter the number of cars:'))
    total_time=calculate(num)
    print(f'The total time taken will be: {total_time:.2f} second(s)')
    
def get_time():
    sum=4*8+4*5.8+4*5+2*10.5+20+12.7
    return sum
def calculate(num):
    extra=30
    spray_print_time=extra*num
    total=0
    for _ in range(num):
        total+=get_time()
    total+=spray_print_time
    return total
    

if __name__=="__main__":
    main()