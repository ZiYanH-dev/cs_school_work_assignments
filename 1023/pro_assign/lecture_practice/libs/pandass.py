import pandas as pd
from pandas import Series

# print(Series(range(4), index=list("1023")).loc["1":"2":2],
# Series(range(4), index=list("1023")).loc["3":"1":-2],
# Series([0, 9, 11], index=[6, 4, 2]).loc[3:],sep='\n\n')
a=pd.Series([2,3,4],index=[1,3,5])

con=Series({3:1,0:2,1:1})
co2=Series({3:2,2:2,2:4})

s1 = pd.Series({495: 42, 42: 74, 74: 495 ,495:22})
s2 = pd.Series({495: 42, 74: 495, 42: 74})

Names= ['Alice', 'Bob', 'Charlie']
Ages=[20, 21, 19]
Grades= [85, 90, 88]

df1=pd.DataFrame({'ages':Ages,'grade':Grades},index=Names)
df2=pd.DataFrame({'ages':Ages,'grade':Grades,'s':[1,2,3]},index=Names)

print(a[3])
# df1['passed']=df1['grade']>=88


# print(df1)

# print(df1.groupby('passed')[['grade','ages']].mean())