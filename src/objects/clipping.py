from enum import Enum
import numpy as np
from numpy.typing import NDArray

from objects.linked_list import CircularLinkedList

OptionalObject = None | NDArray[np.float64]
"""A typing to remove the need to repeat ourselves"""


class ClippingAlgo(Enum):
    Points = 0
    CohenSutherland = 1
    LiangBarsky = 2
    NichollLeeNicholl = 3


class Clipping:
    """Clipping algorithms"""
    @staticmethod
    def clip_by_point(points: NDArray[np.float64]) -> OptionalObject:
        """
        @brief: Basic point clipping

        This algorithm simply deletes the points that are outside the window

        @param points: List of points to clip

        @returns: Vertices that are visible or None if nothing is visible
        """
        vertex: NDArray[np.float64]
        v_x: np.float64
        v_y: np.float64

        clipped_coords: list[NDArray[np.float64]] = []

        for vertex in points:
            (v_x, v_y, _) = vertex

            if v_x > 1 or v_x < -1 or v_y > 1 or v_y < -1:
                continue

            clipped_coords.append(vertex)

        if len(clipped_coords) > 0:
            return np.array(clipped_coords)

        return None

    @staticmethod
    def clip_cohen_sutherland(edge: NDArray[np.float64]) -> OptionalObject:
        """
        Line clipping with Cohen-Sutherland algorithm

        @param edge: Edge (list of two vertices) to clip

        @returns: New clipped edge or None if outside view
        """
        vertex_0: NDArray[np.float64]
        vertex_1: NDArray[np.float64]
        x0: float
        y0: float
        x1: float
        y1: float

        (vertex_0, vertex_1) = edge
        (x0, y0, _) = vertex_0
        (x1, y1, _) = vertex_1
        rc = [  # Top Bottom Right Left
            (
                (y0 > 1) << 3
                | (y0 < -1) << 2
                | (x0 > 1) << 1
                | (x0 < -1)
            ), (
                (y1 > 1) << 3
                | (y1 < -1) << 2
                | (x1 > 1) << 1
                | (x1 < -1)
            ),
        ]

        if rc[0] & rc[1]:  # fully outside
            return None
        elif rc[0] | rc[1]:  # partially outside
            new_edge = edge.copy()
            m = 0.

            if x1 - x0 != 0.:
                m = (y1 - y0) / (x1 - x0)

            for idx in range(0, 2):
                if rc[idx] == 0:
                    continue

                if rc[idx] > 3:  # Top or Bottom
                    y: float = -1 + ((rc[idx] >> 2) & 2)

                    # m would be infinite, but we define as 0
                    # if m = inifinity => x = x0
                    x = x0
                    if m != 0.:
                        x = x0 + (y - y0) / m

                    if x >= -1 and x <= 1:
                        new_edge[idx][0] = x
                        new_edge[idx][1] = y
                        continue

                if rc[idx] & 3:  # Left or Right
                    x = -1 + (rc[idx] & 2)
                    y = m * (x - x0) + y0

                    if y >= -1 or y <= 1:
                        new_edge[idx][0] = x
                        new_edge[idx][1] = y
                        continue

                return None

            return new_edge
        else:  # fully inside
            return edge

    @staticmethod
    def clip_liang_barsky(edge: NDArray[np.float64]) -> OptionalObject:
        """
        Line clipping with Liang-Barsky algorithm

        @param edge: Edge (list of two vertices) to clip

        @returns: New clipped edge or None if outside view
        """
        vertex_0: NDArray[np.float64]
        vertex_1: NDArray[np.float64]
        x0: float
        y0: float
        x1: float
        y1: float

        (vertex_0, vertex_1) = edge
        (x0, y0, _) = vertex_0
        (x1, y1, _) = vertex_1
        new_edge = edge.copy()
        p = [
            0,
            x1 - x0,  # delta x
            0,
            y1 - y0,  # delta y
        ]
        p[0] = -p[1]
        p[2] = -p[3]

        q = [
            x0 + 1,  # - -1 => +1
            1 - x0,
            y0 + 1,  # - -1 => +1
            1 - y0,
        ]

        if (
            (p[1] == 0 and (q[0] < 0 or q[1] < 0))
            or (p[3] == 0 and (q[2] < 0 or q[3] < 0))
        ):
            return None

        r = [0 if p[idx] == 0 else q[idx] / p[idx] for idx in range(0, 4)]
        zeta1 = max([r[idx] if p[idx] < 0 else 0 for idx in range(0, 4)])
        zeta2 = min([r[idx] if p[idx] > 0 else 1 for idx in range(0, 4)])

        if zeta1 <= zeta2:
            if zeta1 > 0:
                new_edge[0][0] = x0 + zeta1 * p[1]
                new_edge[0][1] = y0 + zeta1 * p[3]

            if zeta2 < 1:
                new_edge[1][0] = x0 + zeta2 * p[1]
                new_edge[1][1] = y0 + zeta2 * p[3]

            return new_edge

        return None

    @staticmethod
    def clip_nicholl_lee_nicholl(edge: NDArray[np.float64]) -> OptionalObject:
        """
        Line clipping with Nicholl-Lee-Nicholl algorithm

        @param edge: Edge (list of two vertices) to clip

        @returns: New clipped edge or None if outside view
        """
        vertex_0: NDArray[np.float64]
        vertex_1: NDArray[np.float64]
        x0: float
        y0: float
        x1: float
        y1: float

        clipped_coords: list[NDArray[np.float64]] = []

        (vertex_0, vertex_1) = edge
        (x0, y0, _) = vertex_0
        (x1, y1, _) = vertex_1
        new_edge = edge.copy()

        clipped_coords.append(new_edge)

        return np.array(clipped_coords)

    @staticmethod
    def clip_sutherland_hodgeman(polygon: NDArray[np.float64]) -> OptionalObject:
        """
        Polygon clipping with Liang-Barsky algorithm

        @param polygon: Polygon (list of vertices) to clip

        @returns: New clipped polygon or None if outside view
        """
        temp = polygon.tolist()

        for j in range(0, 4):
            cur = temp
            temp = []
            test_var = j > 1
            test_value = 2 * (j % 2) - 1

            for i in range(0, len(cur)):
                v0 = cur[i % len(cur)]
                v1 = cur[(i + 1) % len(cur)]
                m = 0.

                if v1[0] - v0[0] != 0.:
                    m = (v1[1] - v0[1]) / (v1[0] - v0[0])

                if v0[test_var] < test_value and v1[test_var] < test_value:
                    if test_value == 1:
                        temp.append(v0)
                        temp.append(v1)
                    continue

                if v0[test_var] > test_value and v1[test_var] > test_value:
                    if test_value == -1:
                        temp.append(v0)
                        temp.append(v1)
                    continue

                if not test_var:
                    x = test_value
                    y = m * (x - v0[0]) + v0[1]

                    if (
                        (test_value == 1 and v0[test_var] < test_value)
                        or (test_value == -1 and v0[test_var] > test_value)
                    ):
                        temp.append(v0)
                        temp.append([x, y, 1])
                    else:
                        temp.append([x, y, 1])
                        temp.append(v1)
                else:
                    y = test_value

                    # m would be infinite, but we define as 0
                    # if m = inifinity => x = x0
                    x = v0[0]
                    if m != 0.:
                        x = v0[0] + (y - v0[1]) / m

                    if (
                        (test_value == 1 and v0[test_var] < test_value)
                        or (test_value == -1 and v0[test_var] > test_value)
                    ):
                        temp.append(v0)
                        temp.append([x, y, 1])
                    else:
                        temp.append([x, y, 1])
                        temp.append(v1)

        if len(temp) == 0:
            max_x = 0
            min_x = 0
            max_y = 0
            min_y = 0
            for vertex in temp:
                (x, y, _) = vertex
                max_x = max(max_x, x)
                max_y = max(max_y, y)
                min_x = min(min_x, x)
                min_y = min(min_y, y)
            if max_x > 1 and min_x < -1 and max_y > 1 and min_y < -1:
                return np.array([[-1, 1, 1], [1, 1, 1], [1, -1, 1], [-1, -1, 1]])
            return None

        return np.array(temp)

    @classmethod
    def clip_weiler_atherton(cls, polygon: NDArray[np.float64]) -> OptionalObject:
        """
        Polygon clipping with Liang-Barsky algorithm

        @param polygon: Polygon (list of vertices) to clip

        @returns: New clipped polygon or None if outside view
        """
        # check if it's clockwise
        clockwise = 0

        for i in range(0, len(polygon)):
            v0: NDArray[np.float64] = polygon[i]
            v1: NDArray[np.float64] = polygon[(i + 1) % len(polygon)]
            clockwise += (v1[0] - v0[0]) * (v1[1] + v0[1])

        if clockwise < 0:
            polygon = np.flip(polygon, axis=0)

        polygon_v = CircularLinkedList("p")
        polygon_v2 = []
        window_v = CircularLinkedList("w")
        window_v.append(np.array([-1, 1, 1]))
        window_v.append(np.array([1, 1, 1]))
        window_v.append(np.array([1, -1, 1]))
        window_v.append(np.array([-1, -1, 1]))
        clipped_polygon: list[NDArray[np.float64]] = []
        i = 0
        stop_at = len(polygon)

        while i < stop_at:
            if i == len(polygon) and len(polygon_v) == 0:
                return None

            edge: NDArray[np.float64] = np.array([
                polygon[i % len(polygon)],
                polygon[(i + 1) % len(polygon)],
            ])
            clipped_edge = cls.clip_liang_barsky(edge)
            i += 1

            if clipped_edge is None and len(polygon_v) == 0:
                stop_at += 1
                continue

            if clipped_edge is not None:
                # outside to inside
                if not np.array_equal(edge[0], clipped_edge[0]):
                    polygon_node = polygon_v.append(clipped_edge[0])
                    polygon_v2.append(clipped_edge[0])

                    if clipped_edge[0][1] == 1:
                        window_v.append_top(clipped_edge[0]).set_next(polygon_node)
                    elif clipped_edge[0][0] == 1:
                        window_v.append_right(clipped_edge[0]).set_next(polygon_node)
                    elif clipped_edge[0][1] == -1:
                        window_v.append_bottom(clipped_edge[0]).set_next(polygon_node)
                    elif clipped_edge[0][0] == -1:
                        window_v.append_left(clipped_edge[0]).set_next(polygon_node)

                # inside to outside
                if not np.array_equal(edge[1], clipped_edge[1]):
                    polygon_node = polygon_v.append(clipped_edge[1], True)
                    polygon_v2.append(clipped_edge[1])
                    window_node = None

                    if clipped_edge[1][1] == 1:
                        window_node = window_v.append_top(clipped_edge[1], True)
                    elif clipped_edge[1][0] == 1:
                        window_node = window_v.append_right(clipped_edge[1], True)
                    elif clipped_edge[1][1] == -1:
                        window_node = window_v.append_bottom(clipped_edge[1], True)
                    elif clipped_edge[1][0] == -1:
                        window_node = window_v.append_left(clipped_edge[1], True)

                    if window_node:
                        polygon_node.set_next(window_node)

            polygon_v.append(edge[1])
            polygon_v2.append(edge[1])

        print("polygon")
        for a in polygon:
            print("\t", a)
        # print("polygon_v")
        print("polygon_v2")
        for a in polygon_v2:
            print("\t", a)
        # print("\t", polygon_v)
        print("window_v")
        print("\t", window_v)

        vertex = polygon_v.head()

        if vertex is None:
            return None
        return polygon

        vertex_id = vertex.uid()
        clipped_polygon.append(vertex.coords())
        vertex = vertex.next_node()

        if vertex.is_intersection():
            vertex = vertex.next_node()

        while vertex.uid() != vertex_id:
            clipped_polygon.append(vertex.coords())
            vertex = vertex.next_node()

            if vertex.is_intersection():
                vertex = vertex.next_node()

        print("clipped_polygon")
        for a in clipped_polygon:
            print("\t", a)

        if len(clipped_polygon) == 0:
            return None

        return np.array(clipped_polygon)
