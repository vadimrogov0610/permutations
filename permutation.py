from itertools import permutations
from math import lcm
from random import shuffle


class Permutation:
    def __init__(self, permutation: tuple):
        assert set(permutation) == set(range(1, len(permutation) + 1)),\
            "permutation should contain consecutive numbers from 1 to n"
        self.permutation = permutation
        self.length = len(self.permutation)

    @property
    def number_of_cycles(self):
        return len(self.cyclic_repr)

    @property
    def cyclic_repr(self):
        """
        list of cycles
        """
        s = set(self.permutation)
        ans = []
        while s:
            start = min(s)
            lst = [start]
            s.remove(start)
            curr = start
            while self.permutation[curr - 1] != start:
                curr = self.permutation[curr - 1]
                lst.append(curr)
                s.remove(curr)
            ans.append(tuple(lst))
        return ans

    @property
    def lengths_of_cycles(self):
        """
        lengths of cycles in descending order
        """
        return sorted([len(x) for x in self.cyclic_repr], reverse=True)

    def __repr__(self):
        return '  '.join(f"{i + 1}" for i in range(self.length)) + '\n' +\
               '  '.join("↓" for _ in range(self.length)) + '\n' +\
               '  '.join(f"{self.permutation[i]}" for i in range(self.length)) + ' \n' +\
               f'cycles: ' + " ".join(str(t) for t in self.cyclic_repr) + '\n'

    def __mul__(self, other):
        """
        Note than in self * other the first permutation made is other and second is self
        """
        assert self.length == other.length, "The lengths of the permutations must be equal to each other"
        return Permutation(tuple(self.permutation[other.permutation[i] - 1] for i in range(self.length)))

    def __invert__(self):
        """
        multiplicative inverse of self
        """
        return Permutation(tuple(x[1] for x in sorted(zip(self.permutation, range(1, self.length + 1)))))

    def __pow__(self, power):
        """
        if power is another permutation then it's conjugation in symmetric group
        if power is a number then it's usual power
        """
        if type(power) == Permutation:
            return power * self * (~power)
        if power >= 0:
            ans = unity(self.length)
            for x in range(power):
                ans *= self
            return ans
        return (~self) ** (-power)

    def __eq__(self, other):
        return self.permutation == other.permutation

    def is_conjugate_with(self, other):
        """
        check for two elements if they are conjugate
        """
        return self.lengths_of_cycles == other.lengths_of_cycles

    @property
    def conjugacy_class(self):
        """
        list of permutations which are conjugate with self
        """
        return [Permutation(x) for x in permutations(range(1, self.length + 1))
                if self.is_conjugate_with(Permutation(x))]

    @property
    def order(self):
        """
        order in Symmetric group
        """
        return lcm(*self.lengths_of_cycles)

    @property
    def two_generators_decomposition(self):
        """Representation of a permutation as a product of powers of 2 generators
t: transposition (1, 2)
c: long cycle (1, 2, ..., n)
        """
        c = long_cycle(self.length)
        t = transposition12(self.length)
        e = unity(self.length)

        ans = []

        a = ~self
        while a != e:
            if (a.permutation[0] > a.permutation[1]) and (a.permutation[0] != a.length):
                a *= t
                if ans and ans[-1][0] == "t":
                    ans[-1][1] += 1
                else:
                    ans.append(["t", 1])
            else:
                a *= c
                if ans and ans[-1][0] == "c":
                    ans[-1][1] += 1
                else:
                    ans.append(["c", 1])
        return ''.join(f'{x[0]}^{x[1]}' if x[1] != 1 else x[0] for x in ans) if ans else "e"


def all_permutations(n):
    """
    generator for entire symmetric group
    """
    for x in permutations(range(1, n + 1)):
        yield Permutation(x)


def unity(n):
    """
    unity in symmetric group
    """
    return Permutation(tuple(i + 1 for i in range(n)))


def long_cycle(n):
    """
    cycle (1, 2, ..., n) symmetric group
    """
    return Permutation(tuple(((i + 1) % n) + 1 for i in range(n)))


def transposition12(n):
    """
    transposition (1, 2) symmetric group
    """
    assert n > 1, "n should be more than 1"
    return Permutation(tuple([2, 1] + list(range(3, n + 1))))


def random_permutation(n):
    lst = list(range(1, n + 1))
    shuffle(lst)
    return Permutation(tuple(lst))
