from manim import *
from dataclasses import dataclass
from typing import Optional
from marenimalt.util import wrap_text
from pydub import AudioSegment

@dataclass
class MarenimaltConfig:
    type_map: Optional[dict] = None
    image_map: Optional[dict] = None
    content_key: str = 'utterance'
    type_key: str = 'model'
    image_key: str = 'character'
    audio_file_key: str = 'audio_file'

class Marenimalt:
    def __init__(self,
        data: list[dict[str,str]],
        cfg: MarenimaltConfig = MarenimaltConfig()):
        self.data = data
        self.cfg = cfg

    def export(
        self,
        filename: str,
        manim_config: dict = {
            'quality': 'low_quality',
            'preview': True,
            # Sound does not work without disable_caching
            'disable_caching': True,
        },
        use_ordered : bool = False):
        with tempconfig(manim_config):
            if not use_ordered:
                scene = MarenimaltScene(self.data, self.cfg)
            else:
                scene = MarenimaltOrderScene(self.data, self.cfg)
            scene.render()

# Non-order preserving
class MarenimaltScene(Scene):
    def __init__(self, inpdata, cfg):
        super().__init__()
        self.inpdata = inpdata
        self.cfg = cfg

        self.contents = {}

        # {
        #     content_key: {
        #         image_key: [
        #             {  
        #                 'audio_file': audio_file,
        #                 'type': type
        #             }
        #         ]
        #     }
        # }

        for d in inpdata:
            if not d[cfg.content_key] in self.contents:
                self.contents[d[cfg.content_key]] = {}
            ckd: dict = self.contents[d[cfg.content_key]]
            if not d[cfg.image_key] in ckd:
                ckd[d[cfg.image_key]] = []
            dd: list = ckd[d[cfg.image_key]]
            dd.append({
                'audio_file': d[cfg.audio_file_key],
                'type': d[cfg.type_key]})
        self.transition_times = 0.5

    def construct(self):
        #print(config)

        #text = Text('Hello world').scale(3)
        #self.play(Write(text))
        last_type = None
        text2 = None
        last_image = None
        imgobj = None
        for content, imd in self.contents.items():
            c: dict
            text = MarkupText(wrap_text(content, width=50), font_size=24.0)
            text.to_edge(UP)
            self.play(Write(text, run_time=self.transition_times))
            
            for image, d in imd.items():
                image_loc = image
                if self.cfg.image_map is not None:
                    image_loc = self.cfg.image_map[image_loc]
                d: list

                imgobj = ImageMobject(image_loc)
                imgobj.scale(0.3)
                self.play(FadeIn(imgobj, run_time=self.transition_times))

                for record in d:
                    audio_file = record['audio_file']
                    _type = record['model']
                    if self.cfg.type_map is not None:
                        _type = self.cfg.type_map[_type]

                    audio = AudioSegment.from_file(audio_file)
                    duration = len(audio) / 1000.0

                    if text2 is None:
                        text2 = MarkupText(wrap_text(_type, width=50),
                            font_size=24.0)
                        text2.to_edge(DOWN)
                        self.play(Write(text2, run_time=self.transition_times))
                    elif last_type != _type and text2 is not None:
                        self.play(FadeOut(text2, run_time=self.transition_times))
                        text2 = MarkupText(wrap_text(_type, width=50),
                            font_size=24.0)
                        text2.to_edge(DOWN)
                        self.play(Write(text2, run_time=self.transition_times))
                    self.add_sound(audio_file)
                    self.wait(duration)
                    last_type = _type

                self.play(FadeOut(imgobj, run_time=self.transition_times))
                last_image = image

            self.play(FadeOut(text, run_time=self.transition_times))

class MarenimaltOrderScene(Scene):
    def __init__(self, inpdata : list, cfg : MarenimaltConfig):
        self.inpdata = inpdata
        self.cfg = cfg
        self.transition_times = 0.5

    def construct(self):
        last_model = None
        model_text = None
        last_character = None
        character_img = None
        last_utterance = None
        utterance_text = None
        for record in self.inpdata:
            _type = record[self.cfg.type_key]
            if self.cfg.type_map is not None:
                _type = self.cfg.type_map[_type]
            _image = record[self.cfg.image_key]
            if self.cfg.image_map is not None:
                _image = self.cfg.image_map[_image]

            # TODO dry
            should_wait = False
            if character_img is None:
                character_img = ImageMobject(_image)
                character_img.scale(0.3)
                self.play(FadeIn(character_img, run_time=self.transition_times))
                should_wait = True
            elif last_character != _image and character_img is not None:
                character_img = ImageMObject(_image)
                character_img.scale(0.3)
                self.play(FadeIn(character_img, run_time=self.transition_times))
                should_wait = True

            if model_text is None:
                model_text = MarkupText(wrap_text(_type, width=50),
                    font_size=24.0)
                model_text.to_edge(DOWN)
                self.play(Write(model_text, run_time=self.transition_times))
                should_wait = True
            elif last_model != _type and model_text is not None:
                self.play(FadeOut(model_text, run_time=self.transition_times))
                model_text = MarkupText(wrap_text(_type, width=50),
                    font_size=24.0)
                self.play(Write(model_text, run_time=self.transition_times))
                should_wait = True

            _utterance = record[self.cfg.content_key]
            if utterance_text is None:
                utterance_text = MarkupText(wrap_text(_utterance, width=50),
                    font_size=24.0)
                utterance_text.to_edge(DOWN)
                self.play(Write(utterance_text, run_time=self.transition_times))
                should_wait = True
            elif last_utterance != _utterance and utterance_text is not None:
                self.play(FadeOut(utterance_text, run_time=self.transition_times))
                utterance_text = MarkupText(wrap_text(_utterance, width=50),
                    font_size=24.0)
                self.play(Write(utterance_text, run_time=self.transition_times))
                should_wait = True

            if should_wait:
                self.wait(self.transition_times)

            last_model = _type
            last_character = _image
            last_utterance = _utterance