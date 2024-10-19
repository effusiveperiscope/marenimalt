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
        }):
        with tempconfig(manim_config):
            scene = MarenimaltScene(self.data, self.cfg)
            scene.render()

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

                image = ImageMobject(image_loc)
                image.scale(0.3)
                self.play(FadeIn(image, run_time=self.transition_times))

                for record in d:
                    audio_file = record['audio_file']
                    _type = record['type']
                    if self.cfg.type_map is not None:
                        _type = self.cfg.type_map[_type]

                    audio = AudioSegment.from_file(audio_file)
                    duration = len(audio) / 1000.0

                    text2 = MarkupText(wrap_text(_type, width=50),
                        font_size=24.0)
                    text2.to_edge(DOWN)

                    self.add_sound(audio_file)
                    self.play(Write(text2, run_time=self.transition_times))
                    self.wait(duration)
                    self.play(FadeOut(text2, run_time=self.transition_times))

                self.play(FadeOut(image, run_time=self.transition_times))

            self.play(FadeOut(text, run_time=self.transition_times))