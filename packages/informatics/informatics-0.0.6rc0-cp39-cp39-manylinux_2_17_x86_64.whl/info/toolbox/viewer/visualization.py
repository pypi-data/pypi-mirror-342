from info.basic.functions import assert_info_raiser
from info.basic.decorators import FuncTools
from info.basic.typehint import T
from info.basic.core import TrialDict, F
import info.docfunc as doc
from typing import Union, Optional, Literal, Any
import numpy as np
from numpy import ndarray
from warnings import warn


pg = __import__('pyqtgraph')
Qt = getattr(pg.QtCore, 'Qt')
QMainWindow = getattr(pg.QtWidgets, 'QMainWindow')
QWidget = getattr(pg.QtWidgets, 'QWidget')
QHBoxLayout = getattr(pg.QtWidgets, 'QHBoxLayout')
distance_matrix = __import__('info.basic.functions', fromlist=['distance_matrix']).distance_matrix
dep = __import__('info.basic.visual', fromlist=['_empty_pen'])
_n_dup = getattr(dep, '_n_dup')
_empty_pen = getattr(dep, '_empty_pen')
_max_radius = getattr(dep, '_max_radius')
_polar_to_cartesian = getattr(dep, '_polar_to_cartesian')
_flat_list = getattr(dep, '_flat_list')
_polar_base = getattr(dep, '_polar_base')
_polar_custom = getattr(dep, '_polar_custom')
_cus_labs = getattr(dep, '_cus_labs')
_rescale_radar = getattr(dep, '_rescale_radar')
rescale_radar = F(lambda **kw: [m := _rescale_radar(kw.get('data'), kw.get('scale_base')),
                                (m[0], {'locations': m[1], 'scales': m[2]})][-1])
_cus_position = getattr(dep, '_cus_position')
_line_seg = getattr(dep, '_line_seg')
_box_items = getattr(dep, '_box_items')
_add_cus_labs = getattr(dep, '_add_cus_labs')
_radial_lines = getattr(dep, '_radial_lines')
_polar_ends = getattr(dep, '_polar_ends')
_attach_tag = getattr(dep, '_attach_tag')
_resort = getattr(dep, '_resort')
_spans = getattr(dep, '_spans')
_start_angles = getattr(dep, '_start_angles')
_to_cartesian1 = getattr(dep, '_to_cartesian1')
_to_cartesian2 = getattr(dep, '_to_cartesian2')
_fan = getattr(dep, '_fan')
_circle_fixer = getattr(dep, '_circle_fixer')
_labs_h = getattr(dep, '_labs_h')
_labs_v = getattr(dep, '_labs_v')
_contour_msk = getattr(dep, '_contour_msk')


class GrpSettings(dict):

    def __init__(self, *args, **kwargs):
        super(GrpSettings, self).__init__(*args, **kwargs)
        assert_info_raiser(all(['name' in self.keys(), isinstance(self.get('name'), list)]),
                           TypeError("argument 'name' must be assigned."))
        self._n_groups = len(self.get('name'))
        self._show_warning = kwargs.get('~verbosity', False)

    @property
    def sub(self):
        return self._n_groups

    @property
    def groups(self):
        # _iter = min(self.sub) if self.sub else 0
        _meta = self.copy()
        for k, v in _meta.items():
            if isinstance(v, list) and len(v) != self._n_groups:
                if self._show_warning:
                    warn(f"'{k}' not matches intrinsic number of groups, make adaptation automatically...")
                _meta.update({f"{k}": _n_dup(v, self._n_groups)})

        res = tuple({k: v[:self._n_groups] if isinstance(v, list) else v for k, v in _meta.items()}.copy()
                    for _ in range(self._n_groups))

        for idx, _dict in enumerate(res):
            for k, v in _dict.items():
                if isinstance(v, list):
                    res[idx][k] = v[idx]

        return res

    def update(self, **kwargs):
        return GrpSettings(**{**self, **kwargs})


