import numpy as np

from Sorter import Sorter


class SelectionSorter(Sorter):

    def execute(self, data: np.ndarray) -> None:
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


class HeapSorter(Sorter):

    def execute(self, data: np.ndarray) -> None:
        # heapify data
        HeapSorter._heapify(data)

        # sort heap
        for i in range(len(data) - 1, 0, -1):
            Sorter.swap(data, 0, i)
            HeapSorter._sift_down(data, 0, i - 1)

    @staticmethod
    def _heapify(data: np.ndarray) -> None:
        # transform data into a heap
        n = len(data)
        for i in range(int(n/2) - 1, -1, -1):
            HeapSorter._sift_down(data, i, n - 1)

    @staticmethod
    def _sift_down(data: np.ndarray, i: int, m: int) -> None:
        # sift down data[i] up to data[m]
        Sorter.focus(i, m)
        Sorter.mark(i)
        while 2 * i + 1 <= m:
            # data[i] has left child
            j = 2 * i + 1
            # data[j] is left child
            if j < m:
                # data[i] has right child (data[j + 1] is right child)
                # if data[j] < data[j + 1]
                if Sorter.compare(data, j, j + 1):
                    j += 1
                    # now data[j] is greater child
            # if data[i] < data[j]
            if Sorter.compare(data, i, j):
                Sorter.swap(data, i, j)
                # continue to sift down data[i]
                i = j
            else:
                # done, heap condition is satisfied
                break

class InsertionSorter(Sorter):

    def execute(self, data: np.ndarray) -> None:
        for i in range(1, len(data)):
            # insert data[i] at correct position in data[0], ..., data[i-1]
            Sorter.focus(0, i, delay=False)
            Sorter.mark(i, delay=False)
            j = i
            while j > 0:
                # if data[j - 1] > data[j]
                if Sorter.compare(data, j, j - 1):
                    Sorter.swap(data, j - 1, j)
                    j -= 1
                else:
                    break


class ShellSorter(Sorter):

    def execute(self, data: np.ndarray) -> None:
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

    @staticmethod
    def _get_increments(n: int) -> np.ndarray:
        # calculate all numbers between 1 and n of the form 2^p * 3^q
        increments = []

        for i in range(n - 1, 0, -1):

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

    def execute(self, data: np.ndarray) -> None:
        for i in range(len(data) - 1, 0, -1):
            sorted_flag = True
            for j in range(i):
                # if data[j + 1] <= data[j]
                if Sorter.compare(data, j + 1, j):

                    # mark data entry to visualize bubble rising up
                    Sorter.mark(j, delay=False)

                    Sorter.swap(data, j, j + 1)
                    sorted_flag = False

                else:
                    # unmark data entry as bubble is not rising anymore
                    Sorter.unmark(delay=False)

            # condition for early termination if data is already sorted
            if sorted_flag:
                break


class ShakerSorter(Sorter):

    def execute(self, data: np.ndarray) -> None:
        n = len(data)
        for i in range(1, int(np.floor(n / 2))):

            # perform one iteration of bubblesort moving up
            sorted_flag = True
            for j in range(i - 1, n - i):
                # if data[j] > data[j + 1]:
                if Sorter.compare(data, j + 1, j):
                    # mark data entry to visualize shaker going up
                    Sorter.mark(j, delay=False)

                    Sorter.swap(data, j, j + 1)
                    sorted_flag = False
                else:
                    # unmark data entry as it is not moving anymore
                    Sorter.unmark(delay=False)

            if sorted_flag:
                break

            # perform one iteration of bubblesort moving down
            sorted_flag = True
            for j in range(n - i, i - 1, -1):
                # if data[j - 1] > data[j]:
                if Sorter.compare(data, j, j - 1):
                    # mark data entry to visualize shaker going down
                    Sorter.mark(j, delay=False)

                    Sorter.swap(data, j, j - 1)
                    sorted_flag = False
                else:
                    # unmark data entry as it is not moving anymore
                    Sorter.unmark(delay=False)

            if sorted_flag:
                break


class CombSorter(Sorter):

    def execute(self, data: np.ndarray) -> None:
        n = len(data)
        shrinking_factor = 1.3
        h = n

        sorted_flag = False
        while not sorted_flag:
            h = int(np.floor(h / shrinking_factor))
            if h <= 1:
                sorted_flag = True
                h = 1

            for i in range(n - h):
                j = i + h
                # if data[i] > data[j]
                if Sorter.compare(data, j, i):
                    Sorter.swap(data, i, j)
                    sorted_flag = False


class QuickSorter(Sorter):

    def execute(self, data: np.ndarray) -> None:
        self._quicksort(data, 0, len(data) - 1)

    def _quicksort(self, data: np.ndarray, l: int, r: int) -> None:

        if r > l:
            # set focus to subarray data[l], ..., data[r]
            Sorter.focus(l, r)

            # select position of pivot element
            p = self._select_pivot_element(data, l, r)

            # partition the data into two subarrays
            # - the first containing the elements smaller than the pivot element
            # - the second containing the elements bigger than the pivot element
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
            QuickSorter._quicksort(self, data, l, i - 1)
            # sort the second subarray
            QuickSorter._quicksort(self, data, i + 1, r)

    def _select_pivot_element(self, data: np.ndarray, l: int, r: int) -> int:
        # select element at position r as pivot element
        Sorter.mark(r)
        return r


