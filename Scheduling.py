
import heapq
import math

class Module:
    def __init__(self, name, dim, idx, delay, beta):
        self.start_t = None
        self.etd = None
        self.name = name
        self.idx = idx
        self.dim = dim
        self.delay = delay
        self.end_t = None
        self.beta=beta

    def add_etd(self, etd):
        self.etd = etd

    def add_start_time(self, start_t):
        self.start_t = start_t

    def area(self):
        return self.dim[0]*self.dim[1]

    def storage_size(self):
        return math.ceil(self.beta*self.area())

    def __lt__(self, other):
        return self.etd>other.etd
    
    def __str__(self):
        mod = {}
        mod['name'] = self.name
        mod['dim'] = self.dim
        mod['delay'] = self.delay
        mod['start_t'] = self.start_t
        mod['end_t'] = self.end_t
        mod['beta'] = self.beta
        mod['etd'] = self.etd
        return str(mod)


def _dfs_t(adj_t, v, mod_tab):
    start_t = 0
    for u in adj_t[v]:
        start_t = max(_dfs_t(adj_t, u, mod_tab), start_t)
    mod_tab[v].add_etd(start_t+mod_tab[v].delay)
    # print(mod_tab[v],v)
    return start_t+mod_tab[v].delay


def _get_crit_path(adj_t, mod_tab):
    prev = 0
    crit_path=[0]
    while len(adj_t[prev])>0:
        node = None
        for u in adj_t[prev]:
            if node is None or node.etd<mod_tab[u].etd:
                node=mod_tab[u]
            
        crit_path.append(node.idx)
        prev=node.idx
    crit_path.reverse()
    return crit_path


def _schedule(u, prev_mod, adj_t, mod_tab, Na, max_t, M, S, next, t_curr):
    possible = True
    ts={}
    ts[u]=t_curr
    
    mc=M.copy()
    sc=S.copy()

    if prev_mod is not None:
        for i in range(prev_mod.end_t+1 , t_curr):
            sc[i] += prev_mod.storage_size()
            # print((sc[i]+mc[i]), "patare")
    
    for t in range(t_curr, t_curr+mod_tab[u].delay):
        mc[t]+=mod_tab[u].area()

    q = []
    for v in adj_t[u]:
        if prev_mod is None or v!=prev_mod.idx:
            q.append(mod_tab[v])
    heapq.heapify(q)


    while len(q)>0:
        # n=len(q)
        curr_mod = heapq.heappop(q)
        curr = curr_mod.idx
        # td = curr_mod.delay

        delay_vec = []
        storage = []
        st_next = ts[next[curr]]
        t = st_next- curr_mod.delay
        delay_vec = [m+c for (m,c) in zip(mc[t:st_next], sc[t:st_next])]
        delay_vec.reverse()
        done = False
        while t>=0:
            # if len(delay_vec)==td:
    
            if t+curr_mod.delay<ts[next[curr]]:
                storage.append(sc[t+curr_mod.delay]+mc[t+curr_mod.delay])
            
            if curr_mod.area() + max(delay_vec)<=Na and (len(storage)==0 or curr_mod.storage_size() + max(storage)<=Na):
                done = True
                break
            delay_vec.pop(0)
            delay_vec.append(mc[t]+sc[t])
            t = t-1
        
        if done:
            ts[curr]=t

            for z in range(t,t+curr_mod.delay):
                mc[z]+=curr_mod.area()
            for z in range(t+curr_mod.delay , st_next):
                sc[z]+= curr_mod.storage_size()

            for child in adj_t[curr]:
                heapq.heappush(q, mod_tab[child])
        else:
            return False, None,None,None

    return True, ts , mc , sc


def schedule(adj_t, mod_tab, Na, max_t, next):
    
    N = len(adj_t)
    M = [0]*max_t
    S = [0]*max_t

    _dfs_t(adj_t, 0, mod_tab)

    crit_path = _get_crit_path(adj_t,mod_tab)

    scheduled_all = True
    # scheduled=[False]*N
    prev_mod=None
    for u in crit_path:
        curr_mod = mod_tab[u]
        
        tl = -1
        if prev_mod is not None:
            tl=prev_mod.end_t-1
        tr=max_t-curr_mod.delay

        gts={}
        gmc = []
        gsc = []
        f = False
        while tr-tl>1:
            tm = (tr+tl)//2
            possible, ts , mc,sc=_schedule(u, prev_mod, adj_t, mod_tab, Na, max_t, M, S, next, tm)
            if possible:
                gts.clear()
                gts=ts.copy()
                gmc = mc
                gsc = sc
                
                # gts[u]=tm
                tr=tm
            else:
                tl=tm
            f  = f or possible
        
        # print(curr_mod)
        # print("Storage ",gsc)
        # print("memory ", gmc)
        
        scheduled_all = scheduled_all and f

        if not scheduled_all:
            return False ,None,None

        for v, start_t in gts.items():
            mod_tab[v].start_t=start_t
            mod_tab[v].end_t = mod_tab[v].start_t + mod_tab[v].delay
        
        for i in range(max_t):
            M[i] = gmc[i]
            S[i] = gsc[i]
        prev_mod = curr_mod
    
    return (scheduled_all , M , S)





