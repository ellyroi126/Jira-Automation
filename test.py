a = int(input('What do you have left in Php: '))
b = int(input('What do you have left in Yen: '))
c = int(input('What do you have left in Euro: '))

php = a/54.76
yen = b/131.83
euro = c/0.93

output = php + yen + euro

print('You have a total of ', output ,' USD')
print(php)
print(yen)
print(euro)