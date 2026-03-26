piority={
        'Lift 1':0,
        'Lift 2':0,
        'Lift 3':0
    }

def main():
    lift_1_floor = input("Current floor of lift 1 (G/10): ").strip()
    lift_1_status = input("Status of lift 1 (moving up/moving down/stopped): ").strip()
    lift_2_floor = input("Current floor of lift 2 (G/10): ").strip()
    lift_2_status = input("Status of lift 2 (moving up/moving down/stopped): ").strip()
    lift_3_floor = input("Current floor of lift 3 (G/10): ").strip()
    lift_3_status = input("Status of lift 3 (moving up/moving down/stopped): ").strip()

    lifts=[
        {'Lift 1':(lift_1_floor,lift_1_status)},
        {'Lift 2':(lift_2_floor,lift_2_status)},
        {'Lift 3':(lift_3_floor,lift_3_status)}
        ]
    
    get_score(lifts)
    #sort the dict based on both score
    #if there is tie, sort them based on number after lift
    sorted_dict=dict(sorted(piority.items(),key=lambda x: (x[1], int(x[0].split()[1]))))
    sorted_list=list(sorted_dict.keys())
    winner=sorted_list[0]
    print('Result:')
    print(f'{winner} will come to pick you up.') 

def get_score(lifts):
    '''
    each lift in lifts is a dic with key being current lift and value being the tuple containing floor and status
    get the score of each lift and update the dic named piority
    '''
    for lift in lifts:
        for key in lift:
            floor,status=lift[key]
            score=114514
            match floor:
                case 'G':
                    if status=='moving down':
                        score=1
                    elif status=='moving up':
                        score=6
                    elif status=='stopped':
                        score=2
                    else:
                        score=99999999
                        print('ru fkin serious rn?')
                case '10':
                    #value we get from input function is always a string
                    if status=='moving up':
                        score=5
                    elif status=='stopped':
                        score=4
                    elif status=='moving down':
                        score=3
                    else:
                        score=114154
                        print('get tf out')
                case _:
                    print('invalid')
                    
            piority[key]=score

if __name__=='__main__':
    main()
                
