def main():
    """
    Main function to run the point-of-sale program.
    """
    # Task 1: Get product information from user input
    # In this task, you need to define six variables that holds the two products' names, quantities and costs.
    # The values of these variables should be acquired via user input and type conversions.
    # You can assume the input is always valid, i.e. type conversions should not raise an error.
    # The variables should be as follows:
    # `product1_name` (string): The name of the first product.
    # `product1_qty` (integer): The initial quantity of the first product.
    # `product1_cost`  (float): The individual cost of the first product.
    # `product2_name` (string): The name of the second product.
    # `product2_qty` (integer): The initial quantity of the second product.
    # `product2_cost`  (float): The individual cost of the second product.
    # --- TODO below ---

    questions=['The name of the product.',
   'The initial quantity of the product.',
    'The individual cost of the product.']
    keys=['Name','Quantity','Cost']

    l=len(questions)
    first={}
    second={}
    product=[]
    product.append(first)
    product.append(second)
    
    for pro in product:
        for i in range(l):
            key=keys[i]
            question=questions[i]
            value=input(question)
            if key=='Name':
                value=str(value)
            elif key=='Quantity':
                value=int(value)
            elif key=='Cost':
                value=float(value)
            pro[key]=value
    print(product)

    


    # --- TODO above ---
    
    # Task 2: Calculate the total cost of one kind of item.
    # For each product, calculate the total cost by multiplying its quantity and cost.
    # --- TODO below ---
    cost=[0, 0]
    i=0
    for pro in product:
        sum=pro['Quantity']*pro['Cost']
        cost[i]=sum
        i+=1

    first_cost,second_cost=cost
    print(f'sum of the first is{first_cost} ')
    print(f'sum of the second is{second_cost} ')
        
        
        


    # --- TODO above ---

    # Task 3: Calculate the total cost of both items.
    # Calculate the total cost of both products by summing up their individual total costs.
    # --- TODO below ---
    total_cost=sum(cost)

    # --- TODO above ---

    # Task 4: Display the product information and total cost
    # In this task, you are required to output some basic calculated values using the `print()` function.
    # For example, if you have:
    # Name: Apple,  Quantity: 2, Cost: $5
    # Name: Banana, Quantity: 5, Cost: $8
    # Then you should try to write code so that the output is:
    # Number of Apple bought: 2
    # Cost of Apple: $5
    # Number of Banana bought: 5
    # Cost of Banana: $8
    # Total cost: $50
    # --- TODO below ---

    # --- TODO above ---

if __name__ == "__main__":
    main()
