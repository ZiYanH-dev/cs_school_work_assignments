import re

s='S'
pattern='([A-Z][^S])'
m=re.findall(pattern,s)
match=re.fullmatch(pattern,s)
print(m)