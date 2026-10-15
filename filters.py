"""
Абстрактный интерфейс фильтров для медиаобъектов (видео и аудио) и его
конкретные реализации.

Фильтр работает с любым MediaObject (Video или Audio) — демонстрация
полиморфизма, поскольку оба типа наследуют общие атрибуты duration и
file_size из базового класса.
"""

from abc import ABC, abstractmethod

from media_objects import MediaObject


class MediaFilter(ABC):
    """Абстрактный базовый класс для фильтров медиаобъектов."""

    @abstractmethod
    def apply(self, media_obj):
        """Применяет фильтр к медиаобъекту и возвращает изменённый объект."""
        raise NotImplementedError


class CompressionFilter(MediaFilter):
    """Фильтр сжатия: уменьшает размер файла на заданный коэффициент."""

    def __init__(self, factor: float = 0.5):
        if not (0 < factor <= 1):
            raise ValueError("Коэффициент сжатия должен быть в диапазоне (0, 1]")
        self.factor = factor

    def apply(self, media_obj):
        if not isinstance(media_obj, MediaObject):
            raise TypeError("Фильтр применяется только к объектам MediaObject")
        media_obj.file_size = round(media_obj.file_size * self.factor, 2)
        return media_obj


class TrimFilter(MediaFilter):
    """Фильтр обрезки: ограничивает длительность максимальным значением."""

    def __init__(self, max_duration: int):
        if max_duration < 0:
            raise ValueError("Максимальная длительность не может быть отрицательной")
        self.max_duration = max_duration

    def apply(self, media_obj):
        if not isinstance(media_obj, MediaObject):
            raise TypeError("Фильтр применяется только к объектам MediaObject")
        media_obj.duration = min(media_obj.duration, self.max_duration)
        return media_obj


def process_media(media_obj, filters):
    """Последовательно применяет список фильтров к медиаобъекту (полиморфизм)."""
    result = media_obj
    for filter_obj in filters:
        result = filter_obj.apply(result)
    return result


if __name__ == "__main__":
    from media_objects import Audio, Video

    video = Video("movie.mp4", duration=5400, file_size=1500, resolution="1920x1080", fps=30)
    audio = Audio("track.mp3", duration=210, file_size=8, sample_rate=44100, bitrate=320)

    chain = [CompressionFilter(0.5), TrimFilter(max_duration=200)]

    for media in (video, audio):
        process_media(media, chain)
        print(media.get_info())