_line_ = GrpSettings(**{'pen': [pg.mkPen(pg.intColor(_, hues=10), style=Qt.PenStyle.SolidLine) for _ in range(10)],
                        'symbol': ['o', 't', 't1', 't2', 't3', 's', 'p', 'star', 'd', '+'],
                        'symbolSize': 10,
                        'symbolBrush': [pg.intColor(_, hues=10) for _ in range(10)],
                        'name': ['group_' + str(_ + 1) for _ in range(10)]})
_scatter_ = GrpSettings(**{'pen': pg.mkPen((0, 0, 0, 0)),
                           'symbol': ['o', 't', 't1', 't2', 't3', 's', 'p', 'star', 'd', '+'],
                           'symbolSize': 10,
                           'symbolBrush': [pg.intColor(_, hues=10) for _ in range(10)],
                           'name': ['group_' + str(_ + 1) for _ in range(10)]})
_histogram_ = GrpSettings(**{'bins': 20, 'width': 0.8,
                             'brush': [pg.intColor(_, hues=10) for _ in range(10)],
                             'name': ['group_' + str(_ + 1) for _ in range(10)]})
_beeswarm_ = _scatter_.update(interval=10, method='exact')
_box_ = GrpSettings(**{'pen': pg.mkPen('k', width=1.6), 'band': 0.4,
                       'brush': [pg.intColor(_, hues=10) for _ in range(10)],
                       'name': ['group_' + str(_ + 1) for _ in range(10)]})
_radar_ = _line_.update(**{'n_grids': 8, 'pen_grids': pg.mkPen((0, 0, 0, 50), width=0.3), 'dim_names': np.array([])})
_pie_ = GrpSettings(**{'pen': pg.mkPen('k', width=0.3),
                       'name': ['group_' + str(_ + 1) for _ in range(10)],
                       'symbol': 's',
                       'symbolSize': 8,
                       'symbolBrush': [pg.intColor(_, hues=10) for _ in range(10)],
                       'radius': 10})
_image_ = GrpSettings(**{'name': []})
_heatmap_ = _image_.update(**{'tags': np.array([]), 'colorMap': 'CET-D1A', 'use_horizontal_tags': True})
_contour_ = _image_.update(**{'interval': 0.1, 'colorMap': 'CET-CBL1'})


class FigConfigs:
    Line = _line_
    Scatter = _scatter_
    Histogram = _histogram_
    Beeswarm = _beeswarm_
    Box = _box_
    Heatmap = _heatmap_
    Radar = _radar_
    Pie = _pie_
    Contour = _contour_
    Image = _image_


