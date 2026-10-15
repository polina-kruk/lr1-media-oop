"""
Тестовый скрипт для проверки классов MediaObject, Video, Audio, MediaLibrary
и фильтров из filters.py.
"""

from media_objects import Audio, MediaLibrary, MediaObject, Video
from filters import CompressionFilter, TrimFilter, process_media


def test_media_object():
    obj = MediaObject("clip.raw", duration=42, file_size=10)
    assert obj.get_info() == "clip.raw: 42 сек, 10 МБ"
    assert str(obj) == "<MediaObject(clip.raw)>"
    print("MediaObject: OK")


def test_media_object_validation():
    try:
        MediaObject("", duration=10)
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалась ошибка на пустое имя файла")

    try:
        MediaObject("clip.raw", duration=-5)
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалась ошибка на отрицательную длительность")

    try:
        MediaObject("clip.raw", duration=5, file_size=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалась ошибка на отрицательный размер файла")

    print("Валидация MediaObject: OK")


def test_video():
    video = Video("movie.mp4", duration=5400, file_size=1500, resolution="1920x1080", fps=30)
    assert video.get_file_size() == 1500
    assert "1920x1080" in video.get_info()
    assert "30 FPS" in video.get_info()
    print("Video: OK")


def test_audio():
    audio = Audio("track.mp3", duration=210, file_size=8, sample_rate=44100, bitrate=320)
    assert audio.get_file_size() == 8
    assert "44100 Гц" in audio.get_info()
    assert "320 кбит/с" in audio.get_info()
    print("Audio: OK")


def test_compare_duration():
    video = Video("movie.mp4", duration=5400, file_size=1500)
    audio = Audio("track.mp3", duration=210, file_size=8)
    assert video.compare_duration(audio) == 5190
    assert audio.compare_duration(video) == -5190
    print("compare_duration: OK")


def test_media_library():
    library = MediaLibrary()
    assert library.get_total_duration() == 0

    library.add(Video("a.mp4", duration=100, file_size=500))
    library.add(Audio("b.mp3", duration=50, file_size=5))

    assert library.get_total_duration() == 150
    assert library.get_total_size() == 505
    assert len(library.filter_by_type(Video)) == 1
    assert len(library.filter_by_type(Audio)) == 1
    print("MediaLibrary: OK")


def test_filters():
    video = Video("movie.mp4", duration=5400, file_size=1500, resolution="1920x1080", fps=30)

    process_media(video, [CompressionFilter(0.5), TrimFilter(max_duration=200)])

    assert video.file_size == 750
    assert video.duration == 200
    print("Фильтры: OK")


if __name__ == "__main__":
    test_media_object()
    test_media_object_validation()
    test_video()
    test_audio()
    test_compare_duration()
    test_media_library()
    test_filters()
    print("\nВсе тесты пройдены успешно.")
