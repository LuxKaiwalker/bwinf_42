def bron_kerbosch(graph):
    def bron_kerbosch_recursive(R, P, X):
        if not P and not X:
            cliques.append(R)
            return
        for v in list(P):
            bron_kerbosch_recursive(R.union({v}), P.intersection(graph[v][0]), X.intersection(graph[v][0]))
            P.remove(v)
            X.add(v)

    cliques = []
    vertices = set(graph.keys())
    bron_kerbosch_recursive(set(), vertices, set())
    return cliques

# Example usage:
if __name__ == "__main__":
    # Example graph in dictionary format
    graph = {1: [[2, 3, 4, 5, 6, 8, 10], [17, 0, 59, 33, 0]], 2: [[1, 3, 4, 8, 10], [0, 0, 51, 0, 0]], 3: [[1, 2, 4, 10], [0, 49, 0, 58, 0]], 4: [[1, 2, 3, 10], [0, 32, 0, 50, 0]], 5: [[1, 6, 10], [0, 20, 0, 0, 0]], 6: [[1, 5, 10], [59, 0, 0, 0, 0]], 7: [[9, 10], [38, 0, 0, 0, 0]], 8: [[1, 2, 10], [33, 0, 11, 0, 0]], 9: [[7, 10], [0, 37, 38, 0, 0]], 10: [[1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 0, 0, 13, 102]]}
    
    result = bron_kerbosch(graph)
    print("Cliques:", result)