class MedianQuickSorter(QuickSorter):

    def _select_pivot_element(self, data: np.ndarray, l: int, r: int) -> int:
        # calculate position of element in the middle of l and r
        m = int((l + r) / 2)

        # visualize
        Sorter.mark(l)
        Sorter.mark(m, multiple=True)
        Sorter.mark(r, multiple=True)

        # determine median of data[l], data[m] and data[r]
        # if data[l] > data [r]
        if Sorter.compare(data, r, l):
            Sorter.swap(data, r, l)
        # if data[l] > data[m]
        if Sorter.compare(data, m, l):
            Sorter.swap(data, m, l)
        # if data[r] > data[m]
        if Sorter.compare(data, m, r):
            Sorter.swap(data, m, r)

        # r is now position of pivot element
        Sorter.unmark(delay=False)
        Sorter.mark(r)
        return r


class RandomQuickSorter(QuickSorter):

    def _select_pivot_element(self, data: np.ndarray, l: int, r: int) -> int:
        # select random element in data[l], ..., data[r]
        p = np.random.randint(l, r)
        Sorter.mark(p)

        # place data[p] at the end of data[l], ..., data[r]
        Sorter.swap(data, p, r)

        # r is now position of random pivot element
        return r


class MergeSorter(Sorter):

    def __init__(self):

        # temporary memory for merging
        self._temp = []
    def execute(self, data: np.ndarray) -> None:

        # setup temporary memory for merging
        self._temp = [0 for _ in data]

        # apply the mergesort algorithm
        self._mergesort(data, 0, len(data) - 1)

    def _mergesort(self, data: np.ndarray, l: int, r: int) -> None:
        if l < r:

            Sorter.focus(l, r)
            # divide data into two equal sized subarrays and proceed recursively
            m = int((l + r) / 2)
            self._mergesort(data, l, m)
            self._mergesort(data, m + 1, r)

            # merge the two (now) sorted subarrays
            self.merge(data, l, m, r)

    def merge(self, data: np.ndarray, l: int, m: int, r: int) -> None:

        Sorter.focus(l, r, delay=False)

        i = l
        j = m + 1
        k = l

        while i <= m and j <= r:
            # if data[i] < data[j]
            if Sorter.compare(data, i, j):
                self._temp[k] = data[i]
                i += 1
            else:
                self._temp[k] = data[j]
                j += 1
            k += 1

        if i > m:
            for h in range(j, r + 1):
                self._temp[k + h - j] = data[h]
        else:
            for h in range(i, m + 1):
                self._temp[k + h - i] = data[h]

        for i in range(l, r + 1):
            Sorter.replace(data, i, self._temp[i])

        Sorter.unreplace()


class StraightMergeSorter(MergeSorter):

    def execute(self, data: np.ndarray) -> None:

        # setup temporary memory for merging
        self._temp = [0 for _ in data]

        # index of last entry
        n = len(data) - 1

        # index of left boundary of first subarray
        l: int

        # index of right boundary of first subarray
        m: int

        # index of right boundary of second subarray
        r: int

        # length of subarrays
        s = 1

        while s <= n:
            # merge subarrays of length s
            r = - 1
            while r + s < n:
                # while there are at least two subarrays
                # determine boundaries of subarrays
                l = r + 1
                Sorter.mark(l)
                m = l + s - 1
                Sorter.mark(m, multiple=True)
                if m + s <= n:
                    # n has not been passed
                    r = m + s
                else:
                    # in this case the second subarray is shorter than the first
                    r = n
                Sorter.mark(r, multiple=True)

                # merge the two subarrays
                Sorter.focus(l, r)
                self.merge(data, l, m, r)

            # in the next iteration merge subarrays of double length
            s *= 2


class NaturalMergeSorter(MergeSorter):

    def execute(self, data: np.ndarray) -> None:

        # setup temporary memory for merging
        self._temp = [0 for _ in data]

        # index of last entry
        n = len(data) - 1

        # index of left boundary of first run
        l: int

        # index of right boundary of first run
        m: int

        # index of right boundary of second run
        r: int

        while True:
            r = -1
            while r < n:
                # while there are at least two runs
                # determine the first run
                l = r + 1
                Sorter.mark(l)
                m = l
                while m < n:
                    # if data[m] < data[m + 1]
                    if Sorter.compare(data, m, m + 1):
                        m += 1
                    else:
                        Sorter.mark(m, multiple=True)
                        break

                # determine the second run
                if m < n:
                    # there is a second run
                    r = m + 1
                    while r < n:
                        # if data[r] < data[r + 1]
                        if Sorter.compare(data, r, r + 1):
                            r += 1
                        else:
                            Sorter.mark(r, multiple=True)
                            break

                    # merge the two runs
                    Sorter.focus(l, r)
                    self.merge(data, l, m, r)
                    Sorter.unfocus()

                else:
                    # there is no second run
                    r = n

            if not l:
                break





