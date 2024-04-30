class Node:
    def __init__(self, value, left, right, left_idx, right_idx):
        self.value = value
        self.left = left
        self.right = right
        self.left_idx = left_idx
        self.right_idx = right_idx

class Hit:
    def __init__(self, x, begin_y, end_y, status):
        self.x = x
        self.begin_y = begin_y
        self.end_y = end_y
        self.status = status


def build_tree(left_idx, right_idx):
    if left_idx >= right_idx:
        return Node(0, None, None, left_idx, right_idx)

    mid = (left_idx + right_idx) // 2

    left = build_tree(left_idx, mid)
    right = build_tree(mid + 1, right_idx)

    return Node(left.value + right.value, left, right, left_idx, right.right_idx)


def find_pos(a, val):
    left, right = 0, len(a) - 1

    while left <= right:
        mid = (right + left) // 2

        if a[mid] == val:
            return mid
        elif a[mid] > val:
            right = mid - 1
        else:
            left = mid + 1

    return left - 1


def compress_coordinates(rectangles):
    set_compress_x = set()
    set_compress_y = set()

    for r in rectangles:
        set_compress_x.add(r[0])
        set_compress_y.add(r[1])
        set_compress_x.add(r[2])
        set_compress_y.add(r[3])

    compress_x = sorted(set_compress_x)
    compress_y = sorted(set_compress_y)
    return compress_x, compress_y


def insert(node, begin, end, value):
    if begin <= node.left_idx and end >= node.right_idx:
        return Node(node.value + value, node.left, node.right, node.left_idx, node.right_idx)
    if begin > node.right_idx or end < node.left_idx:
        return node

    ret = Node(node.value, node.left, node.right, node.left_idx, node.right_idx)

    ret.left = insert(ret.left, begin, end, value)
    ret.right = insert(ret.right, begin, end, value)

    return ret


def build_persistent_segment_tree(rectangles, compress_x, compress_y):
    hits = []
    if not rectangles:
        return None

    for r in rectangles:
        begin_y = find_pos(compress_y, r[1])
        end_y = find_pos(compress_y, r[3])

        hits.append(Hit(r[0], begin_y, end_y - 1, 1))
        hits.append(Hit(r[2], begin_y, end_y - 1, -1))
    hits.sort(key=lambda hit: hit.x)

    roots = []
    root = build_tree(0, len(compress_y) - 1)

    end_x = hits[0].x
    for hit in hits:
        if end_x != hit.x:
            roots.append(root)
            end_x = hit.x
        root = insert(root, hit.begin_y, hit.end_y, hit.status)
    roots.append(root)
    return roots


def get_count(node, target):
    if node:
        mid = (node.left_idx + node.right_idx) // 2
        if target <= mid:
            return node.value + get_count(node.left, target)
        else:
            return node.value + get_count(node.right, target)
    return 0


def tree_algorithm(points, compress_x, compress_y, roots):
    answer = []
    if roots is None:
        return answer

    for p in points:
        pos_x, pos_y = find_pos(compress_x, p[0]), find_pos(compress_y, p[1])

        if pos_x == -1 or pos_y == -1:
            answer.append(0)
        else:
            answer.append(get_count(roots[pos_x], pos_y))
    return answer


#for contest

# n = int(input())
# rectangles = []
# for _ in range(n):
#     rect = list(map(int, input().split()))
#     rectangles.append(rect)

# m = int(input())
# points = []
# for _ in range(m):
#     point = list(map(int, input().split()))
#     points.append(point)

# compress_x, compress_y = compress_coordinates(rectangles)
# roots = build_persistent_segment_tree(rectangles, compress_x, compress_y)
# print(*tree_algorithm(points, compress_x, compress_y, roots))