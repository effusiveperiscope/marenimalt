from marenimalt.core import Marenimalt

def test_core():
    data = [
        {'character': 'tests/twilight.png',
        'utterance': 'Letting the mares go by.',
        'model': 'rvc',
        'audio_file': 'tests/twilight.flac',
        },
        {'character': 'tests/fluttershy.png',
        'utterance': 'Letting the mares go by.',
        'model': 'rvc',
        'audio_file': 'tests/fluttershy.flac',
        },
        {'character': 'tests/rarity.png',
        'utterance': 'Letting the mares go by too.',
        'model': 'rvc',
        'audio_file': 'tests/rarity.flac'
        },
    ]
    Marenimalt(data=data).export('test_video.mp4')