
# Hàm đọc ma trận kề từ file txt
def read_adj_matrix(path):
    G = []
    with open(path, "r") as f:
        for line in f:
            row = list(map(int, line.strip().split()))
            G.append(row)
    return G

# Thuật toán tô màu đồ thị theo phương pháp chọn bậc cao nhất
def color_graph(G, node_names=None):
    n = len(G)

    # Nếu không cung cấp tên thì tự gán A, B, C,...
    if node_names is None:
        node_names = [chr(65 + i) for i in range(n)]

    index = {node_names[i]: i for i in range(n)}

    # Tính bậc từng đỉnh
    degree = [sum(G[i]) for i in range(n)]

    # Màu có thể dùng
    color_dict = {node_names[i]: ["Blue", "Red", "Yellow", "Green"] for i in range(n)}

    # Sắp xếp theo bậc giảm dần
    sorted_nodes = []
    chosen = []
    for _ in range(n):
        max_deg = -1
        pos = -1
        for j in range(n):
            if j not in chosen and degree[j] > max_deg:
                max_deg = degree[j]
                pos = j
        chosen.append(pos)
        sorted_nodes.append(node_names[pos])

    # Tô màu
    solution = {}
    for node in sorted_nodes:
        available_colors = color_dict[node]
        chosen_color = available_colors[0]
        solution[node] = chosen_color

        # Cập nhật các đỉnh kề
        for j in range(n):
            if G[index[node]][j] == 1:
                neigh_name = node_names[j]
                if chosen_color in color_dict[neigh_name]:
                    color_dict[neigh_name].remove(chosen_color)

    return solution

# ------------------ DEMO CHẠY -------------------
if __name__ == "__main__":
    matrix = read_adj_matrix("matrix.txt")
    result = color_graph(matrix)

    print("===== KẾT QUẢ TÔ MÀU =====")
    for node, color in sorted(result.items()):
        print(f"Đỉnh {node} → {color}")
