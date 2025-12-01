
# --- HÀM ĐỌC MA TRẬN KỀ TỪ FILE TXT ---
def read_adj_matrix(path):
    G = []
    with open(path, "r") as f:
        for line in f:
            row = list(map(int, line.strip().split()))
            G.append(row)
    return G


# --- THUẬT TOÁN TÔ MÀU ĐỒ THỊ WELSH–POWELL ---
def color_graph(G, node_names=None):
    n = len(G)

    # Nếu không có tên đỉnh → tự sinh A, B, C,...
    if node_names is None:
        node_names = [chr(65 + i) for i in range(n)]

    # Ánh xạ tên đỉnh → vị trí trong ma trận
    index = {node_names[i]: i for i in range(n)}

    # Tính bậc từng đỉnh
    degree = [sum(G[i]) for i in range(n)]

    # Mỗi đỉnh ban đầu có 4 màu khả dụng
    color_dict = {node_names[i]: ["Blue", "Red", "Yellow", "Green"] for i in range(n)}

    # Sắp xếp đỉnh theo bậc giảm dần
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

    # --- TIẾN HÀNH TÔ MÀU ---
    solution = {}

    for node in sorted_nodes:
        available_colors = color_dict[node]
        chosen_color = available_colors[0]     # lấy màu đầu tiên hợp lệ
        solution[node] = chosen_color          # lưu kết quả

        # Cập nhật màu cho các đỉnh kề
        for j in range(n):
            if G[index[node]][j] == 1:         # nếu đỉnh j kề với node
                neigh_name = node_names[j]
                if chosen_color in color_dict[neigh_name]:
                    color_dict[neigh_name].remove(chosen_color)

    return solution


# --- HÀM VẼ ĐỒ THỊ (SỬ DỤNG NETWORKX) ---
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G, solution, node_names):
    graph = nx.Graph()

    # Thêm đỉnh
    for node in node_names:
        graph.add_node(node)

    # Thêm cạnh dựa vào ma trận kề
    n = len(G)
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j] == 1:
                graph.add_edge(node_names[i], node_names[j])

    # Lấy màu đã tô
    node_colors = [solution[node] for node in node_names]

    # Vẽ đồ thị
    plt.figure(figsize=(7, 7))
    nx.draw(
        graph,
        with_labels=True,
        node_color=node_colors,
        node_size=1500,
        font_size=16,
        font_weight='bold'
    )
    plt.title("Đồ thị sau khi tô màu (Thuật toán Welsh–Powell)")
    plt.show()


# --- CHẠY TRỰC TIẾP ---
if __name__ == "__main__":
    # Đọc ma trận từ file
    matrix = read_adj_matrix("matrix.txt")

    # Tạo tên đỉnh A, B, C...
    node_names = [chr(65+i) for i in range(len(matrix))]

    # Tô màu
    result = color_graph(matrix, node_names)

    print("===== KẾT QUẢ TÔ MÀU =====")
    for node, color in sorted(result.items()):
        print(f"{node} → {color}")

    # Vẽ đồ thị
    draw_graph(matrix, result, node_names)
