from collections import deque, defaultdict


class EdmondsKarp:
    def __init__(self):
        self.graph = defaultdict(list)
        self.capacity = defaultdict(lambda: defaultdict(int))
        self.flow = defaultdict(lambda: defaultdict(int))

    def add_edge(self, u, v, capacity):
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.capacity[u][v] += capacity

    def bfs(self, source, sink):
        parent = {source: None}
        queue = deque([source])

        while queue:
            current = queue.popleft()

            for next_node in self.graph[current]:
                residual_capacity = self.capacity[current][next_node] - self.flow[current][next_node]

                if next_node not in parent and residual_capacity > 0:
                    parent[next_node] = current

                    if next_node == sink:
                        bottleneck = float("inf")
                        node = sink

                        while parent[node] is not None:
                            prev = parent[node]
                            bottleneck = min(
                                bottleneck,
                                self.capacity[prev][node] - self.flow[prev][node]
                            )
                            node = prev

                        return parent, bottleneck

                    queue.append(next_node)

        return None, 0

    def max_flow(self, source, sink):
        total_flow = 0
        steps = []

        while True:
            parent, bottleneck = self.bfs(source, sink)

            if bottleneck == 0:
                break

            path = []
            node = sink

            while parent[node] is not None:
                prev = parent[node]
                self.flow[prev][node] += bottleneck
                self.flow[node][prev] -= bottleneck

                path.append((prev, node))
                node = prev

            path.reverse()
            total_flow += bottleneck
            steps.append((path, bottleneck, total_flow))

        return total_flow, steps


# Створюємо граф
network = EdmondsKarp()

source = "Джерело"
sink = "Стік"

terminals = ["Термінал 1", "Термінал 2"]
stores = [f"Магазин {i}" for i in range(1, 15)]

# Додаємо службові ребра від джерела до терміналів
# Велика пропускна здатність означає, що самі термінали не обмежені штучно
for terminal in terminals:
    network.add_edge(source, terminal, 10**9)

# Основні ребра логістичної мережі
edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),

    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),

    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),

    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),

    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),

    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

for u, v, capacity in edges:
    network.add_edge(u, v, capacity)

# Додаємо ребра від магазинів до стоку
for store in stores:
    network.add_edge(store, sink, 10**9)

# Запускаємо алгоритм Едмондса-Карпа
max_flow_value, steps = network.max_flow(source, sink)

print("Максимальний потік:", max_flow_value)
print()

print("Покроковий розрахунок:")
for i, (path, bottleneck, total) in enumerate(steps, 1):
    route = " -> ".join([path[0][0]] + [v for _, v in path])
    print(f"{i}. Шлях: {route}")
    print(f"   Доданий потік: {bottleneck}")
    print(f"   Поточний загальний потік: {total}")
    print()

# Результати потоків між терміналами та магазинами
# Для цього використовуємо фактичні шляхи, які були знайдені алгоритмом
terminal_store_flow = defaultdict(lambda: defaultdict(int))

for path, bottleneck, total in steps:
    terminal = None
    store = None

    for u, v in path:
        if u == source and v in terminals:
            terminal = v

        if u.startswith("Склад") and v.startswith("Магазин"):
            store = v

    if terminal and store:
        terminal_store_flow[terminal][store] += bottleneck

print("Таблиця потоків між терміналами та магазинами:")
print(f"{'Термінал':<15} {'Магазин':<15} {'Фактичний потік'}")

for terminal in terminals:
    for store in stores:
        print(f"{terminal:<15} {store:<15} {terminal_store_flow[terminal][store]}")


print()
print("Сумарний потік з кожного термінала:")

for terminal in terminals:
    total_from_terminal = sum(terminal_store_flow[terminal][store] for store in stores)
    print(f"{terminal}: {total_from_terminal} одиниць")


print()
print("Сумарний потік у кожен магазин:")

for store in stores:
    total_to_store = sum(terminal_store_flow[terminal][store] for terminal in terminals)
    print(f"{store}: {total_to_store} одиниць")