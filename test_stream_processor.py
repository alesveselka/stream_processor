import itertools

import pytest

from primes import is_prime, only_primes
from stream_processor import StreamProcessor
from stats import streaming_statistics


def test_processor_with_prime_mapper() -> None:
	# Given range of 100 numbers and mapping function that append 'prime' flag
	numbers = range(100)

	# When I run the processor
	processor = StreamProcessor(numbers, is_prime)

	# Then I should be able to slide 10 items from the result
	slice = list(itertools.islice(processor, 10))
	assert len(slice) == 10

	# And list of the slice should have 10 Tuples with boolean flag and the number as first and second items, respectively
	for item in list(slice):
		assert isinstance(item, tuple)
		assert isinstance(item[0], bool)
		assert isinstance(item[1], int)


def test_only_primes_reduce_generator() -> None:
	# Given range of 100 numbers and mapping function that append 'prime' flag
	numbers = range(100)

	# When I run the processor with 'only_primes' generator passed in
	processor = StreamProcessor(numbers, is_prime, only_primes)

	# Then I should be able to slide 10 items from the result
	slice = list(itertools.islice(processor, 10))
	assert len(slice) == 10

	# And list of the slice should have 10 integers, each being a prime number
	for prime in slice:
		assert is_prime(prime)[0]


def test_processor_statistics() -> None:
	# Given range of 30 numbers and mapping function that append 'prime' flag
	numbers = range(30)

	# When I run the processor with 'only_primes' generator passed in
	processor = StreamProcessor(numbers, is_prime, only_primes)

	# And calculate the prime stream statistics
	raw, stats = itertools.tee(processor)
	calculated_stats = list(zip(raw, streaming_statistics(stats)))

	# Then I should see correct statistics along side the prime numbers
	expected_stats = [
		(2, {'mean': None, 'std': None}),
		(3, {'mean': 2.5, 'std': 0.7071067811865476}),
		(5, {'mean': 3.3333333333333335, 'std': 1.5275252316519465}),
		(7, {'mean': 4.25, 'std': 2.217355782608345}),
		(11, {'mean': 5.6, 'std': 3.5777087639996634}),
		(13, {'mean': 6.833333333333333, 'std': 4.400757510550504}),
		(17, {'mean': 8.285714285714286, 'std': 5.55920515044749}),
		(19, {'mean': 9.625, 'std': 6.3905622377288305}),
		(23, {'mean': 11.11111111111111, 'std': 7.457285773732365}),
		(29, {'mean': 12.9, 'std': 9.024041962077378})
	]

	for calculated, expected in zip(calculated_stats, expected_stats):
		assert calculated[0] == expected[0]
		if calculated[0] > 2 and expected[0] > 2:
			assert calculated[1]['mean'] - expected[1]['mean'] == pytest.approx(0)
			assert calculated[1]['std'] - expected[1]['std'] == pytest.approx(0)
