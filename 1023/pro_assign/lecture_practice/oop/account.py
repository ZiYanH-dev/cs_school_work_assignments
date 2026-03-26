class Account:
    num_account=0
    def __init__(self,balance=100,monlyInterestRate=0,id=0):

        self.__id=id
        self.__balance=balance
        self.__monlyInterestRate=monlyInterestRate
        self._name='114'
        Account.num_account+=1
    
    def getAnnualInterestRate(self):
        return self.__monlyInterestRate*12

    def getAnnualInterest(self):
        return self.getAnnualInterestRate()*self.__balance

    def get_stats(self):
        return{
            'id':self.__id,
            'balance':self.__balance,
            'mir':self.__monlyInterestRate
        }

    def set_attributes(self,**args):
        attribute_mapping = {
            'id': '_Account__id',          # "id" → internal __id
            'balance': '_Account__balance',# "balance" → internal __balance
            'mir': '_Account__monlyInterestRate' # "mir" → internal __monlyInterestRate
        }

        for key,value in args.items():
            if key not in attribute_mapping:
                print(f'{key} does not exisit')
            else:
                actual_attribute=attribute_mapping[key]
                setattr(self,actual_attribute,value)
            
    def withdraw(self,amount):
        if self.__balance>amount:
            print(f'u withdraw {amount} successfully')
            self.__balance-=amount
        else:
            print('no money')

    def deposit(self,amount):
        self.__balance+=amount
        print(f'u deposit {amount} successfully')

    def __str__(self):
        return str(self.get_stats())

a=Account(id=1122,balance=20000,monlyInterestRate=0.023)

print(a)
a.set_attributes(id=11141)
print(a)