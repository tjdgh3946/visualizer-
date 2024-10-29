import time
from IPython.display import Audio, display, HTML


class Beeper:

    def __init__(self, threshold, url=None, longjob_url=None, click_url=None):
        self.threshold = threshold
        self.start_time = None  # time in sec, or None
        self.shortjob_audio = url
        self.longjob_audio = longjob_url 
        self.click_audio = click_url

    def pre_execute(self):
        if not self.start_time:
            self.start_time = time.time()
            if self.click_audio:
                sound_file = self.click_audio
                display(
                    HTML(
                        f"""
                <audio id="hidden-audio" autoplay hidden>
                <source src="{sound_file}" type="audio/mpeg">
                Your browser does not support the audio element.
                </audio>
                """
                    )
                )

    def post_execute(self):
        end_time = time.time()
        if self.start_time and end_time - self.start_time > self.threshold:
            if end_time - self.start_time > 10*self.threshold:
                sound_file = self.longjob_audio
            else:
                sound_file = self.shortjob_audio 
            display(
                HTML(
                    f"""
            <audio id="hidden-audio" autoplay hidden>
            <source src="{sound_file}" type="audio/mpeg">
            Your browser does not support the audio element.
            </audio>
            """
                )
            )
        self.start_time = None
