from info.basic.decorators import FuncTools
from info.basic.typehint import T, Null, Numeric
import info.docfunc as doc
from info.toolbox.libs.tensor.numeric import laplacian_of_gaussian_filter
from typing import Iterable
from numpy import ndarray
import numpy as np
from typing import Optional


pg = __import__('pyqtgraph')
gl = __import__('pyqtgraph', fromlist=['opengl']).opengl
QMainWindow = getattr(pg.QtWidgets, 'QMainWindow')
QWidget = getattr(pg.QtWidgets, 'QWidget')
QGridLayout = getattr(pg.QtWidgets, 'QGridLayout')
dep = __import__('info.basic.visual', fromlist=['_empty_pen'])
empty_pen = getattr(dep, 'empty_pen')
cursor_brush0 = getattr(dep, 'cursor_brush0')
cursor_brush1 = getattr(dep, 'cursor_brush1')
ruler = getattr(dep, 'ruler')
refresh_seg = getattr(dep, 'refresh_seg')
grab_cur = getattr(dep, 'grab_cur')
sync_cur = getattr(dep, 'sync_cur')
ungrab_cur = getattr(dep, 'ungrab_cur')
overlap_mask = getattr(dep, 'overlap_mask')
_img_to_volume = getattr(dep, '_img_to_volume')
_to_gl_array = getattr(dep, '_to_gl_array')
_msk_surface = getattr(dep, '_msk_surface')
_render_msk = getattr(dep, '_render_msk')


