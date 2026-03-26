'''4 car doors. Car Part	Price ($)
                        A Car Door	55.5
                        A Car Wheel	20
                        A Tire	15.3
                        A Set of lights	10.16
                        An Engine	150
                      A Steering Wheel	40
4 wheels
4 tires
2 sets of lights
1 engine
1 steering wheel
Even though you know he definitely missed some parts, you decided to just go with it, and looked at the pricing of the car parts he provided:


'''

def main():
    num=int(input('Enter the number of cars:'))
    total_cost=calculate(num)
    print(f'The total cost will be: ${total_cost}')

def get_prize():
    sum=4*55.5+4*20+4*15.3+2*10.16+150+40
    return sum
def calculate(num):
    total=0
    for _ in range(num):
        total+=get_prize()
    return total
    

if __name__=="__main__":
    main()