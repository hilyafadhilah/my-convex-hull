#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convex Hull Finder

Notes
-----
This file is meant to be imported and not to be called directly.
"""
import numpy as np

class myConvexHull:
    """Convex Hull Finder

    The algorithm used to find the convex hull is the basic divide-
    and-conquer algorithm. For detailed explanation please refer to
    page 2-15 of this lecture notes:
    `N.U. Maulidevi & R. Munir <https://informatika.stei.itb.ac.id/~rinaldi.munir/Stmik/2021-2022/Algoritma-Divide-and-Conquer-(2022)-Bagian4.pdf/>`

    The implementation in this class uses a bit of a "trick". In the
    lecture notes it is stated that, we must do the algorithm twice,
    for the points on top of the base line and on bottom side. It is also
    stated that after we find the p-max, we must search through the "left
    side" of the triangle and also the "right side". However it would be
    inefficient to write twice the same code just to differentiate left
    and right.
    
    So here, we take advantage of the determinant part of the math: it
    is actually dependent on the direction of the vector. We force the
    notion that "outside" means "left", by manipulating the vectors so
    that it starts and ends at the point which will make the notion true.
    For example when working on the bottom side, the vector of the base line
    is flipped from right to left, so in this case left (left side of the
    vector) means outside. Such trick is also applied to the triangle part.

    Hence why the divide-and-solve part of this class is really simple.
    It only works on one side (left) and each recursion eliminates many
    unneeded values that need to be worked on.

    Notes
    -----
    This class assumes that the data given is a numpy data array,
    consisting of two columns in the format of (X, Y) pair.
    However it works with native list or any other iterables,
    as long as it conforms to the format mentioned above.

    This class also does not contain any methods to be called directly.
    The constructor is the main actor of this class. Result can be
    accessed through the public attributes.

    Parameters
    ----------
    points: np.ndarray
        List of points (list of list of float).
    
    Attributes
    ----------
    solutions: list[tuple[float, float]]
        List of points which are part of the convex hull. Not stored as ndarray.
    simplices: list[list[float]]
        List of simplex to be fed into graphing utilities.
    divideCount: int
        Number of problem-division done.
    operateCount: int
        Number of heavy calculations done.
    """

    _LINE_T = tuple[np.ndarray, np.ndarray]
    """Shorthand for line type used in this class
    
    Line is stored everywhere in this class as a pair tuple of point,
    one starting point and one ending point.
    """

    solutions: list[tuple[float, float]]
    simplices: list[list[float]]

    divideCount: int
    operateCount: int

    def __init__(self, points: np.ndarray) -> None:
        """Perform the convex hull search

        Parameters
        ----------
        points: np.ndarray
            List of points (list of list of float).
        """
        self.solutions = []
        self.divideCount = 0
        self.operateCount = 0

        # Use leftmost and rightmost points to make a base line
        # (these points are guaranteed to be part of the solution)
        idLeftmost = np.argmin(points, axis=0)[0]
        idRightmost = np.argmax(points, axis=0)[0]

        # Traverse "left" area of line
        line = points[idLeftmost], points[idRightmost]
        self._divideAndSolve(points, line)

        # Traverse "right" area of line
        # Note: Here's the trick in action,
        # we flip the line so that left means outside
        line = line[1], line[0]
        self._divideAndSolve(points, line)

        # Generate simplices used for display
        self._generateSimplices()

    def _divideAndSolve(self, points: list, line: _LINE_T) -> None:
        """Divide and solve

        The main divide-and-conquer part. Uses a recursive approach.
        This method assumes that "left" means "outside".

        Parameters
        ----------
        points: list
            List of points to be worked on.
        line: _LINE_T
            The base line.

        Returns
        -------
        None
        """
        self.divideCount += 1

        # Find points which are on the left (outside) of the base line
        outside = []
        for p in points:
            pos = self._pointPosition(p, line)
            self.operateCount += 1
            if pos > 0:
                outside.append(p)

        if len(outside) == 0:
            # No points outside, found outermost line
            self._addSolution(line)
        else:
            # Find furthest point from line (p-max)
            pmax = self._findMaxPoint(outside, line)

            # Create triangle
            # Note: Here's the trick in action,
            # we position vectors so that left means outside
            lineLeft = line[0], pmax
            lineRight = pmax, line[1]

            # Solve for left and right side of the triangle
            self._divideAndSolve(outside, lineLeft)
            self._divideAndSolve(outside, lineRight)

    def _findMaxPoint(self, points: list, line: _LINE_T) -> np.ndarray:
        """Find point with max distance from base line (p-max)

        If there are multiple with same distance, get the one
        with the bigger angle when put together with the line.

        Parameters
        ----------
        points: list
            List of points to be worked on.
        line: _LINE_T
            The base line.

        Returns
        -------
        np.ndarray
            The point furthest away from the line (p-max)
        """
        pmax = []
        dmax = 0.0
        for p in points:
            d = self._pointDistance(p, line)
            self.operateCount += 1
            if pmax is None or d > dmax:
                pmax = [p]
                dmax = d
            elif d == dmax:
                pmax.append(p)

        if len(pmax) == 1:
            pmax = pmax[0]
        else:
            amax = 0.0
            for p in pmax:
                a = self._pointAngle(p, line)
                self.operateCount += 1
                if a > amax:
                    pmax = p

        return pmax

    def _pointPosition(self, point: np.ndarray, line: _LINE_T) -> float:
        """Determine the position of a point relative to a line

        Parameters
        ----------
        points: list
            List of points to be worked on.
        line: _LINE_T
            The base line.
        
        Returns
        -------
        float
            det > 0 : left side of the line
            det = 0 : on the line itself
            det < 0 : right side of the line
        """
        if self._isPointEqual(point, line[0]) or self._isPointEqual(point, line[1]):
            # Optimization and for rounding errors
            return 0.0
        return np.linalg.det([np.append(line[0], [1.0]), np.append(line[1], [1.0]), np.append(point, [1.0])])

    def _pointDistance(self, point: np.ndarray, line: _LINE_T) -> float:
        """Determine the distance of a point relative to a line

        Parameters
        ----------
        points: list
            List of points to be worked on.
        line: _LINE_T
            The base line.
        
        Returns
        -------
        float
        """
        return np.linalg.norm(np.cross(line[1] - line[0], line[0] - point)) / np.linalg.norm(line[1] - line[0])

    def _pointAngle(self, point: np.ndarray, line: _LINE_T) -> float:
        """Determine the angle of a point when connected as a triangle to a line

        Parameters
        ----------
        points: list
            List of points to be worked on.
        line: _LINE_T
            The base line.
        
        Returns
        -------
        float
        """
        v1 = point - line[0]
        v2 = line[1] - point

        uv1 = v1 / np.linalg.norm(v1)
        uv2 = v2 / np.linalg.norm(v2)

        dot = np.dot(uv1, uv2)

        # Adjustments, due to underflow error
        if dot >= 1.0:
            dot = 1.0
        elif dot <= -1.0:
            dot = -1.0

        return np.arccos(dot)

    def _isPointEqual(self, p1: np.ndarray, p2: np.ndarray):
        return p1[0] == p2[0] and p1[1] == p2[1]

    def _addSolution(self, line: _LINE_T):
        for p in line:
            if (p[0], p[1]) not in self.solutions:
                self.solutions.append((p[0], p[1]))

    def _generateSimplices(self):
        self.simplices = []
        for i in range(len(self.solutions)):
            p1 = self.solutions[i]
            p2 = self.solutions[(i + 1) % len(self.solutions)]
            self.simplices.append(([p1[0], p2[0]], [p1[1], p2[1]]))
