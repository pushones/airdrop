import asyncio
import json
from curl_cffi import requests

import os

# os.environ['HTTP_PROXY'] = "http://127.0.0.1:10808"
# os.environ['HTTPS_PROXY'] = "http://127.0.0.1:10808"

import matplotlib.pyplot as plt
from collections import deque
WEST = 8
SOUTH = 4
EAST = 2
NORTH = 1

def get_neighbors(maze, row, col):
    neighbors = []
    rows = len(maze)
    cols = len(maze[0])
    # 检查北方向（修正掩码后）
    if row > 0 and not (maze[row][col] & NORTH):
        neighbors.append((row - 1, col))
    # 检查南方向
    if row < rows - 1 and not (maze[row][col] & SOUTH):
        neighbors.append((row + 1, col))
    # 检查西方向
    if col > 0 and not (maze[row][col] & WEST):
        neighbors.append((row, col - 1))
    # 检查东方向
    if col < cols - 1 and not (maze[row][col] & EAST):
        neighbors.append((row, col + 1))
    return neighbors


def find_path(maze, start, goal):
    queue = deque([start])
    visited = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break

        for neighbor in get_neighbors(maze, *current):
            if neighbor not in visited:
                visited[neighbor] = current
                queue.append(neighbor)

    # 安全路径回溯
    path = []
    if goal in visited:
        current = goal
        while current != start:
            path.append(current)
            current = visited[current]
        path.append(start)
        path.reverse()
    else:
        print("警告：未找到有效路径！")
    return path
# 绘制函数保持不变
def draw_maze(maze, path):
    plt.figure(figsize=(12, 8))
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            y = -row_idx
            x = col_idx
            if cell & NORTH:
                plt.plot([x, x + 1], [y, y], 'k-')
            if cell & EAST:
                plt.plot([x + 1, x + 1], [y, y - 1], 'k-')
            if cell & SOUTH:
                plt.plot([x, x + 1], [y - 1, y - 1], 'k-')
            if cell & WEST:
                plt.plot([x, x], [y, y - 1], 'k-')

    if path:
        path_x = [col + 0.5 for row, col in path]
        path_y = [-row - 0.5 for row, col in path]
        plt.plot(path_x, path_y, 'r-', linewidth=2, marker='o', markersize=4)

    plt.gca().add_patch(plt.Rectangle((0.1, -0.1), 0.8, -0.8, color='green', alpha=0.3))
    plt.gca().add_patch(plt.Rectangle((14.1, -11.1), 0.8, -0.8, color='red', alpha=0.3))
    plt.axis('equal')
    plt.axis('off')
    plt.show()


def convert_path_to_directions(path):
    """将坐标路径转换为方向指令序列"""
    directions = []
    direction_map = {
        (1, 0): "down",
        (-1, 0): "up",
        (0, 1): "right",
        (0, -1): "left"
    }
    for i in range(len(path) - 1):
        current = path[i]
        next_pos = path[i + 1]
        # 计算坐标差
        dy = next_pos[0] - current[0]
        dx = next_pos[1] - current[1]
        # 验证是否为有效移动
        if abs(dy) + abs(dx) != 1:
            raise ValueError(f"无效移动：从 {current} 到 {next_pos}")
        directions.append(direction_map[(dy, dx)])
    return directions

if __name__ == '__main__':

    lock = asyncio.Lock()
    headers = {'sec-ch-ua-platform': '"Windows"',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
               'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
               'trpc-accept': 'application/jsonl',
               'content-type': 'application/json',
               'x-trpc-source': 'nextjs-react',
               'sec-ch-ua-mobile': '?0',
               'Accept': '*/*',
               'Sec-Fetch-Site': 'same-origin',
               'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Dest': 'empty',
               'Referer': 'https://testnet.lenscan.io/faucet',
               'Accept-Encoding': 'gzip, deflate, br, zstd',
               'Accept-Language': 'en',
               }
    url='https://testnet.lenscan.io/api/trpc/faucet.getMaze?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22difficulty%22%3A%22hard%22%7D%7D%7D'
    res = requests.get(url,headers=headers)
    # print(res.text)
    data = res.text.split('\n')[-2]
    data = json.loads(data)['json'][2][0][0]
    # print(data)
    maze_data  = data['walls']
    # print(maze_data)
    goal = (data['goalPos']['row'], data['goalPos']['col'])
    start = (0, 0)
    path = find_path(maze_data, start, goal)
    lenspath = convert_path_to_directions(path)
    print("找到的路径坐标：", path,lenspath)
    # draw_maze(maze_data, path)