class _ImageViewer:

    @FuncTools.params_setting(gui_size=T[(1000, 1000): tuple[int, int]])
    def __init__(self, **params):
        self.app = pg.mkQApp()
        self.main = QMainWindow()
        self.main.resize(*params.get('gui_size'))
        self.main.setWindowTitle("ImageViewer")
        self.cw = QWidget()
        self.main.setCentralWidget(self.cw)
        self.ly = QGridLayout()
        self.cw.setLayout(self.ly)

        self.imv = [[pg.ImageView(view=pg.PlotItem())].copy()[0] for _ in range(3)]+[gl.GLViewWidget()]
        self._add_layout(self.imv, [(0, 0), (0, 1), (1, 0), (1, 1)])

        if 'data' in params.keys():
            self._load_data(**params)

    def _cursor_event(self, pic, sp_xy, org_xy):

        def _inner(event):
            if event.isExit():
                self.prompt.setText(' ')
                return
            _loc = event.pos()
            i, j, _img = _loc.y(), _loc.x(), pic.image[pic.currentIndex]
            i, j = int(np.clip(_loc.x(), 0, _img.shape[0] - 1)), int(np.clip(_loc.y(), 0, _img.shape[1] - 1))
            x, y, val = sp_xy[0]*i + org_xy[0], sp_xy[1]*j + org_xy[1], _img[i, j]
            val = val if not hasattr(val, '__len__') else val[-1]
            self.prompt.setText("X: %0.2f; Y: %0.2f; Value: %.4g" % (x, y, val))

        return _inner

    def _init_volume(self, x):
        _re_sp = [self._sp[1], self._sp[2], self._sp[0]]
        offset = [-v1*0.5*v2 for v1, v2 in zip(x.shape[:3], _re_sp)]
        item = gl.GLVolumeItem(x)
        item.scale(*_re_sp)
        item.translate(*offset)
        res = [item]
        if isinstance(self._msk, list) and len(self._msk) != 0:
            for _msk, _c in zip(self._msk, self._sd):  # self._sd is not None guarantee
                res.append(_render_msk(_to_gl_array(_msk), _c, _re_sp, offset, False))
        self.imv[3].setCameraPosition(distance=np.linalg.norm(offset, ord=2))
        return res

    def _add_layout(self, widgets, positions):
        for w, p in zip(widgets, positions):
            self.ly.addWidget(w, *p)
        self.prompt = pg.VerticalLabel(' ', orientation='horizontal')
        self.ly.addWidget(self.prompt, 2, 0, 2, 2)

    def _init_segs(self, pos):

        for _imv, _c in zip(self.imv, pos):  # centering
            _imv.timeLine.setPos(_c)

        centers, idx = [(pos[1], pos[2]), (pos[1], pos[0]), (pos[2], pos[0])], [(2, 1), (2, 0), (1, 0)]
        cursors = [pg.TargetItem(pos=c, symbol='+', size=8, pen=empty_pen, brush=cursor_brush1,
                                 hoverBrush=cursor_brush0) for c in centers]
        rulers = [[pg.InfiniteLine(angle=90, movable=False, pen=ruler, pos=(c[0], 0)),
                   pg.InfiniteLine(angle=0, movable=False, pen=ruler, pos=(0, c[1]))] for c in centers]

        for in_imv, (_imv, _cursor, _rulers, _idx) in enumerate(zip(self.imv[:3], cursors, rulers, idx)):
            _cursor.sigPositionChanged.connect(refresh_seg(self.imv[_idx[0]], self.imv[_idx[1]]))
            _imv.addItem(_cursor)
            _imv.imageItem.hoverEvent = self._cursor_event(_imv, [self._sp[_idx[0]], self._sp[_idx[1]]],
                                                           [self._org[_idx[0]], self._org[_idx[1]]])
            for _r in _rulers:
                _imv.addItem(_r)
            _cursor.sigPositionChanged.connect(grab_cur(_cursor, _rulers))
            _cursor.sigPositionChanged.connect(sync_cur(in_imv, _cursor, cursors))
            _cursor.sigPositionChangeFinished.connect(ungrab_cur(cursors, rulers))

    def _init_shaders(self, palettes=None):
        shaders = [np.random.randint(0, 100, size=3) * 0.01 for _ in range(len(self._msk))]
        if palettes is not None:
            for i, (_, e) in enumerate(zip(shaders, palettes)):  # replace
                shaders[i] = e
        return [tuple(inner for inner in out) for out in np.array(shaders)]

    @FuncTools.params_setting(data=T[Null: lambda x: isinstance(x, ndarray) and x.ndim == 3],
                              mask=T[None: Optional[list[ndarray]]], spacing=T[(1, 1, 1): Iterable[Numeric]],
                              origin=T[(0, 0, 0): Iterable[Numeric]], img_title=T[None: Optional[str]],
                              levels=T[(0.688, 0.997): tuple[Numeric, Numeric]],
                              palettes=T[None: Optional[list[tuple[Numeric, Numeric, Numeric]]]])
    def _load_data(self, **params):

        if title := params.get('img_title'):
            self.main.setWindowTitle(title)

        for attr in ['_data', '_msk', '_sp', '_org', '_lv', '_sd']:  # clear data
            if hasattr(self, attr):
                _ = getattr(self, attr)
                self.__delattr__(attr)

        self._clear_imv_canvas()

        self._data, self._msk = np.flip(params.get('data'), axis=[0]), params.get('mask')
        self._msk = [np.flip(_, axis=[0]) for _ in self._msk] if isinstance(self._msk, list) else self._msk
        self._msk = [_.astype(float) for _ in self._msk] if (isinstance(self._msk, list) and len(self._msk) > 1 and
                                                             self._msk[0].dtype != float) else self._msk
        self._sp, self._org, self._lv = params.get('spacing'), params.get('origin'), params.get('levels')
        self._sd = self._init_shaders(params.get('palettes')) if isinstance(self._msk, list) else None

        ax = [np.array([k + _ * j for _ in range(i)]) for i, j, k in zip(self._data.shape, self._sp, self._org)]

        if 0 <= self._lv[0] <= 1 and 0 <= self._lv[1] <= 1:
            self._lv = tuple(np.quantile(self._data, self._lv))

        img0 = overlap_mask(self._data, self._msk, self._sd) if self._msk is not None else self._data
        img1 = overlap_mask(self._data.transpose((2, 1, 0)), [_.transpose((2, 1, 0)) for _ in self._msk], self._sd) \
            if self._msk is not None else self._data.transpose((2, 1, 0))
        img2 = overlap_mask(self._data.transpose((1, 2, 0)), [_.transpose((1, 2, 0)) for _ in self._msk], self._sd) \
            if self._msk is not None else self._data.transpose((1, 2, 0))
        img4 = _img_to_volume(laplacian_of_gaussian_filter(data=_to_gl_array(self._data).clip(*self._lv)).astype(int))

        self.imv[0].setImage(img0, xvals=ax[0], pos=(self._org[1], self._org[2]),
                             scale=(self._sp[1], self._sp[2]), levels=self._lv)
        self.imv[1].setImage(img1, xvals=ax[2], pos=(self._org[1], self._org[0]),
                             scale=(self._sp[1], self._sp[0]), levels=self._lv)
        self.imv[2].setImage(img2, xvals=ax[1], pos=(self._org[2], self._org[0]),
                             scale=(self._sp[2], self._sp[0]), levels=self._lv)

        for item in self._init_volume(img4):
            self.imv[3].addItem(item)
        self._init_segs([_[int(np.ceil(len(_)*0.5))] for _ in ax])

    def view(self, **params):
        self._load_data(**params)
        self.main.show()
        self.app.exec()

    def _clear_imv_canvas(self):
        for mv in self.imv[:3]:
            if len(mv.view.items) > 3:  # default items: ROI*2, ImageItem*1
                for s in mv.view.items[3:]:
                    mv.removeItem(s)

        while len(self.imv[3].items) != 0:
            self.imv[3].items.pop()


_default_viewer = _ImageViewer(gui_size=(1000, 1000))


class ImageViewer(_ImageViewer):

    @staticmethod
    def play(**params):
        _default_viewer.view(**params)


doc.redoc(ImageViewer, doc.ImageViewer)


if __name__ == '__main__':
    pass