class _Sketcher:

    def __init__(self, sketch: str):
        _acceptable_type = ['line', 'scatter', 'histogram', 'box', 'beeswarm', 'heatmap', 'radar', 'pie', 'contour',
                            'image']
        assert_info_raiser(sketch in _acceptable_type,
                           ValueError(f"data loader should be option within {_acceptable_type}"))
        self.sketch = sketch

    def preprocess(self, configs: GrpSettings):

        if self.sketch == 'line':
            def func(x: Union[ndarray, tuple[ndarray, ndarray]]):
                if isinstance(x, tuple):
                    if x[0].ndim == 1 and not hasattr(x[0][0], '__len__'):
                        x = (np.array([x[0]]), np.array([x[1]]))
                else:
                    if x.ndim == 1 and not hasattr(x[0], '__len__'):
                        x = np.array([x])
                return x

            return func

        elif self.sketch == 'scatter':
            def func(x: tuple[ndarray, ndarray]):
                if x[0].ndim == 1 and not hasattr(x[0][0], '__len__'):
                    x = (np.array([x[0]]), np.array([x[1]]))
                return x

            return func

        elif self.sketch == 'histogram':
            bins = configs.get('bins', 20)

            def func(x: ndarray):
                if x.ndim == 1 and not hasattr(x[0], '__len__'):
                    x = np.array([x])
                ypos, xpos = [], []
                _min, _max = [], []
                for item in x:
                    _min.append(np.min(item))
                    _max.append(np.max(item))
                _min, _max = min(_min), max(_max)
                _bins = np.linspace(_min, _max, bins)
                _interval = np.diff(_bins)[0]
                for idx, item in enumerate(x):
                    height_, pos_ = np.histogram(item, bins=_bins)
                    ypos.append(height_)
                    xpos.append(pos_[1:] + idx * 0.1 * _interval)
                return np.array(xpos, dtype=object), np.array(ypos, dtype=object)

            return func

        elif self.sketch == 'beeswarm':
            spacing, shuffle = configs.get('spacing', 0.2), configs.get('shuffle', True)
            bidir, method = configs.get('bidir', True), configs.get('method', 'exact')
            interval = configs.get('interval', 5)

            def func(x: ndarray):
                if x.ndim == 1 and not hasattr(x[0], '__len__'):
                    x = np.array([x])
                ypos, xpos = [], []
                for idx, item in enumerate(x):
                    ypos.append(item)
                    xpos.append(pg.pseudoScatter(item, spacing=spacing, shuffle=shuffle, bidir=bidir,
                                                 method=method) + idx * interval)
                return np.array(xpos, dtype=object), np.array(ypos, dtype=object)

            return func

        elif self.sketch == 'box':
            def func(x: ndarray):
                if x.ndim == 1 and not hasattr(x[0], '__len__'):
                    x = np.array([x])
                ypos = []
                for idx, item in enumerate(x):
                    ypos.append(np.quantile(item, [0, 0.25, 0.5, 0.75, 1]))
                return np.array(ypos, dtype=object)

            return func

        elif self.sketch == 'heatmap':
            def func(x: ndarray):
                is_distance_matrix = False
                if x.ndim == 1:
                    x = x[..., np.newaxis]
                if x.ndim == 2:
                    if all([(a-b) == 0 for a, b in zip(x.shape, x.T.shape)]):  # is squared
                        if np.sum(x-x.T) == 0:  # is symmetric
                            is_distance_matrix = True
                res = x if is_distance_matrix else distance_matrix(x)
                return np.flip(res.T, axis=1)

            return func

        elif self.sketch == 'radar':
            def func(x: ndarray):
                return _polar_to_cartesian(x)

            return func

        elif self.sketch == 'pie':
            def func(x: ndarray):
                assert_info_raiser(all([x.ndim == 1, np.abs(np.sum(x) - 1) < 1e-10 or np.abs(np.sum(x) - 100) < 1e-10]),
                                   TypeError('data must be series of fractions with sum of 1 or 100.'))
                return x * 0.01 if np.abs(np.sum(x) - 100) < 1e-10 else x

            return func

        elif self.sketch == 'contour':
            def func(x: ndarray):
                assert_info_raiser(x.ndim == 2, TypeError('data must be 2D array of altitude numeric.'))
                return x

            return func

        else:  # self.sketch == 'image'
            def func(x: ndarray):
                assert_info_raiser(x.ndim == 2 or all([x.ndim == 3, x.shape[-1] in (3, 4)]),
                                   ValueError('data should be ndarray with 2 dims, or 3 dims with 3 or 4 channels'))
                return x

            return func

    def figure(self, configs: GrpSettings):
        _configs = configs.groups

        if self.sketch == 'line':
            def func(x: Union[ndarray, tuple[ndarray, ndarray]]):
                res, count = [], 0
                if isinstance(x, tuple):
                    for _x, _y in zip(*x):
                        res.append(pg.PlotDataItem(_x, _y, **_configs[count % len(_configs)]))
                        count += 1
                else:
                    for _y in x:
                        res.append(pg.PlotDataItem(_y, **_configs[count % len(_configs)]))
                        count += 1
                return res

            return func

        elif self.sketch == 'scatter':
            def func(x: tuple[ndarray, ndarray]):
                res, count = [], 0
                if x[0].ndim == 1 and not hasattr(x[0][0], '__len__'):
                    x = (np.array([x[0]]), np.array([x[1]]))
                for _x, _y in zip(*x):
                    res.append(pg.PlotDataItem(_x, _y, **_configs[count % len(_configs)]))
                    count += 1
                return res

            return func

        elif self.sketch == 'histogram':
            def func(x: tuple[ndarray, ndarray]):
                res, count = [], 0
                for _x, _y in zip(*x):
                    res.append(pg.BarGraphItem(x=_x.astype(float), height=_y.astype(float),
                                               **_configs[count % len(_configs)]))
                    count += 1
                return res

            return func

        elif self.sketch == 'beeswarm':
            def func(x: tuple[ndarray, ndarray]):
                res, count = [], 0
                for _x, _y in zip(*x):
                    res.append(pg.PlotDataItem(_x.astype(float), _y.astype(float), **_configs[count % len(_configs)]))
                    count += 1
                return res

            return func

        elif self.sketch == 'box':
            def func(x: ndarray):
                res, count = [], 0
                for idx, item in enumerate(x):
                    res.extend(_box_items(item, pos=count, **_configs[count % len(_configs)]))
                    count += 1
                return res

            return func

        elif self.sketch == 'heatmap':

            def func(x: ndarray):
                res, dims = [pg.ImageItem(x, **configs)], x.shape[0]
                pos_var, _low, _high = (np.linspace(0.5, dims-0.5, dims), np.array([0 for _ in range(dims)]),
                                        np.array([dims for _ in range(dims)]))

                lut = configs.get('ref_color')
                lut.setColorMap(configs.get('colorMap'))
                lut.layout.setRowFixedHeight(0, 20)
                lut.layout.setRowFixedHeight(10, 20)
                lut.setLevels((np.amin(x), np.amax(x)))
                lut.setImageItem(res[0], insert_in=configs.get('ref_cvs').plotItem)

                if len(tag := configs.get('tags')) != 0:
                    assert_info_raiser(len(tag) == x.shape[0] == x.shape[1],
                                       ValueError('length of tags must be of the same as data.'))
                    res.extend(_labs_v(tag[::-1], _low, pos_var))
                    if configs.get('use_horizontal_tags'):
                        res.extend(_labs_h(tag, pos_var, _high))

                return res

            return func

        elif self.sketch == 'radar':
            def func(x: tuple[ndarray, ndarray]):
                res, count, kw = [], 0, _configs[0]
                n_grids, pen_grids = kw.get('n_grids') + 1, kw.get('pen_grids')
                max_radius, n_dims, dim_names = _max_radius(x), x[0].shape[-1] - 1, configs.get('dim_names', [])
                dim_names = np.array([f'dim{_ + 1}' for _ in range(n_dims)]) if len(dim_names) == 0 else dim_names

                for _x, _y in zip(*x):
                    res.append(pg.PlotDataItem(_x, _y, **_configs[count % len(_configs)]))
                    count += 1

                if lbs := kw.get('rescale_labels'):
                    circles, radius = _polar_custom(max_radius, n_grids, pen_grids)
                    cus_labs = _cus_labs(radius, lbs, n_dims)
                    real, img = _cus_position(radius, n_dims)
                    pos_labs = _flat_list([_add_cus_labs(v1, v2, v3) for v1, v2, v3 in zip(real, img, cus_labs)])
                    base_grids = [*circles, *pos_labs]
                else:
                    base_grids = _polar_base(max_radius, n_grids, pen_grids)

                res.extend(base_grids)  # add circle grids
                ends1 = _polar_ends(np.array([[max_radius for _ in range(n_dims)]]))
                res.extend(_radial_lines(ends1, pen_grids))  # add radial lines
                ends2 = _polar_ends(np.array([[max_radius + 0.8 for _ in range(n_dims)]]))
                res.extend(_attach_tag(dim_names, ends2))  # add tag for dimensions

                return res

            return func

        elif self.sketch == 'pie':
            def func(x: ndarray):
                res, count = [], 0
                _asd_ord = np.argsort(x)[::-1]
                x, names, r = x[_asd_ord], configs.get('name'), configs.get('radius')

                updated_configs = configs.update(name=_resort(names[:len(_asd_ord)], _asd_ord)).groups

                for start, scan, frac in zip(_start_angles(x), _spans(x), x):
                    kw = updated_configs[count % len(_configs)]
                    res.append(_fan(kw.get('radius'), start, scan, kw.get('pen'), kw.get('symbolBrush'), kw, frac))
                    count += 1

                res.append(_circle_fixer(r))
                return res

            return func

        elif self.sketch == 'contour':
            def func(x: ndarray):
                _interval, _min, _max = configs.get('interval'), np.amin(x), np.amax(x)
                if isinstance(_interval, float) and (0 < _interval < 1):
                    _interval = (_max - _min) * _interval
                _bins = [_min + (_ * _interval) for _ in range(round((_max - _min)/_interval))]
                digit_x = np.digitize(x, _bins) * (_max - _min) + _min
                digit_x = np.multiply(digit_x, _contour_msk(digit_x))
                digit_x[np.where(digit_x == 0.0)] = _min - _interval
                res = pg.ImageItem(digit_x, **configs)
                lut = configs.get('ref_color')
                lut.setColorMap(configs.get('colorMap'))
                lut.layout.setRowFixedHeight(0, 20)
                lut.layout.setRowFixedHeight(10, 20)
                lut.setLevels((_min, _max))
                lut.setImageItem(res, insert_in=configs.get('ref_cvs').plotItem)
                return [res]

            return func

        else:  # self.sketch == 'image'
            def func(x: ndarray):
                return [pg.ImageItem(x, **configs)]

            return func


