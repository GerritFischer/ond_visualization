from vedo import Slider2D, Button
#custom classes to save values while creating other objects
class CustomSlider(Slider2D):
    def __init__(self, sliderfunc, xmin, xmax, value=None, pos=4, title="", font="Calco", title_size=1, c="k", alpha=1, show_value=True, delayed=False, **options):
        self.sliderfunc = sliderfunc
        self.pos = pos
        self.value = value
        self.title=title
        self.show_value=show_value
        super().__init__(sliderfunc, xmin, xmax, value=value, pos=pos, title=title, font=font, title_size=title_size, c=c, alpha=alpha, show_value=show_value, delayed=delayed, **options)

class CustomButton(Button):
    def __init__(self, fnc=None, states='Button', c='white',	bc='green4',pos=(0.7, 0.1),	size=24, font='Courier', bold=True,	italic=False,	alpha=1, angle=0):
        self.font_s = font
        self.size_s = size
        super().__init__(fnc, states, c, bc, pos, size, font, bold, italic, alpha, angle)