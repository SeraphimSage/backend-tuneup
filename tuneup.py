#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "Kenneth Pinkerton"

import cProfile
import pstats
import functools
import timeit
import io
from pstats import SortKey
from functools import partial
from collections import Counter


def profile(start_func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    def benchmarker(*args, **kwargs):
        print("Start Benchmark")
        prof = cProfile.Profile()
        prof.enable()
        start_func(*args, **kwargs)
        prof.disable()
        s = io.StringIO()
        sorter = SortKey.CUMULATIVE
        prof_stats = pstats.Stats(prof, stream=s).sort_stats(sorter)
        prof_stats.print_stats()
        print(s.getvalue())
        return prof_stats
    return benchmarker


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    for movie in movies:
        if movie.lower() == title.lower():
            return True
    return False


def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movies = read_movies(src)
    duplicates = Counter(movies)
    return [k for k, v in duplicates.items() if v > 1]


def timeit_helper(func):
    """Part A: Obtain some profiling measurements using timeit."""
    t = timeit.Timer(partial(func)).repeat(repeat=7, number=3)
    times = min(t)/1
    result = (f'Best time across 7 repeats of 5 runs per repeate: {times} sec')
    print(result)
    return result


@profile
def main():
    """Computes a list of duplicate movie entries."""
    result = find_duplicate_movies('movies.txt')
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))


if __name__ == '__main__':
    main()