class Canvas:

    @FuncTools.params_setting(data=T[None: Optional[Union[ndarray, tuple[ndarray, ndarray]]]],
                              fig_type=T['line': Literal['line', 'scatter', 'histogram', 'box', 'beeswarm', 'heatmap',
                                                         'radar', 'pie', 'contour', 'image']],
                              fig_configs=T[None: Optional[GrpSettings]], cvs_main=T['info': str],
                              cvs_size=T[None: Optional[tuple[int, int]]],
                              cvs_background=T[1.0: lambda x: isinstance(x, float) and 0 <= x <= 1],
                              cvs_grid=T[{'x': True, 'y': True}: lambda x: all([all([k in ['x', 'y'],
                                                                 isinstance(v, bool)]) for k, v in x.items()])],
                              cvs_title=T[None: Optional[str]],
                              cvs_title_configs=T[{'color': 'k', 'size': '15pt'}: dict[str, Any]],
                              cvs_left_label=T[None: Optional[str]],
                              cvs_bottom_label=T[None: Optional[str]],
                              cvs_label_configs=T[{'color': 'b', 'font-size': '13pt'}: dict[str, Any]],
                              cvs_legend=T[False: bool],
                              cvs_axes=T[{}: lambda x: all([all([k in ['left', 'top', 'right', 'bottom'],
                                                                 isinstance(v, bool)]) for k, v in x.items()])],
                              **{'~unknown_tp': [GrpSettings]})
    def __init__(self, **params):
        self.configs = params
        self.items, self._meta_fig_config = None, FigConfigs
        self.app, self.main, self.cvs = pg.mkQApp(self.configs.get('cvs_main')), QMainWindow(), pg.PlotWidget()

        self.layout, self.widgets, self.accessory = QHBoxLayout(), QWidget(), None
        self.main.setCentralWidget(self.widgets)
        self.widgets.setLayout(self.layout)
        self.layout.addWidget(self.cvs)

        self._cvs_axes = TrialDict({'left': True, 'top': False, 'right': False, 'bottom': True})

        self.cvs.setBackground(self.configs.get('cvs_background'))
        if gui_size := self.configs.get('cvs_size'):
            self.main.resize(*gui_size)
        self.cvs.showGrid(**self.configs.get('cvs_grid'))
        if self.configs.get('cvs_title'):
            self.cvs.setTitle(self.configs.get('cvs_title'), **self.configs.get('cvs_title_configs'))
        if self.configs.get('cvs_left_label'):
            self.cvs.setLabel('left', self.configs.get('cvs_left_label'), **self.configs.get('cvs_label_configs'))
        if self.configs.get('cvs_bottom_label'):
            self.cvs.setLabel('bottom', self.configs.get('cvs_bottom_label'), **self.configs.get('cvs_label_configs'))
        if self.configs.get('cvs_legend'):
            self.cvs.addLegend()
        if _axes := self.configs.get('cvs_axes'):
            _axes = self._cvs_axes.trial(**_axes)
            self.cvs.showAxes(tuple(_ for _ in _axes.values()), showValues=tuple(_ for _ in _axes.values()))

        self.cvs.plot()
        self._type = self.configs.get('fig_type')
        self.fig_ = _Sketcher(sketch=self._type)
        self.configs_ = eval(f"self._meta_fig_config.{str.upper(self._type)[0] + self._type[1:]}") if not \
            self.configs.get('fig_configs') else self.configs.get('fig_configs')  # guess init for fig_configs
        self._pre_prepare()  # color bar accessory for heatmap, or contour
        self._update_data(data=self.configs.get('data')) if self.configs.get('data') is not None else ...

    def _prepare(self, **params):
        _config = {**self.configs, **params}

        if 'data' in _config.keys():
            self._update_data(data=_config.get('data'))

        if _config.get('fig_type') in ['beeswarm', 'box']:
            _axes = self._cvs_axes if not _config.get('cvs_axes') else {**self._cvs_axes, **_config.get('cvs_axes')}
            _axes.update(bottom=False)  # clear bottom
            self.cvs.showAxes(tuple(_ for _ in _axes.values()), showValues=tuple(_ for _ in _axes.values()))

        if (t := _config.get('fig_type')) in ['heatmap', 'radar', 'pie']:
            cvs_size = (560, 560) if not _config.get('cvs_size') else _config.get('cvs_size')
            cvs_size = (v2 * 1.1 if v1 == 0 else v2 for (v1, v2) in enumerate(cvs_size)) if t == 'heatmap' else cvs_size
            self.main.resize(*cvs_size)
            self.cvs.showGrid(**{'x': False, 'y': False})  # clear cartesian axes
            self.cvs.showAxes(tuple(False for _ in range(4)), showValues=tuple(False for _ in range(4)))

    def _pre_prepare(self):
        if self.configs.get('fig_type') in ['heatmap', 'contour']:
            self.accessory = pg.ColorBarItem()
            self.configs_ = self.configs_.update(ref_cvs=self.cvs, ref_color=self.accessory)

    def view(self, **params):
        self._prepare(**params)
        self.main.show()
        self.app.exec()

    @staticmethod
    def save(**params):
        _ = Canvas(**params)
        file_name = params.get('save_as', 'figure.png')
        _.cvs.plotItem.writeImage(file_name)

    @staticmethod
    def play(**params):
        _ = Canvas(**params)
        _.view()

    def _update_data(self, **params):
        if 'data' in params.keys():
            if self.items:
                for item in self.items:
                    self.cvs.removeItem(item)
            self.data_ = params.get('data')
            self.items = self.fig_.figure(self.configs_)(self.fig_.preprocess(self.configs_)(self.data_))  # FP style
            for item in self.items:
                self.cvs.addItem(item)


doc.redoc(GrpSettings, doc.GrpSettings)
doc.redoc(FigConfigs, doc.FigConfigs)
doc.redoc(Canvas, doc.Canvas)


__all__ = ['GrpSettings', 'Canvas', 'FigConfigs']


if __name__ == '__main__':
    pass
