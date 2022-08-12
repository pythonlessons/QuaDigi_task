import typing
import numpy as np

class ForestCounter:
    """ Script that gets number of isolated forests on the map. Forest is formed of cells X that are connected in one of 8 directions.
    """
    def __init__(
        self, 
        forestMap: typing.Iterable[str],
        grassland: chr = '0', 
        forest: chr = 'X', 
        ):
        """ 
        Args:
            forestMap: typing.Iterable[str] - forest map to be processed
            grassland: chr = '0' - default character for grassland marking in forestMap
            forest: chr = 'X' - default character for forest marking in forestMap
        """
        self._forestMap = forestMap
        self._grassland = grassland
        self._forest = forest

        self._preprocessed_forest = self.preprocess_forest(forestMap)
        self._visited_map = np.zeros(self._preprocessed_forest.shape)

        # index offset around 8 sides of the point
        self._row_offset = np.array([-1, -1, -1,  0, 0,  1, 1, 1])
        self._col_offset = np.array([-1,  0,  1, -1, 1, -1, 0, 1])

        # hold in memory forestMap row and columns range indexes
        self._row_range = list(range(self._preprocessed_forest.shape[0]))
        self._col_range = list(range(self._preprocessed_forest.shape[1]))

    def transform_input(self, input: chr) -> bool:
        """ Transforms input to either 0 or 1, otherwise raise and Exception

        Args:
            input: crh - single character that represents grassland or forest

        Returns:
            Returns int, either 0 or 1 respectfully to the input
        """
        if input == self._grassland:
            return 0
        elif input == self._forest:
            return 1
        else:
            raise Exception(f"Wrong forest input: {input}")

    def preprocess_forest(self, forestMap: typing.Iterable[str]) -> np.ndarray:
        """ Transform given forestMap in typing.Iterable[str] to typing.Iterable[int]
            Fixes wrong length forest rows by adding grassland to it

            Args:
                forestMap: typing.Iterable[str] - forestMap to be preprocessed

            Return:
                forestMap: np.ndarray - preprocessed forestMap in binary format
        """
        preprocessed_forest = []
        longest_string = len(max(forestMap, key=len))
        for row in forestMap:
            preprocessed_forest.append([self.transform_input(r) for r in row])
            if len(preprocessed_forest[-1]) < longest_string:
                preprocessed_forest[-1] += [0] * (longest_string-len(preprocessed_forest[-1]))

        return np.array(preprocessed_forest, dtype=int)

    def check_neightbours(self, row: int, col: int) -> bool:
        """ Checks neighbouts in forestMap with given row and col indexes

        Args:
            row: int - index of current position in row
            col: int - index of current position in col

        Returns:
            found_forest: bool - return true if found forest within neighbours otherweise terurns False
        """
        self._visited_map[row][col] = 1
        if self._preprocessed_forest[row][col] == 0:
            return False

        found_forest = False

        for row_n, col_n in zip(self._row_offset + row, self._col_offset + col):
            if row_n not in self._row_range or col_n not in self._col_range:
                continue

            if self._visited_map[row_n][col_n]:
                continue

            self._visited_map[row_n][col_n] = 1
            if not self._preprocessed_forest[row_n][col_n]:
                continue

            else:
                found_forest = True
                self.check_neightbours(row_n, col_n)

        return found_forest


    def get_forests(self) -> int:
        """ Returns the count of forrests in given forestMap
        """
        forest_counter = 0
        for row in self._row_range:
            for col in self._col_range:
                if self._visited_map[row][col]:
                    continue

                if self.check_neightbours(row, col):
                    forest_counter += 1

        return forest_counter


if __name__ == '__main__':
    # forestMap = [
    #     '0X0X0',
    #     '00XX0',
    #     '00000', 
    #     '0XX00', 
    # ]
    forestMap = [
        '0X0X000',
        '00XX000',
        '00000XX', 
        '0XX000X', 
    ]

    forest = ForestCounter(forestMap)
    print("Forests:", forest.get_forests())