from vedo import Slider2D
#custom classes to save values while creating other objects
class CustomSlider(Slider2D):
    def __init__(self, sliderfunc, xmin, xmax, value=None, pos=4, title="", font="Calco", title_size=1, c="k", alpha=1, show_value=True, delayed=False, **options):
        self.sliderfunc = sliderfunc
        super().__init__(sliderfunc, xmin, xmax, value, pos, title, font, title_size, c, alpha, show_value, delayed, **options)