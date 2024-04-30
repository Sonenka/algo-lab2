def simple_search(rectangles, points):
    occurrence = [0] * len(points)

    for i in range(len(points)):
        x, y = points[i]

        for rectangle in rectangles:
            x1, y1, x2, y2 = rectangle

            if (x1 <= x < x2) and (y1 <= y < y2):
                occurrence[i] += 1
    return occurrence