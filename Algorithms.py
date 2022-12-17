import numpy as np
from dataclasses import dataclass


class Initiator:

    @staticmethod
    def initiate(n):
        pass


class PermutationInitiator(Initiator):

    @staticmethod
    def initiate(n):
        return np.random.permutation(np.arange(1, n + 1))


class ReverseInitiator(Initiator):

    @staticmethod
    def initiate(n):
        return np.arange(n, 0, -1)

class TranspositionInitiater(Initiator):

    @staticmethod
    def initiate(n):
        # determine random positions to swap
        pos_1 = np.random.randint(0, n-2)
        pos_2 = pos_1 + np.random.randint(1, n - pos_1 - 1)

        # generate data
        data = np.arange(1, n + 1)

        # swap
        temp = data[pos_1]
        data[pos_1] = data[pos_2]
        data[pos_2] = temp

        # return data
        return data


class LocalInitiator(Initiator):

    @staticmethod
    def initiate(n):
        # length of section for shuffling
        length = int(np.floor(n/np.random.randint(2,7)))

        # determine local section for shuffling
        pos = np.random.randint(0, n - length - 1)

        # generate data
        data = np.arange(1, n + 1)

        # perform shuffling
        data[pos:pos + length] = np.random.permutation(data[pos:pos + length])

        # return data
        return data

class SortedInitiator:

    @staticmethod
    def initiate(n):
        return np.arange(1, n + 1)




@dataclass
class Comparison:
    pos_1: int
    pos_2: int

@dataclass
class Swap:
    pos_1: int
    pos_2: int

@dataclass
class Mark:
    pos: int

@dataclass
class Focus:
    pos_1: int
    pos_2: int


class Sorter:

    steps = []

    @staticmethod
    def sort(data):
        return Sorter.steps

    @staticmethod
    def compare(data, pos_1, pos_2) -> int:
        # append comparison step to steps
        Sorter.steps.append(Comparison(pos_1=pos_1, pos_2=pos_2))

        # compare and return True if data[pos_1] is smaller than or equal to data[pos_2]
        return True if data[pos_1] <= data[pos_2] else False

    @staticmethod
    def swap(data, pos_1, pos_2,):
        # swap entries in data
        temp = data[pos_1]
        data[pos_1] = data[pos_2]
        data[pos_2] = temp

        # append swap step to steps
        Sorter.steps.append(Swap(pos_1=pos_1, pos_2=pos_2))

    @staticmethod
    def mark(pos):
        # append mark step to steps
        Sorter.steps.append(Mark(pos=pos))

    @staticmethod
    def focus(pos_1, pos_2):
        # append focus step to steps
        Sorter.steps.append(Focus(pos_1=pos_1, pos_2=pos_2))

class SelectionSorter(Sorter):

    @staticmethod
    def sort(data):
        # prepare new round of sorting
        Sorter.steps.clear()

        # sort data by using selectionsort algorithm
        n = len(data)
        for i in range(n):
            # determine position min of smallest element in data[i], ..., data[n]
            min = i
            for j in range(i+1, n):
                # if data[j] <= data[min]
                if Sorter.compare(data, j, min):
                    min = j

            # put smallest element to the front of data[i], ..., data[n]
            Sorter.swap(data, i, min)

        # data is sorted now
        return Sorter.steps

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
                    Sorter.swap(data, j, j+1)
                    no_swap = False
            # condition for early termination if data is already sorted
            if no_swap:
                break

        # data is sorted now
        return Sorter.steps


class Quicksorter(Sorter):

    @staticmethod
    def sort(data):
        # prepare new round of sorting
        Sorter.steps.clear()

        # sort data by using quicksort algorithm
        Quicksorter.recursion(data, 0, len(data) - 1)

        # data is sorted now
        return Sorter.steps

    @staticmethod
    def recursion(data, l, r):

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
            Quicksorter.recursion(data, l, i - 1)
            # sort the second subarray
            Quicksorter.recursion(data, i + 1, r)


