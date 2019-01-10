from typing import Callable, Iterable, Iterator, Optional

import multiprocessing



class StreamProcessor:

	def __init__(
		self,
		input_stream: Iterable,
		map_function: Callable,
		reduce_generator: Optional[Callable] = None,
		*,
		number_of_processes: int = multiprocessing.cpu_count()
	) -> None:
		self._input_stream = input_stream
		self._map_function = map_function
		self._reduce_generator = reduce_generator
		self._pool = multiprocessing.Pool(processes = number_of_processes)


	def __iter__(self) -> Iterator:
		if self._reduce_generator:
			for item in self._reduce_generator(iter(self._pool.imap(self._map_function, self._input_stream))):
				yield item
		else:
			for item in self._pool.imap(self._map_function, self._input_stream):
				yield item

		self._pool.terminate()
		self._pool.join()
