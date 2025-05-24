import random
from typing import Callable, List, Iterable, Tuple

from problog.logic import Term, list2term, Constant
from torch.utils.data import Dataset as TensorDataset
from deepproblog.dataset import Dataset
from deepproblog.query import Query

from .mixmnist import MIXMNIST_BASE

class MNISTOperator(Dataset, TensorDataset):
    def __getitem__(self, index: int) -> Tuple[list, list, int]:
        l1, l2 = self.data[index]
        print("L1L2",l1,l2)
        label = self._get_label(index)
        l1 = [self.dataset[x][0] for x in l1]
        l2 = [self.dataset[x][0] for x in l2]
        return l1, l2, label

    def __init__(
        self,
        dataset_name: str,
        function_name: str,
        operator: Callable[[List[int]], int],
        size=1,
        arity=2,
        seed=None,
        prefix="None"
    ):
        """Generic dataset for operator(img, img) style datasets.

        :param dataset_name: Dataset to use (train, val, test)
        :param function_name: Name of Problog function to query.
        :param operator: Operator to generate correct examples
        :param size: Size of numbers (number of digits)
        :param arity: Number of arguments for the operator
        :param seed: Seed for RNG
        """
        super(MNISTOperator, self).__init__()
        assert size >= 1
        assert arity >= 1
        self.dataset_name = dataset_name
        self.dataset = (MIXMNIST_BASE(prefix=prefix).datasets)[self.dataset_name]
        self.function_name = function_name
        self.operator = operator
        self.size = size
        self.arity = arity
        self.seed = seed
        mnist_indices = list(range(len(self.dataset)))
        if seed is not None:
            rng = random.Random(seed)
            rng.shuffle(mnist_indices)
        dataset_iter = iter(mnist_indices)
        # Build list of examples (mnist indices): [[2,3],[5,7],...] a list of arities of each query
        self.data = []
        try:
            while True:
                self.data.append(
                    [
                        [next(dataset_iter) for _ in range(self.size)]
                        for _ in range(self.arity)
                    ]
                )
        except StopIteration:
            pass

    def _dig2num(self, digits:List[int]) -> int:
        number = 0
        for d in digits:
            number *= 10
            number += d
        return number

    def to_query(self, i: int) -> Query:
        """Generate queries"""
        mnist_indices = self.data[i]
        expected_result = self._get_label(i)

        # Build substitution dictionary for the arguments
        subs = dict()
        var_names = []
        for i in range(self.arity):
            inner_vars = []
            for j in range(self.size):
                t = Term(f"p{i}_{j}")
                subs[t] = Term(
                    "tensor",
                    Term(
                        self.dataset_name,
                        Constant(mnist_indices[i][j]),
                    ),
                )
                inner_vars.append(t)
            var_names.append(inner_vars)

        # Build query
        if self.size == 1:
            args = [e[0] for e in var_names]
        else:
            args = [list2term(e) for e in var_names]

        return Query(
            Term(
                self.function_name,
                *args,
                Constant(expected_result),
            ),
            subs,
        )

    def _get_label(self, i: int):
        mnist_indices = self.data[i]
        # Figure out what the ground truth is, first map each parameter to the value:
        ground_truth = []
        for idx_tuple in mnist_indices:
            digits = [self.dataset[j][1] for j in idx_tuple]
            number = self._dig2num(digits)
            ground_truth.append(number)

        # Then compute the expected value:
        expected_result = self.operator(ground_truth)
        return expected_result

    def __len__(self):
        print("call __len__ Operator:",len(self.data))
        return len(self.data)
