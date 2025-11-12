import heapq

def dijkstra(graph, start, end):
    if start not in graph or end not in graph:
        return None, float("inf")

    dist = {node: float("inf") for node in graph}
    prev = {}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if u == end:
            break
        if d > dist[u]:
            continue
        for v, w in graph[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    if dist[end] == float("inf"):
        return None, float("inf")

    path = [end]
    while path[-1] != start:
        path.append(prev[path[-1]])
    path.reverse()
    return path, dist[end]

def transport_suggestion(distance):
    if distance <= 300: return "Road Cargo (Mini Truck)"
    if distance <= 1000: return "Road Freight (Long Haul Truck)"
    if distance <= 1800: return "Rail Freight"
    return "Air Cargo"

def reliability_score(path):
    if not path: return "Low"
    hops = max(0, len(path) - 1)
    if hops <= 3: return "High"
    if hops <= 5: return "Medium"
    return "Low"