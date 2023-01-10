import numpy as np


class Initiator:
    """
    Base class for initiating the array that will be sorted.
    """

    @staticmethod
    def initiate(n: int) -> np.ndarray:
        """

        Parameters
        ----------
        n: int
            Size of array that will be initiated.

        Returns
        -------
        np.ndarray
            Array that will be sorted.
        """
        pass


class PermutationInitiator(Initiator):

    @staticmethod
    def initiate(n: int) -> np.ndarray:
        return np.random.permutation(np.arange(1, n + 1))


class ReverseInitiator(Initiator):

    @staticmethod
    def initiate(n: int) -> np.ndarray:
        return np.arange(n, 0, -1)


class TranspositionInitiater(Initiator):

    @staticmethod
    def initiate(n: int) -> np.ndarray:
        # determine random positions to swap
        pos_1 = np.random.randint(0, n - 2)
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
    def initiate(n: int) -> np.ndarray:
        # length of section for shuffling
        length = int(np.floor(n / np.random.randint(2, 7)))

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
    def initiate(n: int) -> np.ndarray:
        return np.arange(1, n + 1)