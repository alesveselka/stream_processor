from typing import Any, Dict, Iterable, List, Tuple



def streaming_statistics(stream: Iterable) -> List[Dict[str, Any]]:
	'''
	Calculates cumulative arithmetic mean and Standard Deviation over the numbers in a stream passed in

	There is actually `statistics.stdev` in standard Python 3.4+ library, that could be used as well.
	'''
	stats = []
	cum_sum = 0.0
	cum_len = 0
	cum_items = []
	mean = None
	std = None
	for item in stream:
		cum_items.append(item)
		# I could as well use list comprehension instead of cumulatively adding the values, but this should be faster
		cum_sum += item
		cum_len += 1
		if cum_len > 1:
			# Calculate arithmetic mean
			mean = cum_sum / cum_len

			# Sum of all deviations, i.e. squared difference of the numbers less the mean
			deviations = sum((x - mean) ** 2 for x in cum_items)

			# Variance is 1/length * sum of deviations
			variance = deviations / (cum_len - 1)

			# And Standard Deviation is Square-root of Variance
			std = variance ** 0.5
		stats.append({'mean': mean, 'std': std})
	return stats
