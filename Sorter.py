from dataclasses import dataclass
import numpy as np

import Sorter


@dataclass
class Step:
    delay: bool


@dataclass
class Comparison(Step):
    pos_1: int
    pos_2: int


@dataclass
class Swap(Step):
    pos_1: int
    pos_2: int


@dataclass
class Mark(Step):
    pos: int


@dataclass
class Unmark(Step):
    pass


@dataclass
class Focus(Step):
    pos_1: int
    pos_2: int


class Sorter:
    steps = []

    @staticmethod
    def sort(data):
        return Sorter.steps

    @staticmethod
    def compare(data, pos_1, pos_2, delay=True) -> int:
        # append comparison step to steps
        Sorter.steps.append(Comparison(pos_1=pos_1, pos_2=pos_2, delay=delay))

        # compare and return True if data[pos_1] is smaller than or equal to data[pos_2]
        return True if data[pos_1] <= data[pos_2] else False

    @staticmethod
    def swap(data, pos_1, pos_2, delay=True):
        # swap entries in data
        temp = data[pos_1]
        data[pos_1] = data[pos_2]
        data[pos_2] = temp

        # append swap step to steps
        Sorter.steps.append(Swap(pos_1=pos_1, pos_2=pos_2, delay=delay))

    @staticmethod
    def mark(pos, delay=True):
        # append mark step to steps
        Sorter.steps.append(Mark(pos=pos, delay=delay))

    @staticmethod
    def unmark(delay=True):
        # append unmark step to steps
        Sorter.steps.append(Unmark(delay=delay))

    @staticmethod
    def focus(pos_1, pos_2, delay=True):
        # append focus step to steps
        Sorter.steps.append(Focus(pos_1=pos_1, pos_2=pos_2, delay=delay))


class SelectionSorter(Sorter):

    @staticmethod
    def sort(data):
        # prepare new round of sorting
        Sorter.steps.clear()

        # sort data by using selectionsort algorithm
        n = len(data)
        for i in range(n):
            # determine position min of smallest element in data[i], ..., data[n]
            Sorter.focus(i, n - 1)
            min = i
            Sorter.mark(min, delay=False)
            for j in range(i + 1, n):
                # if data[j] <= data[min]
                if Sorter.compare(data, j, min):
                    min = j
                    Sorter.mark(min, delay=False)

            # put smallest element to the front of data[i], ..., data[n]
            Sorter.swap(data, i, min)

        # data is sorted now
        return Sorter.steps


class InsertionSorter(Sorter):

    @staticmethod
    def sort(data):
        # prepare new round of sorting
        Sorter.steps.clear()

        # sort data using the insertion sort algorithm
        for i in range(1, len(data)):
            # insert data[i] at correct position in data[0], ..., data[i-1]
            Sorter.mark(i, delay=False)
            Sorter.focus(0, i, delay=False)
            j = i
            while j > 0:
                # if data[j - 1] > data[j]
                if Sorter.compare(data, j, j - 1):
                    Sorter.swap(data, j - 1, j)
                    j -= 1
                else:
                    break

        # data is sorted now
        return Sorter.steps


class ShellSorter(Sorter):

    @staticmethod
    def sort(data):
        # prepare new round of sorting
        Sorter.steps.clear()

        # get increments for shellsort
        n = len(data)
        increments = ShellSorter._get_increments(n)

        # sort data using the shellsort algorithm
        for k in increments:
            for i in range(k, n):
                # insert data[i] at correct k-position in data[0], ..., data[i-1]
                Sorter.mark(i, delay=False)
                Sorter.focus(0, i, delay=False)
                j = i
                while j - k >= 0:
                    # if data[j - k] > data[j]
                    if Sorter.compare(data, j, j - k):
                        Sorter.swap(data, j - k, j)
                        j -= k
                    else:
                        break

        # data is sorted now
        return Sorter.steps

    @staticmethod
    def _get_increments(n: int) -> np.ndarray:
        # calculate all numbers between 1 and n of the form 2^p * 3^q
        increments = []

        for i in range(n-1, 0, -1):

            number = i

            # divide out all 2's
            while number % 2 == 0:
                number //= 2

            # divide out all 3's
            while number % 3 == 0:
                number //= 3

            # if number is not equal to 1 now it is not of the form 2^p * 3^q
            if number == 1:
                increments.append(i)

        return np.array(increments)


class BubbleSorter(Sorter):

    @staticmethod
    def sort(data):
        # prepare new round of sorting
        Sorter.steps.clear()

        # sort data using the bubblesort algorithm
        for i in range(len(data) - 1, 0, -1):
            no_swap = True
            for j in range(i):
                # if data[j + 1] <= data[j]
                if Sorter.compare(data, j + 1, j):

                    # mark data entry to visualize bubble rising up
                    Sorter.mark(j, delay=False)

                    Sorter.swap(data, j, j + 1)
                    no_swap = False

                else:
                    # unmark data entry as bubble is not rising anymore
                    Sorter.unmark(delay=False)

            # condition for early termination if data is already sorted
            if no_swap:
                break

        # data is sorted now
        return Sorter.steps


class QuickSorter(Sorter):

    @staticmethod
    def sort(data):
        # prepare new round of sorting
        Sorter.steps.clear()

        # sort data by using quicksort algorithm
        QuickSorter._recursion(data, 0, len(data) - 1)

        # data is sorted now
        return Sorter.steps

    @staticmethod
    def _recursion(data, l, r):

        if r > l:
            # select position of pivot element
            p = r

            # append visualization steps
            Sorter.focus(l, r)
            Sorter.mark(p)

            # partition the data into two subarrays
            # - the first containing the elements smaller than the pivot element
            # - the seccond containing the elements bigger than the pivot element
            i = l - 1
            j = r
            while i < j:
                # find an element that is bigger than the pivot element
                while i < j:
                    i += 1
                    # if data[i] >= data[p]
                    if Sorter.compare(data, p, i):
                        break
                # find an element that is smaller than the pivot element
                while i < j:
                    j -= 1
                    # if data[j] <= data[p]
                    if Sorter.compare(data, j, p):
                        break
                if i < j:
                    # swap the elements if they are not the same
                    Sorter.swap(data, i, j)

            # put the pivot element on its correct position if it is not already there
            if i < p:
                Sorter.swap(data, i, p)
            # sort the first subarray
            QuickSorter._recursion(data, l, i - 1)
            # sort the second subarray
            QuickSorter._recursion(data, i + 1, r)
