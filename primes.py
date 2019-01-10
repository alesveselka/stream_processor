from typing import Generator, Iterator, Tuple



def is_prime(n: float) -> Tuple[bool, float]:
	# time.sleep(3)

	if n < 2:
		return False, n
	elif n == 2:
		return True, n
	sqrt_n = int(n**0.5)+1
	return len([i for i in range(2, sqrt_n+1) if n % i == 0]) == 0, n


def only_primes(stream: Iterator) -> Generator[int, Iterator, None]:
	try:
		while True:
			is_valid, value = next(stream)
			while not is_valid:
				is_valid, value = next(stream)
			yield value
	except StopIteration:
		return
