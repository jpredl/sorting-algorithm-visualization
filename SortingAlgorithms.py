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


class InsertionSorter(Sorter):

    def execute(self, data: np.ndarray) -> None:
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
