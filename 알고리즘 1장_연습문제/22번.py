import queue

instr=input("문자열 입력 : ")
s=queue.LifoQueue()

for ch in instr :
    s.put(ch)

print("역순 문자열", end="")
while not s.empty() :
    print (s.get(), end="")
print()