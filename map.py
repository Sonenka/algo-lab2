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


def create_map(rectangles):
    set_x, set_y = set(), set()

    for rectangle in rectangles:
        set_x.add(rectangle[0])
        set_x.add(rectangle[1])
        set_x.add(rectangle[2])
        set_x.add(rectangle[3])

    set_x, set_y = sorted(set_x), sorted(set_y)

    matrix_map = []
    for y in set_y:
        row = [0 for _ in range(len(set_x))]
        matrix_map.append(row)

    for r in rectangles:
        x1, x2 = find_pos(set_x, r[0]), find_pos(set_x, r[2])
        y1, y2 = find_pos(set_y, r[1]), find_pos(set_y, r[3])

        for i in range(y1, y2):
            for j in range(x1, x2):
                matrix_map[i][j] += 1

    return matrix_map, set_x, set_y


def map_algorithm(matrix_map, points, set_x, set_y):
    result = []

    for point in points:
        pos_x, pos_y = find_pos(set_x, point[0]), find_pos(set_y, point[1])

        if pos_x == -1 or pos_y == -1:
            result.append(0)
        else:
            result.append(matrix_map[pos_y][pos_x])
            
    return result