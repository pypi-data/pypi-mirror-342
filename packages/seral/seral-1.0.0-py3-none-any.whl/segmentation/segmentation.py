import numpy as np
from collections.abc import Generator, Iterable

class Segmentor:
    
    dx_threshold: float
    min_segment_length: int
    max_segment_length: int
    def __init__(self, dx_threshold: float, min_segment_length: int = 10, max_segment_length: int = np.inf):
        self.dx_threshold = dx_threshold
        if min_segment_length < 1:
            raise ValueError("min_segment_length must be greater than 0")
        self.min_segment_length = min_segment_length
        if max_segment_length < min_segment_length:
            raise ValueError("max_segment_length must be greater than min_segment_length")
        self.max_segment_length = max_segment_length

    def get_segments_with_indices(self, data: Iterable) -> Generator[list[tuple[np.ndarray, np.ndarray]], None, None]:
        
        segment: list[float] = []
        for i,x in enumerate(data):
            if len(segment) < self.min_segment_length or len(segment) == 0:
                segment.append(x)
                continue

            dx: float = x - segment[-1]
            if dx < -self.dx_threshold or len(segment) >= self.max_segment_length:
                yield np.array(segment), np.arange(start=i - len(segment), stop=i, step=1)
                segment = [segment[-1]]

            segment.append(x)

        return None
    
    def get_segments(self, data: Iterable) -> Generator[list[np.ndarray], None, None]:
        for segment, _ in self.get_segments_with_indices(data):
            yield segment