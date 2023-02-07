import heapq
import math

class Module:
    def __init__(self, name, dim, idx, delay, s_window):
        self.start_t = None
        self.etd = None
        self.name = name
        self.idx = idx
        self.dim = dim
        self.delay = delay
        self.end_t = None
        self.s_window=s_window

    def add_etd(self, etd):
        self.etd = etd

    def add_start_time(self, start_t):
        self.start_t = start_t

    def area(self):
        return self.dim[0]*self.dim[1]

    def s_window_size(self):
        return self.s_window[0]*self.s_window[1]

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
        mod['etd'] = self.etd # this is the min time window required to schedule current module
        return str(mod)


def _dfs_t(adj_t, v, mod_tab):

    """
    This dfs call sets the etd for each module in bioprotocol
    """

    start_t = 0
    for u in adj_t[v]:
        start_t = max(_dfs_t(adj_t, u, mod_tab), start_t)
    mod_tab[v].add_etd(start_t+mod_tab[v].delay)
    return start_t+mod_tab[v].delay


def _get_crit_path(adj_t, mod_tab):

    """
    Generate critical path in adj and returns list of nodes in critical path
    """
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

    """
    This call schedules the critpath i and all its requirements
    u = index of current critical path node
    prev_mod = module previous to critpath[u]
    """

    possible = True
    ts={}   #start times of modules scheduled in this call
    ts[u]=t_curr
    
    mc=M.copy() #local deep copy of M
    sc=S.copy() #local deep copy of S  

    #update s_window upon scheduling critpath[u]
    if prev_mod is not None:
        for i in range(prev_mod.end_t+1 , t_curr):
            sc[i] += prev_mod.s_window_size()
    
    #update cells ussed by active module upon scheduling critpath[u]
    for t in range(t_curr, t_curr+mod_tab[u].delay):
        mc[t]+=mod_tab[u].area()

    q = [] #priority queue for requirements
    for v in adj_t[u]:
        if prev_mod is None or v!=prev_mod.idx:
            q.append(mod_tab[v])
    heapq.heapify(q)


    while len(q)>0:
        curr_mod = heapq.heappop(q)
        curr = curr_mod.idx

        
        st_next = ts[next[curr]] #start time of next of curr mod in dag
        t = st_next- curr_mod.delay

        m_window = []
        s_window = []

        m_window = [m+c for (m,c) in zip(mc[t:st_next], sc[t:st_next])]
        m_window.reverse()

        done = False
        while t>=0:    

            if t+curr_mod.delay<ts[next[curr]]:
                s_window.append(sc[t+curr_mod.delay]+mc[t+curr_mod.delay])
            

            #checking  m and s requirements for current module
            if curr_mod.area() + max(m_window)<=Na and (len(s_window)==0 or curr_mod.s_window_size() + max(s_window)<=Na):
                done = True
                break
            
            m_window.pop(0)
            m_window.append(mc[t]+sc[t])

            t = t-1
        
        if done:
            ts[curr]=t

            #update mc and sc upon succesful scheduling  of current module
            for z in range(t,t+curr_mod.delay):
                mc[z]+=curr_mod.area()
            for z in range(t+curr_mod.delay , st_next):
                sc[z]+= curr_mod.s_window_size()

            #push all prerequisits of current module
            for preq in adj_t[curr]:
                heapq.heappush(q, mod_tab[preq])
        else:
            return False, None,None,None

    return True, ts , mc , sc


def schedule(adj_t, mod_tab, Na, max_t, next):
    
    N = len(adj_t)
    M = [0]*max_t           #M[t] = cells occupied by active modules at time t
    S = [0]*max_t           #S[t] = cells occupied for storage at time t

    _dfs_t(adj_t, 0, mod_tab)

    crit_path = _get_crit_path(adj_t,mod_tab)

    scheduled_all = True
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
        scheduled_critpath_u = False
        while tr-tl>1:
            tm = (tr+tl)//2
            possible, ts , mc,sc=_schedule(u, prev_mod, adj_t, mod_tab, Na, max_t, M, S, next, tm)
            if possible:
                gts.clear()
                gts=ts.copy()
                gmc = mc
                gsc = sc 
                tr=tm
            else:
                tl=tm
            sheduled_critpath_u  = scheduled_critpath_u or possible
        
        scheduled_all = scheduled_all and scheduled_critpath_u

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





