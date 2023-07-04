from permutation import *

n = 9

a = random_permutation(n)
b = random_permutation(n)
print(f'a = \n{a}')
print(f'b = \n{b}')
print(f'a * b = \n{a * b}')
print(f'a^b = \n{a ** b}')  # bab^{-1}
print(f'b^5 = \n{b ** 5}')
print(f'a^{-3} = \n{a ** (-3)}')


print(f'Ord(a) = {a.order}')
print(a**a.order == unity(n))  # Should be true

print()
print(Permutation.two_generators_decomposition.__doc__)  # documentation
print(f'a = {a.two_generators_decomposition}')
print(f'b = {b.two_generators_decomposition}')
