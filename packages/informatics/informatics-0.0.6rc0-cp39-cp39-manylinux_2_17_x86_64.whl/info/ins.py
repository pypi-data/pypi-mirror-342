from info.basic import instances as datasets
from info.docfunc import args_highlighter


_escape = True
if not _escape:
    args_highlighter(datasets)


__all__ = [_ for _ in dir() if _[:1] != '_' and _ != 'args_highlighter']


if __name__ == '__main__':
    pass
