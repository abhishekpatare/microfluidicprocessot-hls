from Scheduling import Module , schedule ,_get_crit_path,_dfs_t
import random
import time

N = 11
Na = 150
max_t = 35

delays = list(map(int , input().split()))
dimx = []
for _ in range(11):
    dimx.append(list(map(int , input().split())))

mod_tab = []
for i in range(0,N):
    name = "M" + str(i)
    dim = dimx[i]
    beta = 0.25
    idx = i
    delay = delays[i]
    mod = Module(name=name , dim=dim,idx=idx,delay=delay,beta=beta)
    mod_tab.append(mod)

next = [0]*N
adj_t = []

for _ in range(0,N):
    adj_t.append([])

for _ in range(0,N-1):
    u , v = map(int , input().split())
    next[u]=v
    adj_t[v].append(u)

# print(next)

# print("*"*20)
# print("*"*20)
# for mod in mod_tab:
#     print(mod)

# print("*"*20)
# print("*"*20)

# _dfs_t(adj_t,0,mod_tab)

 
# for mod in mod_tab:
#     print(mod)

# print("*"*20)
# print("*"*20)



(done, M , S) = schedule(adj_t,mod_tab,Na,max_t,next)





crit_path = _get_crit_path(adj_t, mod_tab)

print(crit_path)

print("*"*20)
print("*"*20)

for mod in mod_tab:
    print(mod)

if done:

    total_cells = [m+s for  ( m , s) in (zip(M,S))]

    print("total_cells",total_cells)

    ts = int(time.time()/(1000))
    file1 = open(f'D:\\lbp\\timestamps_{ts}.csv','w+')
    file1.write('task,Start,Finish\n')

    for mod in mod_tab:
        file1.write(f'{mod.name},{mod.start_t},{mod.end_t}\n')
    file1.close()

    file2 = open(f'D:\\lbp\\storage_{ts}.csv','w+')


    file2.write("Time,M,S,Total\n")
    for i ,(m,s) in enumerate(zip(M,S)):
        file2.write(f'{i},{m},{s},{m+s}\n')
    file2.close()
else:
    print("Not schedulable under current constraints")

