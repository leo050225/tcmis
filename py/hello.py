def square(y):
  print("{} 的平方為 {}".format(y, y*y)) 


x = int(input("請輸入一個正整數："))
if (x<=0):
	print(f"您輸入的值是{x}小於等於0")
else:
	print(f"您輸入的值是{x}大於0")
	for i in range(1, x+1):
		#print(i, end = ";")
            square(i)