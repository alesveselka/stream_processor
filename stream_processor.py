from typing import Callable, Iterable, Iterator, List, Optional

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
		self._reduce_generator = reduce_generator
		self._processed: Optional[List] = None

		# Process input stream in mapping function provided.
		# Similar functionality could be implemented with Futures and `concurrent.futures.Executor`
		with multiprocessing.Pool(processes = number_of_processes) as pool:
			mapped = pool.map(map_function, input_stream)

		self._mapped = mapped


	def __items(self) -> List:
		'''
		Return mapped input stream, or processed generator if specified;
		saves the result in a variable if accessed again
		'''
		if not self._processed:
			self._processed = [result for result in self._reduce_generator(iter(self._mapped))] \
				if self._reduce_generator else self._mapped
		return self._processed


	def __len__(self) -> int:
		return len(self.__items())


	def __iter__(self) -> Iterator:
		for item in self.__items():
			yield item
