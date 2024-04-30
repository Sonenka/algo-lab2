from time import perf_counter_ns
from simple import simple_search
from map import *
from persistent_tree import *

def generate_data(n_rectangles, n_points):
    rectangles = []
    for i in range(n_rectangles):
        x1, y1, x2, y2 = 10 * i, 10 * i, 10 * (2 * n_rectangles - i), 10 * (2 * n_rectangles - i)
        rectangles.append((x1, y1, x2, y2))

    points = []
    for i in range(n_points):
        x = (i * 313) ** 31 % (20 * n_points)
        y = (i * 233) ** 31 % (20 * n_points)
        points.append([x, y])

    return rectangles, points


def test():
    for i in range(11):
        n_rectangles, n_points = 2 ** i, 2 ** (i + 1)
        rectangles, points = generate_data(n_rectangles, n_points)
        simple_search_time, map_time, tree_time = 0, [0, 0], [0, 0]

        for _ in range(10):
            start = perf_counter_ns()
            simple_search(rectangles, points)
            finish = perf_counter_ns()
            simple_search_time += finish - start

            start = perf_counter_ns()
            matrix_map, set_x, set_y = create_map(rectangles)
            finish = perf_counter_ns()
            map_time[0] += finish - start

            start = perf_counter_ns()
            map_algorithm(matrix_map, points, set_x, set_y)
            finish = perf_counter_ns()
            map_time[1] += finish - start

            start = perf_counter_ns()
            compress_x, compress_y = compress_coordinates(rectangles)
            roots = build_persistent_segment_tree(rectangles, compress_x, compress_y)
            finish = perf_counter_ns()
            tree_time[0] += finish - start

            start = perf_counter_ns()
            tree_algorithm(points, compress_x, compress_y, roots)
            finish = perf_counter_ns()
            tree_time[1] += finish - start
        
        print(simple_search_time, sum(map_time), sum(tree_time))
        with open('results.txt', 'a') as f:
            f.write(f'{n_rectangles} rectangles, {n_points} points:\n')
            f.write(f'    Simple search: {simple_search_time}\n')
            f.write(f'    Map algorithm: {map_time}\n')
            f.write(f'    Tree algorithm: {tree_time}\n')
            f.write('\n')


def main():
    test()

if __name__ == "__main__":
    main()
        
