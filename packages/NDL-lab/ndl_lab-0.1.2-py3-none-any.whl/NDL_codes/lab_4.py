import numpy as n
import matplotlib.pyplot as plt
inputs=n.array([[0,0],[0,1],[1,0],[1,1]])
w1=[1,1];w2=[0,0]
f1=[];f2=[]
print("input\tfunction 1\tfunction 2")
for i in inputs:
 v1=n.exp(-n.linalg.norm(i-w1)**2)
 v2=n.exp(-n.linalg.norm(i-w2)**2)
 f1.append(v1);f2.append(v2)
for i in range(len(f1)):
 print(f"{inputs[i]}\t{f1[i]:.3f}\t\t{f2[i]:.3f}")
fig,ax=plt.subplots(figsize=(4,4))
plt.xlabel("F1")
plt.ylabel("F2")
x=n.linspace(0,1,10)
y=-x+1
ax.scatter(f1[:2],f2[:2],marker="X")
ax.scatter(f1[2:],f2[2:],marker="s")
ax.plot(x,y)
ax.set_xlim(left=-0.1)
ax.set_ylim(bottom=-0.1)
plt.show()
