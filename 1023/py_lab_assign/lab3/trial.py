questions=['The name of the product.',
   'The initial quantity of the product.',
    'The individual cost of the product.']

keys=['name','quantity','cost']
j=0
l=len(questions)
product=[]

for i in range(2):
    pro={}
    for j in range(3):
        key=keys[j]
        question=questions[j]
        pro[key]=input(question)
    product.append(pro)
print(product)
    

