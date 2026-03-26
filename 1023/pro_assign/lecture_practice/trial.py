import numpy as np
import pandas as pd
import os
import ast

a1=np.array([[1,2,3],[3,2,1]])
oned=np.array([1,2,3,4])
one2=np.array([1,2])
# print(a1[:,None,:]-oned[:,np.newaxis])

# print(one2[:,None])
# print(one2[None,:])

csv_path='./employees.csv'
ddf=pd.read_csv(csv_path)
ddf['Passed']=ddf['Salary']>=70000
print(ddf)
average_salary = ddf.groupby('Passed')['Salary'].mean()
print(average_salary)
ddf.to_csv('./employee_update')