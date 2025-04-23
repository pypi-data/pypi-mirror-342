_no_use = False
if _no_use:
    from info.basic.decorators import FuncTools
    from info.basic.functions import default_param, assert_info_raiser
    from info.basic.typehint import T, Null
    from typing import Any
    from numpy import ndarray
    import numpy as np
    from typing import Union, Optional
    from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout
    from PySide6.QtCore import QPointF
    import pyqtgraph as pg
    from pyqtgraph.Point import Point


    class Viewer1:

        settings = {
            'gui_size': (1400, 500)
        }

        def __init__(self, **params):
            self.settings.update(**params)
            self.viewer = pg.mkQApp()
            self.win = QMainWindow()
            self.win.resize(*self.settings.get('gui_size'))
            self.win.setWindowTitle("ImageViewer")
            self.cw = QWidget()
            self.win.setCentralWidget(self.cw)
            self.ly = QGridLayout()
            self.cw.setLayout(self.ly)
            self.imv1 = pg.ImageView(view=pg.PlotItem(), discreteTimeLine=True)
            self.imv2, self.imv3 = pg.ImageView(view=pg.PlotItem()), pg.ImageView(view=pg.PlotItem())
            self.ly.addWidget(self.imv1, 0, 0)
            self.ly.addWidget(self.imv2, 0, 1)
            self.ly.addWidget(self.imv3, 0, 2)

            self.legend1, self.legend2, self.legend3 = (pg.TextItem(anchor=(-0.45, -0.3), color=(255, 255, 70)),
                                                        pg.TextItem(anchor=(-0.45, -0.3), color=(255, 255, 70)),
                                                        pg.TextItem(anchor=(-0.45, -0.3), color=(255, 255, 70)))

        @staticmethod
        def _unpack_qt_point(x: Union[Point, QPointF]) -> ndarray:
            if isinstance(x, Point):
                _x, _y = x
            else:  # isinstance(x, QPointF)
                ax: QPointF = x
                _x, _y = ax.x(), ax.y()
            return np.array([_x, _y])

        @FuncTools.params_setting(data=T[Null: ndarray], mask=T[Null: ndarray],
                                  spacing=T[Null: lambda x: len(x) == 3 and all([isinstance(_, (int, float))
                                                                                 for _ in x])],
                                  levels=T[Null: lambda x: len(x) == 2 and all([isinstance(_, (int, float))
                                                                                for _ in x])])
        def _load_data(self, **params):

            data, levels = params.get('data'), params.get('levels')
            mask = params.get('mask')
            flag = np.sum(mask)
            assert_info_raiser(data.shape == mask.shape, ValueError('different shape between input data & mask'))

            if 0 <= levels[0] <= 1 and 0 <= levels[1] <= 1:
                levels = tuple(np.quantile(data, levels))

            mask_base = np.max(data) - np.min(np.multiply(data, mask))
            d1 = data + mask * mask_base

            def _minus_mask_base(x, base):
                return x - base if x >= base else x

            sp1, sp2, sp3 = params.get('spacing')
            ax1, ax2, ax3 = (np.array([_ * j for _ in range(i)]) for i, j in zip(data.shape, (sp1, sp2, sp3)))
            center = [np.ptp(item) * 0.5 for item in (ax1, ax2, ax3)]

            if params.get('img_title'):
                self.win.setWindowTitle(params.get('img_title'))

            if not hasattr(self, 'seg2'):  # init segmentations
                self.seg2 = pg.LineSegmentROI([[np.min(ax2), center[2]], [np.max(ax2), center[2]]], pen='r',
                                              resizable=False)
                self.seg3 = pg.LineSegmentROI([[center[1], np.min(ax3)], [center[1], np.max(ax3)]], pen='g',
                                              resizable=False)

                self.imv1.addItem(self.seg2)
                self.imv1.addItem(self.seg3)
            else:  # update segmentations
                self.seg2.setState(state={'pos': Point(0, 0), 'size': Point(1, 1), 'angle': 0,
                                          'points': [Point(np.min(ax2), center[2]), Point(np.max(ax2), center[2])]})
                self.seg3.setState(state={'pos': Point(0, 0), 'size': Point(1, 1), 'angle': 0,
                                          'points': [Point(center[1], np.min(ax3)), Point(center[1], np.max(ax3))]})

            d2, d3 = np.zeros((3, 3)), np.zeros((3, 3))
            self.imv2.setImage(d2, autoLevels=False, levels=levels)
            self.imv3.setImage(d3, autoLevels=False, levels=levels)

            def update_section1():
                nonlocal d2
                _d2 = self.seg2.getArrayRegion(d1, self.imv1.imageItem, axes=(1, 2))
                (_, pos1), (_, pos2) = self.seg2.getLocalHandlePositions()
                d2, *dis = np.rot90(_d2, -1), self._unpack_qt_point(pos1), self._unpack_qt_point(pos2)
                new_sp = (np.linalg.norm(dis[0] - dis[1], ord=2)) / d2.shape[0]
                self.imv2.setImage(d2, scale=(new_sp, sp1), autoLevels=False)

            def update_section2():
                nonlocal d3
                _d3 = self.seg3.getArrayRegion(d1, self.imv1.imageItem, axes=(1, 2))
                (_, pos1), (_, pos2) = self.seg3.getLocalHandlePositions()
                d3, *dis = np.rot90(_d3, -1), self._unpack_qt_point(pos1), self._unpack_qt_point(pos2)
                new_sp = (np.linalg.norm(dis[0] - dis[1], ord=2)) / d3.shape[0]
                self.imv3.setImage(d3, scale=(new_sp, sp1), autoLevels=False)

            # binding two sections in main view
            self.seg2.sigRegionChanged.connect(update_section1)
            self.seg3.sigRegionChanged.connect(update_section2)

            self.imv1.setImage(d1, xvals=ax1, scale=(sp2, sp3), levels=levels)

            # locate view objects & add label
            t = self.imv1.timeLine
            img1, view1 = self.imv1.getImageItem(), self.imv1.getView()
            img2, view2 = self.imv2.getImageItem(), self.imv2.getView()
            img3, view3 = self.imv3.getImageItem(), self.imv3.getView()
            self.legend1.setParentItem(view1)
            self.legend2.setParentItem(view2)
            self.legend3.setParentItem(view3)

            def cursor_event_main(event):
                if event.isExit():
                    return
                pos = event.pos()
                _dt = d1[np.where(ax1 == t.getPos()[0])][0]
                i, j = int(np.clip(pos.x(), 0, _dt.shape[0] - 1)), int(np.clip(pos.y(), 0, _dt.shape[1] - 1))
                loc = img1.mapToParent(pos)
                x, y = loc.x(), loc.y()
                val = int(_minus_mask_base(_dt[i, j], mask_base)) if flag else int(_dt[i, j])
                info = "X: {:.2f} (mm)\nY: {:.2f} (mm)\nVal: {}\nmask+: {}".format(x, y, val, int(mask_base)) if \
                    flag else "X: {:.2f} (mm)\nY: {:.2f} (mm)\nVal: {}".format(x, y, val)
                self.legend1.setText(info)

            def cursor_event_seg2(event):
                if event.isExit():
                    return
                pos = event.pos()
                i, j = int(np.clip(pos.x(), 0, d2.shape[0] - 1)), int(np.clip(pos.y(), 0, d2.shape[1] - 1))
                loc = img2.mapToParent(pos)
                x, y = loc.x(), loc.y()
                val = int(_minus_mask_base(d2[i, j], mask_base)) if flag else int(d2[i, j])
                info = "X: {:.2f} (mm)\nY: {:.2f} (mm)\nVal: {}\nmask+: {}".format(x, y, val, int(mask_base)) if \
                    flag else "X: {:.2f} (mm)\nY: {:.2f} (mm)\nVal: {}".format(x, y, val)
                self.legend2.setText(info)

            def cursor_event_seg3(event):
                if event.isExit():
                    return
                pos = event.pos()
                i, j = int(np.clip(pos.x(), 0, d3.shape[0] - 1)), int(np.clip(pos.y(), 0, d3.shape[1] - 1))
                loc = img3.mapToParent(pos)
                x, y = loc.x(), loc.y()
                val = int(_minus_mask_base(d3[i, j], mask_base)) if flag else int(d3[i, j])
                info = "X: {:.2f} (mm)\nY: {:.2f} (mm)\nVal: {}\nmask+: {}".format(x, y, val, int(mask_base)) if \
                    flag else "X: {:.2f} (mm)\nY: {:.2f} (mm)\nVal: {}".format(x, y, val)
                self.legend3.setText(info)

            img1.hoverEvent = cursor_event_main
            img2.hoverEvent = cursor_event_seg2
            img3.hoverEvent = cursor_event_seg3

            update_section1()
            update_section2()

        @FuncTools.params_setting(data=T[Null: ndarray], mask=T[None: Optional[ndarray]],
                                  img_title=T[None: Optional[str]],
                                  spacing=T[(1, 1, 1): Any], levels=T[(0.688, 0.997): Any])
        def view(self, **params):
            data = params.get('data')
            mask = default_param(params, 'mask', np.zeros_like(data))
            self._load_data(data=data, mask=mask, img_title=params.get('img_title'), spacing=params.get('spacing'),
                            levels=params.get('levels'))
            self.win.show()
            self.viewer.exec()

        @staticmethod
        def play(**params):
            _ = Viewer1(gui_size=params.get('gui_size', (1400, 500)))
            _.view(**params)


    auto_config = """
    #!/bin/bash


    home=${1:-'/home/chen'}
    conda_file=${2:-'https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh'}
    conda_src=${3:-'https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free'}
    pip_src=${4:-'https://pypi.tuna.tsinghua.edu.cn/simple/'}
    cwd=$(pwd)
    null='/dev/null'


    function init_info() {
        echo 'initiate system...'
    }

    function net_automation() {
        msg1='net-tools has been detected...'
        msg2='openssh-server has been detected...'
        msg3='ssh server has been activated...'
        if ifconfig --version >& ${null}; then echo ${msg1}; else sudo apt install net-tools; fi
        if sudo /etc/init.d/ssh start >& ${null}; then echo ${msg2}; else sudo apt-get install openssh-server; fi
        if sudo ps -e | grep ssh >& ${null}; then echo ${msg3}; else sudo /etc/init.d/ssh start; fi
    }


    function anaconda_automation() {
        cd ${1}'/Downloads'
        msg1='anaconda installer has been detected...'
        msg2='anaconda has been installed...'
        not_tuna=1
        if [ $(ls | grep Anaconda3) ]; then echo ${msg1}; else wget ${2}; fi
        if conda --version >& ${null}; then echo ${msg2}; else bash $(ls | grep Anaconda3); fi
        source ${home}'/anaconda3/etc/profile.d/conda.sh'
        conda activate
        if conda config --show channels | grep tsinghua >& ${null}; then not_tuna=0; fi
        if ((${not_tuna}==1)); 
        then 
            conda config --add channels ${3}
            conda config --set show_channel_urls yes
            pip config set global.index-url ${4}
        fi
        cd ${cwd}
    }


    function gcc_automation() {
        msg1='gcc has been detected...'
        if gcc --version >& ${null}; then echo ${msg1}; else sudo apt install gcc; fi
    }


    function make_automation() {
        msg1='make has been detected...'
        if make --version >&{null}; then echo ${msg1}; else sudo apt install make; fi
    }


    function auto_main() {
        init_info
        net_automation
        gcc_automation
        make_automation
        anaconda_automation ${1} ${2} ${3} ${4}
        echo end here
    }


    auto_main ${home} ${conda_file} ${conda_src} ${pip_src}
    """

if __name__ == '__main__':
    pass
