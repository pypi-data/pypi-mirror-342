from info.toolbox.networks import Module, full_connected_neural, convolutional_neural, unet, transformer
from info.docfunc import args_highlighter


_escape = True
if not _escape:
    args_highlighter(Module, full_connected_neural, convolutional_neural, unet, transformer)


__all__ = [_ for _ in dir() if _[:1] != '_' and _ != 'args_highlighter']


if __name__ == '__main__':
    pass
