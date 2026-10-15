"""
Модуль с классами для мультимедийных объектов.
Вариант 4: смешанный (видео + аудио) — длительность, размер файла.
"""


class MediaObject:
    """Базовый класс для всех мультимедийных объектов."""

    def __init__(self, filename, duration=0, file_size=0):
        if not filename:
            raise ValueError("Имя файла не может быть пустым")
        if duration < 0:
            raise ValueError("Длительность не может быть отрицательной")
        if file_size < 0:
            raise ValueError("Размер файла не может быть отрицательным")

        self.filename = filename
        self.duration = duration
        self.file_size = file_size

    def get_info(self):
        """Возвращает строку с базовой информацией об объекте."""
        return f"{self.filename}: {self.duration} сек, {self.file_size} МБ"

    def get_file_size(self):
        """Возвращает размер файла в мегабайтах."""
        return self.file_size

    def compare_duration(self, other):
        """Сравнивает длительность с другим медиаобъектом.

        Возвращает разницу в секундах (self.duration - other.duration):
        положительное число, если self длиннее other.
        """
        if not isinstance(other, MediaObject):
            raise TypeError("Сравнивать можно только с другим MediaObject")
        return self.duration - other.duration

    def __str__(self):
        return f"<{self.__class__.__name__}({self.filename})>"


class Video(MediaObject):
    """Класс для работы с видеофайлами (MP4, MKV)."""

    def __init__(self, filename, duration=0, file_size=0, resolution="0x0", fps=0):
        super().__init__(filename, duration, file_size)

        if fps < 0:
            raise ValueError("FPS не может быть отрицательным")

        self.resolution = resolution
        self.fps = fps

    def get_info(self):
        info = super().get_info()
        return f"{info}, {self.resolution}, {self.fps} FPS"


class Audio(MediaObject):
    """Класс для работы с аудиофайлами (MP3, WAV)."""

    def __init__(self, filename, duration=0, file_size=0, sample_rate=44100, bitrate=192):
        super().__init__(filename, duration, file_size)

        if sample_rate <= 0:
            raise ValueError("Частота дискретизации должна быть положительной")
        if bitrate <= 0:
            raise ValueError("Битрейт должен быть положительным")

        self.sample_rate = sample_rate
        self.bitrate = bitrate

    def get_info(self):
        info = super().get_info()
        return f"{info}, {self.sample_rate} Гц, {self.bitrate} кбит/с"


class MediaLibrary:
    """Класс для управления коллекцией медиафайлов."""

    def __init__(self):
        self.media_objects = []

    def add(self, media_obj):
        """Добавляет объект в коллекцию."""
        if not isinstance(media_obj, MediaObject):
            raise TypeError("В библиотеку можно добавлять только объекты MediaObject")
        self.media_objects.append(media_obj)

    def get_total_duration(self):
        """Возвращает общую длительность всех объектов (0 для пустой коллекции)."""
        return sum(obj.duration for obj in self.media_objects)

    def get_total_size(self):
        """Возвращает суммарный размер всех объектов в мегабайтах."""
        return sum(obj.file_size for obj in self.media_objects)

    def filter_by_type(self, media_type):
        """Возвращает список объектов заданного типа."""
        return [obj for obj in self.media_objects if isinstance(obj, media_type)]


if __name__ == "__main__":
    library = MediaLibrary()

    video = Video("movie.mp4", duration=5400, file_size=1500, resolution="1920x1080", fps=30)
    audio = Audio("track.mp3", duration=210, file_size=8, sample_rate=44100, bitrate=320)

    library.add(video)
    library.add(audio)

    print(f"Всего объектов: {len(library.media_objects)}")
    print(f"Общая длительность: {library.get_total_duration()} сек")
    print(f"Общий размер: {library.get_total_size()} МБ")
    print(f"Разница в длительности (видео - аудио): {video.compare_duration(audio)} сек")

    for item in library.media_objects:
        print(item.get_info())
