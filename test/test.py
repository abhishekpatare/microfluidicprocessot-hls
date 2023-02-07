from Scheduling import Module , schedule ,_get_crit_path,_dfs_t
import random
import time
import json


test_case = input("Enter path to test file : ")
Na = int(input("Enter max chip size : "))
max_t = int(input("Enter maximum time to schedule : "))

test_case = open(test_case)
data = json.load(test_case)

N = data['module_count']
mod_tab = [None]*N
next = [0]*N
adj_t = []
for _ in range(0,N):
    adj_t.append([])
i = 0
for mod in (data['module_list']):
    mod_tab[i] = Module(name=mod['name'],dim = mod['dim'],idx =i ,delay=mod['delay'],beta=0.25 )
    next[i] = mod['next']
    if next[i]!=-1:
        adj_t[next[i]].append(i)
    i+=1

# for mod in mod_tab:
#     print(mod)


(done, M , S) = schedule(adj_t,mod_tab,Na,max_t,next)

crit_path = _get_crit_path(adj_t, mod_tab)
print(crit_path)

print(M)

if done:

    total_cells = [m+s for  ( m , s) in (zip(M,S))]

    print("total_cells",total_cells)

    ts = int(time.time()/(1000))
    file1 = open('timestamps.csv','w+')
    file1.write('Task,Start,Finish\n')

    for mod in mod_tab:
        file1.write(f'{mod.name},{mod.start_t},{mod.end_t}\n')
    file1.close()

    file2 = open('storage.csv','w+')


    file2.write("Time,M,S,Total\n")
    for i ,(m,s) in enumerate(zip(M,S)):
        file2.write(f'{i},{m},{s},{m+s}\n')
    file2.close()
else:
    print("Not schedulable under current constraints")

