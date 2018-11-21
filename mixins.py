import svgwrite


class RGBMixin(object):

    @staticmethod
    def hex_to_rgb(hex_):
            hex_ = hex_.lstrip('#')
            r, g, b = tuple(int(hex_[i:i + 2], 16) for i in (0, 2, 4))
            return svgwrite.utils.rgb(r, g, b)


class NameMixin(object):

    def __repr__(self):
        return self.__class__.__name__
