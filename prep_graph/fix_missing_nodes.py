#!/usr/bin/env python3

import numpy as np
import sys


def main():
    path = sys.argv[1]
    fuel = sys.argv[2]
    savefile = f"{path}/{fuel}.sorted"
    edgelist, missing = import_graph(path, fuel)
    new_edgelist = make_new_graph(edgelist, missing)
    save_graph(new_edgelist, savefile)


def save_graph(new_edgelist, savefile):
    with open(savefile, "w") as f:
        for u, v, p in new_edgelist:
            f.write(f"{u} {v} {p/1000:.3f}\n")


def make_new_graph(edgelist, missing):


    # Determine the current highest vertex number
    max_vertex = max(max(edge) for edge in edgelist)

    # Create a mapping of old vertex numbers to new vertex numbers
    #vertex_map = {old: new for new, old in enumerate(range(max_vertex + 1)) if old not in missing}
    vertex_map = dict()
    count = 0
    for old in range(max_vertex+1):
        if old in missing:
            continue
        vertex_map[old] = count
        count+=1
        
    # Create the new edgelist with updated vertex numbers
    new_edgelist = []
    for u, v, p in edgelist:
        new_u = vertex_map[u]
        new_v = vertex_map[v]
        new_edgelist.append((new_u, new_v, p))

    return new_edgelist
"""
    new_edgelist = np.copy(edgelist)
    for missed in missing:
        old_name = missed - 1
        print(missed)
        ind = np.where(new_edgelist[:,0] == old_name)[0]
        print(ind)
        new_edgelist[ind, 0] = missed
    return new_edgelist
"""

def import_graph(path, fuel):
    edgelist = []
    missing = []
    with open(path+fuel, "r") as el:
        last_u = -1
        for line in el:
            u, v, p = line.rstrip().split()
            u = int(u)
            v = int(v)
            p = int(float(p)*1000)

            if u - last_u > 1:
                missing.append(u-1)
            arr = [u,v,p]
            last_u = u
            edgelist.append(arr)
    edgelist = np.array(edgelist)
    missing = np.array(missing)
    return edgelist, missing


if __name__=="__main__":
    main()
