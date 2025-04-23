from info.basic.typehint import Numeric, Tp
from typing import Union, Optional, Sequence, Generator, Iterable, Literal, Callable, Any, TypeVar, Type
from numpy import ndarray as np_ndarray
from pandas import DataFrame
from scipy.stats import norm as gs
from functools import partial
import os
try:
    cp_ndarray = __import__('cupy', fromlist=['ndarray']).ndarray
except ImportError as _:
    cp_ndarray = np_ndarray

dual_ndarray = Union[np_ndarray, cp_ndarray]
_ExeDict = TypeVar('_ExeDict')
ReLU = _Ctype = _GrpSettings = _Canvas = _KernelGen = _DcmSetConstructor = _DcmSeries = _ImageViewer = _dist = \
    _cdist = _mean = _std = _ka_opt = np_nan = _ExeDict
BernTP = BinTP = MultTP = DirTP = BetaTP = PoiTP = GamTP = ExpTP = ErlTP = GauTP = MGauTP = WisTP = GauWisTP = _dist
_dict = type('_dict', (dict,), {})
_list = type('_list', (list,), {})
PI2 = 2 * 3.141592653


class _FigConfigs:
    Line = ...


def args_highlighter(*args, **kwargs):
    print(args, kwargs)


def summary_sub(func: callable, sub_str: str = None) -> Callable:
    derived_func = partial(func)
    _main = func.__doc__.split('.')
    derived_func.__doc__ = '.'.join([sub_str] + _main[1:])
    derived_func.description = func.__annotations__
    return derived_func


def tag_sub(func: Callable, append_str: str = None) -> Callable:
    derived_func = partial(func)
    _main = func.__doc__.split('\n')
    derived_func.__doc__ = '\n'.join([_ + f" ({append_str})" if ':name:' in _ or ':label:' in _ else _ for _ in _main])
    derived_func.description = getattr(func, 'description')
    return derived_func


def redoc(x, sub_str: Union[str, Callable] = None):
    sub_str = sub_str.__doc__ if callable(sub_str) else sub_str
    x.__doc__ = sub_str


def under_editing():
    """docstring is under editing"""
    pass


def T():
    """
    indicator for setting default values, add constraint type for keyword arguments. Using combined with
    :py:class:`~info.docfunc.FuncTools`.

    .. attribute:: Examples:

       .. code-block:: python
          :caption: using T for multi purposes
          :name: using T for multi purposes

          from info.me import T, Null, FuncTools
          from numpy import ndarray
          import numpy as np
          img = np.random.random((40, 40))

          @FuncTools.params_setting(data=T[Null: ndarray], spacing=T[(1, 1, 1): tuple[int, ...]],
                                    mask=T[None: lambda x: x.dtype == bool and x.ndim == 3 if isinstance(x, ndarray)
                                    else True], whichever=T[12: int: True])
          def func(**params):
              mask = params.get('mask') if params.get('mask') else np.ones_like(params.get('data'))
              ...

          func(x=img)  # error detected here: 'data' is Null but not assigned
          func(data=img, spacing=[1, 1, 1])  # error detected here: typing hint is tuple but got list
          func(data=img, spacing=(1, 0.8, 1))  # error detected here: int only based on typing hint
          func(data=img, mask=img)  # error detected here: img.dtype is not bool
          func(data=img)  # correct, using (1, 1, 1) as default spacing, all ones mask
          func(data=img, spacing=(1, 1, 2), mask=np.zeros_like(img))  # correct as well
          func(data=img, whichever='not_int')  # correct, the last True in T refers to escape this check

    .. attribute:: Notes:

       In info, the built-in value ``Null`` is a mnemonic name to remind the required argument(s):

       .. code-block:: python
          :caption: null value to remind required arguments
          :name: null value to remind required arguments

          @FuncTools.params_setting(a=T[Null: object], b=T[Null: object], c=T[1: int])
          def func(**params):
              ...

          func.required_args  # {'a', 'b'}

       Note under this circumstance, if call ``func`` without assignment for ``a`` or ``b``, ``TypeError`` raised.

    .. attribute:: See also:

       - :py:class:`~info.docfunc.FuncTools`

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       .. versionchanged:: 0.0.4

          Support new union typing hint like A | B in python 3.10 or later.

       -- |signature|
    """
    ...


def assert_info_raiser(expr: object, err_msg: Exception):
    """
    one line try something except something block. used for data pre-checking.

    .. attribute:: Arguments:

       :param object expr: expression to be tested
       :param Exception err_msg: raised error if exception captured
       :raises Exception: when catches exception in ``expr``

    .. attribute:: Examples:

       .. code-block:: python
          :caption: data pre-checking in function
          :name: data pre-checking in function

          from info.me import assert_info_raiser
          from numpy import ndarray

          def func(x):  # assume ndarray with shape of (5, 6) is desired
              assert_info_raiser(all([isinstance(x, ndarray), x.ndim == 2, x.shape[0] ==5 and x.shape[1] == 6]),
                                 TypeError(f"desired ndarray with shape of (5, 6), got {x.shape}"))
              ...

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(expr, err_msg)


def datasets():
    """
    example images collection.

    .. attribute:: Methods:

       .. method:: cat:

          grey level image with shape of (1000, 781)

       .. method:: accent:

          grey level image with shape of (1152, 768)

       .. method:: blackcurrant:

          grey level image with shape of (725, 544)

       .. method:: bricks:

          grey level image with shape of (1280, 696)

       .. method:: blackcurrant:

          boolean image with shape of (748, 533)

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    pass


def default_param(param: dict, k: str, v: Any):
    """
    dynamic default value setting in function body.

    .. attribute:: Arguments:

       :param param: dict params to be detected
       :param k: keyword for parameter
       :param v: default value
       :return: ``v`` if ``k`` in ``params`` is ``None``, else the value in ``params``
       :rtype: Any

    .. attribute:: See also:

       - :py:class:`~info.docfunc.FuncTools`

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(param, k, v)


def distance_matrix(x: np_ndarray, method: Callable = None, is_symmetric: bool = None):
    """
    calculate the distance of a tensor.

    .. attribute:: Arguments:

       :param ndarray x: data at least in one dimension
       :param Optional[Callable] method: callable object that must map two tensor with identical shape into a scalar;
                                         ``None`` as default to calculate the Euclidean distance
       :param Optional[bool] is_symmetric: whether the ``method`` to calculate distance is commutative; ``None`` as
                                           default to automatically select the proper calculation branch
       :return: ndarray with shape of (x.shape[0], x.shape[0])
       :rtype: ndarray

    .. attribute:: Notes:

       Distance matrix is widely applied in analyzing high-dimensional data. See the
       :ref:`related section <High dimensional data>` for more details. The interface design of
       :ref:`multi graph correlation test <Multi Graph Correlation>` to evaluate high dimensional data through
       :py:func:`~info.docfunc.hypoj_mgc` using this calculation embedded as connection.

    .. attribute:: See also:

       - :py:func:`~info.docfunc.hypoj_mgc`

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(x, method, is_symmetric)


def FuncTools():
    """
    decorator collections for multi purposes.

    .. attribute:: Methods:

       .. method:: attach_attr:

          static method to add document to function, applying typing hint, or type checking with hint

          :var Union[str, Callable] docstring: replace document of decorated function
          :var bool info_func: marker whether is info function; if ``True``, the ``entry_tp`` and ``return_tp`` will
                             be added into type checker flow, and keyword ``'data'`` argument must be included;
                             otherwise just hint only
          :var type entry_tp: the data type for decorated function to process; use python builtin class or typing hint;
                              when ``'info_func'`` is ``True``, it is considered as the type of ``'data'`` value and
                              will be checked before processing start
          :var type return_tp: return type for decorated function; can use python builtin class or typing hint;
                               when ``'info_func'`` is ``True``, the result will be checked before actually return
          :var bool ~deep_inspect: whether check deeper when meet a simple iterable object; ``True`` as default
          :var Union[bool, list[type]] ~unknown_tp: if ``False``, will raise ``UnSupportableTypeError`` when dealing
                                                    with unparseable type; ``True`` will pass the test for unparseable
                                                    type; and list of unparseable type(s) will add those types in
                                                    checking workflow; ``False`` as default
          :raise NoDataInflowError: if ``info_func`` is ``True`` and no keyword assignment for ``'data'``
          :raise TypeError: if ``info_func`` is ``True`` and entry type of ``'data'``, or return data do not match the
                            desired type

          It can be used to attach documents on decorated function, or checking whether the data match the desired
          type in entry, or the data after processing matched the desired type as well. for example:

          .. code-block:: python
             :caption: decorator to attach documents or execute type checking
             :name: decorator to attach documents or execute type checking

             from info.me import FuncTools

             @FuncTools.attach_attr(docstring='''simple function''')
             def func1(**params):
                 ...

             @FuncTools.attach_attr(docstring=func1)
             def func2(**params):
                 ...

             help(func1)  # simple function
             help(func2)  # simple function

             @FuncTools.attach_attr(entry_tp=int, return_tp=float)
             def func3(**params):
                 return float(params.get('x'))

             @FuncTools.attach_attr(entry_tp=int, return_tp=float)
             def func4(**params):
                 return params.get('x')

             func3(x=5)  # 5.0
             func4(x=5)  # 5, without error

             @FuncTools.attach_attr(info_func=True, entry_tp=int, return_tp=float)
             def func5(**params):
                 return float(params.get('x'))

             @FuncTools.attach_attr(info_func=True, entry_tp=int, return_tp=float)
             def func6(**params):
                 return params.get('data')

             @FuncTools.attach_attr(info_func=True, entry_tp=int, return_tp=float)
             def func7(**params):
                 return float(params.get('data'))

             func5(x=5)  # NoDataInflowError here, remind for using 'data' keyword
             func6(data='5')  # TypeError here, 'data' requires <class 'int'>, but got <class 'str'>
             func6(data=5)  # TypeError here, return requires <class 'float'>, but got int 5
             func7(data=5)  # correct

          However, this decorator can also handy to attach some customized attribute if necessary:

          .. code-block:: python
             :caption: customize function by decorator
             :name: customize function by decorator

             @FuncTools.attach_attr(author='Chen', foo=12, bar='sz')
             def func(**params):
                 ...

             func.author  # 'Chen'
             func.foo  # 12
             func.bar  # 'sz'

       .. method:: params_setting:

          static method to set default values, applying typing hint, or type checking with those hints. some
          complicated situation can also use anonymous ``lambda`` function to check.

          :var bool ~deep_inspect: whether check deeper when meet a simple iterable object; ``True`` as default
          :var Union[bool, list[type]] ~unknown_tp: if ``False``, will raise UnSupportableTypeError when meet
                                                    unparseable type; ``True`` will pass the test for unparseable type;
                                                    and list of unparseable type(s) will add those types in checking
                                                    workflow; ``False`` as default
          :raise NoDataInflowError: if ``info_func`` is ``True`` and no keyword assignment for ``'data'``
          :raise TypeError: if ``info_func`` is ``True`` and entry type of ``'data'``, or return data do not match the
                            desired type

          Flowing examples show how to pre-define default parameters for info function.

          .. code-block:: python
             :caption: decorator for parameter setting
             :name: decorator for parameter setting

             from info.me import T, Null, FuncTools, default_param
             from typing import Optional
             from numpy import ndarray
             import numpy as np

             @FuncTools.params_setting(data=T[Null: ndarray], clip=T[(0.2, 0.8): tuple[float, float]],
                                       coefficient=T[0.6: lambda x: 0 <= x <= 1],
                                       normalize=T[None: Optional[tuple[float, float]]])
             def func(**params):
                 dt = params.get('data').clip(*params.get('clip')) * params.get('coefficient')
                 _mean, _std = default_param(params, 'normalize', (dt.mean(), dt.std()))
                 return (dt - _mean) / _std

             func.required_args  # {'data'}, if calling without assignment for 'data', error raised

          This example show the convenience to use ``params_setting`` to build the function. for ``data``, the ``Null``
          mark it as a required argument when calling, ``ndarray`` confines its type; the same as ``clip`` but with
          default value as ``(0.2, 0.8)``; for ``coefficient``, its acceptable value is no less than zero and no
          greater than one.

          As all conditions are guaranteed so it can safely using one line pythonic statement to obtain ``dt``,
          without worrying about wrong parameters passed in. Additionally, maybe sometimes it needs dynamic setting
          for some arguments. For instance the ``normalize`` in above code can hardly determined using ``T`` as it
          depends ``data``, in this circumstance, set it as ``None`` then use ``default_param`` to implement the
          calculation in the body. If calling without assignment of ``normalize``, the ``_mean`` and ``_std`` will
          be automatically calculated based on ``dt``, otherwise using the parameters passed in.

          Additionally, use ``params_setting`` to initialize arguments is safe with mutable built-in Python object.
          The following example shows this feature:

          .. code-block:: python
             :caption: assign mutable arguments
             :name: assign mutable arguments

             from info.me import FuncTools, T

             def py_func(*, x=[]):
                 x.append(len(x))
                 return x

             @FuncTools.params_setting(x=T[[]: list])
             def info_func(**params):
                 (res := params.get('x')).append(len(res))
                 return res

             _ = [print(_, id(_)) for _ in [py_func(), py_func(), info_func(), info_func()]]
             # [0, 1] 2763346399552
             # [0, 1] 2763346399552
             # [0] 2763804769280
             # [0] 2761764188160

       .. method:: test_for:

          :var bool ~in_decorator: whether use as the decorator; if ``False``, will return a none argument lambda
                                   function to get test result, and cost time; ``True`` as default

          static method to test the decorated function.

          .. code-block:: python
             :caption: decorator to do function testing
             :name: decorator to do function testing

             from info.me import FuncTools
             from time import sleep


             @FuncTools.test_for(2, 'foo')
             def func1(a, b):  # test for common function
                 print('string here: ', b)
                 sleep(a)
                 return 'bar'

             # string here:  foo
             # running test for func1(2, foo) ...
             # time cost: 0:00:02.007849
             # final result: bar

             @FuncTools.test_for(a=2, b='bar')
             def func2(**params):  # test for info like function
                 print('another string here: ', params.get('b'))
                 sleep(params.get('a'))
                 return 'bar'

             # another string here:  bar
             # running test for func2(a=2, b=bar) ...
             # time cost: 0:00:02.014251
             # final result: bar

          Unnecessary to edit the test script in addition. It capable for testing while editing. When finish function,
          clean the test arguments inside, or comment that line.

    .. attribute:: Examples:

       With ``FuncTools``, you can design, implement, and test for function all in one script. Using the previous
       :numref:`decorator for parameter setting` , make it as a info version, then doing test, the script will be:

       .. code-block:: python
          :caption: all in one script
          :name: all in one script

          from info.me import T, Null, FuncTools, default_param
          from typing import Optional
          from numpy import ndarray
          import numpy as np

          @FuncTools.test_for(data=np.random.random((50, 60)), coefficient=0.8)
          @FuncTools.params_setting(data=T[Null: ndarray], clip=T[(0.2, 0.8): tuple[float, float]],
                                    coefficient=T[0.6: lambda x: 0 <= x <= 1],
                                    normalize=T[None: Optional[tuple[float, float]]])
          @FuncTools.attach_attr(docstring='under editing', info_func=True, entry_tp=ndarray, return_tp=ndarray)
          def func(**params):
              dt = params.get('data').clip(*params.get('clip')) * params.get('coefficient')
              _mean, _std = default_param(param, 'normalize', (dt.mean(), dt.std()))
              return (dt - _mean) / _std

    .. attribute:: See also:

       - :py:const:`~info.docfunc.T`

       - :py:func:`~info.docfunc.default_param`

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       .. versionchanged:: 0.0.4

          branch ``~in_decorator`` in ``test_for`` method.

       .. versionchanged:: 0.0.5

          use copy to initiate arguments with set, list, or dict type; safe to use mutable object for
          default initialization in :py:func:`~info.docfunc.T` indicator inside ``params_setting``.

       -- |signature|
    """
    ...


def window_to_clipper(x: list[Numeric]):
    """
    convert window width and level to lower and upper bounds in grey level.

    .. attribute:: Arguments:

       :param list[Numeric] x: 2-length list, composed of window level and window width
       :return: lower and upper bounds in grey level
       :rtype: list[Numeric]

    .. attribute:: Logs:

       .. versionadded:: 0.0.1

       -- |signature|
    """
    args_highlighter(x)


def drop_down(x: Iterable):
    """
    print each object in an iterable object vertically.

    .. attribute:: Arguments:

       :param Iterable x: iterable object
       :return: NoReturn
       :rtype: NoneType

    .. attribute:: Examples:

       print out iterable object vertically

       .. code-block:: python
          :caption: drop down iterable python objects
          :name: drop down iterable python objects

          from info.me import drop_down

          # drop down set
          drop_down({1, 2})
          # 1
          # 2

          # drop down tuple
          drop_down((3, 4))
          # 3
          # 4

          # drop down list
          drop_down([5, 6])
          # 5
          # 6

          # drop down dict
          drop_down({'a': 9, 'b': 10}.items())
          # ('a', 9)
          # ('b', 10)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(x)


def cookbook():
    """

    * less talk, more action;

    * less complain, more construct;

    * innovation starts from practice;

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    ...


def traversal_on_params(data: Callable, params_pool: dict[str, list[Any]], scope_in_builtin: bool = False,
                        concise_result: bool = True):
    """
    traversal on parameters pool. function to make auto unit test, or auto experiment, for info pipeline.

    .. attribute:: Arguments:

       :param Callable data: info function or unit
       :param dict[str, list[Any]] params_pool: pool for parameters, values to be investigated should be collected
                                                into a list
       :param bool scope_in_builtin: trigger to determine whether testing for built-in parameters in pool; ``False``
                                     as default
       :param bool concise_result: trigger to determine whether reserve the test results; if ``False``, original
                                   will be included, otherwise class type if final results are not short enough;
                                   ``True`` as default for unit test
       :return: DataFrame container for testing result
       :rtype: DataFrame

    .. attribute:: Examples:

       .. code-block:: python
          :caption: testing on parameters pool
          :name: testing on parameters pool

          from info.me import FuncTools
          from info.me import autotesting as tst

          @FuncTools.attach_attr(docstring="simple function", info_func=True, entry_tp=int, return_tp=int)
          def simple_function(**params):
              return (params.get('a') + params.get('b') * params.get('c')) ** params.get('d')

          test_pool = {
              'a': [1, 2, 3],
              'b': [3, 4],
              'c': [5, 6, 7, 8],
              'd': [2, 3]
          }

          tst.traversal_on_params(data=simple_function, params_pool=test_pool)

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, params_pool, scope_in_builtin, concise_result)


def experiments(data: Callable, params_pool: dict[str, list[Any]], to_file: str, branch_comment: str = '',
                scope_in_builtin: bool = False):
    """
    experiment test pipeline for info function or unit.

    .. attribute:: Arguments:

       :param Callable data: info function or unit
       :param dict[str, list[Any]] params_pool: pool for parameters, values to be investigated should be collected
                                                into a list
       :param str to_file: cache file to dump result of test parameters; ``None`` will create a new dict in each
                           invocation
       :param bool branch_comment: prefix marker for callable object to be tested if necessary; ``''`` as default
                                   for no prefix attached to the function name
       :param bool scope_in_builtin: trigger to determine whether testing for built-in parameters in pool; ``False``
                                     as default
       :return: DataFrame container for testing result
       :rtype: DataFrame

    .. attribute:: Examples:

       .. code-block:: python
          :caption: experiment pipeline
          :name: experiment pipeline

          from info.me import FuncTools
          from info.me import autotesting as tst

          @FuncTools.attach_attr(docstring="simple function", info_func=True, entry_tp=int, return_tp=int)
          def simple_function(**params):
              return (params.get('a') + params.get('b') * params.get('c')) ** params.get('d')

          test_pool = {
              'a': [1, 2, 3],
              'b': [3, 4],
              'c': [5, 6, 7, 8],
              'd': [2, 3]
          }

          res = tst.experiments(data=simple_function, params_pool=test_pool)

    .. attribute:: Notes:

       experiments dump the original result for each test.

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, params_pool, to_file, branch_comment, scope_in_builtin)


def functest(data: Callable, params_pool: dict[str, list[Any]], to_file: str, branch_comment: str = '',
             scope_in_builtin: bool = False):
    """
    unit test pipeline for info function or unit.

    .. attribute:: Arguments:

       :param Callable data: info function or unit
       :param dict[str, list[Any]] params_pool: pool for parameters, values to be investigated should be collected
                                                into a list
       :param str to_file: cache file to dump result of test parameters; ``None`` will create a new dict in each
                           invocation
       :param bool branch_comment: prefix marker for callable object to be tested if necessary; ``''`` as default
                                   for no prefix attached to the function name
       :param bool scope_in_builtin: trigger to determine whether testing for built-in parameters in pool; ``False``
                                     as default
       :return: DataFrame container for testing result
       :rtype: DataFrame

    .. attribute:: Examples:

       .. code-block:: python
          :caption: function test pipeline
          :name: function test pipeline

          from info.me import FuncTools
          from info.me import autotesting as tst

          @FuncTools.attach_attr(docstring="simple function", info_func=True, entry_tp=int, return_tp=int)
          def simple_function(**params):
              return (params.get('a') + params.get('b') * params.get('c')) ** params.get('d')

          test_pool = {
              'a': [1, 2, 3],
              'b': [3, 4],
              'c': [5, 6, 7, 8],
              'd': [2, 3]
          }

          res = tst.functest(data=simple_function, params_pool=test_pool)

    .. attribute:: Notes:

       functest dump the class type of result for each test, if the final result is difficult to be printed out
       concisely.

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, params_pool, to_file, branch_comment, scope_in_builtin)


def diagnosing_tests(data: DataFrame):
    """
    diagnose unit test result then return a list of bool values.

    .. attribute:: Arguments:

       :param DataFrame data: dataframe result
       :var bool ~verbosity: trigger to show details for the exceptive cases; ``True`` as default
       :return: list of bool for dataframe result; ``True`` for case with 0 exit code, otherwise ``False``
       :rtype: list[bool]

    .. attribute:: Notes:

       the tool is used for auto unit test framework. If all cases pass, its return will be list of ``True``
       only.

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data)


def cropper(data: dual_ndarray, crop_range: list[tuple[Numeric]]):
    """
    function or Unit to crop data via start and end assignments. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: data to be cropped
       :param list[tuple[Numeric]] crop_range: list composed of start & end points or ratios, values in end points or
                                               ratios must strictly greater than starts ones in each dimension
       :return: cropped ndarray
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: if ``data`` or ``crop_range`` was not assigned as available type

    .. attribute:: Examples:

       .. code-block:: python
          :caption: crop an image
          :name: crop an image

          from info.ins import datasets
          from info.me import tensorn as tsn
          img = datasets.blackcurrant()

          # absolute cropping via start & end indices
          tsn.cropper(data=img, crop_range=[(40, 0), (512, 370)])

          # relative cropping via start & end ratios
          tsn.cropper(data=img, crop_range=[(.07, 0.), (1., .72)])

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, crop_range)


def standardization(data: dual_ndarray):
    r"""
    standard scaler function or Unit to shrink data with values distributed as :math:`\mathcal{N}(1, 0)`.
    available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: data to be standardized
       :return: data after standardization
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: if ``data`` was not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: standardize a series
          :name: standardize a series

          from info.me import tensorn as tsn
          import numpy as np

          tsn.standardization(data=np.random.random(100)*100+50)

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data)


def normalization(data: dual_ndarray):
    """
    normal scalar function or Unit to shrink values of data confined from 0 to 1. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: data to be normalized
       :return: data after normalization
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: if ``data`` was not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: normalize a series
          :name: normalize a series

          from info.me import tensorn as tsn
          import numpy as np

          tsn.normalization(data=np.random.random(100)*100+50)

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data)


def clipper(data: dual_ndarray, clip: tuple[Numeric]):
    """
    clipper scalar function or Unit to clip values of data with lower and upper bound. available for numpy and
    cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: data to be clipped
       :param tuple[Numeric, Numeric] clip: 2-length list, composed of lower and upper bound
       :return: data with values after clipping
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: if ``data`` or ``clip`` was not assigned properly

    .. attribute:: Examples:

        .. code-block:: python
           :caption: clip a series
           :name: clip a series

           from info.me import tensorn as tsn
           import numpy as np

           tsn.clipper(data=np.random.random(100)*100+50, clip=[60, 120])

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, clip)


def resize(data: dual_ndarray, new_size: tuple[int], decomp_method: Literal['cp', 'tucker', 'tt', 'tr'] = 'cp',
           decomp_rank: Union[int, tuple[int, ...]] = None,
           interp_method: Literal['linear', 'nearest', 'nearest-up', 'zero', 'slinear', 'quadratic', 'cubic',
           'previous', 'next'] = 'linear'):
    """
    resizing data into specific shape. spline interpolation supported. algorithm is implemented through canonical
    decomposition :ref:`[Battaglino2018] <[Battaglino2018]>`, or Tucker decomposition for tensor
    :ref:`[Kolda2009] <[Kolda2009]>`. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: data to be resized
       :param tuple[int] new_size: tuple to determine new size for input data
       :param Literal['cp', 'tucker', 'tt', 'tr'] decomp_method: decomposition method for ``data``; ``'cp'`` for
                                                                 canonical decomposition into parallel factors,
                                                                 ``'tucker'`` for Tucker decomposition; ``'tt'`` for
                                                                 tensor train decomposition; ``'tr'`` for tensor ring
                                                                 decomposition;``'cp'`` as default
       :param Union[int, tuple[int, ...]] decomp_rank: decomposition rank; integer for all ranks, or tuple of integers
                                                       for each rank; ``None`` as default to calculate automatically
       :param Literal[...] interp_method: interpolation method links to ``kind`` argument of ``interp1d``; options are
                                          ``'linear'``, ``'nearest'``, ``'nearest-up'``, ``'zero'``, ``'slinear'``,
                                          ``'quadratic'``, ``'cubic'``, ``'previous'``, and ``'next'``; ``'linear'``
                                          as default
       :return: re-sized data
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: if ``data`` or ``new_size`` was not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: resize an image through interpolation
          :name: resize an image through interpolation

          from info.ins import datasets
          from info.me import tensorn as tsn
          img = datasets.blackcurrant()

          dt_1 = tsn.resize(data=img, new_size=(200, 200))

          # or use 2nd order spline
          dt_2 = tsn.resize(data=img, new_size=(200, 200), interp_method='quadratic')

    .. attribute:: See also:

        - `Interpolation <https://scipy.github.io/devdocs/tutorial/interpolate/1D.html>`_

        - `Tensor decomposition and synthesis <http://tensorly.org/stable/user_guide/tensor_decomposition.html>`_

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, new_size, decomp_method, decomp_rank, interp_method)


def F(expr):
    """
    info lambda function.

    .. attribute:: Arguments:

       :param Callable expr: lambda expression with key word arguments ``**kwargs``
       :return: anonymous function in info version

    .. attribute:: Examples:

       .. code-block:: python
          :caption: fast register an info function
          :name: fast register an info function

          from info.me import F, Unit

          f1 = F(lambda **_: _.get('data'))
          f2 = (lambda **_: _.get('data'))

          u1 = Unit(mappings=[f1])  # no problem here
          u2 = Unit(mappings=[f2])  # raise TypeError here, as no registered f2

    .. attribute:: See also:

       - :py:class:`~info.docfunc.Unit`

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(expr)


def Unit(mappings: list[Callable], structure: Literal['sequential', 'parallel'] = 'sequential',
         entry_tp: Tp = None, return_tp: Tp = None, docstring: Union[str, Callable] = None):
    """
    package a single or multiple data processing or operation steps within a Unit.

    .. attribute:: Arguments:

       :param list[Callable] mappings: list composed of :ref:`info function(s) <Informatics function>`, or
                                       :py:class:`~info.docfunc.Unit` instance(s)
       :param Literal['sequential', 'parallel'] structure: ``'sequential'`` or ``'parallel'``, to determine the mapping
                                                           order of the Unit; ``'sequential'`` as default
       :param Optional[type] entry_tp: the type of data in entry of this Unit; ``None`` as default to guess the inflow
                                       type based on ``structure``
       :param Optional[type] return_tp: the type of return data of this Unit; ``None`` as default to guess the
                                        outflow type based on ``structure``
       :param str docstring: docstring or formal function which contains objective docstring; ``None`` as default to
                             automatically generate based on docstrings of elements
       :return: a Unit for data processing or operation
       :rtype: :py:class:`~info.docfunc.Unit`
       :raises TypeError: when ``mappings`` are not all registered functions or unit; or inflow data not pass correctly
                          through type checker

    .. attribute:: Methods:

       .. method:: add_locker:

          lock arguments of current unit as default values, through ``**kwargs`` assignments.

       .. method:: refresh_locker:

          update arguments of current unit as default values, through ``**kwargs`` assignments.

       .. method:: shadow:

          return a copy of self, with a set of specified ``**kwargs`` parameters related to the inner functions.

       .. method:: append_document:

          overwrite docstring of the unit.

          :var Union[str, Callable] docstring: str for docstring, or callable object contained that str.

       .. method:: reset:

          reset default values for all arguments when initiate the Unit.

       .. method:: get_equivalent_config:

          output the equivalent values for all arguments when the unit is actually called.

       .. method:: __call__:

          call as function using ``data`` as required argument.

          :var Any data: instance to be processed via this unit.

       .. method:: __rshift__:

          sequentially connects the next unit.

       .. method:: __or__:

          parallel connects the next unit.

    .. attribute:: Examples:

       Using info Unit to build comprehensive processing steps sequentially:

       .. code-block:: python
          :caption: coupled crop and resize processing via info Unit
          :name: coupled crop and resize processing via info Unit

          from info.me import tensorn as tsn
          from info.me import Unit, datasets
          img = datasets.blackcurrant()

          u = Unit(mappings=[tsn.cropper, tsn.resize])
          center_to_500x500 = u.shadow(crop_range=[(.25, .25), (.75, .75)], new_size=(500, 500))

          img1 = center_to_500x500(data=img)

       Or applied parallel structure to process data in different sets of processing parameters simultaneously. The
       inner functions use Unit instance self:

       .. code-block:: python
          :caption: crop and resize processing steps with different sets of parameters, in a parallel Unit
          :name: crop and resize processing steps with different sets of parameters, in a parallel Unit

          topleft_to_200x200 = u.shadow(crop_range=[(0., 0.), (.25, .25)], new_size=(200, 200))
          u_parallel = Unit(mappings=[center_to_500x500, topleft_to_200x200], structure='parallel')

          img2, img3 = u_parallel(data=img)

    .. attribute:: Logs:

       .. versionadded:: 0.0.1

       .. versionchanged:: 0.0.4

          Support operator ``>>`` and ``|`` to build pipeline.

       -- |signature|
    """
    args_highlighter(mappings, structure, entry_tp, return_tp, docstring)


def TrialDict(**kwargs):
    """
    dict with ``trial`` method. The argument assignment in ``trial`` does not modify the dict itself.

    .. attribute:: Arguments:

       :param dict kwargs: ``**kwargs`` as general dict
       :return: the dict with ``trial`` method
       :rtype: :py:class:`~info.docfunc.TrialDict`

    .. attribute:: Methods:

       .. method:: trial:

          return a copy of self with updated keywords and values

    .. attribute:: Logs:

       .. versionadded:: 0.0.1

       -- |signature|
    """
    args_highlighter(kwargs)


def ExeDict(execute: Callable, **kwargs):
    """
    executable dict composed of ``execute`` keyword and function or generic function as value. uses for high-order
    function.

    .. attribute:: Arguments:

       :param Callable execute: a Callable object, usually function for generic function
       :param dict kwargs: dict contains other keyword and default values as parameters of that executable object
       :rtype: an ExeDict object
       :raises TypeError: required argument ``execute`` is not assigned properly

    .. attribute:: Methods:

       .. method:: __call__:

          run using ``execute`` as the function body, while other keywords and values as its parameter assignments

    .. attribute:: Examples:

       Without ExeDict, for building derived function with different default assignment values must require
       high-order function, which one is usually of high abstract and low readability:

       .. code-block:: python
          :caption: high-order function to derive version with different argument values
          :name: high-order function to derive version with different argument values

          rom info.me import ExeDict, datasets
          img = datasets.blackcurrant()

          add_baseline = (lambda **k1: (lambda **k2: (k2.update(**k1), k2.get('data') + k2.get('baseline'))[1]))
          aug_30 = add_baseline(baseline=30)
          dec_50 = add_baseline(baseline=-50)

          img_aug, img_dec = aug_30(data=img), dec_50(data=img)

       The calling of high-order function is not such explicit as common functions, because of the
       :ref:`currying <function currying>` character of it. With the previous example, it can be found the following
       calling are equivalent, but difficult to understand as common function:

       .. code-block:: python
          :caption: currying of high-order function calling
          :name: currying of high-order function calling

          img1 = add_baseline(data=img, baseline=20)()
          img2 = add_baseline(data=img)(baseline=20)
          img3 = add_baseline()(data=img, baseline=20)  # img1 == img2 == img3

       With ExeDict, it can derive a common function to versions with different argument assignments. This property
       also supports :ref:`info function <Informatics function>` intrinsically.

       .. code-block:: python
          :caption: functions derived from a meta using different arguments
          :name: functions derived from a meta using different arguments

          add_baseline = (lambda **kwargs: kwargs.get('data') + kwargs.get('baseline'))
          aug_30 = ExeDict(execute=add_baseline, baseline=30)
          dec_50 = ExeDict(execute=add_baseline, baseline=-50)

          img_aug, img_dec = aug_30(data=img), dec_50(data=img)

       Obviously, the call itself of ``add_baseline`` in the last example is more explicit than that of high-order
       functions.

    .. attribute:: Logs:

       .. versionadded:: 0.0.1

       -- |signature|
    """
    args_highlighter(execute, kwargs)


def SingleMap(x: dict):
    """
    tool to make single map function.

    .. attribute:: Arguments:

       :param dict x: an 1-length dict with a callable object as keyword, and a dict composed of keywords and
                      values for the default arguments assignment for this callable object
       :return: a partial function
       :rtype: Callable
       :raises TypeError: if the argument ``x`` was not assigned properly

    .. attribute:: Examples:

       This class is usually used for building single map function ``f(x)`` when the arguments require adaptive
       modification in the main process. It is mainly used for lazy calculation, for example:

       .. code-block:: python
          :caption: build single map function via SingleMap
          :name: build single map function via SingleMap

          from info.me import SingleMap, datasets
          imgs = [datasets.accent(), datasets.blackcurrant()]

          f = (lambda x, **k: (x-k.get('loc'))/k.get('scale'))
          fs_imgs = {SingleMap({f: {'loc': img.mean(), 'scale': img.std()}}): img for img in imgs}  # define calculation
          norm_imgs = [f(img) for f, img in fs_imgs.items()]  # execute calculation

    .. attribute:: Logs:

       .. versionadded:: 0.0.1

       -- |signature|
    """
    args_highlighter(x)


def operations(data: Any, o_prt: _ExeDict, o_sav: _ExeDict, o_vis: _ExeDict):
    """
    generic data operation function or Unit. The meta function in info that can be derived for different usage.

    .. attribute:: Arguments:

       :param Any data: input data
       :param ExeDict o_prt: ExeDict instance to determine printing method on data; ``None`` as default to escape
       :param ExeDict o_sav: ExeDict instance to determine saving method for data; ``None`` as default to escape
       :param ExeDict o_vis: ExeDict instance to determine visualization method for data; ``None`` as default to escape
       :return: the input data itself
       :rtype: Any
       :raises TypeError: required arguments ``data``, ``o_prt``, ``o_sav`` or ``o_vis`` were not assigned properly

    .. attribute:: Examples:

       For task to standardize image, if it is required informing the center and scale if its grey level, following by
       visualization after standardization. Following code shows an example implementation in plain Python style:

       .. code-block:: python
          :caption: plain python image processing flow
          :name: plain python image processing flow

          from info.ins import datasets
          from info.vis import visualization as vis
          from info.me import tensorn as tsn
          imgs = [datasets.blackcurrant(), datasets.accent(), datasets.cat()]

          # define simple info and view operations on data:
          _info = (lambda **kw: print('img center:', kw.get('data').mean(), 'img scale:', kw.get('data').std()))
          _view = (lambda **kw: vis.Canvas.play(data=kw.get('data'), fig_type='image'))

          for img in imgs:
              _info(data=img)
              img_rescale = tsn.standardization(data=img)
              _view(data=img_rescale)

       The ``operation_u`` is an info function wrapper unit, through which wrapped function ``info`` and ``view``
       will return the original ``data`` after executing operation. Of course, the wrapped function can be called in
       the form of their original ones.

       .. code-block:: python
          :caption: function wrapped by operation unit
          :name: function wrapped by operation unit

          from info.me import ExeDict, operations_u
          info = operations_u.shadow(o_prt=ExeDict(execute=_info), o_vis=None, o_sav=None)
          view = operations_u.shadow(o_vis=ExeDict(execute=_view), o_prt=None, o_sav=None)

          for img in imgs:
              info(data=img)
              img_rescale = tsn.standardization(data=img)
              view(data=img_rescale)

       The most significance of utilizing ``operation`` Unit is the property of original return for data, based on
       which the processing flow can be integrated into a pipeline with more compact and concise form:

       .. code-block:: python
          :caption: build image processing pipeline with wrapped function
          :name: build image processing pipeline with wrapped function

          from info.me import Pipeline
          p = Pipeline([info, tsn.standardization_u, view])
          rescale_imgs = [p(data=img) for img in imgs]

    .. attribute:: See also:

       - :py:class:`~info.docfunc.ExeDict`

    .. attribute:: Logs:

       .. versionadded:: 0.0.1

       -- |signature|
    """
    args_highlighter(data, o_prt, o_sav, o_vis)


def printing_u(data: Any, o_prt: _ExeDict):
    """
    generic data printing unit. The meta function in info that can be derived for different printing
    usage.

    .. attribute:: Arguments:

       :param Any data: input data
       :param o_prt: ExeDict instance to determine printing method; ``None`` as default to escape
       :return: the input data itself
       :rtype: Any
       :raises TypeError: if ``data`` or ``o_prt`` were not assigned properly

    .. attribute:: Examples:

       For plain python script, printing for mean and standard variation of grey level can be implemented as the
       follow code:

       .. code-block:: python
          :caption: plain python processing flow for printing image information
          :name: plain python processing flow for printing image information

          from info.ins import datasets
          imgs = [datasets.cat(), datasets.accent(), datasets.blackcurrant()]
          _info = (lambda **kw: print('img center:', kw.get('data').mean(), 'img scale:', kw.get('data').std()))

          for img in imgs:
              _info(data=img)

       In info, an alternative implementation is using ``printing_u`` unit coupled with ``ExeDict``:

       .. code-block:: python
          :caption: wrapped printing unit
          :name: wrapped printing unit

          from info.me import printing_u, ExeDict
          info = printing_u.shadow(o_prt=ExeDict(execute=_info))
          imgs = [info(data=img) for img in imgs]

    .. attribute:: See also:

       - :py:class:`~info.docfunc.ExeDict`

    .. attribute:: Logs:

       .. versionadded:: 0.0.1

       -- |signature|
    """
    args_highlighter(data, o_prt)


def generic_printer(data: object, attrs: list[str] = _list()):
    """
    generic printing function to show print attributes or methods for data.

    .. attribute:: Arguments:

       :param object data: original data with attributes or methods to be showed
       :param list[str] attrs: list of callable attributes; no assignment uses empty list ``[]`` as default
       :return: NoReturn
       :rtype: NoneType
       :raises AttributeError: invalid attribute or method calling in ``attrs`` assignment

    .. attribute:: Examples:

       For exporting dimension, shape and max value for images individually:

       .. code-block:: python
          :caption: attribute printing through generic printer
          :name: attribute printing through generic printer

          from info.ins import datasets, generic_printer
          imgs = [datasets.cat(), datasets.accent(), datasets.blackcurrant()]

          for img in imgs:
              generic_printer(data=img, attrs=['ndim', 'shape', 'max()'])

       Or alternative implementation using ``printing_u`` unit coupled with ``ExeDict`` class:

       .. code-block:: python
          :caption: attribute printing through printing unit wrapper
          :name: attribute printing through printing unit wrapper

          describe = printing_u.shadow(o_prt=ExeDict(execute=generic_printer, attrs=['ndim', 'max()',
                                       'clip(min=0.2).sum()']))
          imgs = [describe(data=img) for img in imgs]

    .. attribute:: See also:

       - :py:func:`~info.docfunc.printing_u`

       - :py:class:`~info.docfunc.ExeDict`

    .. attribute:: Logs:

       .. versionadded:: 0.0.1

       -- |signature|
    """
    args_highlighter(data, attrs)


def saving_u(data: Any, o_sav: _ExeDict):
    """
    generic saving unit to log something mapped from data.

    .. attribute:: Arguments:

       :param Any data: input data
       :param o_sav: ExeDict instance to determine saving method; ``None`` as default to escape
       :return: the input data itself
       :rtype: Any
       :raises TypeError: if ``data`` or ``o_sav`` were not assigned properly

    .. attribute:: Examples:

       As an example, logging the mean and standard variation in file ``'describe.log'`` can be implemented in the
       following code:

       .. code-block:: python
          :caption: logger to record mean and standard variation of grey level
          :name: logger to record mean and standard variation of grey level

          from info.ins import datasets
          imgs = [datasets.cat(), datasets.accent(), datasets.blackcurrant()]

          logger = (lambda **kw: [f := open(kw['file'], 'a+'), dt := kw['data'],
                                  f.write(f"mean: {dt.mean()}, std: {dt.std()}\\n"), f.close(), None][-1])

          for img in imgs:
              logger(data=img, file='describe.log')

       Or an equivalent using saving unit wrapper:

       .. code-block:: python
          :caption: saving unit wrapper for recording
          :name: saving unit wrapper for recording

          from info.me import saving_u, ExeDict
          record = saving_u.shadow(o_sav=ExeDict(execute=logger, file='describe.log'))
          imgs = [record(data=img) for img in imgs]

    .. attribute:: See also:

       - :py:class:`~info.docfunc.ExeDict`

    .. attribute:: Logs:

       .. versionadded:: 0.0.1

       -- |signature|
    """
    args_highlighter(data, o_sav)


def archive(data: object, to_file: str, compress_in: str = None):
    """
    python object(s) persistence toolkit. append `pyp` or `pyp.gz` suffix on file name(s).

    .. attribute:: Arguments:

       :param object data: object, or objects to be saved contained in an iterable container
       :param Union[str, list[str]] to_file: file name(s) for objects to be saved
       :param Optional[str] compress_in: file name when use compression; if assigned, a ``_header.pyp`` will be
                                         generated to note down file list; ``None`` as default to not activate
       :var Optional[int] ~compress_algorithm: compression method code; 0 for ``STORED``; 8 for ``DEFLATED``; 12 for
                                               ``BZIP2``; and 14 for ``LZMA``; 8 as default; available only if
                                               ``compress_in`` is not ``None``
       :var Optional[int] ~compress_level: int of 0 (``DEFLATED``), 1 to 9 (``DEFLATED`` and ``BZIP2``) are accepted;
                                           5 as default; available only if ``compress_in`` is not ``None``
       :return: NoReturn
       :rtype: NoneType

    .. attribute:: Examples:

       Without compression, python object can be saved integrally and individually:

       .. code-block:: python
          :caption: data persistence for python objects
          :name: data persistence for python objects

          from info.me import archive
          objs = [py_obj1, py_obj2, ..., py_objn]

          archive(data=objs, to_file='all')  # generate 'all.pyp'

          names = [f"case{idx+1}" for idx, _ in range(len(objs))]
          archive(data=objs, to_file=names)  # generate 'case1.pyp', 'case2.pyp', ..., 'casen.pyp'

       Or integrate all individual cases into a compressed file:

       .. code-block:: python
          :caption: data persistence for python objects with compression
          :name: data persistence for python objects with compression

          archive(data=objs, to_files=names, compress_in='compress')  # generated 'compress.pyp.gz'

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, to_file, compress_in)


def generic_logger(data: object, extractors: dict[str, Callable[[Any], str]] = _dict(), directory: str = os.getcwd(),
                   to_file: str = '.df_sav', other_params: dict = _dict()):
    """
    generic logger function for saving export from feature extracting functions.

    .. attribute:: Arguments:

       :param object data: data prepared to be executed via extractors
       :param dict[str, Union[Unit, Pipeline, Callable]] extractors: dict composed of feature names and mapping
                                                                     methods on data as values; no assignment uses
                                                                     empty dict ``{}`` as default
       :param str directory: path-like string for folder where the file will be saved; no assignment uses current work
                             directory (``os.getcwd()``) as default
       :param str to_file: file name for recording output; ``'.df_sav'`` as default
       :param dict other_params: the global parameters passed on all mapping methods in extractors; no assignment uses
                                 empty dict ``{}`` as default
       :return: NoReturn
       :rtype: None

    .. attribute:: Examples:

       For example, logging max and percentile values for each image into the file ``'describe.log'``:

       .. code-block:: python
          :caption: logger to record max and percentile values
          :name: logger to record max and percentile values

          from info.me import generic_logger, datasets
          import numpy as np
          imgs = [datasets.cat(), datasets.accent(), datasets.blackcurrant()]

          # define two extraction functions for max and percentile values
          get_max = (lambda **kw: np.max(kw['data']))
          get_percentiles = (lambda **kw: np.percentile(kw['data'], q=kw['percentiles']))

          for img in imgs:
              generic_logger(data=img, extractors={'max': get_max, 'percentiles': get_percentiles},
                             to_file='describe.log', other_params={'percentiles': [25, 50, 75]})

       It can also be wrapped into a saving unit:

       .. code-block:: python
          :caption: generic logger wrapped into saving unit
          :name: generic logger wrapped into saving unit

          from info.me import saving_u, ExeDict
          record = saving_u.shadow(o_sav=ExeDict(execute=generic_logger,
                                                 extractors={'max': np_max, 'percentiles': percentile},
                                                 to_file='describe.log',
                                                 other_params={'percentiles': [25, 50, 75]}))
          imgs = [record(data=img) for img in imgs]

    .. attribute:: See also:

       - :py:func:`~info.docfunc.saving_u`

       - :py:class:`~info.docfunc.ExeDict`

    .. attribute:: Logs:

       .. versionadded:: 0.0.1

       -- |signature|
    """
    args_highlighter(data, extractors, directory, to_file, other_params)


def exception_logger(data: tuple[str, Exception], directory: str = os.getcwd(), to_file: str = 'run_error.log'):
    """
    info function or Unit implementation for recording exceptive case.

    .. attribute:: Arguments:

       :param tuple[str, Exception] data: tuple composed of str for exceptive case, and exception raised during
                                          running the corresponding case
       :param str directory: path-like string for folder where the file will be saved; no assignment uses current work
                             directory (``os.getcwd()``) as default
       :param str to_file: file name for recording exceptive cases; ``'run_error.log'`` as default
       :return: NoReturn
       :rtype: None

    .. attribute:: Examples:

       .. code-block:: python
          :caption: exception logger used in try except code block
          :name: exception logger used in try except code block

          from info.me import exception_logger
          import numpy as np
          rand_sizes = np.random.randint(0, 50, 20)

          for _ in range(20):
              try:
                  dt = np.random.random(rand_sizes[_])
                  _ = dt[17]  # IndexError raised for some certain steps
              except Exception as err:
                  exception_logger(data=(f"case_{_}", err))

    .. attribute:: See also:

       - :py:func:`~info.docfunc.generic_logger`

       - :py:func:`~info.docfunc.saving_u`

       - :py:class:`~info.docfunc.ExeDict`

    .. attribute:: Logs:

       .. versionadded:: 0.0.1

       -- |signature|
    """
    args_highlighter(data, directory, to_file)


def visual_u(data: Any, o_vis: _ExeDict):
    """
    generic visualization unit.

    .. attribute:: Arguments:

       :param Any data: input data
       :param ExeDict o_vis: ExeDict instance to determine visualization method; ``None`` as default to escape
       :return: the input data itself
       :rtype: Any
       :raises TypeError: if ``data`` or ``o_vis`` were not assigned properly

    .. attribute:: Examples:

       Customized ``imshow`` function to visualize images:

       .. code-block:: python
          :caption: image show function
          :name: image show function

          from info.ins import datasets
          imgs = [datasets.cat(), datasets.accent(), datasets.blackcurrant()]
          imshow = (lambda **kw: [pg := __import__('pyqtgraph'), pg.image(kw['data'].T), pg.exec(), None][-1])

          for img in imgs:
              imshow(data=img)

       Or the alternative implementation through ``visual_u`` wrapper:

       .. code-block:: python
          :caption: image show unit wrapped from function
          :name: image show unit wrapped from function

          from info.me import visual_u, ExeDict
          imshow_u = visual_u.shadow(o_vis=ExeDict(execute=imshow))
          imgs = [imshow_u(data=img) for img in imgs]

    .. attribute:: See also:

       - :py:class:`~info.docfunc.ExeDict`

    .. attribute:: Logs:

       .. versionadded:: 0.0.1

       -- |signature|
    """
    args_highlighter(data, o_vis)


def GrpSettings(**kwargs):
    """
    configuration for plotting group data. arguments vary among groups should to be listed as the identical size
    as the number of groups.

    .. attribute:: Arguments:

       :param dict kwargs: initiate using keywords and values; no assignment for empty dict ``{}`` as default
       :var bool ~verbosity: show warning or not; ``False`` as default
       :return: figure configuration dict
       :rtype: GrpSettings
       :raises TypeError: if ``name`` is not assigned properly

    .. attribute:: Property:

       .. property:: sub:

          intrinsic number of groups for valid iteration.

       .. property:: groups:

          tuple composed of plot configuration for each group. prompt UserWarning if self adaption run due to
          length of list container does not match ``self.sub`` if ``~verbosity`` is ``True``.

    .. attribute:: Methods:

       .. method:: update:

          return a copy of self. can be updated from ``kwargs``

    .. attribute:: Examples:

       .. code-block:: python
          :caption: customized scatter plot
          :name: customized scatter plot

          from info.vis import visualization as vis
          import pyqtgraph as pg
          import numpy as np

          # prepare data
          mvn, r_mu, r_sigma = (np.random.multivariate_normal, (lambda: np.random.randint(0, 10, 2)),
                                (lambda: np.diag(np.random.random(2))))
          groups = [mvn(mean=r_mu(), cov=r_sigma(), size=_).T for _ in [20, 40, 30]]
          x, y = np.array([v for v, _ in groups], dtype=object), np.array([v for _, v in groups], dtype=object)

          # assign plot configuration for 3 groups via GrpSettings:
          config = vis.GrpSettings(**{'pen': [pg.mkPen((0, 0, 0, 0)) for _ in range(3)],
                                      'symbol': ['star', 'd', '+'],
                                      'symbolSize': 15,
                                      'symbolBrush': [_ for _ in 'rgb'],
                                      'name': [f"type_{_+1}" for _ in range(3)]})

          # scatter with customized configuration:
          app = vis.Canvas(fig_type='scatter', fig_configs=config, cvs_main='scatter figure',
                           cvs_left_label='y_value', cvs_bottom_label='x_value', cvs_legend=True)
          app.view(data=(x, y))

       The final plot will be:

       .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/1c4c443e-2c9b-43e0-a000-86e292d5f0d5
          :name: customized scatter figure
          :width: 450
          :align: center

          canvas used for customized scatter plot

    .. attribute:: See also:

       - :py:class:`~info.docfunc.Canvas`

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(kwargs)


def FigConfigs():
    """
    default figure configuration container. support types of line, scatter, histogram, beeswarm, box, and image.
    all properties in ``FigConfigs`` are ``GrpSettings`` instances.

    .. attribute:: Arguments:

        :return: a basic figure configuration container
        :rtype: FigConfigs

    .. attribute:: Property:

       .. property:: Line:

          basic figure configuration for line plot.

       .. property:: Scatter:

          basic figure configuration for scatter plot.

       .. property:: Histogram:

          basic figure configuration for histogram plot.

       .. property:: Beeswarm:

          basic figure configuration for beeswarm plot.

       .. property:: Box:

          basic figure configuration for box plot.

       .. property:: Radar:

          basic figure configuration for radar plot.

       .. property:: Image:

          basic figure configurations for image viewer.

    .. attribute:: Examples:

       With ``FigConfigs``, it is handy to visualize data via :py:class:`~data.docfunc.Canvas`:

       .. code-block:: python
          :caption: scatter using default configuration
          :name: scatter using default configuration

          from info.vis import visualization as vis
          import numpy as np

          # prepare data
          mvn, r_mu, r_sigma = (np.random.multivariate_normal, (lambda: np.random.randint(0, 10, 2)),
                                (lambda: np.diag(np.random.random(2))))
          groups = [mvn(mean=r_mu(), cov=r_sigma(), size=_).T for _ in [20, 40, 30]]
          x, y = np.array([v for v, _ in groups], dtype=object), np.array([v for _, v in groups], dtype=object)

          # scatter with default configuration:
          vis.Canvas.play(data=(x, y), fig_type='scatter', fig_configs=vis.FigConfigs.Scatter,
                          cvs_main='scatter figure', cvs_left_label='y_value', cvs_bottom_label='x_value',
                          cvs_legend=True)

       Or customized some arguments based on ``FigConfigs``. For example, use the default histogram configuration with
       ``width`` as 0.2.

       .. code-block:: python
          :caption: histogram with customized width
          :name: histogram with customized width

          vis.Canvas.play(data=y, fig_type='histogram', fig_configs=vis.FigConfigs.Histogram.update(width=0.2),
                          cvs_main='histogram figure', cvs_left_label='y_value', cvs_bottom_label='x_value',
                          cvs_legend=True)

    .. attribute:: See also:

       - :py:class:`~info.docfunc.GrpSettings`

       - :py:class:`~info.docfunc.Canvas`

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       .. versionchanged:: 0.0.3

          include default configuration for radar plot.

       -- |signature|
    """
    ...


def Canvas(data: Union[np_ndarray, tuple[np_ndarray, np_ndarray]] = None,
           fig_type: Literal['line', 'scatter', 'histogram', 'beeswarm', 'box', 'heatmap', 'radar', 'pie',
           'image'] = 'line',
           fig_configs: _GrpSettings = _FigConfigs.Line,
           cvs_main: str = 'info', cvs_size: tuple[int, int] = (640, 480),
           cvs_background: str = 'w', cvs_grid: dict = _dict({'x': True, 'y': True}),
           cvs_title: str = None, cvs_title_configs: dict = _dict({'color': 'k', 'size': '15pt'}),
           cvs_left_label: str = None, cvs_bottom_label: str = None,
           cvs_label_configs: dict = _dict({'color': 'b', 'font-size': '13pt'}),
           cvs_legend: bool = False, cvs_axes: dict[str, bool] = None):
    """
    generic visualization utility. making line, scatter, histogram, beeswarm, box, heatmap, radar, pie, contour figures
    for group and ungrouped data, or viewer for images.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, tuple[numpy.ndarray, numpy.ndarray]] data: specified data during initialize a Canvas
                                                                              instance; ``None`` as default
       :param Literal[...] fig_type: figure type for visualizer; should be option among ``'line'``, ``'scatter'``,
                                     ``'histogram'``, ``'beeswarm'``, ``'box'``, ``'heatmap'``, ``'radar'``, ``'pie'``,
                                     ``'contour'`` and ``'image'``; ``'line'`` as default
       :param GrpSettings fig_configs: instance of GrpSettings; FigConfigs is the collection of default configurations
                                       for all figure types; ``None`` as default will heuristically guess then
                                       configure from ``fig_type``
       :param str cvs_main: main title for application window; ``'info'`` as default
       :param tuple[int, int] cvs_size: main window size; ``None`` as default for applying ``(640, 480)`` on line,
                                        scatter, histogram, beeswarm, box plots or image viewer, ``(560, 560)`` on
                                        radar and pie plots
       :param str cvs_background: background color for canvas; ``'w'`` as default
       :param dict cvs_grid: trigger to (un)enable grids of x and y in figure; ``{'x': True, 'y': True}`` as default
       :param str cvs_title: title of figure; ``None`` as default
       :param dict cvs_title_configs: configurations of figure title; ``{'color': 'k', 'size': '15pt'}`` as default
       :param str cvs_left_label: text content for left label; ``None`` as default
       :param str cvs_bottom_label: text content for bottom label; ``None`` as default
       :param dict cvs_label_configs: configurations of left and bottom labels; ``{'color': 'b', 'font-size': '13pt'}``
                                      as default
       :param bool cvs_legend: trigger to (un)enable figure legend; ``False`` as default
       :param dict[str, bool] cvs_axes: (un)display axes triggers; ``{'left': True, 'top': False, 'right': False,
                                        'bottom': True}`` as default
       :return: a visualization application
       :rtype: Canvas
       :raises ValueError: invalid argument exists

    .. attribute:: Methods:

       .. method:: view:

          show figure. ``data`` can be updated.

       .. method:: save:

          static method; ``save_as`` to specify the file name for figure to be exported; ``figure.png`` as default

       .. method:: play:

          static method; create a new canvas then show figure. all ``**kwargs`` assignment supported.

    .. attribute:: Examples:

       Use ``Canvas`` to build line plot:

       .. code-block:: python
          :caption: Canvas for line plot
          :name: Canvas for line plot

          from info.vis import visualization as vis
          import numpy as np

          # prepare data
          mvn, r_mu, r_sigma = (np.random.multivariate_normal, (lambda: np.random.randint(0, 10, 2)),
                                (lambda: np.diag(np.random.random(2))))
          groups = [mvn(mean=r_mu(), cov=r_sigma(), size=_).T for _ in [20, 40, 30]]
          x, y = np.array([v for v, _ in groups], dtype=object), np.array([v for _, v in groups], dtype=object)

          vis.Canvas.play(data=y, fig_type='line', cvs_main='line figure', cvs_left_label='y_value', cvs_legend=True)

       .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/c5005a23-7ae5-41de-9248-ef313ba4107e
          :name: line figure
          :width: 450
          :align: center

          canvas used for line plot

       And for scatter plot:

       .. code-block:: python
          :caption: Canvas for scatter plot
          :name: Canvas for scatter plot

          vis.Canvas.play(data=(x, y), fig_type='scatter', cvs_main='scatter figure', cvs_left_label='y_value',
                          cvs_bottom_label='x_value', cvs_legend=True)

       .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/30e96d10-0b21-47e6-ba65-ec3068314d8e
          :name: scatter figure
          :width: 450
          :align: center

          canvas used for scatter plot

       And also for histogram plot:

       .. code-block:: python
          :caption: Canvas for histogram plot
          :name: Canvas for histogram plot

          vis.Canvas.play(data=y, fig_type='histogram', fig_configs=vis.FigConfigs.Histogram.update(width=0.2),
                          cvs_main='histogram figure', cvs_left_label='y_value', cvs_bottom_label='x_value',
                          cvs_legend=True)

       .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/5742afe3-2141-4779-95db-825147eca9c7
          :name: histogram figure
          :width: 450
          :align: center

          canvas used for histogram plot

       Also support for beeswarm plot:

       .. code-block:: python
          :caption: Canvas for beeswarm plot
          :name: Canvas for beeswarm plot

          vis.Canvas.play(data=y, fig_type='beeswarm', cvs_main='beeswarm figure', cvs_left_label='y_value',
                          cvs_legend=True)

       .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/330e8951-e587-4f0c-a94f-f6ed5bd0190b
          :name: beeswarm figure
          :width: 450
          :align: center

          canvas used for beeswarm plot

       For making box plot:

       .. code-block:: python
          :caption: Canvas for box plot
          :name: Canvas for box plot

          vis.Canvas.play(data=y, fig_type='box', cvs_main='box figure', cvs_left_label='y_value', cvs_legend=True)

       .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/71c25828-26e0-45ee-bca6-3c349421e58c
          :name: box figure
          :width: 450
          :align: center

          canvas used for box plot

       For making heatmap plot:

       .. code-block:: python
          :caption: Canvas for heatmap plot
          :name: Canvas for heatmap plot

          vec, mat = np.random.random(10), np.random.random((10, 4))
          config1 = vis.FigConfigs.Heatmap.update(tags=np.array([f"V{_+1}" for _ in range(10)]))
          config2 = vis.FigConfigs.Heatmap.update(tags=np.array([f"S{_+1}" for _ in range(10)]))
          vis.Canvas.play(data=vec, fig_type='heatmap', fig_configs=config1, cvs_main='heatmap figure 1')
          vis.Canvas.play(data=mat, fig_type='heatmap', fig_configs=config2, cvs_main='heatmap figure 2')

       .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/9b2d97d2-85f4-4c35-864e-96e1e3fd43e8
          :name: heatmap figure
          :width: 650
          :align: center

          canvas used for heatmap plot

       For radar plot:

       .. code-block:: python
          :caption: Canvas for radar plot
          :name: Canvas for radar plot

          # generic radar plot
          vecs = np.array([np.random.randint(5, 10, 5) + np.random.random(5) for _ in range(3)])
          vis.Canvas.play(data=vecs, fig_type='radar', cvs_main='radar figure', cvs_legend=True)

          # or be more customized
          import pyqtgraph as pg
          rescale_vecs, rescale_params = vis.rescale_radar(data=vecs, scale_base=2.3)
          cus_pen = pg.mkPen(color="#6a6da9", style=pg.QtGui.Qt.PenStyle.DashLine)
          vis.Canvas.play(data=rescale_vecs, fig_type='radar', cvs_main='radar figure', cvs_legend=True,
                          fig_configs=vis.FigConfigs.Radar.update(name=['var1', 'var2', 'var3'],
                                                                  rescale_labels=rescale_params,
                                                                  dim_names=['d1', 'd2', 'd3', 'd4', 'd5'],
                                                                  n_grids=5, pen_grids=cus_pen))

       .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/23f84d63-0f8f-422e-b4f6-4af3c754f6b7
          :name: radar figure
          :width: 650
          :align: center

          canvas used for radar plot

       For pie plot:

       .. code-block:: python
          :caption: Canvas for pie plot
          :name: Canvas for pie plot

          frac = np.array([20, 15, 40, 25])
          vis.Canvas.play(data=frac, fig_type='pie', cvs_main='pie figure', cvs_legend=True)

       .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/da6212ef-a1ef-4d02-80f5-5eabff8dd1d1
          :name: pie figure
          :width: 450
          :align: center

          canvas used for pie plot

       For contour plot:

       .. code-block:: python
          :caption: Canvas for iso-contour plot
          :name: Canvas for iso-contour plot

          _cont = (lambda x1, x2: (1-x1/2+x1**5+x2**3)*np.exp(-x1**2-x2**2))
          dens = _cont(*np.meshgrid(*[np.linspace(-3, 3, 256) for _ in range(2)]))
          vis.Canvas.play(data=dens, fig_type='contour', fig_configs=vis.FigConfigs.Contour.update(rect=(-3, -3, 6, 6)))

       .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/c8279371-1de0-4f56-9dfe-42653d7873d6
          :name: contour figure
          :width: 450
          :align: center

          canvas used for contour plot

       Use as an image viewer:

       .. code-block:: python
          :caption: Canvas as image viewer
          :name: Canvas as image viewer

          from info.ins import datasets
          vis.Canvas.play(data=datasets.cat(), fig_type='image', cvs_main='image viewer')

       .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/6c63cea8-b3c4-4645-a389-97edad188c70
          :name: image figure
          :width: 450
          :align: center

          canvas used for image viewer

    .. attribute:: Note:

       If ``IndexError`` raised, reassign ``name`` in ``fig_configs`` by :py:class:`~info.docfunc.GrpSettings`,
       or by updating default configuration set :py:class:`~info.docfunc.FigConfigs`.

    .. attribute:: See Also:

       - :py:class:`~info.docfunc.GrpSettings`

       - :py:class:`~info.docfunc.FigConfigs`

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       .. versionchanged:: 0.0.3

          support heatmap, radar, and pie plot. heuristically guess and configuration of ``fig_configs``.

       .. versionchanged:: 0.0.4

          support writing image via ``save`` method. no limitation for 10 groups of data in maximum anymore.

       .. versionchanged:: 0.0.5

          support iso contour plot. attach interactive color bar item to heatmap and contour plot. add logic of length
          check, as well as horizontal label trigger for tags in heatmap.

       -- |signature|
    """
    args_highlighter(data, fig_type, fig_configs, cvs_main, cvs_size, cvs_background, cvs_grid, cvs_title,
                     cvs_title_configs, cvs_left_label, cvs_bottom_label, cvs_label_configs, cvs_legend, cvs_axes)


def KernelGen(shape: tuple[int, ...], dtype: type = int, buffer: np_ndarray = None, offset: int = 0,
              strides: tuple = None, order: Literal['C', 'F'] = None, origin: Union[int, Iterable[int]] = 0,
              fill: Numeric = 1, replace: dual_ndarray = None):
    """
    kernel generator. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param tuple[int, ...] shape: tuple for kernel shape
       :param Type dtype: element type passed on numpy ndarray; int as default
       :param Optional[Union[numpy.ndarray]] buffer: argument passed on numpy ndarray; ``None`` as default
       :param Optional[int] offset: argument passed on numpy ndarray; 0 as default
       :param Optional[tuple[int]] strides: argument passed on numpy ndarray; ``None`` as default
       :param Literal['C', 'F'] order: argument passed on numpy ndarray; ``'C'`` for row-major and ``'F'`` for
                                       column-major; ``'C'`` as default
       :param Union[int, Iterable[int]] origin: bias of kernel center; must be Iterable object of int to specify bias
                                                for each axis, or int assignment applied that bias to all axis;
                                                0 as default
       :param Numeric fill: int or float for filling all elements in Kernel; 1 as default
       :param Union[numpy.ndarray, cupy.ndarray] replace: substituting element by customized ndarray if specified;
                                                          ``None`` as default
       :return: a ndarray kernel
       :rtype: KernelGen

    .. attribute:: Properties:

       .. property:: rela_anchor:

          anchor coordinate relative to zero-origin anchor.

       .. property:: center:

          physical center of kernel.

       .. property:: anchor:

          anchor coordinate of kernel.

       .. property:: anchor_id:

          anchor index in raveled kernel.

       .. property:: rela_pos_rv:

          a raveled coordinates of all kernel elements relative to kernel center.

    .. attribute:: Examples:

       .. code-block:: python
          :caption: averaging kernel with shape (2, 3)
          :name: averaging kernel with shape (2, 3)

          from info.me import kernel_utils as ku
          import numpy as np

          shape_ = (2, 3)
          avg_k = ku.KernelGen(shape=shape_, fill=1/np.prod(shape_))

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(shape, dtype, buffer, offset, strides, order, origin, fill, replace)


def averaging_kernel(k_shape: tuple[int, ...]):
    """
    generate an averaging kernel with specified shape. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param tuple[int, ...] k_shape: tuple for kernel shape
       :return: an averaging kernel
       :rtype: KernelGen
       :raises TypeError: argument ``'k_shape'`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: generate an averaging kernel
          :name: generate an averaging kernel

          from info.me import kernel_utils as ku
          avg_k = ku.averaging_kernel(k_shape=(2, 3))

    .. attribute:: See also:

       - :py:class:`~info.docfunc.KernelGen`

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(k_shape)


def gaussian_kernel(k_shape: tuple[int, ...], k_mu: dual_ndarray = None, k_sigma: dual_ndarray = None):
    r"""
    generate a Gaussian kernel from a multivariate gaussian distribution. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param tuple[int, ...] k_shape: tuple for kernel shape
       :param Union[numpy.ndarray, cupy.ndarray] k_mu: mean of Gaussian; :math:`\boldsymbol{0}` vector as default
       :param Union[numpy.ndarray, cupy.ndarray] k_sigma: covariance matrix of Gaussian; diagonal matrix of ``k_shape``
                                                          as default
       :var bool ~other_info: whether return the other information about kernel; ``False`` as default
       :return: a Gaussian kernel object, and possibly the covariance :math:`\boldsymbol{\Sigma}` and the corresponding
                rank :math:`r(\boldsymbol{\Sigma})`
       :rtype: Union[KernelGen, tuple[KernelGen, list[Union[ndarray, int]]]]
       :raises TypeError: argument ``k_shape`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: generate a Gaussian kernel
          :name: generate a Gaussian kernel

          from info.me import kernel_utils as ku
          gs_k = ku.gaussian_kernel(k_shape=(2, 3))

    .. attribute:: Notes:

       The kernel generation uses Gaussian multivariate probability density function as follows:

       .. math::
          :label: multivariate Gaussian

          f(\boldsymbol{x}|\boldsymbol{\mu},\boldsymbol{\Sigma}) = \frac{1}{(2\pi)^{\frac{k}{2}} \vert
          \boldsymbol{\Sigma} \vert^{\frac{1}{2}}} \exp{[-\frac{1}{2} (\boldsymbol{x} - \boldsymbol{\mu})^T
          \boldsymbol{\Sigma}^{-1} (\boldsymbol{x} - \boldsymbol{\mu})]}

       Where :math:`\boldsymbol{m}^T\boldsymbol{\Sigma}\boldsymbol{m} > 0`, for all
       :math:`\boldsymbol{m} \in \mathbb{R}^k`.

       Internal variable ``'~other_info'`` can be overwritten, default value uses ``False``; if ``True``, the values of
       returned kernel will not be rescaled, and :math:`\boldsymbol{\Sigma}` and :math:`\mathrm{r}(\boldsymbol{\Sigma})`
       will be returned as well. here shows the demonstration:

       .. code-block:: python
          :caption: Gaussian kernel returned with extra information
          :name: Gaussian kernel returned with extra information

          from info.me import kernel_utils as ku
          gs_k, other_info = ku.gaussian_kernel(k_shape=(2, 3), **{'~other_info': True})

       Final effect of gaussian kernel showed with a 3-dimensional surface is showed as
       :numref:`Figure %s <gaussian kernel>`.

    .. attribute:: See also:

       - :py:class:`~info.docfunc.KernelGen`

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(k_shape, k_mu, k_sigma)


def gabor_kernel(k_shape: tuple[int, ...], k_orientation: list[Numeric], k_rescale: Numeric = 1,
                 k_wavelength: Numeric = PI2, k_phase: Numeric = 0):
    r"""
    generate a Gabor kernel via a harmonic sine multivariate gaussian distribution. available for numpy and cupy
    ndarray.

    .. attribute:: Arguments:

       :param tuple[int, ...] k_shape: tuple for kernel shape
       :param list[Numeric] k_orientation: spatial orientation where the harmonic sine function periodically repeats;
                                           ``None`` as default to automatically generate 1 for each dimension (e.g.
                                           ``[1, 1, 1]`` for 3D data)
       :param Numeric k_rescale: rescale coefficient to determine the size of gaussian envelope; 1 as default
       :param Numeric k_wavelength: wavelength of harmonic sine function; :math:`2\pi` as default
       :param Numeric k_phase: phase position of harmonic sine function; 0 as default
       :return: a complex number domain Gabor kernel object
       :rtype: KernelGen
       :raises TypeError: argument ``k_shape`` or ``k_orientation`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: generate a Gabor kernel
          :name: generate a Gabor kernel

          from info.me import kernel_utils as ku
          gb_k = ku.gabor_kernel(k_shape=(10, 15), k_orientation=[1, 0.8])

    .. attribute:: Notes:

       The kernel generation uses multivariate gaussian, combined with
       :ref:`spatial sine harmonic function <spatial sine function>` as follows:

       .. math::
          :label: multivariate Gabor

          G(\boldsymbol{x}|\boldsymbol{\mu}, \boldsymbol{\Sigma}, \boldsymbol{n}, A, \lambda, \phi) = A \cdot
          \exp{[-\frac{1}{2} (\boldsymbol{x} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} (\boldsymbol{x} -
          \boldsymbol{\mu})]} \cdot \exp{[i(2\pi\frac{\boldsymbol{x}^T \boldsymbol{n} }{\lambda} + \phi)]}

       Where :math:`\boldsymbol{\mu}` and :math:`\boldsymbol{\Sigma}` are parameters in multivariate gaussian
       kernel. Generally, :math:`\boldsymbol{\mu} = \boldsymbol{0}`, and :math:`\boldsymbol{\Sigma}` is automatically
       determined based on ``k_shape``. :math:`A` refers amplitude for rescaling the gaussian envelope.
       :math:`\boldsymbol{n}` is the normal direction for hyperplane of spatial sine (cosine) function (see
       note in :ref:`spatial filtering <spatial sine function>`), therefore, the scalar
       :math:`\boldsymbol{x} \cdot \boldsymbol{n}` is the projection of :math:`\boldsymbol{x}` in direction of
       :math:`\boldsymbol{n}`. :math:`\lambda` and :math:`\phi` is the wavelength and phase position for the spatial
       sine (cosine) function respectively.

       As the last item in :eq:`multivariate Gabor` is of the Euler's formula, the
       :math:`G(\boldsymbol{x}|\boldsymbol{\mu}, \boldsymbol{\Sigma}, \boldsymbol{n}, A, \lambda, \phi)` must
       be a complex kernel. More specifically, let
       :math:`N^\prime(\boldsymbol{x} | \boldsymbol{\mu}, \boldsymbol{\Sigma}) = \exp{[-\frac{1}{2} (\boldsymbol{x} -
       \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} (\boldsymbol{x} - \boldsymbol{\mu})]}`, the real part of
       :eq:`multivariate Gabor` will be:

       .. math::
          :label: real part of multivariate Gabor

          G_{\mathrm{rel}}(\boldsymbol{x}|\boldsymbol{\mu}, \boldsymbol{\Sigma}, \boldsymbol{n}, A, \lambda, \phi)
          = A \cdot N^\prime(\boldsymbol{x} | \boldsymbol{\mu}, \boldsymbol{\Sigma}) \cdot \cos{(2\pi
          \frac{\boldsymbol{x}^T \boldsymbol{n} }{\lambda} + \phi)}

       And for the imaginary part:

       .. math::
          :label: imaginary part of multivariate Gabor

          G_{\mathrm{img}}(\boldsymbol{x}|\boldsymbol{\mu}, \boldsymbol{\Sigma}, \boldsymbol{n}, A, \lambda,
          \phi) = A \cdot N^\prime(\boldsymbol{x} | \boldsymbol{\mu}, \boldsymbol{\Sigma}) \cdot \sin{(2\pi
          \frac{\boldsymbol{x}^T \boldsymbol{n} }{\lambda} + \phi)}

    .. attribute:: See also:

       - :py:class:`~info.docfunc.KernelGen`

       - :py:func:`~info.docfunc.gaussian_kernel`

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(k_shape, k_orientation, k_rescale, k_wavelength, k_phase)


def laplacian_of_gaussian_kernel(k_shape: tuple[int, ...], k_mu: dual_ndarray = None, k_sigma: dual_ndarray = None):
    r"""
    generate a :ref:`LoG <LoG>` kernel through multivariate gaussian distribution. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param tuple[int, ...] k_shape: tuple for kernel shape
       :param Union[numpy.ndarray, cupy.ndarray] k_mu: mean of Gaussian; :math:`\boldsymbol{0}` vector as default
       :param Union[numpy.ndarray, cupy.ndarray] k_sigma: covariance matrix of Gaussian; diagonal matrix of ``k_shape``
                                                          as default
       :return: an un-rescaled :ref:`LoG <LoG>` kernel
       :rtype: KernelGen
       :raises TypeError: argument ``k_shape`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: generate a Laplacian of Gaussian kernel
          :name: generate a Laplacian of Gaussian kernel

          from info.me import kernel_utils as ku
          log_k = ku.laplacian_of_gaussian_kernel(k_shape=(2, 3))

    .. attribute:: Notes:

       The 1st order derivative of gaussian distribution :eq:`multivariate Gaussian` are:

       .. math::
          :label: 1st order derivative of multivariate Gaussian

          \frac{\partial f(\boldsymbol{x}|\boldsymbol{\mu},\boldsymbol{\Sigma})}{\partial \boldsymbol{x}} = -
          \frac{\boldsymbol{\Sigma}^{-1}(\boldsymbol{x} - \boldsymbol{\mu})}{(2\pi)^\frac{k}{2} \vert
          \boldsymbol{\Sigma} \vert^\frac{1}{2}} \exp{[-\frac{1}{2} (\boldsymbol{x} - \boldsymbol{\mu})^T
          \boldsymbol{\Sigma}^{-1} (\boldsymbol{x} - \boldsymbol{\mu})]} = - \boldsymbol{\Sigma}^{-1}(\boldsymbol{x} -
          \boldsymbol{\mu}) f(\boldsymbol{x}|\boldsymbol{\mu},\boldsymbol{\Sigma})

       And the derivative of 2nd order:

       .. math::
          :label: 2nd order derivative of multivariate Gaussian

          \begin{eqnarray}
          \frac{\partial^2 f(\boldsymbol{x}|\boldsymbol{\mu},\boldsymbol{\Sigma})}{\partial \boldsymbol{x} \partial
          \boldsymbol{x}^T} &=& \frac{[\boldsymbol{\Sigma}^{-1}(\boldsymbol{x}-\boldsymbol{\mu})(\boldsymbol{x} -
          \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} - \boldsymbol{\Sigma}^{-1}]}{(2\pi)^\frac{k}{2} \vert
          \boldsymbol{\Sigma} \vert^\frac{1}{2}} \exp{[-\frac{1}{2} (\boldsymbol{x} - \boldsymbol{\mu})^T
          \boldsymbol{\Sigma}^{-1} (\boldsymbol{x} - \boldsymbol{\mu})]} \\ &=& [\boldsymbol{\Sigma}^{-1}(\boldsymbol{x}
          - \boldsymbol{\mu}) (\boldsymbol{x}-\boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} - \boldsymbol{\Sigma}^{-1}]
          f(\boldsymbol{x}|\boldsymbol{\mu},\boldsymbol{\Sigma})
          \end{eqnarray}

       Based on the definition of 2nd order gradient operator :math:`\nabla^2`, the Laplacian of Gaussian can be
       calculated through traces of each matrices in :eq:`2nd order derivative of multivariate Gaussian` theoretically,
       however for simplification, generating its weights via the following kernel is much speedy and practical:

       .. math::
          :label: laplacian of gaussian kernel

          f(\boldsymbol{x} | \boldsymbol{\mu}, \boldsymbol{\Sigma}) \propto  [\frac{(\boldsymbol{x} -
          \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} (\boldsymbol{x} - \boldsymbol{\mu})}{2} - 1]
          \exp{[-\frac{(\boldsymbol{x} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} (\boldsymbol{x} -
          \boldsymbol{\mu})}{2}]}

       Where the :math:`\boldsymbol{\mu}` denotes the geometric center of the kernel, for any
       :math:`\boldsymbol{m} \in \mathbb{R}^k` (:math:`k` is the number of dimensions), the
       :math:`\boldsymbol{\Sigma}` must be positive definite
       (:math:`\boldsymbol{m}^T \boldsymbol{\Sigma} \boldsymbol{m} > 0`).

       In practice, info takes :math:`\boldsymbol{\mu} = \boldsymbol{0}`, and the kernel will be of the
       following form:

       .. math::
          :label: laplacian of gaussian in practice

          \mathrm{LoG}(\boldsymbol{x} | \boldsymbol{0}, \boldsymbol{\Sigma}) = C_1 \cdot (1 - \boldsymbol{x}^T
          \boldsymbol{\Sigma_{d}^{-1}} \boldsymbol{x}) \exp{(- \boldsymbol{x}^T \boldsymbol{\Sigma_{d}^{-1}}
          \boldsymbol{x})} + C_2

       :math:`C_1` and :math:`C_2` are constants for scale and location respectively. :math:`\boldsymbol{0}` and
       :math:`\boldsymbol{\Sigma}` are parameters for Gaussian component in kernel. The sign of :math:`C_1`
       determine how this kernel works: if :math:`\mathrm{sgn}(C_1) = 1`, it will perform as a 2nd-order differential
       operator to highlight the areas with high change rate in value (or edge-like areas in conventional description);
       if :math:`\mathrm{sgn}(C_1) = -1`, it will obtain a reversed the high change rate areas, with which overlapped
       into the original data the result will be revealed in higher contrast in edge-like areas.

       Final effect of gaussian kernel showed with a 3-dimensional surface is showed as
       :numref:`Figure %s <LoG kernel>`.

    .. attribute:: See also:

       - :py:class:`~info.docfunc.KernelGen`

       - :py:func:`~info.docfunc.gaussian_kernel`

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(k_shape, k_mu, k_sigma)


def averaging_filter(data: dual_ndarray, k_shape: tuple[int, ...],
                     k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
                     k_cval: Numeric = 0.0, k_origin: Union[int, Iterable[int]] = 0):
    """
    averaging filter for tensor. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: the shape of averaging kernel
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Union[int, Iterable[int]] k_origin: origin of anchor pixel in kernel; 0 as default
       :return: a filtered tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` or ``k_shape`` are not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: averaging filter for image
          :name: averaging filter for image

          from info.me import tensorn as tsn
          from info.ins import datasets

          tsn.averaging_filter(data=datasets.blackcurrant(), k_shape=(4, 5))

    .. attribute:: See also:

       - :py:func:`~info.docfunc.averaging_kernel`

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, k_shape, k_mode, k_cval, k_origin)


def rank_filter(data: dual_ndarray, k_shape: tuple[int, ...], k_rank: Numeric,
                k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
                k_cval: Numeric = 0.0, k_origin: Union[int, Iterable[int]] = 0):
    """
    rank filter for tensor. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: the shape of averaging kernel
       :param Numeric k_rank: rank for filter, int as indexing or float from 0. to 1. as quantile; for examples, 0 for
                              minimum, -1 for maximum using int assignment, 0.5 for median using float assignment
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Union[int, Iterable[int]] k_origin: origin of anchor pixel in kernel; 0 as default
       :return: a filtered tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data``, ``k_shape`` or ``k_rank`` are not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: rank filter for image
          :name: rank filter for image

          from info.me import tensorn as tsn
          from info.ins import datasets

          tsn.rank_filter(data=datasets.blackcurrant(), k_shape=(4, 5), k_rank=0.75)
          tsn.rank_filter(data=datasets.blackcurrant(), k_shape=(4, 5), k_rank=-1)

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, k_shape, k_rank, k_mode, k_cval, k_origin)


def agg_func_filters(data: dual_ndarray, k_shape: tuple[int, ...],
                     k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
                     k_cval: Numeric = 0.0, k_origin: Union[int, Iterable[int]] = 0):
    """
    aggregation functional filter for tensor. an :ref:`aggregation function <aggregation function>` is type of data
    transfer method to map a multi-element data into a scalar. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: the shape of averaging kernel
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Union[int, Iterable[int]] k_origin: origin of anchor pixel in kernel; 0 as default
       :return: a filtered tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` or ``k_shape`` are not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: aggregation functional filters for image
          :name: aggregation functional filters for image

          from info.me import tensorn as tsn
          from info.ins import datasets
          img, shape = datasets.blackcurrant(), (4, 5)

          tsn.minimum_filter(data=img, k_shape=shape)
          tsn.maximum_filter(data=img, k_shape=shape)
          tsn.mean_filter(data=img, k_shape=shape)
          tsn.median_filter(data=img, k_shape=shape)

    .. attribute:: Notes:

       Some aggregation functions are specific forms of :py:func:`~info.docfunc.rank_filter`:

       .. code-block:: python
          :caption: homogeneity of mappings for some aggregation functional filters and rank filter
          :name: homogeneity of mappings for some aggregation functional filters and rank filter

          from info.me import tensorn as tsn
          from info.ins import datasets
          img, shape, rf = datasets.blackcurrant(), (4, 5), tsn.rank_filter

          assert (tsn.minimum_filter(data=img, k_shape=shape) - rf(data=img, k_shape=shape, k_rank=0)).any() == False
          assert (tsn.maximum_filter(data=img, k_shape=shape) - rf(data=img, k_shape=shape, k_rank=-1)).any() == False
          assert (tsn.median_filter(data=img, k_shape=shape) - rf(data=img, k_shape=shape, k_rank=0.5)).any() == False

    .. attribute:: See also:

       - :py:func:`~info.docfunc.rank_filter`

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, k_shape, k_mode, k_cval, k_origin)


maximum_filter = summary_sub(agg_func_filters, 'local maximum filter for tensor')
maximum_filter = tag_sub(maximum_filter, 'maximum')
minimum_filter = summary_sub(agg_func_filters, 'local minimum filter for tensor')
minimum_filter = tag_sub(minimum_filter, 'minimum')
mean_filter = summary_sub(agg_func_filters, 'local mean filter for tensor')
mean_filter = tag_sub(mean_filter, 'mean')
median_filter = summary_sub(agg_func_filters, 'local median filter for tensor')
median_filter = tag_sub(median_filter, 'median')


def gaussian_filter(data: dual_ndarray, k_shape: tuple[int, ...], k_mu: dual_ndarray = None,
                    k_sigma: dual_ndarray = None,
                    k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
                    k_cval: Numeric = 0.0, k_origin: Union[int, Iterable[int]] = 0):
    r"""
    gaussian filter for tensor. gaussian kernel is generated using :py:func:`~info.docfunc.gaussian_kernel` based
    on :eq:`multivariate Gaussian`. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: the shape of averaging kernel
       :param Union[numpy.ndarray, cupy.ndarray] k_mu: mean of Gaussian; :math:`\boldsymbol{0}` vector as default
       :param Union[numpy.ndarray, cupy.ndarray] k_sigma: covariance matrix of Gaussian; diagonal matrix of ``k_shape``
                                                          as default
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Union[int, Iterable[int]] k_origin: origin of anchor pixel in kernel; 0 as default
       :return: a filtered tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` or ``k_shape`` are not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: gaussian filter for image
          :name: gaussian filter for image

          from info.me import tensorn as tsn
          from info.ins import datasets

          tsn.gaussian_filter(data=datasets.blackcurrant(), k_shape=(4, 5))

    .. attribute:: See also:

       - :py:func:`~info.docfunc.gaussian_kernel`

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, k_shape, k_mu, k_sigma, k_mode, k_cval, k_origin)


def gabor_filter(data: dual_ndarray, k_shape: tuple[int, ...], k_rescale: Numeric = 1,
                 k_orientation: list[Numeric] = None, k_wavelength: Numeric = PI2, k_phase: Numeric = 0,
                 k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
                 k_cval: Numeric = 0.0, k_origin: Union[int, Sequence[int]] = 0):
    r"""
    gabor filter for tensor. gabor kernel is generated using :py:func:`~info.docfunc.gabor_kernel` based
    on :eq:`multivariate Gaussian`. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: tuple for kernel shape
       :param Numeric k_rescale: rescale coefficient to determine the size of gaussian envelope; 1 as default
       :param list[Numeric] k_orientation: spatial orientation where the harmonic sine function periodically repeats;
                                           ``None`` as default to automatically generate 1 for each dimension (e.g.
                                           ``[1, 1, 1]`` for 3D data)
       :param Numeric k_wavelength: wavelength of harmonic sine function; :math:`2\pi` as default
       :param Numeric k_phase: phase position of harmonic sine function; 0 as default
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Union[int, Iterable[int]] k_origin: origin of anchor pixel in kernel; 0 as default
       :return: a filtered tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data``, ``k_shape`` or ``k_orientation`` are not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: gabor filter for image
          :name: gabor filter for image

          from info.me import tensorn as tsn
          from info.ins import datasets

          tsn.gabor_filter(data=datasets.blackcurrant(), k_shape=(15, 15), k_orientation=[1, 1])

    .. attribute:: See also:

       - :py:func:`~info.docfunc.gabor_kernel`

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, k_shape, k_rescale, k_orientation, k_wavelength, k_phase, k_mode, k_cval, k_origin)


def bilateral_filter(data: dual_ndarray, k_shape: tuple[int, ...], sigma_d: dual_ndarray = None,
                     sigma_r: dual_ndarray = None,
                     k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
                     k_cval: Numeric = 0.0, k_origin: Union[int, Iterable[int]] = 0):
    r"""
    bilateral filter for tensor. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: the shape of averaging kernel
       :param Union[numpy.ndarray, cupy.ndarray] sigma_d: covariance matrix of Gaussian; diagonal matrix of ``k_shape``
                                                          as default
       :param Union[numpy.ndarray, cupy.ndarray] sigma_r: variance of ranged space; ``None`` for local adaptive
                                                          variance as default
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Union[int, Iterable[int]] k_origin: origin of anchor pixel in kernel; 0 as default
       :return: a filtered tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` or ``k_shape`` are not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: bilateral filter for image
          :name: bilateral filter for image

          from info.me import tensorn as tsn
          from info.ins import datasets
          img = datasets.blackcurrant()

          # using self-adaptive sigma_r
          tsn.bilateral_filter(data=img, k_shape=(4, 5))

          # using fixed sigma_r
          tsn.bilateral_filter(data=img, k_shape=(4, 5), sigma_r=10)

          # in extremely large sigma_r, bilateral_filter will degenerate into the effect of Gaussian kernel:
          tsn.bilateral_filter(data=img, k_shape=(4, 5), sigma_r=1e10)

    .. attribute:: Notes:

       For each element-dependent block, the general form of wight kernel follow:

       .. math::
          :label: bilateral weight kernel

          W(\boldsymbol{x}, \boldsymbol{s}) \propto \exp{[-\frac{(\boldsymbol{x}-\boldsymbol{s})^T
          \boldsymbol{\Sigma}^{-1}_{d} (\boldsymbol{x}-\boldsymbol{s})}{2} - \frac{\Vert I(\boldsymbol{x}) -
          I(\boldsymbol{s}) \Vert^{2}}{2 \sigma^{2}_{r}}]}

       Where :math:`I(\boldsymbol{x})` and :math:`I(\boldsymbol{s})` are the values spaced in tensor and kernel
       respectively. In kernel space, :math:`\boldsymbol{x}` is the anchor pixel with zero offset, therefore the 1st
       exponential item in :eq:`bilateral weight kernel` is the Gaussian kernel (:eq:`multivariate Gaussian`) with
       :math:`\boldsymbol{\mu} = \boldsymbol{0}`. For each element, :math:`W(\boldsymbol{x}, \boldsymbol{s})` is
       rescaled by :math:`W = W(\boldsymbol{x},\boldsymbol{s})/\sum_{\boldsymbol{s}}W(\boldsymbol{x}, \boldsymbol{s})`

       Bilateral filter was proposed by :ref:`C. Tomasi et. al. <[Tomasi1998]>` for an edge-preserving smoothing on
       image processing. As a no-linear method, kernel of bilateral will be a function of both Gaussian distribution,
       and the local element in tensor itself. Therefore, the computing cost of bilateral is heavier, compared to other
       static kernels

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, k_shape, sigma_d, sigma_r, k_mode, k_cval, k_origin)


def prewitt(data: dual_ndarray, k_shape: tuple[int, ...],
            k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
            k_cval: Numeric = 0.0, k_origin: Union[int, Iterable[int]] = 0,
            prewitt_limen: Numeric = 0.9, sharp_alpha: Numeric = 1):
    """
    prewitt operations for tensor. each derivative operator is constructed with planes filled with -1 and 1 in start
    and end surface, respectively. for prewitt filter, gradient components of tensor were calculated for all axis
    then integrated through 2 norm. for prewitt detector, pixels with gray level upper more than threshold
    will be identified as edges. for prewitt sharpen, pixels around edge-like area will be augmented into the effect
    of higher contrast. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: the shape of averaging kernel; 3 for each dimension as default
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Union[int, Iterable[int]] k_origin: origin of anchor pixel in kernel; 0 as default
       :param Numeric prewitt_limen: (detector only) threshold for edge identification; values ranged from 0. to 1. for
                                     relative threshold using quantiles, otherwise the absolute one; 0.9 as default
       :param Numeric sharp_alpha: (sharpen only) intensity for increasing edge contrast; 1 as default
       :return: a numeric (filter, sharpen) or bool (detector) tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: prewitt detector, filter and sharpen for image
          :name: prewitt detector, filter and sharpen for image

          from info.me import tensorn as tsn
          from info.ins import datasets
          img = datasets.blackcurrant()

          # apply prewitt detector
          tsn.prewitt_detector(data=img)

          # apply prewitt filter
          tsn.prewitt_filter(data=img)

          # apply prewitt sharpen
          tsn.prewitt_sharpen(data=img)

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, k_shape, k_mode, k_cval, k_origin, prewitt_limen, sharp_alpha)


prewitt_filter = summary_sub(prewitt, 'prewitt filter to highlight edge of tensor')
prewitt_filter = tag_sub(prewitt_filter, 'filter')
prewitt_detector = summary_sub(prewitt, 'prewitt detector to determine edge of tensor')
prewitt_detector = tag_sub(prewitt_detector, 'detector')
prewitt_sharpen = summary_sub(prewitt, 'prewitt sharpen to get higher-contrast-edge tensor')
prewitt_sharpen = tag_sub(prewitt_sharpen, 'sharpen')


def sobel(data: dual_ndarray, k_shape: tuple[int, ...],
          k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
          k_cval: Numeric = 0.0, k_origin: Union[int, Iterable[int]] = 0,
          sobel_limen: Numeric = 0.9, sharp_alpha: Numeric = 1):
    r"""
    sobel operations for tensor. each derivative operator is constructed with planes distributed as :math:`-G`
    and :math:`G` in start and end surface respectively, where :math:`G` is 1-dimensional degenerated marginal
    distribution of Gaussian (see :ref:`marginal probability <Marginal probability>`). for sobel filter, gradient
    components of tensor were calculated for all axis then integrated through 2 norm. for sobel detector, pixels
    with gray level upper more than threshold will be identified as edges. for sobel sharpen, pixels around
    edge-like area will be augmented into the effect of higher contrast. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: the shape of averaging kernel; 3 for each dimension as default
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Union[int, Iterable[int]] k_origin: origin of anchor pixel in kernel; 0 as default
       :param Numeric sobel_limen: (detector only) threshold for edge identification; values ranged from 0. to 1. for
                                   relative threshold using quantiles, otherwise the absolute one; 0.9 as default
       :param Numeric sharp_alpha: (sharpen only) intensity for increasing edge contrast; 1 as default
       :return: a numeric (filter, sharpen) or bool (detector) tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: sobel detector, filter and sharpen for image
          :name: sobel detector, filter and sharpen for image

          from info.me import tensorn as tsn
          from info.ins import datasets
          img = datasets.blackcurrant()

          # apply sobel detector
          tsn.sobel_detector(data=img)

          # apply sobel filter
          tsn.sobel_filter(data=img)

          # apply sobel sharpen
          tsn.sobel_sharpen(data=img)

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, k_shape, k_mode, k_cval, k_origin, sobel_limen, sharp_alpha)


sobel_filter = summary_sub(sobel, 'sobel filter to highlight edge of tensor')
sobel_filter = tag_sub(sobel_filter, 'filter')
sobel_detector = summary_sub(sobel, 'sobel detector to determine edge of tensor')
sobel_detector = tag_sub(sobel_detector, 'detector')
sobel_sharpen = summary_sub(sobel, 'sobel sharpen to get higher-contrast-edge tensor')
sobel_sharpen = tag_sub(sobel_sharpen, 'sharpen')


def canny(data: dual_ndarray, k_shape: tuple[int, ...],
          k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
          k_cval: Numeric = 0.0, k_origin: Union[int, Iterable[int]] = 0,
          canny_limen: Numeric = 0.9, sharp_alpha: Numeric = 1):
    r"""
    canny operations for tensor. each derivative operator is constructed with planes distributed as :math:`-G`
    and :math:`G` in start and end surface respectively, where :math:`G` is 1-dimensional degenerated marginal
    distribution of Gaussian (see :ref:`marginal probability <Marginal probability>`). tensor will be preprocessed
    through kernel :math:`\mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})`. for canny filter, gradient components
    of tensor were calculated for all axis then integrated through 2 norm. for canny detector, pixels with gray level
    upper more than threshold will be identified as edges. for canny sharpen, pixels around edge-like area will be
    augmented into the effect of higher contrast. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: the shape of averaging kernel; 3 for each dimension as default
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Union[int, Iterable[int]] k_origin: origin of anchor pixel in kernel; 0 as default
       :param Numeric canny_limen: (detector only) threshold for edge identification; values ranged from 0. to 1. for
                                   relative threshold using quantiles, otherwise the absolute one; 0.9 as default
       :param Numeric sharp_alpha: (sharpen only) intensity for increasing edge contrast; 1 as default
       :return: a numeric (filter, sharpen) or bool (detector) tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: canny detector, filter and sharpen for image
          :name: canny detector, filter and sharpen for image

          from info.me import tensorn as tsn
          from info.ins import datasets
          img = datasets.blackcurrant()

          # apply canny detector
          tsn.canny_detector(data=img)

          # apply canny filter
          tsn.canny_filter(data=img)

          # apply canny sharpen
          tsn.canny_sharpen(data=img)

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, k_shape, k_mode, k_cval, k_origin, canny_limen, sharp_alpha)


canny_filter = summary_sub(canny, 'canny filter to highlight edge of tensor')
canny_filter = tag_sub(canny_filter, 'filter')
canny_detector = summary_sub(canny, 'canny detector to determine edge of tensor')
canny_detector = tag_sub(canny_detector, 'detector')
canny_sharpen = summary_sub(canny, 'canny sharpen to get higher-contrast-edge tensor')
canny_sharpen = tag_sub(canny_sharpen, 'sharpen')


def laplacian_of_gaussian(data: dual_ndarray, k_shape: tuple[int, ...],
                          k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
                          k_cval: Numeric = 0.0, k_origin: Union[int, Iterable[int]] = 0,
                          log_limen: Numeric = 0.9, sharp_alpha: Numeric = 1):
    r"""
    :ref:`LoG <LoG>` operations for tensor. kernel of :ref:`LoG <LoG>` is determined by :eq:`laplacian of gaussian in
    practice`. for LoG filter, :math:`C_1 > 0` then all weights in kernel will sum to 0, gradient components of tensor
    were calculated for all axis then integrated through 2 norm. for LoG detector, pixels with gray level upper more
    than threshold will be identified as edges. for LoG sharpen, :math:`C_1 < 0` and pixels around edge-like area
    will be augmented into the effect of higher contrast. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: the shape of averaging kernel; 3 for each dimension as default
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Union[int, Iterable[int]] k_origin: origin of anchor pixel in kernel; 0 as default
       :param Numeric log_limen: (detector only) threshold for edge identification; values ranged from 0. to 1. for
                                 relative threshold using quantiles, otherwise the absolute one; 0.9 as default
       :param Numeric sharp_alpha: (sharpen only) intensity for increasing edge contrast; 1 as default
       :return: a numeric (filter, sharpen) or bool (detector) tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: LoG detector, filter and sharpen for image
          :name: LoG detector, filter and sharpen for image

          from info.me import tensorn as tsn
          from info.ins import datasets
          img = datasets.blackcurrant()

          # apply LoG detector
          tsn.laplacian_of_gaussian_detector(data=img)

          # apply LoG filter
          tsn.laplacian_of_gaussian_filter(data=img)

          # apply LoG sharpen
          tsn.laplacian_of_gaussian_sharpen(data=img)

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, k_shape, k_mode, k_cval, k_origin, log_limen, sharp_alpha)


laplacian_of_gaussian_filter = summary_sub(laplacian_of_gaussian,
                                           'laplacian of gaussian filter to highlight edge of tensor')
laplacian_of_gaussian_filter = tag_sub(laplacian_of_gaussian_filter, 'filter')
laplacian_of_gaussian_detector = summary_sub(laplacian_of_gaussian,
                                             'laplacian of gaussian detector to determine edge of tensor')
laplacian_of_gaussian_detector = tag_sub(laplacian_of_gaussian_detector, 'detector')
laplacian_of_gaussian_sharpen = summary_sub(laplacian_of_gaussian,
                                            'laplacian of gaussian sharpen to get higher-contrast-edge tensor')
laplacian_of_gaussian_sharpen = tag_sub(laplacian_of_gaussian_sharpen, 'sharpen')


def difference_of_gaussian(data: dual_ndarray, sigma_ratio: Numeric, k_shape: tuple[int, ...],
                           k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
                           k_cval: float = 0.0, k_origin: Union[int, Iterable[int]] = 0, dog_limen: Numeric = 0.9,
                           sharp_alpha: Numeric = 1):
    r"""
    :ref:`DoG <DoG>` operations for tensor. two kernels are determined by :py:func:`~info.docfunc.gaussian_kernel`
    based on :eq:`multivariate Gaussian`. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param Numeric sigma_ratio: ratio of two scales of two kernels; 1.6 as default, suggested by Marr and Hildreth
                                   for balancing bandwidth and sensitivity :ref:`[Marr1980] <[Marr1980]>`
       :param tuple[int, ...] k_shape: the shape of averaging kernel; 3 for each dimension as default
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Union[int, Iterable[int]] k_origin: origin of anchor pixel in kernel; 0 as default
       :param Numeric dog_limen: (detector only) threshold for edge identification; values ranged from 0. to 1. for
                                 relative threshold using quantiles, otherwise the absolute one; 0.9 as default
       :param Numeric sharp_alpha: (sharpen only) intensity for increasing edge contrast; 1 as default
       :return: a numeric (filter, sharpen) or bool (detector) tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: DoG detector, filter and sharpen for image
          :name: DoG detector, filter and sharpen for image

          from info.me import tensorn as tsn
          from info.ins import datasets
          img = datasets.blackcurrant()

          # apply DoG detector
          tsn.difference_of_gaussian_detector(data=img)

          # apply DoG filter
          tsn.difference_of_gaussian_filter(data=img)

          # apply DoG sharpen
          tsn.difference_of_gaussian_sharpen(data=img)

    .. attribute:: Notes:

       For covariance :math:`\boldsymbol{\Sigma}` of multivariate gaussian distribution, its inverse
       :math:`\boldsymbol{\Sigma}^{-1}` is also symmetric. Therefore, the derivative of covariance matrix
       :math:`\boldsymbol{\Sigma}` in multivariate gaussian is:

       .. math::
          :label: derivative of covariance matrix in multivariate gaussian

          \begin{eqnarray}
          \frac{\partial f(\boldsymbol{x}|\boldsymbol{\mu},\boldsymbol{\Sigma})}{\partial \boldsymbol{\Sigma}} &=&
          \frac{[\boldsymbol{\Sigma}^{-1}(\boldsymbol{x}-\boldsymbol{\mu})(\boldsymbol{x}-\boldsymbol{\mu})^{T}
          \boldsymbol{\Sigma}^{-1} - \boldsymbol{\Sigma}^{-1}]}{2 \cdot (2\pi)^\frac{k}{2} \vert \boldsymbol{\Sigma}
          \vert^\frac{1}{2}} \exp{[-\frac{1}{2} (\boldsymbol{x} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1}
          (\boldsymbol{x} - \boldsymbol{\mu})]} \\ &=& \frac{[\boldsymbol{\Sigma}^{-1}(\boldsymbol{x}-\boldsymbol{\mu})
          (\boldsymbol{x}-\boldsymbol{\mu})^{T} \boldsymbol{\Sigma}^{-1} - \boldsymbol{\Sigma}^{-1}]}{2}
          f(\boldsymbol{x}|\boldsymbol{\mu},\boldsymbol{\Sigma})
          \end{eqnarray}

       Whose format is almost identical as :eq:`2nd order derivative of multivariate Gaussian`. That is, the
       :ref:`LoG <LoG>` can be approximated using gaussian filtered results with different scales.

    .. attribute:: See also:

       - :py:func:`~info.docfunc.gaussian_kernel`

       - :py:func:`~info.docfunc.laplacian_of_gaussian_kernel`

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, sigma_ratio, k_shape, k_mode, k_cval, k_origin, dog_limen, sharp_alpha)


difference_of_gaussian_filter = summary_sub(difference_of_gaussian,
                                            'difference of gaussian filter to highlight edge of tensor')
difference_of_gaussian_filter = tag_sub(difference_of_gaussian_filter, 'filter')
difference_of_gaussian_detector = summary_sub(difference_of_gaussian,
                                              'difference of gaussian detector to determine edge of tensor')
difference_of_gaussian_detector = tag_sub(difference_of_gaussian_detector, 'detector')
difference_of_gaussian_sharpen = summary_sub(difference_of_gaussian,
                                             'difference of gaussian sharpen to get higher-contrast-edge tensor')
difference_of_gaussian_sharpen = tag_sub(difference_of_gaussian_sharpen, 'sharpen')


def hessian(data: dual_ndarray, k_shape: tuple[int, ...],
            k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect', k_cval: Numeric = 0.0,
            in_spacing: Union[Numeric, Iterable[Numeric]] = None, hessian_limen: Numeric = 0.9,
            sharp_alpha: Numeric = 1):
    r"""
    :ref:`DoG <DoG>` operations for tensor. two kernels are determined by :py:func:`~info.docfunc.gaussian_kernel`
    based on :eq:`multivariate Gaussian`. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: the shape of averaging kernel; 3 for each dimension as default
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Union[Numeric, Iterable[Numeric]] in_spacing: pixel spacing to determine differential operator; if
                                                            numeric, operator uses equal spacing for all dimensions; if
                                                            iterable of numeric, operator applies spacing in accordance
                                                            with each numeric for each dimension; ``None`` as default
                                                            to generate 1 spacing for all dimensions
       :param Numeric hessian_limen: (detector only) threshold for edge identification; values ranged from 0. to 1. 0.9
                                     as default
       :param Numeric sharp_alpha: (sharpen only) intensity for increasing corner contrast; 1 as default
       :return: a numeric (determinant, curvature) or bool (detector) tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: hessian detector, filter and sharpen for image
          :name: hessian detector, filter and sharpen for image

          from info.me import tensorn as tsn
          from info.ins import datasets
          img = datasets.accent()

          # apply hessian detector
          tsn.hessian_detector(data=img)

          # apply hessian filter
          tsn.hessian_filter(data=img)

          # apply hessian sharpen
          tsn.hessian_sharpen(data=img)

    .. attribute:: Notes:

       The gaussian curvature of :math:`m`-dimensional tensor :math:`\textbf{I}` is defined as:

       .. math::
          :label: gaussian curvature

          \textbf{K} = \frac{\det{(\boldsymbol{H}(\textbf{I}))}}{(1+\sum_{i=1}^m \textbf{I}_{d_i}^2)^2}

       Where :math:`I_{d_i}` refers the 1st order differentiate of :math:`I`, in aspect of the :math:`i`-th dimension;
       :math:`\boldsymbol{H}(\textbf{I})` is hessian matrix:

       .. math::
          :label: hessian matrix

          \boldsymbol{H}(\textbf{I}) =
          \begin{bmatrix}
          \textbf{I}_{d_{1}d_{1}}  & \dots  & \textbf{I}_{d_{1}d_{m}} \\
          \vdots  & \ddots  & \vdots \\
          \textbf{I}_{d_{m}d_{1}} & \dots & \textbf{I}_{d_{m}d_{m}}
          \end{bmatrix}

       determinant and curvature responses the measure of the hessian matrix, and the gaussian curvature respectively.
       detector uses the limen based on numerical response of curvature.

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, k_shape, k_mode, k_cval, in_spacing, hessian_limen, sharp_alpha)


hessian_determinant_response = summary_sub(hessian, 'hessian determinant to highlight corner of tensor')
hessian_determinant_response = tag_sub(hessian_determinant_response, 'determinant')
hessian_curvature_response = summary_sub(hessian, 'hessian curvature to highlight corner of tensor')
hessian_curvature_response = tag_sub(hessian_curvature_response, 'curvature')
hessian_curvature_detector = summary_sub(hessian, 'hessian detector to determine corners of tensor')
hessian_curvature_detector = tag_sub(hessian_curvature_detector, 'detector')


def moravec_response(data: dual_ndarray, norm_order: int = 2,
                     k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
                     k_cval: Numeric = 0.0):
    r"""
    moravec response for tensor. approach using for edge and corner augment. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param int norm_order: norm order to determine how to aggregate differentials vector; ``2`` as default to use
                              Euclidean norm
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :return: the moravec response tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: moravec response on image
          :name: moravec response on image

          from info.me import tensorn as tsn
          from info.ins import datasets
          img = datasets.accent()

          tsn.moravec_response(data=img)

    .. attribute:: Notes:

       The moravec response can be summarized simply as:

       .. math::
          :label: moravec response

          \textbf{M} = f(\textbf{T}_{\boldsymbol{i}(\boldsymbol{j})} - \textbf{T}_\boldsymbol{j})

       Where :math:`\textbf{T}` and :math:`\textbf{M}` is the original tensor, and its moravec response respectively.
       :math:`\boldsymbol{j}` and :math:`\boldsymbol{i}(\boldsymbol{j})` are indices both in :math:`\mathbb{Z}^{m+}`,
       and :math:`\boldsymbol{i}(\boldsymbol{j})` is the function of :math:`\boldsymbol{j}` who satisfies
       (assume :math:`\boldsymbol{v} = \boldsymbol{i}(\boldsymbol{j}) - \boldsymbol{j}`) each element :math:`v_k` in
       :math:`\boldsymbol{v}` is in set :math:`\{0, 1\}`, and :math:`\sum_{k=1}^{m} v_k \neq 0`.

       As for each index :math:`\boldsymbol{j}`, the function mapping :math:`\boldsymbol{i}(\boldsymbol{j})` will
       expand :math:`\textbf{T}_{\boldsymbol{i}(\boldsymbol{j})}` one dimension plus, to contain the indices who
       satisfy the above-mentioned constraints. This results the container is in :math:`\mathbb{R}^{(m+1)}` who
       packages all differentials related to original pixels, the function :math:`f` needs to degenerate this
       expanded dimension, via aggregation approaches.

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, norm_order, k_mode, k_cval)


def harris_response(data: dual_ndarray, in_spacing: Union[Numeric, Iterable[Numeric]] = 1,
                    trace_coef: Numeric = 0.05, clip_window: Literal['binomial', 'continuous'] = 'binomial',
                    k_shape: tuple[int, ...] = None, k_cval: Numeric = 0.0,
                    k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect'):
    r"""
    harris curvature response for tensor. approach using for corner augment. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param Union[Numeric, Iterable[Numeric]] in_spacing: spacing for each dimension in the unit voxel; if
                                                            no-iterable numeric object, this value will be applied on
                                                            all dimensions. 1 as default, to calculate in pixel spacing
       :param Numeric trace_coef: coefficient of trace in harris response; range from 0.04 to 0.06 is suggested; 0.05
                                  as default
       :param Literal['binomial', 'continuous'] clip_window: window function for harris kernel; ``'binomial'`` applies
                                                             a rescaled binary gaussian kernel, and ``'continuous'``
                                                             applies a gaussian kernel; ``'binomial'`` as default
       :param tuple[int, ...] k_shape: tuple for kernel shape; ``None`` as default to apply 3 in all dimensions
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :return: the harris curvature response tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: harris response on image
          :name: harris response on image

          from info.me import tensorn as tsn
          from info.ins import datasets
          img = datasets.accent()

          tsn.harris_response(data=img)

    .. attribute:: Nots:

       For harris response, it can be defined as:

       .. math::
          :label: harris response

          \textbf{H}(\boldsymbol{i}) = \sum_{\boldsymbol{j}} w(\boldsymbol{j}) [\textbf{T}(\boldsymbol{i} +
          \boldsymbol{j}) - \textbf{T}(\boldsymbol{i})]^2

       Where :math:`\textbf{T}` and :math:`\textbf{M}` is the original tensor, and its moravec response respectively.
       :math:`\boldsymbol{i}` is the index in :math:`\textbf{T}`, and :math:`\boldsymbol{j}` is the index in harris
       kernel. :math:`w(\boldsymbol{j})` is the clip window for computing weight of kernel. if it uses binary
       option, all values in kernel will be :math:`\{0, a\}` where the sum of :math:`a` is positions of
       :math:`m`-dimensional ellipse determined by kernel shape, and the sum of kernel will be 1; if continuous
       option is selected, weight uses general gaussian distribution.

       Using 1st order Taylor expansion as approximation, each pixel of :math:`\textbf{T}` will be expanded in
       two extra dimensions (cornerness matrix) as:

       .. math::
          :label: cornerness matrix in harris

          \boldsymbol{M} = \sum_{j} w(\boldsymbol{j})
          \begin{bmatrix}
          \textbf{T}_{d_{1}}^2  & \cdots  & \textbf{T}_{d_1} \textbf{T}_{d_m} \\
          \vdots  & \ddots  & \vdots \\
          \textbf{T}_{d_m}\textbf{T}_{d_1} & \cdots & \textbf{T}_{d_{m}}^2
          \end{bmatrix}

       Where :math:`T_{d_i}` refers the 1st order differentiate of :math:`\textbf{T}`, in aspect of the
       :math:`i`-th dimension. In practice, cornerness is implemented using
       :math:`C = \det{\boldsymbol{M}} - k (\mathrm{Tr}(\boldsymbol{M}))^2`, where :math:`k` is the hyperparameter
       had effect on cornerness computing, the determinant and trace of :math:`\boldsymbol{M}` can be obtained
       through its singular values.

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, in_spacing, trace_coef, clip_window, k_shape, k_cval, k_mode)


def usan_response(data: dual_ndarray, k_shape: tuple[int, ...] = None, k_cval: Numeric = 0.0,
                  k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
                  clip_window: Literal['binomial', 'continuous'] = 'binomial'):
    r"""
    usan response for tensor. approach using for edge and corner augment. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: the shape of averaging kernel; 3 for each dimension as default
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Literal['binomial', 'continuous'] clip_window: window function for harris kernel; ``'binomial'`` applies
                                                             a rescaled binary gaussian kernel, and ``'continuous'``
                                                             applies 3rd moment of gaussian kernel; ``'binomial'`` as
                                                             default
       :return: the usan response tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: usan and susan response on image
          :name: usan and susan response on image

          from info.me import tensorn as tsn
          from info.ins import datasets
          img = datasets.accent()

          usan = tsn.usan_response(data=img)
          susan = (40 - usan).clip(0, None)  # use 40 as susan threshold

    .. attribute:: Notes:

       usan response generates a series of kernels, to obtain differentials from :math:`m`-dimensional ellipse
       determined by shape, related to the center of the kernel. By determining the threshold :math:`g`, the
       function mapping :math:`\min(0, g-\mathrm{usan\_response}(\textbf{T}))` will be the corresponding susan
       response (see :ref:`Smith1997 <[Smith1997]>`).

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, k_shape, k_cval, k_mode, clip_window)


def segment_response(data: dual_ndarray, k_shape: tuple[int, ...] = None, k_cval: Numeric = 0,
                     k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
                     segment_threshold: Numeric = 0.6):
    r"""
    segment test response for tensor. approach using for edge and corner augment. available for numpy and cupy
    ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: the shape of averaging kernel; 3 for each dimension as default
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Numeric segment_threshold: threshold, to reject pixels whose differential is lower than that value in
                                         any orthogonal direction; if it ranges in :math:`(0, 1)`, the quantile will
                                         be used; 0.6 as default
       :return: the segment test response tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: segment test response on image
          :name: segment test response on image

          from info.me import tensorn as tsn
          from info.ins import datasets
          img = datasets.accent()

          tsn.segment_response(data=img)

    .. attribute:: Notes:

       Kernel of segment test uses :math:`m`-dimensional ellipsoidal shell, instead of :math:`m`-dimensional ellipse.
       Pixels whose differential in any orthogonal direction is lower than the threshold will be rejected, then the
       accepted pixels will be subdivided into positive and negative classes. Absolute sum mapping is applied on the
       two classes, then the final response of pixel is determined by the maximum of the two sums.

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, k_shape, k_cval, k_mode, segment_threshold)


def fast_response(data: dual_ndarray, k_shape: tuple[int, ...] = None, k_cval: Numeric = 0,
                  k_mode: Literal['reflect', 'constant', 'nearest', 'mirror', 'wrap'] = 'reflect',
                  fast_reject_thresholds: Union[Numeric, tuple[Numeric, Numeric]] = (0.4, 0.6),
                  fast_classifier: Callable = None):
    r"""
    fast response for tensor. approach using for edge and corner augment. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the input tensor
       :param tuple[int, ...] k_shape: the shape of averaging kernel; 3 for each dimension as default
       :param Literal k_mode: method of edge filling; valid options are ``'reflect'``, ``'constant'``, ``'nearest'``,
                              ``'mirror'``, and ``'wrap'``; ``'reflect'`` as default
       :param Numeric k_cval: filling number when ``k_mode`` is ``'constant'``; 0.0 as default
       :param Union[float, tuple[Numeric, Numeric]] fast_reject_thresholds: thresholds of ``(a, b)`` to
                                                                            make :math:`\mathbb{R}^1` into
                                                                            division :math:`(-\infty, a] \cup (a, b]
                                                                            \cup (b,+\infty)`, as the scopes for
                                                                            differentials lower than, similar as, and
                                                                            greater than the kernel center
                                                                            respectively; if single float :math:`t`,
                                                                            it must range from 0 to 0.5, for quantiles
                                                                            of ``(t, 1-t)``; if ``a`` and ``b``
                                                                            both range from 0 to 1, quantiles are
                                                                            calculated automatically; else uses the
                                                                            numeric themselves; ``(0.4, 0.6)`` as
                                                                            default
       :param Optional[Callable] fast_classifier: callable object to transfer vector container for differentials to
                                                  numeric; ``None`` as default to not apply
       :return: the fast response tensor
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: fast response on image
          :name: fast response on image

          from info.me import tensorn as tsn
          from info.ins import datasets
          img = datasets.accent()

          tsn.fast_response(data=img)

    .. attribute:: Notes:

       Kernel of segment test uses :math:`m`-dimensional ellipsoidal shell, instead of :math:`m`-dimensional ellipse.
       Pixels whose differentials will be subdivided into three classes: similar as, lower, and greater than, through
       two pre-defined thresholds. Two sums are calculated in last two types, then final response is determined by
       the maximum of the two sums.

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, k_shape, k_cval, k_mode, fast_reject_thresholds, fast_classifier)


def prober(data: dual_ndarray, prob_nums: int, prob_radius: Numeric, in_spacing: tuple[Numeric, ...] = None):
    """
    sub segmentation generator from a bool ndarray. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the bool ndarray segmentation
       :param int prob_nums: number of generated sub segmentations
       :param Numeric prob_radius: radius for each generated sub segmentations
       :param Optional[tuple[Numeric, ...]] in_spacing: voxel spacing for all dimensions; if assigned, ``prob_radius``
                                                        will be re-calculated, to adapt voxel space; ``None`` as
                                                        default to use pixel space
       :return: generator composed of sub segmentations with specified radius
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data``, ``prob_nums`` or ``prob_radius`` are not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: generate 15 sub segmentations from a meta segmentations
          :name: generate 15 sub segmentations from a meta segmentations

          from info.me import tensorb as tsb
          for seg in tsb.prober(data=meta_segmentation, prob_nums=15, prob_radius=5):
              print(seg.sum())

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       .. versionchanged:: 0.0.4

          support ``in_spacing`` argument for sampling in voxel space.

       -- |signature|
    """
    args_highlighter(data, prob_nums, prob_radius, in_spacing)


def grid_mesh(data: dual_ndarray, grid_nums: Union[int, list[int]] = 7):
    """
    divides a data-containing region into uniform grid cells and yields data-containing subregions.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the bool ndarray segmentation
       :param Union[int, list[int]] grid_nums: number of grid divisions per dimension; if integer, applies to all
                                               dimensions; ``7`` as default
       :return: generator composed of sub segmentations
       :rtype: Union[numpy.ndarray, cupy.ndarray]

    .. attribute:: Examples:

       .. code-block:: python
          :caption: mesh sub segmentations
          :name: mesh sub segmentations

          import numpy as np
          from info.me import tensorb as tsb

          msk = np.zeros((100, 100))
          msk[20:80, 30:90] = 1
          for seg in tsb.grid_mesh(data=msk.astype(bool), grid_nums=3):
              print(seg.sum())

    .. attribute:: Notes:

       this function is suited for:

       - smart padding: automatically computes minimal bounding box with symmetric padding for uniform partitioning

       - view generation: uses memory views for zero-copy operations and efficient memory usage

       - data filtering: automatically skips grid cells without valid data

       - dimension adaptability: Supports arrays of arbitrary dimensions (2D/3D/etc.)

       - coordinate preservation: output arrays maintain identical shape to input for easy coordinate transformation

       typical use cases:

       - chunked processing of medical imaging data

       - distributed computation with sparse matrices

       - local rendering optimization for volumetric data

       - block-wise feature extraction in machine learning

    .. attribute:: Logs:

       .. versionadded:: 1.0

       -- |signature|
    """
    args_highlighter(data, grid_nums)


def connected_domain(data: dual_ndarray, detector: dual_ndarray):
    """
    connected domain generator from a bool or an integer ndarray. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: bool ndarray segmentation, or int ndarray using different
                                                       integers for connected domains
       :param Union[numpy.ndarray, cupy.ndarray] detector: structure to determine connected domain; ``None`` as default
                                                           to use orthogonal connection in each dimension
       :return: generator composed of connected domains as segmentations
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: generate connected domains from a meta segmentation
          :name: generate connected domains from a meta segmentation

          from info.me import tensorb as tsb
          from info.ins import datasets
          for msk in tsb.connected_domain(data=datasets.segs()):
              print(msk.sum())

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, detector)


def seg_resize(data: dual_ndarray, new_size: tuple[int],
               interp_method: Literal['linear', 'nearest', 'nearest-up', 'zero', 'slinear', 'quadratic', 'cubic',
               'previous', 'next'] = 'linear'):
    """
    resizing data into specific shape. spline interpolation supported. algorithm is implemented through canonical
    decomposition :ref:`[Battaglino2018] <[Battaglino2018]>`. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: data to be resized
       :param tuple[int] new_size: tuple to determine new size for input data
       :param Literal[...] interp_method: interpolation method links to ``kind`` argument of ``interp1d``; options are
                                          ``'linear'``, ``'nearest'``, ``'nearest-up'``, ``'zero'``, ``'slinear'``,
                                          ``'quadratic'``, ``'cubic'``, ``'previous'``, and ``'next'``; ``'linear'``
                                          as default
       :return: re-sized data
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: if ``data`` or ``new_size`` was not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: resize a meta segmentation
          :name: resize a meta segmentation

          from info.me import tensorb as tsb
          from info.ins import datasets

          new_seg = tsb.resize(data=datasets.segs(), new_size=(70, 80))

    .. attribute:: See also:

        - `Interpolation <https://scipy.github.io/devdocs/tutorial/interpolate/1D.html>`_

        - `Tensor decomposition and synthesis <http://tensorly.org/stable/user_guide/tensor_decomposition.html>`_

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, new_size, interp_method)


def erosion(data: dual_ndarray, norm: Union[Numeric, Iterable[Numeric]], in_spacing: Iterable[Numeric]):
    """
    morphological erosion operation for boolean tensor. can be applied in pixel or voxel space. available for numpy
    and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the bool ndarray segmentation
       :param Union[Numeric, Iterable[Numeric]] norm: criterion to be eroded; 2nd order norm for orthogonal components
                                                      in each dimension if numeric; or a sequence of numeric,
                                                      customized in each dimension; ``1`` as default
       :param Iterable[Numeric] in_spacing: spacing for each dimension in the unit voxel; ``None`` as default for pixel
                                            spacing
       :return: eroded segmentation
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: if ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: erosion for segmentations
          :name: erosion for segmentations

          from info.me import tensorb as tsb
          from info.ins import datasets
          segs = datasets.segs()

          # erosion in pixel space
          seg1 = tsb.erosion(data=segs)

          # erosion in voxel space
          seg2 = tsb.erosion(data=segs, in_spacing=(1.1, 3))

          # customized erosion in voxel space
          seg3 = tsb.erosion(data=segs, norm=(3.3, 6), in_spacing=(1.1, 3))

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, norm, in_spacing)


def dilation(data: dual_ndarray, norm: Union[Numeric, Iterable[Numeric]], in_spacing: Iterable[Numeric]):
    """
    morphological dilation operation for boolean tensor. can be applied in pixel or voxel space. available for numpy
    and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the bool ndarray segmentation
       :param Union[Numeric, Iterable[Numeric]] norm: criterion to be eroded; 2nd order norm for orthogonal components
                                                      in each dimension if numeric; or a sequence of numeric,
                                                      customized in each dimension; ``1`` as default
       :param Iterable[Numeric] in_spacing: spacing for each dimension in the unit voxel; ``None`` as default for pixel
                                            spacing
       :return: eroded segmentation
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: if ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: dilation for segmentations
          :name: dilation for segmentations

          from info.me import tensorb as tsb
          from info.ins import datasets
          segs = datasets.segs()

          # dilation in pixel space
          seg1 = tsb.dilation(data=segs)

          # dilation in voxel space
          seg2 = tsb.dilation(data=segs, in_spacing=(1.1, 3))

          # customized dilation in voxel space
          seg3 = tsb.dilation(data=segs, norm=(3.3, 6), in_spacing=(1.1, 3))

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, norm, in_spacing)


def intersection(data: dual_ndarray, instances: Union[dual_ndarray, list[dual_ndarray]]):
    """
    intersection operation for boolean tensor. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the bool ndarray segmentation
       :param Union[ndarray, list[ndarray]] instances: the intersection of ``data`` and ``instances`` segmentations
       :return: intersection segmentation
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: if ``data`` and ``instances`` are not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: calculate intersection of segmentations
          :name: calculate intersection of segmentations

          from info.me import tensorb as tsb
          seg, other_segs = ...  # ndarray, list of boolean ndarray

          intersection_seg = tsb.intersection(data=seg, instances=other_segs)

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, instances)


def union(data: dual_ndarray, instances: Union[dual_ndarray, list[dual_ndarray]]):
    """
    union operation for boolean tensor. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the bool ndarray segmentation
       :param Union[ndarray, list[ndarray]] instances: the union of ``data`` and ``instances`` segmentations
       :return: union segmentation
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: if ``data`` and ``instances`` are not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: calculate union of segmentations
          :name: calculate union of segmentations

          from info.me import tensorb as tsb
          seg, other_segs = ...  # ndarray, list of boolean ndarray

          union_seg = tsb.union(data=seg, instances=other_segs)

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, instances)


def difference(data: dual_ndarray, instances: Union[dual_ndarray, list[dual_ndarray]]):
    """
    difference operation for boolean tensor. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the bool ndarray segmentation
       :param Union[ndarray, list[ndarray]] instances: the difference of ``data`` and ``instances`` segmentations
       :return: difference segmentation
       :rtype: Union[numpy.ndarray, cupy.ndarray]
       :raises TypeError: if ``data`` and ``instances`` are not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: calculate difference of segmentations
          :name: calculate difference of segmentations

          from info.me import tensorb as tsb
          seg, other_segs = ...  # ndarray, list of boolean ndarray

          difference_seg = tsb.difference(data=seg, instances=other_segs)

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, instances)


def watershed(data: dual_ndarray, flood_seeds: dual_ndarray, flood_geography: dual_ndarray = None,
              label_output: bool = True):
    """
    watershed algorithm for labeling segmentation. available for numpy and cupy ndarray.

    .. attribute:: Arguments:

       :param Union[numpy.ndarray, cupy.ndarray] data: the bool ndarray segmentation
       :param Union[numpy.ndarray, cupy.ndarray] flood_seeds: initial positions for flooding; must be label object with
                                                              integers to mark each individual segmentation
       :param Union[numpy.ndarray, cupy.ndarray] flood_geography: geography for flooding; ``None`` as default will
                                                                  calculate through basic segmentation
       :param bool label_output: trigger to determine whether return label-like result; if ``True``, a label-like
                                 ndarray will be obtained, otherwise a generator of bool ndarray for each label;
                                 ``True`` as default
       :return: ndarray of labels as ``flood_seeds``, or generator of bool ndarray for each label
       :rtype: Union[numpy.ndarray, cupy.ndarray, Generator]
       :raises TypeError: if ``data`` and ``flood_seeds`` are not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: watershed for segmentations
          :name: watershed for segmentations

          from info.me import tensorb as tsb
          import numpy as np

          msk = np.zeros((512, 512))
          y, x = np.ogrid[0:512, 0:512]
          centers = np.array([(200, 100), (350, 400), (260, 200)])
          m1, m2, m3 = [(y - c[0]) ** 2 + (x - c[1]) ** 2 < 30 ** 2 for c in centers]
          msk[m1 + m2 + m3] = 1
          seeds = np.zeros_like(msk)
          _ = [seeds.__setitem__(tuple(c), idx+1) for idx, c in enumerate(centers)]
          msk = msk.astype(bool)

          res = tsb.watershed(data=msk, flood_seeds=seeds)

    .. attribute:: Notes:

       Numpy implementation for topological watershed algorithm suggested by
       :ref:`Beucher, S. and & Meyer, F. <[Beucher2018]>`.

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, flood_seeds, flood_geography, label_output)


def leaf_folders(data: str, file_system: Literal['desktop', 'hdfs'] = 'desktop'):
    """
    search leaf folders recursively from a root folder.

    .. attribute:: Arguments:

       :param str data: path-like string of root folder
       :param Literal['desktop', 'hdfs'] file_system: file system mode; ``'desktop'`` for desktop file system and
                                                      ``'hdfs'`` for distributed file system; ``'desktop'`` as default
       :return: a generator for paths of leaf folders from root folder
       :rtype: Generator
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: list all leaf folders from root
          :name: list all leaf folders from root

          # for file folder tree as:
          # --- root
          #  |--- folder1
          #  | | --- file1
          #  | | --- file2
          #  |--- folder2
          #    | --- file3
          #    | --- sub_folder
          #       | --- file4
          #       | --- file5

          from info.me import io
          for leaf_folder in io.leaf_folders(data=root):
              print(leaf_folder)

          # expected output:
          # root/folder1
          # root/folder2/sub_folder

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       .. versionchanged:: 0.0.4

          support search in distributed file system

       -- |signature|
    """
    args_highlighter(data, file_system)


def search_from_root(data: str, search_condition: Callable[[str], bool] = lambda x: x,
                     file_system: Literal['desktop', 'hdfs'] = 'desktop'):
    """
    search (specific) files recursively from root folder.

    .. attribute:: Arguments:

       :param str data: path-like string of root folder
       :param Callable[[str], bool] search_condition: function to determine selected files; ``lambda x: x`` as default
       :param Literal['desktop', 'hdfs'] file_system: file system mode; ``'desktop'`` for desktop file system and
                                                      ``'hdfs'`` for distributed file system; ``'desktop'`` as default
       :return: a generator for selected files from root folder
       :rtype: Generator
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: list all python scripts from root
          :name: list all python scripts from root

          from info.me import io
          for script in io.search_from_root(data='.', search_condition=lambda x: x[-2:] == 'py'):
              print(script)

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       .. versionchanged:: 0.0.4

          support search in distributed file system

       -- |signature|
    """
    args_highlighter(data, search_condition, file_system)


def generic_filter(data: Iterable[str], filter_pattern: str = None, apply_map: Callable[[str], Any] = None):
    """
    filter a sequence of str using regex pattern. return a generator for a sequence composed of filtered str, or
    mapped object from those str.

    .. attribute:: Arguments:

       :param Iterable[str] data: a str sequence
       :param str filter_pattern: regular pattern for filter; ``r'.*'`` as default
       :param Callable[[str], Any] apply_map: mapping function for filtered str as input; ``None`` as default
       :return: a generator of filtered str, or mapped object from those str
       :rtype: Generator
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: filtering and mapping for names
          :name: filtering and mapping for names

          from info.me import io
          names = ['Kane', 'Elfin', 'Kyle', 'Elena', 'Dark', 'Kate', 'David', 'Ezra', 'Deborah']

          for init_with_E in io.generic_filter(data=names, filter_pattern=r'^E'):
              print(init_with_E)

          for len_of_init_with_E in io.generic_filter(data=names, filter_pattern=r'^E', get_map=lambda x: len(x)):
              print(len_of_init_with_E)

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, filter_pattern, apply_map)


def files_regroup(data: Iterable[str], regroup_labels: list[str] = None):
    """
    regroup a str sequence based on a list of patterns. regular expression supported.

    .. attribute:: Arguments:

       :param Iterable[str] data: a str sequence
       :param list[str] regroup_labels: a regular expression list; ``[r'.*']`` as default
       :return: a dict with patterns as keywords, and elements matched those patterns as their respective values
       :rtype: dict[str, Sequence[str]]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: regroup names by initial
          :name: regroup names by initial

          from info.me import io
          names = ['Kane', 'Elfin', 'Kyle', 'Elena', 'Dark', 'Kate', 'David', 'Ezra', 'Deborah']

          for k, v in io.files_regroup(data=names, regroup_labels=[r'^K', r'^D', r'^E']).items():
              print(k, v)

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, regroup_labels)


def dict_filter(data: dict[str, Iterable[str]], match_pattern: str = r'.*', using_map: Callable[[str], Any] = None):
    """
    filter values of dict using regex pattern. return a dict composed of elements which matches pattern, or mapped
    objects from that elements as values.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: a dict composed of keywords and str sequence values
       :param str match_pattern: regular pattern for filter; ``r'.*'`` as default
       :param Callable[[str], Any] using_map: mapping function for matched str as input; ``None`` as default
       :return: dict composed of elements which matches pattern, or mapped objects from that elements as values
       :rtype: dict[str, Iterable[Any]]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: select female names and calculate name length
          :name: select female names and calculate name length

          from info.me import io

          names = ['Kane_F', 'Elfin_M', 'Kyle_M', 'Elena_M', 'Dark_F', 'Kate_F', 'David_M', 'Ezra_F', 'Deborah_F']
          name_group = io.files_regroup(data=names, regroup_labels=[r'^K', r'^D', r'^E'])

          for k, v in io.dict_filter(data=name_group, match_pattern=r'F$').items():
              print(k, v)

          for k, v in io.dict_filter(data=name_group, match_pattern=r"F$", using_map=lambda x: len(x)-2).items():
              print(k, v)

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       -- |signature|
    """
    args_highlighter(data, match_pattern, using_map)


def unarchive(data: Union[str, list[str]]):
    """
    toolkit to load python persistence object(s).

    .. attribute:: Arguments:

       :param Union[str, list[str]] data: archived file with `pyp.gz` or 'pyp' suffix, or list of archived files with
                                          `pyp` suffix
       :var Optional[int] ~compress_algorithm: compression method code; 0 for ``STORED``; 8 for ``DEFLATED``; 12 for
                                               ``BZIP2``; and 14 for ``LZMA``; 8 as default
       :var Optional[int] ~compress_level: int of 0 (``DEFLATED``), 1 to 9 (``DEFLATED`` and ``BZIP2``) are accepted;
                                           5 as default
       :return: NoReturn
       :rtype: NoneType

    .. attribute:: Examples:

       .. code-block:: python
          :caption: load persistent python objects
          :name: load persistent python objects

          from info.me import unarchive
          names = ['case1.pyp', 'case2.pyp', ..., 'casen.pyp']

          case2 = unarchive(data=names[1])  # load 'case2.pyp'

          for f in unarchive(data=names):  # or load all cases one by one
              print(f)

          for f in unarchive(data='compress.pyp.gz'):  # or load from a 'pyp.gz' compressed file, if existed
              print(f)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data)


def DcmSetConstructor(data: Iterable[str], loader: Literal['SimpleITK', 'pydicom'] = 'SimpleITK',
                      series_k: str = "0020|000e", instance_k: str = "0008|0018",
                      image_orientation_k: str = "0020|0037", pixel_spacing_k: str = "0028|0030",
                      image_position_k: str = "0020|0032", spacing_between_slices_k: str = "0018|0088"):
    """
    load and re-organize a set of dicom slices in memory.

    .. attribute:: Arguments:

       :param Iterable[str] data: Iterable object composed of paths of dicom slices
       :param Literal['SimpleITK', 'pydicom'] loader: library as load engine; ``'SimpleITK'`` as default
       :param str series_k: keyword or tag for determining the same set of dicom slices; ``"0020|000e"`` as default
       :param str instance_k: keyword or tag for determining the individual dicom slice instance; ``"0008|0018"`` as
                              default
       :param str image_orientation_k: keyword or tag of Image Orientation (Patient); ``"0020|0037"`` as default
       :param str pixel_spacing_k: keyword or tag of Pixel Spacing; ``"0028|0030"`` as default
       :param str image_position_k: keyword or tag of Image Position (Patient); ``"0020|0032"`` as default
       :param str spacing_between_slices_k: keyword or tag of Spacing Between Slices; ``"0018|0088"`` as default
       :var int ~stacking_axis: index of stacking axis; 2 as default
       :var bool ~verbosity: trigger for prompting message during data loading; ``False`` as default
       :var Callable[[str], ...] ~user_defined_io: customized loader to transfer string of file path, to object in
                                                   memory; ``None`` as default to use ``pydicom`` or ``SimpleITK``
                                                   automatically
       :return: a DcmSetConstructor instance
       :rtype: DcmSetConstructor

    .. attribute:: Property:

       .. property:: files:

          list of original dicom slice paths.

       .. property:: files_set:

          nested lists of re-organized dicom slice paths. paths attributed to the identical series were gathered into
          the same inner list.

       .. property:: loader:

          engine for loading and meta information. SimpleITK and pydicom are supported.

       .. property:: headers:

          header files using data loading engine mapped from ``files`` attribute.

       .. property:: dcm_set:

          nested lists of re-organized header files. header files attributed to the identical series were gathered
          into the same inner list.

       .. property:: series_k:

          keyword or tag for determining the same set of dicom slices. fetched from ``settings`` attribute.

       .. property:: instance_k:

          keyword or tag for determining the individual dicom slice instance. fetched from ``settings`` attribute.

       .. property:: settings:

          default settings for re-organizing.

       .. property:: stacking_axis:

          index for stacking axis. determined by internal parameter ``~stacking_axis``.

    .. attribute:: Examples:

       .. code-block::
          :caption: re-organizing dicom slices
          :name: re-organizing dicom slices

          from info.med import rebuild as dcm
          dcm_slices = ['./data/Image0_0.dcm', './data/Image0_1.dcm', ..., './data/Image0_154.dcm',
                        './data/Image1_0.dcm', './data/Image1_1.dcm',  ..., './data/Image1_154.dcm']  # two dicom sets

          res = dcm.DcmSetConstructor(data=dcm_slices)
          print(res.dcm_set)  # [[dicom_set_of_image0], [dicom_set_of_image1]]

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       .. versionchanged:: 0.0.4

          support customized file loader via built-in argument ``~user_defined_io``, to enable dicom construction in
          distributed file system.

       -- |signature|
    """
    args_highlighter(data, loader, series_k, instance_k, image_orientation_k, pixel_spacing_k, image_position_k,
                     spacing_between_slices_k)


def DcmSeries(data: Iterable[str], loader: Literal['SimpleITK', 'pydicom'] = 'SimpleITK',
              series_k: str = "0020|000e", instance_k: str = "0008|0018", image_orientation_k: str = "0020|0037",
              pixel_spacing_k: str = "0028|0030", image_position_k: str = "0020|0032",
              spacing_between_slices_k: str = "0018|0088", axis_order: str = "zyx", template_meta: object = None):
    r"""
    build 3D image from a dicom series.

    .. attribute:: Arguments:

       :param Iterable[str] data: Iterable object composed of paths of dicom slices
       :param Literal['SimpleITK', 'pydicom'] loader: library as load engine; ``'SimpleITK'`` as default
       :param str series_k: keyword or tag for determining the same set of dicom slices; ``"0020|000e"`` as default
       :param str instance_k: keyword or tag for determining the individual dicom slice instance; ``"0008|0018"`` as
                              default
       :param str image_orientation_k: keyword or tag of Image Orientation (Patient); ``"0020|0037"`` as default
       :param str pixel_spacing_k: keyword or tag of Pixel Spacing; ``"0028|0030"`` as default
       :param str image_position_k: keyword or tag of Image Position (Patient); ``"0020|0032"`` as default
       :param str spacing_between_slices_k: keyword or tag of Spacing Between Slices; ``"0018|0088"`` as default
       :param str axis_order: combination of ``'x'``, ``'y'`` and ``'z'`` to specify axis order; ``'zyx'`` as default
       :param object template_meta: get a meta information template; ``None`` for default
       :var bool ~is_sorted: trigger to escape sort step; ``True`` as default
       :var int ~stacking_axis: index of stacking axis; 2 as default
       :var bool ~verbosity: trigger for prompting message during data loading; ``False`` as default
       :return: a DcmSeries instance
       :rtype: DcmSeries

    .. attribute:: Property:

       .. property:: metas:

          dict composed of header information for a set of dicom file series.

       .. property:: affine:

          a :math:`\mathbb{R}^{4 \times 4}` ndarray of affine matrix. affine describe the transformation
          from pixel to voxel space (see
          `affine matrix <https://dicom.innolitics.com/ciods/ct-image/image-plane/00200037>`_).

       .. property:: rcs_spacing:

          a :math:`\mathbb{R}^3` ndarray of voxel spacing in order of ``_intrinsic_order`` attribute.

       .. property:: rcs_origin:

          a :math:`\mathbb{R}^3` ndarray of original location in order of ``_intrinsic_order`` attribute.

       .. property:: rcs_coordinates:

          tuple composed of ndarray as coordinate in order of ``_intrinsic_order`` attribute.

       .. property:: rcs_array:

          3-dimensional ndarray of image.

       .. property:: rcs_suv:

          3-dimensional ndarray of standard uptake values built from image. applied exclusively in positron emission
          tomography (:ref:`PET <[Wiyaporn2011]>`) modality.

       .. property:: affine_matrix:

          the same as ``affine``.

       .. property:: _intrinsic_order:

          a certain combination of ``(0, 1, 2)``, determined by parameter ``axis_order``. for example, the default
          ``axis_order`` used ``'zyx'`` will result in intrinsic order of ``(2, 1, 0)``.

       .. property:: struct:

          acquired attribute after linkage to struct file via ``link_struct``.

       .. property:: dose:

          acquired attribute after linkage to dose file via ``link_dose``.

       .. property:: plan:

          acquired attribute after linkage to plan file via ``link_plan``.

    .. attribute:: Methods:

       .. method:: link_struct:

          link object to current dicom series.

          :var str data: path-like string for struct file
          :var list[str] roi_name_k: attribute keywords to visit roi names; ``['StructureSetROISequence', 'ROIName']``
                                     as default
          :var list[str] roi_number_k: attribute keywords to visit roi numbers; ``['StructureSetROISequence',
                                       'ROINumber']`` as default
          :var list[str] contour_sequence_k: attribute keywords to visit contour sequence; ``['ROIContourSequence',
                                             'ContourSequence']`` as default
          :var list[str] referenced_roi_number_k: attribute keywords to visit referenced roi numbers;
                                                  ``['ROIContourSequence', 'ReferencedROINumber']`` as default
          :var Callable[[list[str]], list[ndarray]] roi_name_map: callable object to map roi from name to ndarray;
                                                                  a ``SingleMap`` instance generated through previous
                                                                  arguments as default

          .. code-block:: python
             :caption: link to struct file
             :name: link to struct file

             from info.med import rebuild as dcm
             dcm_slices = ['./data/Image0_0.dcm', './data/Image0_1.dcm', ..., './data/Image0_154.dcm']
             dcm_struct = './data/Image0_struct.dcm'
             img = dcm.dcm_constructor(data=dcm_slices)[0]  # one set only
             img.link_struct(data=dcm_struct)

       .. method:: roi_name_map:

          acquired method after linking to struct file via ``link_struct``. obtain the :ref:`ROI <ROI>` ndarray from
          names.

          :var list[str] data: names for desired rois

          .. code-block:: python
             :caption: load rois after struct linkage
             :name: load rois after struct linkage

             for roi in img.roi_name_map(['Spinal', 'Liver', 'Lung']):
                 print(roi.shape)

       .. method:: link_dose:

          link object to current dicom dose.

          :var str data: path-like string for dose file
          :var Union[str, list[str]] grid_frame_offset_vector_k: attribute keywords to visit grid frame offset vector;
                                                                 ``"3004|000c"`` as default
          :var Union[str, list[str]] dose_grid_scaling_k: attribute keywords to visit dose grid scaling; ``"3004|000e"``
                                                          as default
          :var Literal['cp', 'tucker'] decomp_method: decomposition method when applying
                                                      :py:func:`~info.docfunc.resize` for resampling; ``'cp'`` or
                                                      ``'tucker'`` is available; ``'tucker'`` as default
          :var Literal[...] interp_method: interpolation method when applying :py:func:`~info.docfunc.resize`;
                                           options are ``'linear'``, ``'nearest'``, ``'nearest-up'``, ``'zero'``,
                                           ``'slinear'``, ``'quadratic'``, ``'cubic'``, ``'previous'``, and ``'next'``;
                                           ``'linear'`` as default
          :var int linspace_nums: number of points to be generated for dose volume histogram; 100 as default
          :var Callable[[Union[list[str], dict[str, ndarray]]], list[ndarray, ndarray]] dvh_name_map: callable object
                                                                                                      to map roi from
                                                                                                      name to dose
                                                                                                      volume histogram
                                                                                                      points in (x, y)
                                                                                                      pairs; before
                                                                                                      which the
                                                                                                      ``link_struct``
                                                                                                      method must be
                                                                                                      activated; a
                                                                                                      ``SingleMap``
                                                                                                      instance generated
                                                                                                      through previous
                                                                                                      argument as
                                                                                                      default

          .. code-block:: python
             :caption: link to dose file
             :name: link to dose file

             from info.med import rebuild as dcm
             dcm_slices = ['./data/Image0_0.dcm', './data/Image0_1.dcm', ..., './data/Image0_154.dcm']
             dcm_struct = './data/Image0_struct.dcm'
             dcm_dose = './data/Image0_dose.dcm'
             img = dcm.dcm_constructor(data=dcm_slices)[0]  # one set only
             img.link_struct(data=dcm_struct)
             img.link_dose(data=dcm_dose)

       .. method:: rcs_dose:

          acquired attribute to obtain the dose ndarray calibrated via original image

       .. method:: dvh_name_map:

          acquired method after linking to dose file via ``link_dose``. obtain the :ref:`DVH <DVH>` ndarray from
          names.

          :var list[str] data: names for desired rois

          .. code-block:: python
             :caption: load points after struct and dose linkage
             :name: load points after struct and dose linkage

             from info.vis import visualization as vis
             from info.basic.functions import dvh_res_to_vis

             roi_names = ['CTV', 'Spinal', 'Eye']
             dvh = img.dvh_name_map(data=roi_names)
             vis.Canvas.play(data=dvh_res_to_vis(dvh),
                             fig_configs=vis.FigConfigs.Line.update(name=roi_names, symbol=None,
                                                                    pen=[_ for _ in 'rgb']),
                             cvs_legend=True, cvs_left_label='Volume (%)', cvs_bottom_label='Dose (Gy)',
                             cvs_title='Dose Volume Histogram (DVH)')

          the corresponding dose volume histogram plot using :py:class:`~info.docfunc.Canvas` to visualize
          will be like:

          .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/9a7d4292-f97b-4733-9878-65036e62b2e4
             :name: dose volume histogram plot
             :width: 450
             :align: center

             dose volume histogram plot

       .. method:: link_plan:

          |und dev|

    .. attribute:: Examples:

       .. code-block:: python
          :caption: rebuild re-organized dicom slices
          :name: rebuild re-organized dicom slices

          from info.med import rebuild as dcm
          dcm_slices = ['./data/Image0_0.dcm', './data/Image0_1.dcm', ..., './data/Image0_154.dcm',
                        './data/Image1_0.dcm', './data/Image1_1.dcm',  ..., './data/Image1_154.dcm']  # two dicom sets

          res = dcm.DcmSetConstructor(data=dcm_slices)  # [[dicom_set_of_image0], [dicom_set_of_image1]]
          for image_set in res.dcm_set:
              dcm.DcmSeries(data=image_set)

    .. attribute:: See also:

       - :py:class:`~info.docfunc.SingleMap`

       - :py:func:`~info.docfunc.dcm_constructor`

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       .. versionchanged:: 0.0.3

          support linkage to struct file, acquired attribute and ``roi_name_map`` method after linkage.

       -- |signature|
    """
    args_highlighter(data, loader, series_k, instance_k, image_orientation_k, pixel_spacing_k, image_position_k,
                     spacing_between_slices_k, axis_order, template_meta)


def dcm_constructor(data: Iterable[str], loader: Literal['SimpleITK', 'pydicom'] = 'SimpleITK',
                    series_k: str = "0020|000e", instance_k: str = "0008|0018", image_orientation_k: str = "0020|0037",
                    pixel_spacing_k: str = "0028|0030", image_position_k: str = "0020|0032",
                    spacing_between_slices_k: str = "0018|0088", axis_order: str = "zyx"):
    """
    rebuild dicom image(s) from a set of dicom slice files.

    .. attribute:: Arguments:

       :param Iterable[str] data: Iterable object composed of paths of dicom slices
       :param Literal['SimpleITK', 'pydicom'] loader: library as load engine; ``'SimpleITK'`` as default
       :param str series_k: keyword or tag for determining the same set of dicom slices; ``"0020|000e"`` as default
       :param str instance_k: keyword or tag for determining the individual dicom slice instance; ``"0008|0018"`` as
                              default
       :param str image_orientation_k: keyword or tag of Image Orientation (Patient); ``"0020|0037"`` as default
       :param str pixel_spacing_k: keyword or tag of Pixel Spacing; ``"0028|0030"`` as default
       :param str image_position_k: keyword or tag of Image Position (Patient); ``"0020|0032"`` as default
       :param str spacing_between_slices_k: keyword or tag of Spacing Between Slices; ``"0018|0088"`` as default
       :param str axis_order: combination of ``'x'``, ``'y'`` and ``'z'`` to specify axis order; ``'zyx'`` as default
       :var bool ~use_template_meta: whether save a template meta via ``pydicom`` for each ``DcmSeries``; ``True`` will
                                     use headers in the first slice as example meta; ``False`` as default
       :var Callable[[str], ...] ~user_defined_io: customized loader to transfer string of file path, to object in
                                                   memory; ``None`` as default to use ``pydicom`` or ``SimpleITK``
                                                   automatically
       :return: a list composed of DcmSeries instance
       :rtype: list[DcmSeries]
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       .. code-block:: python
          :caption: dicom image rebuilding pipeline
          :name: dicom image rebuilding pipeline

          from info.med import rebuild as dcm
          dcm_slices = ['./data/Image0_0.dcm', './data/Image0_1.dcm', ..., './data/Image0_154.dcm',
                        './data/Image1_0.dcm', './data/Image1_1.dcm',  ..., './data/Image1_154.dcm']  # two dicom sets

          # use default SimpleITK loader
          imgs = dcm.dcm_constructor(data=dcm_slices)

          # or use pydicom loader
          imgs = dcm.dcm_constructor(data=dcm_slices, **dcm.pydicom_config)

          for img in imgs:
              print(img.metas)

    .. attribute:: See also:

       - :py:class:`~info.docfunc.DcmSetConstructor`

       - :py:class:`~info.docfunc.DcmSeries`

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       .. versionchanged:: 0.0.4

          support customized file loader via built-in argument ``~user_defined_io``, to enable dicom construction in
          distributed file system.

       -- |signature|
    """
    args_highlighter(data, loader, series_k, instance_k, image_orientation_k, pixel_spacing_k, image_position_k,
                     spacing_between_slices_k, axis_order)


def dcm_regroup(data: Generator, regroup_reference: list[str], loader: Literal['SimpleITK', 'pydicom'] = 'SimpleITK',
                rearrange: bool = True, dump_as: str = '_regroup_refs'):
    """
    generate a cache for logging regrouped dicom files.

    .. attribute:: Arguments:

       :param Generator data: generator for dicom files to be integrated
       :param list[str] regroup_reference: list of tags using for regrouping; tag from first to last refers the
                                           hierarchical structure from root to leaf in regrouped reference
       :param Literal['SimpleITK', 'pydicom'] loader: loader engine for dicom files; ``'SimpleITK'`` or ``'pydicom'``
                                                      is acceptable; ``'SimpleTIK'`` as default
       :param bool rearrange: whether rearrange dicom files with pre-defined ``loader`` engine; if ``False``, regrouped
                              dicom-like files will be rearranged by file names in a simple list, otherwise in a nested
                              list composed of file names rearranged by their stacking axis locations, defined
                              intrinsically in the data loading engine; ``True`` as default
       :param str dump_as: file name for saving regroup file reference; ``'_regroup_refs'`` as default to generate a
                           ``_regroup_refs.pyp`` file in work directory
       :var bool ~verbosity: trigger for prompting message during data processing and loading; ``False`` as default
       :var Callable[[str], ...] ~user_defined_io: customized loader to transfer string of file path, to object in
                                                   memory; ``None`` as default to use ``pydicom`` or ``SimpleITK``
                                                   automatically
       :return: dict composed of basic settings of regrouping, and regroup files reference
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: regroup dicom files
          :name: regroup dicom files

          from info.med import rebuild as dcm
          from info.me import io

          gen = io.search_from_root(data=r"path/to/dicom/folder", search_condition=lambda x: x[-3:] == 'dcm')

          res = dcm.dcm_regroup(data=gen, regroup_reference=["0020|000e"])
          res['regroup_result']
          # {'uid_1': [[dicom_series_1, ...]],
          #  'uid_2': [[dicom_series_2, ...]],
          #  ...
          #  'uid_n': [[dicom_series_n, ...]]}

          res = dcm.dcm_regroup(data=gen, regroup_reference=["0010|0010"])
          res['regroup_result']
          # {'patient_1': [[dicom_series_1, ...]],
          #  'patient_2': [[dicom_series_2, ...]],
          #  ...
          #  'patient_n': [[dicom_series_n, ...]]}

          res = dcm.dcm_regroup(data=gen, regroup_reference=["0010|0010", "0020|000e"])
          res['regroup_result']
          # {'patient_1': {'uid_1': [[dicom_series_1, ...]], ..., 'uid_m1': [[dicom_series_m1, ...]]},
          #  'patient_2': {'uid_1': [[dicom_series_1, ...]], ..., 'uid_m2': [[dicom_series_m2, ...]]},
          #  ...
          #  'patient_n': {'uid_1': [[dicom_series_1, ...]], ..., 'uid_mn': [[dicom_series_mn, ...]]}}

    .. attribute:: Notes:

       When ``rearrange`` is ``True``, this function will call :py:func:`~info.docfunc.DcmSetConstructor` using
       ``loader`` as data loading engine. In this condition, arguments can be passed into
       :py:func:`~info.docfunc.DcmSetConstructor` (like the ``~verbosity`` does).

    .. attribute:: See also:

       - :py:func:`~info.docfunc.DcmSetConstructor`

    .. attribute:: Logs:

       .. versionadded:: 0.0.4

       -- |signature|
    """
    args_highlighter(data, regroup_reference, loader, rearrange, dump_as)


def dcm_hierarchical_parser(data: Union[str, Any]):
    """
    parse keywords in dicom headers recursively.

    .. attribute:: Arguments:

       :param Union[str, Any] data: path-like str, the return from :py:func:`~info.docfunc.dcm_attr_loader`, or
                                    ``Sequence`` instance from ``pydicom``
       :return: the parsed structure of keywords
       :rtype: str

    .. attribute:: Examples:

       .. code-block:: python
          :caption: parse the structure of keywords in dicom
          :name: parse the structure of keywords in dicom

          from info.me.rebuild import dcm_hierarchical_parser, dcm_attr_loader
          file = "path/to/dcm/file.dcm"

          dcm_hierarchical_parser(data=file)  # parse from a dicom file
          # |--- AccessionNumber
          # |--- BitsAllocated
          # ...
          # |--- ReferencedRTPlanSequence
          # | |--- ReferencedFractionGroupSequence
          # | | |--- ReferencedFractionGroupNumber
          # | |--- ReferencedSOPClassUID
          # | |--- ReferencedSOPInstanceUID
          # |--- ReferringPhysicianName
          # ...
          # |--- StudyTime

          plan_seq = dcm_attr_loader(data=file, attr_path="ReferencedRTPlanSequence")
          dcm_hierarchical_parser(data=plan_seq)  # or parse from a dicom sequence
          # |--- ReferencedFractionGroupSequence
          # | |--- ReferencedFractionGroupNumber
          # |--- ReferencedSOPClassUID
          # |--- ReferencedSOPInstanceUID

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data)


def dcm_attr_loader(data: Union[str, object], attr_path: Union[str, list[str]]):
    """
    generic attribute loader for dicom file. with attribute keyword, or list of keywords describing the hierarchical
    relationship, corresponding values can be obtained.

    .. attribute:: Arguments:

       :param Union[str, object] data: path-like string for dicom file, or pydicom ``DataFileset`` object
       :param Union[str, list[str]] attr_path: str for attribute, list of keywords for attribute path, or tuple of path
                                               list for multiple attributes reading
       :return: values in dicom headers
       :rtype: object
       :raises TypeError: ``data`` is not assigned properly

    .. attribute:: Examples:

       Load attributes starting from a dicom file:

       .. code-block:: python
          :caption: dicom attribute loading pipeline from file
          :name: dicom attribute loading pipeline from file

          from info.med import rebuild as dcm
          file = "/path/to/dicom/file.dcm"

          # get referenced SOP instance UID via str assignment:
          uid = dcm.dcm_attr_loader(data=file, attr_path='ReferencedSOPInstanceUID')

          # get referenced fraction group number inside structured sequence, via list of keywords assignment:
          _path = ['ReferencedRTPlanSequence', 'ReferencedFractionGroupSequence', 'ReferencedFractionGroupNumber']
          group_num = dcm.dcm_attr_loader(data=file, attr_path=_path)

          # get multiple attributes, via tuple composed of keyword paths
          _paths = (['ReferencedSOPInstanceUID'],
                    ['ReferencedRTPlanSequence', 'ReferencedFractionGroupSequence', 'ReferencedFractionGroupNumber'])
          uid, group_num = dcm.dcm_attr_loader(data=file, attr_path=_paths)

       Or load attributes, from the return of :py:func:`~info.docfunc.dcm_attr_loader` self. This property is
       expected to be used in the circumstance of existing complicated parallel structure in parent attributes.

       .. code-block:: python
          :caption: dicom attribute loading pipeline from self return
          :name: dicom attribute loading pipeline from self return

          _path_parent = ['ReferencedRTPlanSequence', 'ReferencedFractionGroupSequence']  # paralleled sequences here
          _path_sub = ['ReferencedFractionGroupNumber']

          for sequence in dcm.dcm_attr_loader(data=file, attr_path=_path_parent):
              group_num = dcm.dcm_attr_loader(data=sequence, attr_path=_path_sub)

    .. attribute:: Notes:

       ``pydicom`` styled attribute path is supported exclusively, due to its stable capability to parse header.

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, attr_path)


def NIfTI(data: str, preprocess_meta: Callable[[str, str], Union[str, Numeric, list[Numeric]]],
          axis_order: Literal['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx'] = 'zyx'):
    r"""
    build 3D image from a NIfTI file.

    .. attribute:: Arguments:

       :param str data: path of *nii* or *nii.gz* NIfTI file
       :param Optional[Callable[[str, str], Any]] preprocess_meta: callable object to preprocess header information,
                                                  should be capable to convert keyword and value pairs, into
                                                  accessible data type in Python; default uses a built-in function
       :param str axis_order: combination of ``'x'``, ``'y'`` and ``'z'`` to specify axis order; ``'zyx'`` as default
       :return: NIfTI image
       :rtype: NIfTI

    .. attribute:: Property:

       .. property:: metas:

          dict composed of header information for NIfTI image.

       .. property:: affine:

          a :math:`\mathbb{R}^{4 \times 4}` ndarray of affine matrix. affine describe the transformation
          from pixel to a relative, or absolute voxel space (see
          `NIfTI-1 Data Format <https://nifti.nimh.nih.gov/nifti-1/>`_).

       .. property:: rcs_spacing:

          a :math:`\mathbb{R}^3` ndarray of voxel spacing in order of ``_intrinsic_order`` attribute.

       .. property:: rcs_origin:

          a :math:`\mathbb{R}^3` ndarray of original location in order of ``_intrinsic_order`` attribute.

       .. property:: rcs_coordinates:

          tuple composed of ndarray as coordinate in order of ``_intrinsic_order`` attribute.

       .. property:: rcs_array:

          3-dimensional ndarray of image.

       .. property:: rcs_suv:

          3-dimensional ndarray of standard uptake values built from image. applied exclusively in positron emission
          tomography (:ref:`PET <[Wiyaporn2011]>`) modality.

       .. property:: affine_matrix:

          the same as ``affine``.

       .. property:: _intrinsic_order:

          a certain combination of ``(0, 1, 2)``, determined by parameter ``axis_order``. for example, the default
          ``axis_order`` used ``'zyx'`` will result in intrinsic order of ``(2, 1, 0)``.

    .. attribute:: Examples:

       .. code-block:: python
          :caption: rebuild a NIfTI image
          :name: rebuild a NIfTI image

          from info.med import rebuild as nii
          nii_file = './data/image.nii'
          img = nii.NIfTI(data=nii_file)
          print(img.rcs_array.shape, img.rcs_spacing, img.rcs_origin)

    .. attribute:: See also:

       - :py:class:`~info.docfunc.SingleMap`

       - :py:func:`~info.docfunc.dcm_constructor`

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(data, preprocess_meta, axis_order)


def nii_constructor(data: str, preprocess_meta: Callable[[str, str], Union[str, Numeric, list[Numeric]]],
                    axis_order: Literal['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx'] = 'zyx'):
    """
    build 3D image(s) from NIfTI file(s).

    .. attribute:: Arguments:

       :param Union[str, list[str]] data: path, or list of paths of *nii* or *nii.gz* NIfTI file
       :param Optional[Callable[[str, str], Any]] preprocess_meta: callable object to preprocess header information,
                                                  should be capable to convert keyword and value pairs, into
                                                  accessible data type in Python; default uses a built-in function
       :param str axis_order: combination of ``'x'``, ``'y'`` and ``'z'`` to specify axis order; ``'zyx'`` as default
       :var Callable[[str], ...] ~user_defined_io: customized loader to transfer string of file path, to object in
                                                   memory; ``None`` as default to use ``SimpleITK`` automatically
       :return: NIfTI image(s)
       :rtype: Union[NIfTI, list[NIfTI]]

    .. attribute:: Examples:

       .. code-block:: python
          :caption: rebuild NIfTI images
          :name: rebuild NIfTI images

          from info.med import rebuild as nii
          nii_files = ['./data/image0.nii', './data/image1.nii', ..., './data/image100.nii']

          img_12 = nii.nii_constructor(data=nii_files[1:3])  # if not too much images
          imgs = (nii.nii_constructor(data=_) for _ in nii_files)  # or mapping for all via generator

    .. attribute:: See also:

       - :py:class:`~info.docfunc.NIfTI`

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(data, preprocess_meta, axis_order)


def ImageViewer(gui_size: tuple[int, int] = (1000, 1000)):
    """
    interactive viewer for 3D image.

    .. attribute:: Arguments:

       :param tuple[int, int] gui_size: size for main window of application; ``(1000, 1000)`` as default
       :return: an ImageViewer instance
       :rtype: ImageViewer

    .. attribute:: Methods:

       .. method:: view:

          view 3D image.

          :var ndarray data: 3-dimensional ndarray
          :var Optional[list[ndarray]] mask: list of bool ndarray with 3 dimension; ``None`` as default for no mask
          :var Iterable[Numeric] spacing: iterable object with length of 3 to specify spacing values;
                                          ``(1, 1, 1)`` as default
          :var Iterable[Numeric] origin: iterable object with length of 3 to specify origin values; ``(0, 0, 0)`` as
                                         default
          :var Optional[str] img_title: title to be displayed in main window; ``None`` as default
          :var tuple[Numeric, Numeric] levels: initial low and high values of grey level; values should be numeric;
                                               if those values range from 0. to 1. simultaneously, grey level
                                               percentage will be applied; ``(0.688, 0.997)`` as default
          :var Optional[list[tuple[Numeric, ...]]] palettes: RGB shader colors if ``mask`` was assigned; value ranges
                                                             from 0.0 to 1.0 in each channel; ``None`` as default
                                                             for random colors; if specified, substitution for
                                                             mask shaders takes places sequentially

       .. method:: play:

          static method; create a new ImageViewer then view 3D image. all parameters defined the same as those
          when calling ``view``.

    .. attribute:: Examples:

       .. code-block:: python
          :caption: interactively view 3D image
          :name: interactively view 3D image

          from info.vis import ImageViewer
          img, spacing, origin = ...  # ndarray, len(spacing) == 3, len(origin) == 3

          # simple 3D image viewer:
          ImageViewer.play(data=img)

          # 3D image viewer with spacing:
          ImageViewer.play(data=img, spacing=spacing)

          # 3D image viewer with spacing and origin
          ImageViewer.play(data=img, spacing=spacing, origin=origin)

       Following :ref:`figure <image viewer for 3D image>` for preview:

       .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/f2b027f9-a04b-4244-808f-a25ee012f567
          :name: image viewer for 3D image
          :width: 700
          :align: center

          ImageViewer for 3D image

       Or if the images have the corresponding segmentations:

       .. code-block:: python
          :caption: interactively view 3D image with segmentation
          :name: interactively view 3D image with segmentation

          segs = ...  # list of bool ndarray

          # 3D image viewer with image and segmentations:
          ImageViewer.play(data=img, spacing=spacing, origin=origin, mask=[segs])

       .. figure:: https://github.com/users/CubicZebra/projects/6/assets/34041412/947bbcc3-365e-433b-9985-7173b685d9e4
          :name: image viewer for 3D image with segmentation
          :width: 700
          :align: center

          ImageViewer for 3D image with segmentation

    .. attribute:: Logs:

       .. versionadded:: 0.0.2

       .. versionchanged:: 0.0.4

          Implementation uses linked views, instead of projection with sliced segmentation line. Support origin,
          colored segmentations, and 3D visualization with OpenGL rendering.

       .. versionchanged:: 0.0.5

          No limitation for mask numbers during visualization (3 in maximum the former); fix the exception raised
          in sequential playing.

       -- |signature|
    """
    args_highlighter(gui_size)


def hypoi_f(data: dict[str, np_ndarray]):
    """
    perform :ref:`one-way ANOVA test <one-way ANOVA test>` among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :return: F statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: one-way ANOVA on multi groups
          :name: one-way ANOVA on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_f(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data)


def hypoi_t(data: dict[str, np_ndarray], equal_var: bool = False, trim: float = 0., permutations: Union[int] = None,
            random_state: int = None, nan_policy: Literal['propagate', 'raise', 'omit'] = 'propagate',
            alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided'):
    r"""
    perform :ref:`pair-wise independent T test <Student's T test>` among multi-grouped data. statistic uses
    :eq:`statistic_t1`.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param bool equal_var: tigger to determine whether groups under comparison are of the identical variance;
                              ``False`` as default
       :param float trim: fraction to trim data from two-tails (:ref:`Yuen's T test <[Yuen1974]>`); valid value ranges
                          from 0.0 to 0.5; 0.0 as default
       :param Optional[int] permutations: :math:`\mathbb{N}`, number of permutations used for calculating numerical
                                          solution for :math:`p`-value; 0 or ``None`` for analytical solution using `t`
                                          distribution without permutations; ``None`` as default
       :param Optional[int] random_state: random state in Monte Carlo; effective when ``permutations`` is activated;
                                          ``None`` as default
       :param Literal['propagate', 'raise', 'omit'] nan_policy: strategy for null value-contained in data;
                                                                ``'propagate'`` return ``nan``; ``'raise'`` will throw
                                                                exception; ``'omit'`` will ignore null values;
                                                                ``'propagate'`` as default
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :return: t statistics and :math:`p`-values on pair-wised groups
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: independent t test on multi groups
          :name: independent t test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_t(data=data)

    .. attribute:: See also:

       - :py:func:`~info.docfunc.hypoj_t`

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, equal_var, trim, permutations, random_state, nan_policy, alternative)


def hypoj_t(data: dict[str, np_ndarray], nan_policy: Literal['propagate', 'raise', 'omit'] = 'propagate',
            alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided'):
    r"""
    perform :ref:`pair-wise related T test <Student's T test>` among multi-grouped data. statistic uses
    :eq:`statistic_t4`.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['propagate', 'raise', 'omit'] nan_policy: strategy for null value-contained in data;
                                                                ``'propagate'`` return ``nan``; ``'raise'`` will throw
                                                                exception; ``'omit'`` will ignore null values;
                                                                ``'propagate'`` as default
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :var bool ~full_return: if ``True``, degree of freedom will be returned as extra information as well; ``False``
                               as default
       :return: t statistics and :math:`p`-values on pair-wised groups
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: related t test on multi groups
          :name: related t test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoj_t(data=data)

    .. attribute:: See also:

       - :py:func:`~info.docfunc.hypoi_t`

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, nan_policy, alternative)


def hypoi_sw(data: dict[str, np_ndarray]):
    """
    perform :ref:`Shapiro-Wilk test <Shapiro-Wilk test>` on each group among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :return: shapiro statistic and :math:`p`-value via Monte Carlo simulation
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Shapiro-Wilk test on multi groups
          :name: Shapiro-Wilk test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_sw(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data)


def hypoi_normality(data: dict[str, np_ndarray], nan_policy: Literal['propagate', 'raise', 'omit'] = 'omit'):
    """
    perform :ref:`Omnibus Normality test <Omnibus Normality test>` on each group among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['propagate', 'raise', 'omit'] nan_policy: strategy for null value-contained in data;
                                                                ``'propagate'`` return ``nan``; ``'raise'`` will throw
                                                                exception; ``'omit'`` will ignore null values;
                                                                ``'omit'`` as default
       :return: statistic and :math:`p`-value on each group
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: omnibus test for normality on multi groups
          :name: omnibus test for normality on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_normality(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, nan_policy)


def hypoi_ks(data: dict[str, np_ndarray], dist: Union[_dist, list[_dist]] = gs(loc=0, scale=1),
             alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided',
             method: Literal['exact', 'approx', 'asymp', 'auto'] = 'auto', n_sample: int = 20):
    """
    perform :ref:`Kolmogorov-Smirnov test <Kolmogorov-Smirnov test>` among multi-grouped data. calculating on
    each group, as well as on pair-wised groups.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Union[dist, list[dist]] dist: distribution pre-defined as criterion (or criteria); ``rv_frozen`` object,
                                            or list of those objects in ``scipy``; the standard uni-variate gaussian
                                            ``scipy.stats.norm(loc=0, scale=1)`` as default
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :param Literal['exact', 'asymp', 'auto'] method: the method to calculate :math:`p`-value; ``'exact'`` uses exact
                                                        distribution of distribution(s); ``'asymp'`` uses asymptotic
                                                        distribution(s); ``'auto'`` uses one of the above options;
                                                        ``'auto'`` as default
       :param int n_sample: number of samples generated from pre-defined distribution(s); 20 as default
       :return: statistic and :math:`p`-value on each group, and pair-wised groups
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Kolmogorov-Smirnov test on multi groups
          :name: Kolmogorov-Smirnov test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_ks(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, dist, alternative, method, n_sample)


def hypoi_cvm(data: dict[str, np_ndarray], dist: Union[_dist, list[_dist]] = gs(loc=0, scale=1),
              method: Literal['exact', 'asymptotic', 'auto'] = 'auto'):
    """
    perform :ref:`Cramér-von Mises test <Cramér-von Mises test>` among multi-grouped data. calculating on
    each group, as well as on pair-wised groups.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Union[dist, list[dist]] dist: distribution pre-defined as criterion (or criteria); ``rv_frozen`` object,
                                            or list of those objects in ``scipy``; the standard uni-variate gaussian
                                            ``scipy.stats.norm(loc=0, scale=1)`` as default
       :param Literal['exact', 'asymp', 'auto'] method: the method to calculate :math:`p`-value; ``'exact'`` uses
                                                        exact distribution of distribution(s); ``'asymp'`` uses
                                                        asymptotic distribution(s); ``'auto'`` uses one of the above
                                                        options; ``'auto'`` as default
       :return: statistic and :math:`p`-value on each group, and pair-wised groups
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Cramér-von Mises test on multi groups
          :name: Cramér-von Mises test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_cvm(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, dist, method)


def hypoi_ag(data: dict[str, np_ndarray], nan_policy: Literal['propagate', 'raise', 'omit'] = 'propagate'):
    """
    perform :ref:`Alexander Govern test <Alexander Govern test>` among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['propagate', 'raise', 'omit'] nan_policy: strategy for null value-contained in data;
                                                                ``'propagate'`` return ``nan``; ``'raise'`` will throw
                                                                exception; ``'omit'`` will ignore null values;
                                                                ``'propagate'`` as default
       :return: statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Alexander Govern test on multi groups
          :name: Alexander Govern test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_ag(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, nan_policy)


def hypoi_thsd(data: dict[str, np_ndarray]):
    """
    perform :ref:`Tukey's range test <Tukey's range test>` among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :var bool ~full_return: if ``True``, low and high of confidence interval will be returned as extra information
                               as well; ``False`` as default
       :return: statistic and :math:`p`-value on pair-wised groups
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Tukey's range test on multi groups
          :name: Tukey's range test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_thsd(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data)


def hypoi_kw(data: dict[str, np_ndarray], nan_policy: Literal['propagate', 'raise', 'omit'] = 'propagate'):
    """
    perform :ref:`Kruskal-Wallis H-test <Kruskal-Wallis H-test>` among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['propagate', 'raise', 'omit'] nan_policy: strategy for null value-contained in data;
                                                                ``'propagate'`` return ``nan``; ``'raise'`` will throw
                                                                exception; ``'omit'`` will ignore null values;
                                                                ``'propagate'`` as default
       :return: statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Kruskal-Wallis H-test on multi groups
          :name: Kruskal-Wallis H-test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_kw(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, nan_policy)


def hypoi_mood(data: dict[str, np_ndarray], ties: Literal['below', 'above', 'ignore'] = 'below',
               power_lambda: float = 1., nan_policy: Literal['propagate', 'raise', 'omit'] = 'propagate',
               alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided'):
    """
    perform :ref:`Mood's median and scale test <Mood's test>` among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['below', 'above', 'ignore'] ties: determines how values equal to the grand median are classified;
                                                        ``'below'`` and ``'above'`` counts for below and above
                                                        respectively; ``'ignore'`` will not count; ``'below'`` as
                                                        default
       :param float power_lambda: number used for power divergence; 1.0 as default for Pearson's chi-squared statistic
       :param Literal['propagate', 'raise', 'omit'] nan_policy: strategy for null value-contained in data;
                                                                ``'propagate'`` return ``nan``; ``'raise'`` will throw
                                                                exception; ``'omit'`` will ignore null values;
                                                                ``'propagate'`` as default
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :var bool ~full_return: if ``True``, median and contingency table will be returned as extra information from
                               median test as well; ``False`` as default
       :return: statistics and :math:`p`-values for median and scale tests
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Mood's median and scale test on multi groups
          :name: Mood's median and scale test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_mood(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, ties, power_lambda, nan_policy, alternative)


def hypoi_bartlett(data: dict[str, np_ndarray]):
    """
    perform :ref:`Bartlett's test <Bartlett's test>` among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :return: statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Bartlett's test on multi groups
          :name: Bartlett's test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_bartlett(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data)


def hypoi_levene(data: dict[str, np_ndarray], center: Literal['mean', 'median', 'trimmed'] = 'median',
                 proportiontocut: float = 0.05):
    """
    perform :ref:`Levene test <Levene test>` among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['mean', 'median', 'trimmed'] center: the referenced center to determine absolute distance for
                                                           each observation; ``'mean'`` uses mean; ``'median'`` uses
                                                           median; ``'trimmed'`` uses the mean calculate from trimmed
                                                           data; ``'median'`` as default
       :param float proportiontocut: fraction from leftmost and rightmost to be trimmed; effective when ``center`` is
                                     ``'trimmed'``; valid value ranges from 0.0 to 0.5; 0.05 as default
       :return: statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Levene test on multi groups
          :name: Levene test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_levene(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, center, proportiontocut)


def hypoi_fk(data: dict[str, np_ndarray], center: Literal['mean', 'median', 'trimmed'] = 'median',
             proportiontocut: float = 0.05):
    """
    perform :ref:`Fligner-Killeen test <Fligner-Killeen test>` among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['mean', 'median', 'trimmed'] center: the referenced center to determine absolute distance for
                                                           each observation; ``'mean'`` uses mean; ``'median'`` uses
                                                           median; ``'trimmed'`` uses the mean calculate from trimmed
                                                           data; ``'median'`` as default
       :param float proportiontocut: fraction from leftmost and rightmost to be trimmed; effective when ``center`` is
                                     ``'trimmed'``; valid value ranges from 0.0 to 0.5; 0.05 as default
       :return: statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Fligner-Killeen test on multi groups
          :name: Fligner-Killeen test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_fk(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, center, proportiontocut)


def hypoi_ad(data: dict[str, np_ndarray], midrank: bool = True):
    """
    perform :ref:`Anderson-Darling test <Anderson-Darling test>` among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param bool midrank: type of Anderson-Darling test; ``True`` for to continuous and discrete distributions;
                            ``False`` for right side empirical distribution; ``True`` as default
       :var bool ~full_return: if ``True``, critical values in different significance levels will be returned as
                               extra information; ``False`` as default
       :return: statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Anderson-Darling test on multi groups
          :name: Anderson-Darling test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_ad(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, midrank)


def hypoi_rank(data: dict[str, np_ndarray], alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided'):
    """
    perform :ref:`rank sum test <Wilcoxon rank test>` among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :return: statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Rank sum test on multi groups
          :name: Rank sum test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_rank(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, alternative)


def hypoj_rank(data: dict[str, np_ndarray], zero_method: Literal['wilcox', 'pratt', 'zsplit'] = 'wilcox',
               correction: bool = False, alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided',
               method: Literal['exact', 'approx', 'auto'] = 'auto'):
    """
    perform :ref:`single-rank test <Wilcoxon rank test>` among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['wilcox', 'pratt', 'zsplit'] zero_method: method for counting the pairs with equal value;
                                                                ``'wilcox'`` ignore that cases; ``'pratt'`` only
                                                                include that cases in ranking process; ``'zsplit'``
                                                                include that cases in ranking process and split
                                                                half-half to positive and negative counts; ``'wilcox'``
                                                                as default
       :param bool correction: Whether apply continuity correction to adjust rank statistic if normal approximation
                               used; ``False`` as default
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :param Literal['exact', 'approx', 'auto'] method: the method to calculate :math:`p`-value; ``'exact'`` uses
                                                         exact distribution of distribution(s); ``'approx'`` uses
                                                         approximate distribution(s); ``'auto'`` uses one of the above
                                                         options; ``'auto'`` as default
       :var bool ~full_return: if ``True``, the :math:`Z` statistic will be returned; ``False`` as default
       :return: statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Single rank test on multi groups
          :name: Single rank test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoj_rank(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, zero_method, correction, alternative, method)


def hypoi_es(data: dict[str, np_ndarray], es_t: tuple[float, float] = (0.4, 0.8)):
    """
    perform :ref:`Epps-Singleton test <Epps-Singleton test>` on each possible pairs among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param tuple[float, float] es_t: where the characteristic function to be evaluated; ``(0.4, 0.8)`` as default
       :return: statistic and :math:`p`-value on each group
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Epps-Singleton on multi groups
          :name: Epps-Singleton on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_es(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, es_t)


def hypoi_u(data: dict[str, np_ndarray], method: Literal['asymptotic', 'exact', 'auto'] = 'auto',
            alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided', u_continuity: bool = True):
    """
    perform :ref:`Mann–Whitney U test <Mann–Whitney U test>` on each possible pairs among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['asymptotic', 'exact', 'auto'] method: the method to calculate :math:`p`-value; ``'exact'`` uses
                                                             exact distribution of distribution(s); ``'asymptotic'``
                                                             uses approximate distribution(s); ``'auto'`` uses one of
                                                             the above options; ``'auto'`` as default to choose
                                                             ``'exact'`` when one of the samples is no greater than 8
                                                             and no ties, otherwise ``'asymptotic'``
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :param bool u_continuity: whether apply continuity correction; effective when ``'method'`` is ``'asymptotic'``;
                                 default is ``True``
       :return: statistic and :math:`p`-value on each group
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Mann–Whitney U test on multi groups
          :name: Mann–Whitney U test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_u(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, method, alternative, u_continuity)


def hypoi_bm(data: dict[str, np_ndarray], nan_policy: Literal['propagate', 'raise', 'omit'] = 'propagate',
             alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided', bm_dis: Literal['t', 'normal'] = 't'):
    """
    perform :ref:`Brunner-Munzel test <Brunner-Munzel test>` on each possible pairs among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['propagate', 'raise', 'omit'] nan_policy: strategy for null value-contained in data;
                                                                ``'propagate'`` return ``nan``; ``'raise'`` will throw
                                                                exception; ``'omit'`` will ignore null values;
                                                                ``'propagate'`` as default
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :param Literal['t', 'normal'] bm_dis: determine :math:`p`-value calculated from t or normal distribution;
                                             ``"t"`` as default
       :return: statistic and :math:`p`-value on each group
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Brunner-Munzel test on multi groups
          :name: Brunner-Munzel test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_bm(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, nan_policy, alternative, bm_dis)


def hypoi_ab(data: dict[str, np_ndarray], alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided'):
    """
    perform :ref:`Ansari-Bradley test <Ansari-Bradley test>` on each possible pairs among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :return: statistic and :math:`p`-value on each group
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Ansari-Bradley test on multi groups
          :name: Ansari-Bradley test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_ab(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, alternative)


def hypoi_skew(data: dict[str, np_ndarray], nan_policy: Literal['propagate', 'raise', 'omit'] = 'propagate',
               alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided'):
    """
    perform :ref:`skew test <Skew test>` on each group among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['propagate', 'raise', 'omit'] nan_policy: strategy for null value-contained in data;
                                                                ``'propagate'`` return ``nan``; ``'raise'`` will throw
                                                                exception; ``'omit'`` will ignore null values;
                                                                ``'propagate'`` as default
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :return: statistic and :math:`p`-value on each group
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: skew test on multi groups
          :name: skew test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_skew(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, nan_policy, alternative)


def hypoi_kurtosis(data: dict[str, np_ndarray], nan_policy: Literal['propagate', 'raise', 'omit'] = 'propagate',
                   alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided'):
    """
    perform :ref:`kurtosis test <Kurtosis test>` on each group among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['propagate', 'raise', 'omit'] nan_policy: strategy for null value-contained in data;
                                                                ``'propagate'`` return ``nan``; ``'raise'`` will throw
                                                                exception; ``'omit'`` will ignore null values;
                                                                ``'propagate'`` as default
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :return: statistic and :math:`p`-value on each group
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: kurtosis test on multi groups
          :name: kurtosis test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_kurtosis(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, nan_policy, alternative)


def hypoi_jb(data: dict[str, np_ndarray]):
    """
    perform :ref:`Jarque-Bera test <Jarque-Bera test>` on each group among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :return: statistic and :math:`p`-value on each group
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Jarque-Bera test on multi groups
          :name: Jarque-Bera test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_jb(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data)


def hypoi_pd(data: dict[str, np_ndarray], f_exp: Iterable[int] = None, ddf: int = 0, pd_lambda: Numeric = 1):
    """
    perform :ref:`Cressie-Read power divergence test <Cressie-Read power divergence test>` on each group
    among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Iterable[int] f_exp: expected frequencies of all categories; ``None`` as default for all equal for all
                                   categories
       :param int ddf: number to be subtracted from degree of freedom; ``0`` as default uses degree of freedom
                       :math:`k-1` where :math:`k` is the number of all observations
       :param Numeric pd_lambda: real-value to determine the power of statistic; 1 as default for Pearson version
       :return: statistic and :math:`p`-value on each group
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Power divergence on multi groups
          :name: Power divergence on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_pd(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, f_exp, ddf, pd_lambda)


def hypoi_chi2(data: dict[str, np_ndarray], f_exp: Iterable[int] = None):
    """
    perform :ref:`Chi-Squared test <Chi-Squared test>` on each group among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Iterable[int] f_exp: expected frequencies of all categories; ``None`` as default for all equal for all
                                   categories
       :return: statistic and :math:`p`-value on each group
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Chi-Squared test on multi groups
          :name: Chi-Squared test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoi_chi2(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, f_exp)


def hypoj_pearson(data: dict[str, np_ndarray], alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided'):
    """
    compute :ref:`Pearson correlation coefficient <Pearson correlation coefficient>` on each possible pairs among
    multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :return: statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Pearson correlation coefficient on multi groups
          :name: Pearson correlation coefficient on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoj_pearson(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, alternative)


def hypoj_spearman(data: dict[str, np_ndarray], nan_policy: Literal['propagate', 'raise', 'omit'] = 'propagate',
                   alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided'):
    """
    compute :ref:`Spearman correlation coefficient <Spearman correlation coefficient>` on each possible pairs among
    multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['propagate', 'raise', 'omit'] nan_policy: strategy for null value-contained in data;
                                                                ``'propagate'`` return ``nan``; ``'raise'`` will throw
                                                                exception; ``'omit'`` will ignore null values;
                                                                ``'propagate'`` as default
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :return: statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Spearman correlation coefficient on multi groups
          :name: Spearman correlation coefficient on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoj_spearman(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, nan_policy, alternative)


def hypoj_kendall(data: dict[str, np_ndarray], nan_policy: Literal['propagate', 'raise', 'omit'] = 'propagate',
                  alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided',
                  method: Literal['asymptotic', 'exact', 'auto'] = 'auto', kendall_tau: Literal['b', 'c', 'w'] = 'b',
                  rank: bool = True, weigher: Callable = None, additive: bool = True):
    """
    compute :ref:`Kendall's tau correlation coefficient <Kendall's tau correlation coefficient>` on each possible
    pairs among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['propagate', 'raise', 'omit'] nan_policy: strategy for null value-contained in data;
                                                                ``'propagate'`` return ``nan``; ``'raise'`` will throw
                                                                exception; ``'omit'`` will ignore null values;
                                                                ``'propagate'`` as default
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :param Literal['asymptotic', 'exact', 'auto'] method: the method to calculate :math:`p`-value; ``'exact'``
                                                             uses exact distribution of distribution(s);
                                                             ``'approx'`` uses double probability of
                                                             `single-tailed` to approximate that of `two-tailed`;
                                                             ``'asymp'`` uses asymptotic distribution(s);
                                                             ``'auto'`` uses one of the above options; ``'auto'``
                                                             as default
       :param Literal['b', 'c', 'w'] kendall_tau: determine type of :math:`\tau` to be calculated; ``'b'`` uses
                                                  Kendall :math:`\tau`; ``'c'`` uses Stuart's :math:`\tau`; ``'w'``
                                                  will activate weighted :math:`\tau`.
       :param bool rank: whether using decreasing lexicographical rank; if ``False``, index of element will be
                         processed as rank; effective when weighted :math:`\tau` is activated; ``True`` as default
       :param Optional[Callable] weigher: trigger to determine whether using weight when computing rank :math:`r`;
                                          acceptable mapping must be able to convert positive integer into weight
                                          (e.g. :math:`f(r) = (1+r)^{-1}`); ``None`` as default to use no weight
       :param bool additive: determine how weight be calculated on statistic; if ``True``, weight will be processed
                             as item to be added; Otherwise the item to be multiplied; effective when weighted
                             :math:`\tau` is activated; ``True`` as default;
       :return: statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Kendall's tau correlation coefficient on multi groups
          :name: Kendall's tau correlation coefficient on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoj_kendall(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, nan_policy, alternative, method, kendall_tau, rank, weigher, additive)


def hypoj_friedman(data: dict[str, np_ndarray]):
    """
    perform :ref:`Friedman test <Friedman test>` among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :return: statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Friedman test on multi groups
          :name: Friedman test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypoj_friedman(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data)


def hypoj_mgc(data: dict[str, np_ndarray], distance_criteria: Callable = lambda x, y: _cdist(x, y),
              n_resamples: int = 1000, random_state: int = None):
    """
    perform :ref:`Multiscale Graph Correlation test <Multiscale Graph Correlation test>` on each possible
    pairs among multi high-dimensional data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Callable distance_criteria: criterion to measure the distance of two element when calculating distance
                                          matrix; ``lambda x, y: np.linalg.norm(x-y, ord=2, axis=0)`` as default
                                          to calculate the Euclidean distance
       :param int n_resamples: number of resampled permutations to calculate :math:`p`-value; 1000 as default
       :param Optional[int] random_state: random state to control random sample generation; ``None`` as default
       :var bool ~full_return: if ``True``, scale map, optimal scales, and random points for null distribution will be
                               returned as extra information as well; ``False`` as default
       :return: statistic and :math:`p`-value
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Multiscale Graph Correlation test on multi groups
          :name: Multiscale Graph Correlation test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random((10, 5)) for _ in range(3)}

          res = ht.hypoj_mgc(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, distance_criteria, n_resamples, random_state)


def hypos_mc(data: dict[str, np_ndarray], dist: Union[_dist, list[_dist]] = gs(loc=0, scale=1),
             n_resamples: int = 9999, agg_statistics: dict[str, Callable] = _dict(a=(lambda x: _mean(x))),
             batch: int = None, alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided'):
    """
    perform :ref:`Monte Carlo hypothesis test <Monte Carlo hypothesis test>` on each group among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Union[dist, list[dist]] dist: distribution(s) predefined; standard uni-variate gaussian
                                            ``norm(loc=0, scale=1)`` as default
       :param int n_resamples: number of resampled datapoints generated from predefined distribution(s); 9999 as
                               default
       :param dict[str, Callable] agg_statistics: dict composed of name and aggregation function mapping to calculate
                                                  statistic; ``{'mean': lambda x: numpy.mean(x)}`` as default
       :param Optional[int] batch: number of samples used for each call of values in ``agg_statistics``; ``None`` as
                                   default which equals the ``n_resamples``
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :var bool ~full_return: if ``True``, random points for null distribution will be returned as extra information
                               as well; ``False`` as default
       :return: statistic and :math:`p`-value on each group
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Monte Carlo hypothesis test on multi groups
          :name: Monte Carlo hypothesis test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypos_mc(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, dist, n_resamples, agg_statistics, batch, alternative)


def hypos_permu(data: dict[str, np_ndarray], permu_type: Literal['independent', 'samples', 'pairings'] = 'independent',
                n_resamples: int = 9999, binding_groups: int = 2,
                agg_statistics: dict[str, Callable] = _dict(std_of_mean=lambda *x: _std([_mean(_) for _ in x])),
                batch: int = None, alternative: Literal['two-sided', 'less', 'greater'] = 'two-sided'):
    """
    perform :ref:`Permutation test <Permutation test>` on each possible permutation of groups among multi-grouped data.

    .. attribute:: Arguments:

       :param dict[str, ndarray] data: dict composed of group names as keywords and corresponding values
       :param Literal['independent', 'samples', 'pairings'] permu_type: permutation type; ``'samples'`` and
                                                                        ``'pairings'`` requires all data to be compared
                                                                        have the same size; ``'independent'`` assume
                                                                        all input data are of independent;
                                                                        ``'independent'`` as default
       :param int n_resamples: number of resampled datapoints generated from predefined distribution(s); 9999 as
                               default
       :param int binding_groups: number of groups for each call of test; acceptable value is integer equal or greater
                                  than 2; 2 as default
       :param dict[str, Callable] agg_statistics: dict composed of name and aggregation mapping to calculate statistic;
                                                  ``{'std_of_mean': lambda *x: np.std([np.mean(_) for _ in x])}`` as
                                                  default
       :param Optional[int] batch: number of samples used for each call of values in ``agg_statistics``; ``None`` as
                                   default which equals the ``n_resamples``
       :param Literal['two-sided', 'less', 'greater'] alternative: type of alternative hypothesis :math:`H_1`;
                                                                   ``'two-sided'`` as default
       :var bool ~full_return: if ``True``, random points for null distribution will be returned as extra information
                               as well; ``False`` as default
       :return: statistic and :math:`p`-value on each group
       :rtype: dict

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Permutation test on multi groups
          :name: Permutation test on multi groups

          from info.me import hypotest as ht
          import numpy as np
          data = {f"group{_+1}": np.random.random(20) for _ in range(3)}

          res = ht.hypos_permu(data=data)

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, permu_type, n_resamples, binding_groups, agg_statistics, batch, alternative)


def radiomics_features(data: Generator, extractor_setting: dict = None, err_file: str = None,
                       image_types: dict[str, dict] = None, feature_class: dict[str, list[str]] = None):
    r"""
    feature extraction automation. this function requires the readiness of a configured
    `pyradiomics <https://pypi.org/project/pyradiomics/>`_ environment.

    .. attribute:: Arguments:

       :param Generator data: generator to yield case name, ndarray image, ndarray segmentation, spacing
       :param Optional[dict] extractor_setting: parameters passed on radiomics extractor when initiation; empty dict
                                                ``{}`` as default to use default setting
       :param Optional[str] err_file: log to note down exceptive case; ``None`` as default to use 'err_case.log'
                                      inplace, if any exceptive case captured during extraction
       :param Optional[dict[str, dict]] image_types: parameters use image type as keyword to specify desired modality;
                                                     value should be extraction setting during extraction, empty dict
                                                     for using default setting; ``None`` as default to apply all image
                                                     types
       :param Optional[dict[str, Optional[list[str]]]] feature_class: customize selection features from sub feature
                                                                      class; keyword should be valid name of sub
                                                                      feature class, and the value is list composed of
                                                                      desired feature names; value can be ``None``, or
                                                                      empty list ``[]`` to enable all features of that
                                                                      modality; ``None`` as default, for not applying
                                                                      customized feature selection
       :return: table uses case names as indexing, and feature names as column names
       :rtype: DataFrame

    .. attribute:: Examples:

       .. code-block:: python
          :caption: radiomic feature extraction implementation
          :name: radiomic feature extraction implementation

          from info.med import radiomics_features

          def gen():
              for img in imgs:
                  for roi in img.rois:
                      yield str(img.name+roi.name), img, roi, img.spacing

          res = radiomics_features(data=gen())
          res.to_csv('result.csv', encoding='utf-8-sig')

    .. attribute:: Notes:

       Default installation might result in no valid export for certain feature classes. If all features are
       desired, in case, ensure that `PyWavelets <https://pypi.org/project/PyWavelets/>`_,
       `trimesh <https://pypi.org/project/trimesh/>`_ and `scikit-image <https://pypi.org/project/scikit-image/>`_
       are installed in the environment.

       The dependent pyradiomics package raises some unaddressed build issues in Python greater than 3.9 until now
       Aug 4, 2024. Recreate a downgraded Python (:math:`\leq` 3.9) environment if necessary, otherwise await for
       the bugs-fixing from develop team of pyradiomics.

       Incompatibility of some dependencies might raise due to `numpy <https://pypi.org/project/numpy/>`_ with
       version greater than 2.0.0.; Further test is required. If unknown error has been raised, try to downgrade
       numpy.

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       .. versionchanged:: 0.0.4

          remove `pyradiomics <https://pypi.org/project/pyradiomics/>`_ from dependencies due to its unaddressed
          issues from source code building and no support for up-to-date Python version among its binary releases.

       -- |signature|
    """
    args_highlighter(data, extractor_setting, err_file, image_types, feature_class)


def vascular_invasion(data: tuple[np_ndarray, np_ndarray], in_spacing: Iterable[Numeric] = None,
                      scope_radius: Numeric = None):
    """
    vascular invasion angle evaluation.

    .. attribute:: Arguments:

       :param tuple[ndarray, ndarray] data: tuple contained vascular and tumor masks
       :param Iterable[Numeric] in_spacing: spacing for each dimension in the unit voxel; ``None`` as default for using
                                            1 on each dimension
       :param Numeric scope_radius: radius of scope to make constraint on mask of vessel, to determine the center
                                    point of vessel; ``None`` as default to automatically calculate the vector from the
                                    mass center of overlapped region, to the geometric center of tumor as its radius
       :var int ~differential_tolerance: positive integer used as differential operator to evaluate the status of
                                         penetration; 3 as default
       :return: 1-length dict with boolean keyword as referred to whether was invaded, while value as represented for
                the spatial distance if no-connection; radian angle if invaded. If a list of numerical numbers
                was calculated, it is the set of radian angles for multiple invasion regions.
       :rtype: dict[bool, Union[Numeric, list[Numeric]]]

    .. attribute:: Examples:

       .. code-block:: python
          :caption: evaluation on vascular invasion state
          :name: evaluation on vascular invasion state

          from info.med import vascular_invasion
          tumor, vessel, spacing = ...
          res = vascular_invasion(data=(tumor, vessel), in_spacing=spacing)

    .. attribute:: Notes:

       Implemented via dimension-irrelevant paradigm, with compatibility for tensor in 2-rank or higher.

       No warranty in precision and efficiency for calculation on 3-dimensional case currently. This issue will be
       addressed in next official release.

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

          Scheme determination and clinical validation are conducted by Yajiao Zhang and Haoran Zhang.

       -- |signature|
    """
    args_highlighter(data, in_spacing, scope_radius)


def priori_scoring(data: DataFrame, constructor: dict[str, list[str]], response_dimensions: list[str],
                   inertia_dimensions: list[str] = None, measure: Callable[[list[list[list[Numeric]]]], Numeric] = None,
                   empty_value: Any = np_nan, score_output: bool = False):
    """
    :ref:`priori scoring <Priori scoring>` implementation for :ref:`multi factors analysis <Factor analysis>`.

    .. attribute:: Arguments:

       :param DataFrame data: table with multi factors as indexing, whose columns are un-ranked
       :param dict[str, list[str]] constructor: constructor to parse the factors and corresponding levels in indexing
                                                of data; dict used factor names as keywords, and list composed of level
                                                names as the corresponding value
       :param list[str] response_dimensions: list composed of factors that sensitive to affect the final numeric; the
                                             factor selection should follow the common sense, or expertise in that
                                             field
       :param Optional[list[str]] inertia_dimensions: list composed of factors that no sensitive to affect the
                                                      final numeric; ``None`` as default will automatically the
                                                      unselected factors based on ``constructor`` and
                                                      ``response_dimensions``
       :param Optional[Callable] measure: the callback :ref:`aggregation function <aggregation function>` to map the
                                          :ref:`rearranged pseudo-tensor <Rearranged pseudo-tensor>` to a scalar;
                                          ``None`` as default to use :ref:`normality <Shapiro-Wilk test>` combined
                                          with :ref:`ANOVA <one-way ANOVA test>` to measure how extent the data
                                          departure from the priori hypothesis
       :param Optional[Any] empty_value: value to fill the un-existed factor combinations; the ``measure`` function
                                         should be capable to deal with this value if use customized method;
                                         ``numpy.nan`` as default
       :param Optional[bool] score_output: whether export the final scores for all column names; ``False`` as default
       :return: a dict composed of importance level, and column names (and corresponding scores) in that level
       :rtype: dict[str, ndarray]

    .. attribute:: Examples:

       .. code-block:: python
          :caption: factor analysis automation using priori scoring algorithm
          :name: factor analysis automation using priori scoring algorithm

          from info.me import priori_scoring
          from itertools import product
          import numpy as np
          import pandas as pd

          cons = {
              'A': ['a1', 'a2'],
              'B': ['b1', 'b2', 'b3'],
              'C': ['c1', 'c2']
          }

          index = np.repeat(['-'.join(_) for _ in product(*[v for k, v in cons.items()])], 10)
          where_c1 = np.array(['c1' in _ for _ in index])
          columns = np.array([f"group_{_+1}" for _ in range(20)])
          _values = np.random.random((len(index), len(columns)))
          values = np.array([vec * 10.8 if c1 else vec * 0.3 for c1, vec in zip(where_c1, _values)])

          df = pd.DataFrame(values, index=index, columns=columns)
          #            group_1   group_2   group_3  ...  group_18  group_19  group_20
          # a1-b1-c1  8.330263  0.224121  6.843401  ...  3.152262  9.911961  7.717418
          # a1-b1-c1  5.859479  1.535437  4.032080  ...  8.949758  0.506480  6.763901
          # ...            ...       ...       ...  ...       ...       ...       ...
          # a2-b3-c2  0.205181  0.175918  0.293796  ...  0.020738  0.017385  0.094473
          # a2-b3-c2  0.162649  0.077234  0.133392  ...  0.122661  0.200381  0.172522

          res = priori_scoring(data=df, constructor=cons, response_dimensions=['C'], score_output=True)
          # {'importance_level_0': array([['group_11', 10.583273152581747]]),  # most discriminative
          #  'importance_level_1': array([['group_1', 5.543840398683746],
          #                               ['group_2', 6.006970191046672],
          #                               ['group_3', 4.691317734172809],
          #                               ...}

    .. attribute:: Logs:

       .. versionadded:: 0.0.3

       -- |signature|
    """
    args_highlighter(data, constructor, response_dimensions, inertia_dimensions, measure, empty_value, score_output)


def Hotelling(data: np_ndarray, significance_level: float = 0.05):
    r"""
    Hotelling T\ :sup:`2` constructor for multivariate gaussian distribution.

    .. attribute:: Arguments:

       :param ndarray data: :math:`\boldsymbol{R}^{n \times m}` matrix with :math:`n` observations of :math:`m`
                            dimensions
       :param float significance_level: significance level used for anomaly threshold determination; 0.05 as default
       :return: Hotelling T\ :sup:`2` distribution
       :rtype: Hotelling

    .. attribute:: Property:

       .. property:: settings:

          Hotelling configuration when initializing

       .. property:: model:

          :math:`\boldsymbol{R}^{n \times m}` data container; the number of observations :math:`n` will increase
          when use data updating

       .. property:: mean:

          :math:`\boldsymbol{R}^m` mean vector of all observations

       .. property:: sigma:

          :math:`\boldsymbol{R}^{m \times m}` covariance matrix of all observations

       .. property:: threshold:

          threshold calculated for determining anomalous observations, under assigned significance level

    .. attribute:: Methods:

       .. method:: update:

          append new observations via ``data``, then synchronize related properties

       .. method:: predict_dissimilarity:

          calculate anomaly scores of new observations, via ``data`` keyword assignment; will return a numeric
          sequence

       .. method:: predict:

          determine whether anomalous or not for new observations, via ``data`` keyword assignment; will return a
          boolean sequence

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Hotelling T2 for anomaly determination
          :name: Hotelling T2 for anomaly determination

          from info.me import anomaly as ano
          from scipy.stats import multinomial
          import numpy as np

          p = np.array([0.03, 0.06, 0.1, 0.34, 0.22, 0.11, 0.08, 0.06])
          obs = np.array([multinomial.rvs(50, p) for _ in range(100)])

          model = ano.Hotelling(data=obs)
          model.predict(data=np.vstack([obs, np.array([multinomial.rvs(50, np.roll(p, 4)) for _ in range(100)])]))

    .. attribute:: Notes:

       Hotelling T\ :sup:`2` is a classic method to detect outliers, from :ref:`I.I.D. <I.I.D.>` observations which
       in consistence of multivariate gaussian distribution (definition see :eq:`multivariate Gaussian`). It
       can be seen as the multivariate extension for :ref:`uni-variate t-test <Student's T test>`. The related
       :ref:`section <Hotelling T-squared>` collected the detailed mathematical deduction of this method.

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(data, significance_level)


def Neighbors(data: np_ndarray, labels: np_ndarray, distance_measure: int = 2,
              kamap_optimizer: Callable[[np_ndarray, np_ndarray, np_ndarray], tuple[int, float]] = _ka_opt,
              nearing_mode: Literal['KNN', 'LMNN'] = 'LMNN', k_determine: int = 10, eta_determine: float = 0.05,
              prior_prob_determine: list[float] = None):
    r"""
    Neighbor algorithm frame for modeling based on empirical distribution. For definition of empirical distribution,
    see :eq:`empirical distribution`, and :ref:`supplementary material <Empirical distribution and neighbors>` for
    the principles.

    .. attribute:: Arguments:

       :param ndarray data: :math:`\boldsymbol{R}^{n \times m}` matrix with :math:`n` observations of :math:`m`
                            dimensions
       :param ndarray labels: non-negative integer array as labels in consistence of ``data``; if for anomaly
                              detection, suggest labeling the normal data as 0 while other integers for anomalies
                              with other patterns.
       :param int distance_measure: order of norm to calculate distance; ``2`` as default for Euclidean
       :param Callable kamap_optimizer: method to determine the optimal :math:`k_{i,j}`, and threshold :math:`a_{i,j}`
                                        to distinguish the :math:`i`- and :math:`j`-class; the value should be capable
                                        to accept :math:`k` vs. :math:`a` map, axes of :math:`k` and :math:`a` as
                                        three arguments, then return the optimal values of :math:`k_{\mathrm{opt}}`
                                        and :math:`a_{\mathrm{opt}}`; ``None`` as default to call a built-in method,
                                        that determines these two optimal values via local minial of 1st order
                                        differentiation of :math:`k`, and the global maximum of :math:`a`
       :param Literal nearing_mode: use which method to initiate the transformation; valid options are ``'KNN'``, and
                                    ``'LMNN'``; ``'KNN'`` is for computation in original Cartesian space, ``'LMNN'``
                                    is in a computed Riemannian space (see :ref:`related definitions
                                    <Empirical distribution and neighbors>`); ``'KNN'`` as default
       :param int k_determine: the maximum number of :math:`k` during initiative training; 10 as default
       :param float eta_determine: the coefficient used for updating (sub)gradient during initiative training, if
                                   spatial calculation and transformation is necessary; 0.05 as default
       :param list[float] prior_prob_determine: prior weights assigned for all classes; in consistence with
                                               :math:`\boldsymbol{\alpha}` of certain dirichlet distribution; ``None``
                                               as default using all-equal weights
       :return: optimal data set based on an empirical distribution
       :rtype: Neighbors

    .. attribute:: Property:

       .. property:: settings:

          Neighbors configuration when initializing

       .. property:: x:

          :math:`\boldsymbol{R}^{n \times m}` data container; the number of observations :math:`n` will increase
          when use data updating

       .. property:: y:

          :math:`\boldsymbol{R}^n` vector of integers in consistence with ``x``

       .. property:: trans:

          :math:`\boldsymbol{C}^{m \times m}` transformation; real domain for ``'KNN'`` while complex domain for
          ``'LMNN'``

       .. property:: thre:

          dict constructed as ``dict[tuple[i, j], tuple[k_ij, a_ij]]`` determined by ``kamap_optimizer``; ``i``, ``j``
          are indicators for different classes

    .. attribute:: Methods:

       .. method:: update:

          append new observations and corresponding labels via ``data`` and ``labels``, then synchronize related
          properties

       .. method:: predict_dissimilarity:

          calculate anomaly scores of new observations, via ``data`` keyword assignment; will return a dict
          with construction as ``dict[tuple[i, j], ndarray]``; ``i`` and ``j`` are indicators for different classes

       .. method:: predict:

          determine which maximum likely class, via ``data`` keyword assignment; will return a sequence of integers

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Neighbors frame for multi classification
          :name: Neighbors frame for multi classification

          from info.me import anomaly as ano
          from scipy.stats import multinomial
          import numpy as np

          p1 = np.array([0.03, 0.06, 0.1, 0.34, 0.22, 0.11, 0.08, 0.06])
          p2 = np.array([0.03, 0.08, 0.06, 0.12, 0.35, 0.2, 0.11, 0.05])
          obs = np.vstack([np.array([multinomial.rvs(50, p) for _ in range(100)]) for p in [p1, p2]])
          cls = np.array([0 for _ in range(100)] + [1 for _ in range(100)])

          model = ano.Neighbors(data=obs, labels=cls)
          model.predict(data=np.vstack([obs, np.array([multinomial.rvs(50, np.roll(p1, 4)) for _ in range(100)])]))

    .. attribute:: Notes:

       initialization differs from defined method:

       - **KNN**:

          :math:`k`-nearest neighbors uses the unit matrix :math:`\boldsymbol{I}` as transformation, for calculation
          in original Cartesian space

       - **LMNN**:

          Large margin nearest neighbors (LMNN) needs to initialize a Riemannian space. In each updating step,
          use the gradient of :eq:`Riemannian optimization` (:math:`\boldsymbol{R} = \boldsymbol{R} - \eta (\partial
          \Psi (\boldsymbol{R}) / \partial \boldsymbol{R})`).

          In :eq:`Riemannian optimization`, the major form of item is :math:`d^2_{\boldsymbol{R}} (\boldsymbol{a},
          \boldsymbol{b}) = (\boldsymbol{a} - \boldsymbol{b})^T \boldsymbol{R} (\boldsymbol{a} - \boldsymbol{b})`.
          Because :math:`\boldsymbol{m}^\top \boldsymbol{A} \boldsymbol{n} = \mathrm{Tr} (\boldsymbol{m}^\top
          \boldsymbol{A} \boldsymbol{n})`, and :math:`(\partial \mathrm{Tr} [ \boldsymbol{m}^\top \boldsymbol{A}
          \boldsymbol{n} ]) / (\partial \boldsymbol{A}) = \boldsymbol{m} \boldsymbol{n}^\top`. Therefore:

          .. math::
             :label: computing method for gradient in Riemannian optimization

             \frac{\partial d^2_{\boldsymbol{R}} (\boldsymbol{a}, \boldsymbol{b})}{\partial \boldsymbol{R}} =
             \frac{\partial \mathrm{Tr} [ (\boldsymbol{a} - \boldsymbol{b})^\top \boldsymbol{R} (\boldsymbol{a} -
             \boldsymbol{b}) ]}{\partial \boldsymbol{R}} = (\boldsymbol{a} - \boldsymbol{b}) (\boldsymbol{a} -
             \boldsymbol{b})^\top

          As the result, the computation for gradient is in series of linear subspaces on original space. Using the
          eigen decomposition of updated :math:`\boldsymbol{R}=\boldsymbol{L}\boldsymbol{\Lambda}\boldsymbol{L}^\top`,
          to guarantee the semi-positive constraint in :eq:`Riemannian optimization`, floor the negative eigen values
          as 0 in :math:`\boldsymbol{\Lambda}` (denoted as :math:`[\boldsymbol{\Lambda}]_{+}`). Then final Riemannian
          space can be updated through :math:`\boldsymbol{L} [\boldsymbol{\Lambda}]_{+} \boldsymbol{L}^\top`.

          Repeating the previous calculation until :math:`\boldsymbol{R}` converge. The final :math:`\boldsymbol{R}^*`
          is the optimal Riemannian space based on the trained data.

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(data, labels, distance_measure, kamap_optimizer, nearing_mode, k_determine, eta_determine,
                     prior_prob_determine)


def VonMisesFisher(data: np_ndarray, significance_level: float = 0.05):
    r"""
    Algorithm frame for spherical like data. Theoretical definition of Von Mises Fisher distribution can refer
    :eq:`Von Mises Fisher pdf`. And the :ref:`associated deduction <Directional data>` is also provided.

    .. attribute:: Arguments:

       :param ndarray data: :math:`\boldsymbol{R}^{n \times m}` matrix with :math:`n` observations of :math:`m`
                            dimensions
       :param float significance_level: significance level used for anomaly threshold determination; 0.05 as default
       :return: the Von Mises Fisher distribution
       :rtype: VonMisesFisher

    .. attribute:: Property:

       .. property:: settings:

          VonMisesFisher configuration when initializing

       .. property:: model:

          :math:`\boldsymbol{R}^{n \times m}` data container; the number of observations :math:`n` will increase
          when use data updating

       .. property:: mean:

          mean vector :math:`\boldsymbol{s}` of all observations as referred in the
          :ref:`supplementary materials <Directional data>`

       .. property:: a:

          degree of anomalies for all observations

       .. property:: m:

          the estimation on degree of freedom for the calculated :math:`\chi^2` distribution

       .. property:: s:

          the scale factor for the calculated :math:`\chi^2` distribution

       .. property:: dis:

          the Von Mises Fisher distribution

    .. attribute:: Methods:

       .. method:: update:

          append new observations and corresponding labels via ``data``, then synchronize related properties

       .. method:: predict_dissimilarity:

          calculate anomaly scores of new observations, via ``data`` keyword assignment; will return a numeric
          sequence

       .. method:: predict:

          determine whether anomalous or not for new observations, via ``data`` keyword assignment; will return a
          boolean sequence

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Von Mises Fisher for anomaly determination
          :name: Von Mises Fisher for anomaly determination

          from info.me import anomaly as ano
          from scipy.stats import multinomial
          import numpy as np

          p = np.array([0.03, 0.06, 0.1, 0.34, 0.22, 0.11, 0.08, 0.06])
          obs = np.array([multinomial.rvs(50, p) for _ in range(100)])

          model = ano.VonMisesFisher(data=obs)
          model.predict(data=np.vstack([obs, np.array([multinomial.rvs(50, np.roll(p, 4)) for _ in range(100)])]))

    .. attribute:: Notes:

       From the :ref:`supplementary deduction <Directional data>` it is known the degree of anomaly in the
       context of Von Mises Fisher distribution is in consistent with a certain :math:`\chi^2(a | m, s)`.

       Using the substitution :math:`\Gamma(m/2) = (2/m) \Gamma((m/2)+1) = (2/(m+2)) (2/m) \Gamma((m/2)+2)`, the
       moment estimation for solving :math:`E[a]` and :math:`E[a^2]` can be obtained through:

       .. math::
          :label: 1st moment of chi2 in vmf

          E[a] &= \int_0^{\infty} da \cdot a \cdot \chi^2 (a | m, s) \\
          &= \int_0^{\infty} da \cdot a \cdot \frac{1}{2s\Gamma(\frac{m}{2})} (\frac{a}{2s})^{\frac{m}{2}-1}
          \exp(-\frac{a}{2s}) \\
          &= ms \cdot \int_0^{\infty} da \cdot (\frac{a}{2s}) \cdot \frac{1}{2s\Gamma(\frac{m}{2}+1)}
          (\frac{a}{2s})^{\frac{m}{2}-1} \exp(-\frac{a}{2s}) \\
          &= ms \cdot \int_0^{\infty} da \cdot \chi^2(a | m+2, s) = ms

       .. math::
          :label: 2nd moment of chi2 in vmf

          E[a^2] &= \int_0^{\infty} da \cdot a^2 \chi^2 (a | m, s) \\
          &= \int_0^{\infty} da \cdot a^2 \cdot \frac{1}{2s\Gamma(\frac{m}{2})} (\frac{a}{2s})^{\frac{m}{2}-1}
          \exp(-\frac{a}{2s}) \\
          &= m(m+2)s^2 \cdot \int_0^{\infty} da \cdot (\frac{a}{2s})^2 \cdot \frac{1}{2s\Gamma(\frac{m}{2}+2)}
          (\frac{a}{2s})^{\frac{m}{2}-1} \exp(-\frac{a}{2s}) \\
          &= m(m+2)s^2 \cdot \int_0^{\infty} da \cdot \chi^2(a | m+4, s) = m(m+2)s^2

       :math:`\hat{m}` and :math:`\hat{s}` represent for the estimations on :math:`m` and :math:`s` respectively.
       Simultaneously consider the :eq:`1st moment of chi2 in vmf` and :eq:`2nd moment of chi2 in vmf`, the following
       formula can be established:

       .. math::
          :label: solution for infer chi2 parameters in vmf

          \hat{m} = \frac{2(E[a])^2}{E[a^2] - (E[a])^2};\ \hat{s} = \frac{E[a^2] - (E[a])^2}{E[a]}

       Compare to the form of :math:`\chi^2 (M-1, 0.5\kappa)`, the estimation :math:`\hat{s}` is nothing else but
       :math:`0.5\kappa`, while the :math:`\hat{m}` is generally no greater than :math:`M-1`. In the view point of
       informatics, the estimation :math:`\hat{m}` represents to some extent the valid number of dimension that takes
       part in the subsequent modeling and calculations.

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(data, significance_level)


def NaiveBayes(data: np_ndarray, label: np_ndarray, prior: list[_dist] = None, validation_rate: float = 0.2,
               model_lightweight: bool = True):
    r"""
    NaiveBayes framework. await for :ref:`completion <Bayesian and mixture Gaussian>`.

    .. attribute:: Arguments:

       :param ndarray data: :math:`\boldsymbol{R}^{n \times m}` matrix with :math:`n` observations of :math:`m`
                            dimensions
       :param ndarray label: 1D boolean label of ``data``, ``False`` for normal instances while ``True``  for
                             anomalous ones
       :param list[DirTP] prior: list composed dirichlet distributions of normal and anomalous respectively; ``None``
                                 as default to initialize two dirichlet distributions with 1 for all :math:`\alpha`
       :param float validation_rate: the ratio of test data in cross validation, to determine the threshold; 0.2 as
                                     default to use 5-fold validation
       :param bool model_lightweight: whether cache the data points; ``True`` will save the ``data``, ``label`` and
                                      the calculated anomalous statistic; ``False`` merely update those two models;
                                      the default value uses ``True``
       :return: naive Bayes model
       :rtype: NaiveBayes

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Naive Bayes for anomaly determination
          :name: Naive Bayes for anomaly determination

          from info.me import anomaly as ano
          from scipy.stats import multinomial
          import numpy as np

          p = np.array([0.03, 0.06, 0.1, 0.34, 0.22, 0.11, 0.08, 0.06])
          obs = np.vstack([np.array([multinomial.rvs(50, p) for _ in range(100)]),
                           np.array([multinomial.rvs(50, np.roll(p, 4)) for _ in range(100)])])
          cls = np.concatenate([np.array([0 for _ in range(100)]), np.array([1 for _ in range(100)])]).astype(bool)

          model = ano.NaiveBayes(data=obs, labels=cls)
          model.predict(data=np.vstack([np.array([multinomial.rvs(50, p) for _ in range(20)]),
                                        np.array([multinomial.rvs(50, np.roll(p, 4)) for _ in range(20)])]))

    .. attribute:: Notes:

       await for :ref:`completion <Bayesian and mixture Gaussian>`.

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(data, label, prior, validation_rate, model_lightweight)


def Bayes(name: str, kernel: _dist, prior: _dist, likelihood_check: Callable[[Union[np_ndarray, _dist]], bool],
          update_conjugate: Callable[[_dist, Union[np_ndarray, _dist]], _dist],
          update_predictive: Callable[[_dist, Union[np_ndarray, _dist]], _dist]):
    """
    Essential Bayes framework.

    .. attribute:: Arguments:

       :param str name: the name of the kernel likelihood function
       :param dist kernel: the kernel likelihood distribution
       :param dist prior: the Bayesian prior distribution
       :param Callable[[...], bool] likelihood_check: likelihood checker to validate the investigated data
                                                      or distribution
       :param Callable[[...], dist] update_conjugate: method to update the Bayesian conjugate posterior distribution;
                                                      its arguments should be the corresponding Bayesian conjugate
                                                      prior, and followed by the likelihood data set in presentation of
                                                      numpy array or the form of certain distribution
       :param Callable[[...], dist] update_predictive: method to update the Bayesian posterior predictive distribution;
                                                       its arguments should be the updated Bayesian conjugate prior,
                                                       and followed by the likelihood data set in presentation of numpy
                                                       array or the form of certain distribution if necessary
       :return: a kind of Bayesian family
       :rtype: Bayes

    .. attribute:: Properties:

       .. property:: name:

          Name of Bayesian framework. It suggests to use the family name of likelihood function during declaration.

       .. property:: kernel:

          Distribution of likelihood function used in initialization.

       .. property:: conjugate:

          The Bayesian prior distribution. Its associated parameters be updated by invoking the method of
          ``update_posterior`` with input of the likelihood data set or distribution.

       .. property:: predictive:

          The Bayesian predictive distribution under the pre-condition of ``conjugate`` as Bayesian posterior.

       .. property:: update_conjugate:

          The callable function to compute conjugate prior and likelihood data set into conjugate posterior.

       .. property:: update_predictive:

          The callable function to compute conjugate posterior and likelihood data set into posterior predictive.

    .. attribute:: Methods:

       .. method:: update_posterior:

          Update the ``conjugate`` and ``predictive`` distributions, via likelihood distribution or data set.

       .. method:: compare_posterior:

          Test for the ``conjugate`` posterior under the condition of likelihood distribution or data set, without
          updating the property ``conjugate`` and ``predictive`` indeed.

    .. attribute:: Notes:

       A Bayes instance should be a set of correlated distributions and their corresponding rules of calculations that
       basically follows the principles of :ref:`Bayes theory <The basic theories>`. In real implementations, without
       the loss of the scientific rigorousness, our informatics still consider the degeneration relationship of
       distributions, induced by dimensional collapse. For example, the likelihood functions used bernoulli, binomial,
       and categorical are all fulfilled from the multinomial framework. Their relationship can be ascertained in
       :numref:`Table %s <discrete distribution relations>`, and the concrete reduction tutorial can be referred
       in the chapter of :ref:`multinomial distribution <Multinomial distribution>`. Similarly, the Gauss family is
       basically achieved from the multivariate Gauss distribution, on the basis of
       :ref:`Gauss Bayesian framework <summary of gauss family>` as established in the chapter of
       :ref:`continuous Gauss <Continuous distribution family>`.

       Customarily, the parameters ``update_conjugate`` and ``update_predictive`` takes conjugate distribution and
       likelihood function or data set as input arguments, then return the corresponding Bayesian posterior and
       predictive distributions, respectively.

    .. attribute:: See also:

       - :py:func:`~info.docfunc.bernoulli`

       - :py:func:`~info.docfunc.categorical`

       - :py:func:`~info.docfunc.binomial`

       - :py:func:`~info.docfunc.multinomial`

       - :py:func:`~info.docfunc.poisson`

       - :py:func:`~info.docfunc.gaussian`

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(name, kernel, prior, likelihood_check, update_conjugate, update_predictive)


def bernoulli(kernel: Union[BernTP, BinTP, MultTP], prior: Union[BetaTP, DirTP] = None) -> Bayes:
    """
    Bayesian framework of bernoulli kernel.

    .. attribute:: Arguments:

       :param Union[BernTP, BinTP, MultTP] kernel: a certain bernoulli distribution, a certain binomial distribution
                                                   with only one trial, or a certain multinomial distribution with
                                                   one trial and two categories.
       :param Union[BetaTP, DirTP] prior: a certain beta distribution or dirichlet distribution with a two-length
                                          alpha; ``None`` as default to use uniform prior.
       :return: the bernoulli Bayesian instance
       :rtype: :py:func:`~info.docfunc.Bayes`

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Bayesian of bernoulli kernel
          :name: Bayesian of bernoulli kernel

          from info.me import bayes as bys
          from scipy import stats as st
          import numpy as np

          model1 = bys.bernoulli(kernel=st.bernoulli(0.3), prior=st.beta(4, 5))
          model1.update_posterior(posterior=np.array([[1, 0], [0, 1], [1, 0], [1, 0]]))

          # or equivalently using the categorical kernel with one trial:
          model2 = bys.categorical(kernel=st.multinomial(1, [0.7, 0.3]), prior=st.dirichlet([4, 5]))
          model2.update_posterior(posterior=np.array([[1, 0], [0, 1], [1, 0], [1, 0]]))

    .. attribute:: Notes:

       On the basis of the degeneration with :math:`M = 1` and :math:`K = 2` from the
       :ref:`Bayesian multinomial distribution <Multinomial distribution>`, although the kernel and prior support
       to be initialized via multiple types of valid distributions, the kernel, conjugate and predictive distributions
       are all fulfilled in multinomial context.

    .. attribute:: See also:

       - :py:func:`~scipy.stats.bernoulli`

       - :py:func:`~info.docfunc.categorical`

       - :py:func:`~scipy.stats.multinomial`

       - :py:func:`~scipy.stats.beta`

       - :py:func:`~scipy.stats.dirichlet`

       - :py:func:`~scipy.stats.dirichlet_multinomial`

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(kernel, prior)


def binomial(kernel: Union[BinTP, MultTP], prior: Union[BetaTP, DirTP]) -> Bayes:
    """
    Bayesian framework of binomial kernel.

    .. attribute:: Arguments:

       :param Union[BinTP, MultTP] kernel: a certain binomial distribution or a certain two-categorical multinomial
                                           distributions with multiple trials.
       :param Union[BetaTP, DirTP] prior: a certain beta distribution or dirichlet distribution with a two-length
                                          alpha; ``None`` as default to use uniform dirichlet prior.
       :return: the binomial Bayesian instance
       :rtype: :py:func:`~info.docfunc.Bayes`

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Bayesian of binomial kernel
          :name: Bayesian of binomial kernel

          from info.me import bayes as bys
          from scipy import stats as st
          import numpy as np

          model1 = bys.binomial(kernel=st.binom(5, 0.3), prior=st.beta(4, 5))
          model1.update_posterior(posterior=np.array([[4, 1], [3, 2], [2, 3], [5, 0]]))

          # or equivalently in the multinomial context:
          model2 = bys.multinomial(kernel=st.multinomial(5, [0.7, 0.3]), prior=st.dirichlet([4, 5]))
          model2.update_posterior(posterior=st.multinomial(20, [0.7, 0.3]))

    .. attribute:: Notes:

       On the basis of the second degeneration situation with :math:`K = 2` from the
       :ref:`Bayesian multinomial distribution <Multinomial distribution>`, although the kernel and prior support
       to be initialized via multiple types of valid distributions, the kernel, conjugate and predictive distributions
       are all fulfilled in multinomial context.

    .. attribute:: See also:

       - :py:func:`~scipy.stats.binom`

       - :py:func:`~scipy.stats.multinomial`

       - :py:func:`~scipy.stats.beta`

       - :py:func:`~scipy.stats.dirichlet`

       - :py:func:`~scipy.stats.dirichlet_multinomial`

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(kernel, prior)


def categorical(kernel: MultTP, prior: DirTP = None) -> Bayes:
    """
    Bayesian framework of categorical kernel.

    .. attribute:: Arguments:

       :param MultTP kernel: a certain multinomial distribution instance with one trial.
       :param DirTP prior: a certain dirichlet distribution; ``None`` as default to use uniform dirichlet prior.
       :return: the categorical Bayesian instance
       :rtype: :py:func:`~info.docfunc.Bayes`

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Bayesian of categorical kernel
          :name: Bayesian of categorical kernel

          from info.me import bayes as bys
          from scipy import stats as st
          import numpy as np

          model = bys.categorical(kernel=st.multinomial(1, [0.3, 0.2, 0.5]), prior=st.dirichlet([3, 2, 4]))
          model.update_posterior(posterior=np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0], [0, 0, 1]]))

    .. attribute:: Notes:

       Implementation is on the basis of the first degeneration situation with :math:`M = 1` from the
       :ref:`Bayesian multinomial distribution <Multinomial distribution>`. There is temporarily no explicit
       application programming interface of categorical distribution in scipy, it employs the collapsed multinomial
       one with single trial.

    .. attribute:: See also:

       - :py:func:`~scipy.stats.multinomial`

       - :py:func:`~scipy.stats.dirichlet`

       - :py:func:`~scipy.stats.dirichlet_multinomial`

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(kernel, prior)


def multinomial(kernel: MultTP, prior: DirTP) -> Bayes:
    """
    Bayesian framework of multinomial kernel.

    .. attribute:: Arguments:

       :param MultTP kernel: a certain multinomial distribution instance multiple trials.
       :param DirTP prior: a certain dirichlet distribution; ``None`` as default to use uniform dirichlet prior.
       :return: the multinomial Bayesian instance
       :rtype: :py:func:`~info.docfunc.Bayes`

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Bayesian of multinomial kernel
          :name: Bayesian of multinomial kernel

          from info.me import bayes as bys
          from scipy import stats as st
          import numpy as np

          model = bys.multinomial(kernel=st.multinomial(5, [0.3, 0.2, 0.5]), prior=st.dirichlet([3, 2, 4]))
          model.update_posterior(posterior=np.array([[1, 1, 3], [2, 1, 2], [1, 0, 4], [2, 1, 2]]))

    .. attribute:: Notes:

       Implementation is on the basis of the general situation with :math:`M > 1` and :math:`K > 2` of the
       :ref:`Bayesian multinomial distribution <Multinomial distribution>`.

    .. attribute:: See also:

       - :py:func:`~scipy.stats.multinomial`

       - :py:func:`~scipy.stats.dirichlet`

       - :py:func:`~scipy.stats.dirichlet_multinomial`

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(kernel, prior)


def poisson(kernel: PoiTP, prior: Union[GamTP, ExpTP, ErlTP] = None) -> Bayes:
    r"""
    Bayesian framework of poisson kernel.

    .. attribute:: Arguments:

       :param PoiTP kernel: a certain poisson distribution instance.
       :param Union[GamTP, ExpTP, ErlTP] prior: a certain gamma distribution; ``None`` as default to use
                                                :math:`\mathrm{Gam}(x|1, 1)` prior.
       :return: the poisson Bayesian instance
       :rtype: :py:func:`~info.docfunc.Bayes`

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Bayesian of poisson kernel
          :name: Bayesian of poisson kernel

          from info.me import bayes as bys
          from scipy import stats as st
          import numpy as np

          model = bys.poisson(kernel=st.poisson(2.3), prior=st.gamma(1, 0, 0.5))
          model.update_posterior(posterior=np.array([0, 3, 2, 1, 4, 6]))

    .. attribute:: Notes:

       Implementation is on the basis of the deduction in the :ref:`poisson distribution <Poisson distribution>`.
       In addition, consider the exponential and erlang distributions are too specific forms of gamma distribution,
       however all the prior should be here reinterpreted under the gamma context.

       For example, the initialization method in :numref:`Bayesian of poisson kernel` can also be equivalently
       achieved by:

       .. code-block:: python
          :caption: Bayesian of poisson with other priors
          :name: Bayesian of poisson with other priors

          model1 = bys.poisson(kernel=st.poisson(2.3), prior=st.expon(2))
          model2 = bys.poisson(kernel=st.poisson(2.3), prior=st.erlang(1, 0, 0.5))
          model1.conjugate.dist.name == model2.conjugate.dist.name == 'gamma'  # True

    .. attribute:: See also:

       - :py:func:`~scipy.stats.poisson`

       - :py:func:`~scipy.stats.gamma`

       - :py:func:`~scipy.stats.nbinom`

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(kernel, prior)


def GaussianWishart(mean: np_ndarray, beta: Numeric, nu: int, w: np_ndarray):
    """
    the initializer of gauss-wishart distribution.

    .. attribute:: Arguments:

       :param ndarray mean: mean vector of gauss distribution.
       :param Numeric beta: coefficient for the distribution of precision matrix.
       :param int nu: degree of freedom, should be no less than 1 minus the number of dimensions of ``w``.
       :param ndarray w: a positive definite matrix.
       :return: a gauss-wishart distribution if all arguments are configured valid, otherwise 0.
       :rtype: Union[GauWisTP, int]

    .. attribute:: Examples:

       .. code-block:: python
          :caption: gauss wishart instance
          :name: gauss wishart instance

          from info.me import bayes as bys
          import numpy as np

          _temp = np.random.random((20, 3))
          gauss_wishart = bys.GaussianWishart(np.random.random(3), 3.4, 5, _temp.T @ _temp)

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(mean, beta, nu, w)


def gaussian(kernel: Union[GauTP, MGauTP], prior: Union[GauTP, MGauTP, GamTP, WisTP, GauWisTP]) -> Bayes:
    r"""
    Bayesian framework of gauss kernel.

    .. attribute:: Arguments:

       :param Union[GauTP, MGauTP] kernel: a certain gauss distribution instance.
       :param Union[GauTP, MGauTP, GamTP, WisTP, GauWisTP] prior: a certain prior distribution; in case of univariate
                                                                  gauss kernel, it supports initializing using
                                                                  univariate gauss, gamma, or one dimension confined
                                                                  multivariate gauss, wishart, or gauss-wishart;
                                                                  in case of multivariate gauss kernel, it supports
                                                                  initializing using multivariate gauss, wishart,
                                                                  or gauss-wishart; their detailed relationships
                                                                  and deduction can refer
                                                                  :numref:`Table %s <summary of gauss family>`;
                                                                  ``None`` as default to automatically employ the
                                                                  gauss-wishart :math:`\mathcal{NW}(\boldsymbol{x}
                                                                  | \boldsymbol{0}_D, 1, D, \boldsymbol{I}_D)`.
       :return: the gauss Bayesian instance
       :rtype: :py:func:`~info.docfunc.Bayes`

    .. attribute:: Examples:

       .. code-block:: python
          :caption: Bayesian of gauss kernel
          :name: Bayesian of gauss kernel

          from info.me import bayes as bys
          from scipy import stats as st
          import numpy as np

          mean, cov = np.array([1, 2]), np.diag([1.5, 1])
          dis = st.multivariate_normal(mean+0.7, cov+0.45)

          # framework to infer mean vector:
          model1 = bys.gaussian(kernel=st.multivariate_normal(mean, cov), prior=st.multivariate_normal(mean+1, cov+0.3))
          model1.update_posterior(posterior=dis.rvs(size=30))

          # framework to infer precision matrix:
          model2 = bys.gaussian(kernel=st.multivariate_normal(mean, cov), prior=st.wishart(3, np.linalg.inv(cov+0.31)))
          model2.update_posterior(posterior=dis.rvs(size=30))

          # framework to infer both mean vector and precision matrix:
          model3 = bys.gaussian(kernel=st.multivariate_normal(mean, cov),
                                prior=bys.GaussianWishart(mean+0.92, 1.4, 3, np.linalg.inv(cov+0.31)))
          model3.update_posterior(posterior=dis.rvs(size=30))

    .. attribute:: Notes:

       Implementation is on the basis of the deduction in the
       :ref:`gauss distribution family <Continuous distribution family>`. According to the deduction, application
       programming interface of gauss here also support the Bayesian inference in context of univariate gauss:

       .. code-block:: python
          :caption: Bayesian of univariate gauss kernel
          :name: Bayesian of univariate gauss kernel

          mean, var, dis = 1.2, 1.5, st.norm(1.5, 0.7)

          # framework to infer mean:
          model1 = bys.gaussian(kernel=st.norm(mean, var), prior=st.norm(1.1, 0.9))
          model1.update_posterior(posterior=dis.rvs(size=30)[..., np.newaxis])

          # framework to infer precision:
          model2 = bys.gaussian(kernel=st.norm(mean, var), prior=st.gamma(3, 5))
          model2.update_posterior(posterior=dis.rvs(size=30)[..., np.newaxis])

          # framework to infer both mean and precision:
          model3 = bys.gaussian(kernel=st.norm(mean, var),
                                prior=bys.GaussianWishart(np.array([1.1]), 0.5, 3, np.array([[1.8]])))
          model3.update_posterior(posterior=dis.rvs(size=30)[..., np.newaxis])

    .. attribute:: See also:

       - :py:func:`~scipy.stats.norm`

       - :py:func:`~scipy.stats.multivariate_normal`

       - :py:func:`~scipy.stats.gamma`

       - :py:func:`~scipy.stats.wishart`

       - :py:func:`~info.docfunc.GaussianWishart`

    .. attribute:: Logs:

       .. versionadded:: 0.0.5

       -- |signature|
    """
    args_highlighter(kernel, prior)


def Module():
    """
    a flexible neural network base class with enhanced training/inference capabilities.
    this module extends PyTorch's ``nn.Module`` with additional features including:

    - configurable training/inference sessions

    - automatic data type handling

    - built-in training loop with stopping conditions

    - support for both regression and classification tasks

    - generator-based online learning support

    .. attribute:: Logs:

       .. versionadded:: 1.0

       -- |signature|
    """
    ...


def full_connected_neural(structure: list[int], bias: bool = True, dropout: float = None,
                          activation: Union[Callable, list[Callable]] = ReLU,
                          ctype_option: _Ctype = 'float32'):
    """
    a configurable fully connected neural network module with flexible architecture options. This implementation
    provides a multi-layer perceptron (MLP) with customizable layer dimensions, activation functions, dropout, and
    data type specifications. The network can be either statically sized or dynamically initialized with lazy weight
    initialization.

    .. attribute:: Arguments:

       :param list[int] structure: list specifying layer dimensions; its first element can be ``None`` to enable lazy
                                   initialization; e.g. ``[None, 256, 128]`` for lazy input or ``[784, 256, 128]``
                                   for fixed input
       :param Union[Callable, list[Callable]] activation: activation function(s) between layers; can be single function
                                                          or list per layer; ``nn.ReLU``, or ``[nn.ReLU, nn.Sigmoid]``
                                                          for different activation per layer;
       :param bool bias: whether to include bias terms in linear layers; ``True`` as default
       :param Optional[float] dropout: dropout probability (0-1) applied after last hidden layer; ``None`` as default
                                       to disable dropout
       :param _Ctype ctype_option: torch datatype for network parameters; ``'float32'`` as default
       :return: a fully connected neural network
       :rtype: :py:func:`~info.docfunc.Module`

    .. attribute:: Examples:

       .. code-block:: python
          :caption: multi neural network
          :name: multi neural network

          import torch as tch
          from info.net import full_connected_neural
          num_samples, input_size, output_size = 120, 10, 5
          x, y_classification, y_regression = (tch.randn(num_samples, input_size),
                                               tch.randint(0, output_size, (num_samples,)),
                                               tch.randn(num_samples, output_size))
          x_train, x_validation = x[:100], x[100:]
          yc_train, yc_validation = y_classification[:100], y_classification[100:]
          yr_train, yr_validation = y_regression[:100], y_regression[100:]

          # apply on classification task
          model1 = full_connected_neural(structure=[input_size, 40, output_size], activation=tch.nn.ReLU)
          with model1.train_session() as md:
              md.solve(train=x_train, target=yc_train, validation=(x_validation, yc_validation))

          # apply on regression task, with specified configuration
          model2 = full_connected_neural(structure=[None, 40, 50, output_size], bias=False,
                                         activation=[tch.nn.LeakyReLU, tch.nn.Tanh], dropout=0.2)
          with model2.train_session(criterion=tch.nn.MSELoss()) as md:
              md.solve(train=x_train, target=yr_train, validation=(x_validation, yr_validation))

    .. attribute:: Notes:

       this implementation provides a flexible fully connected network that supports:

       - both static and dynamic (lazy) input dimension handling

       - per-layer activation function specification

       - configurable precision through dtype options

       - optional dropout regularization

       - automatic training configuration (SGD optimizer with CrossEntropy loss by default)

       the network uses PyTorch's LazyLinear when input dimension is unspecified (None), which automatically infers
       input size during first forward pass.

    .. attribute:: See Also:

       - :py:class:`~info.docfunc.Module`

    .. attribute:: Logs:

       .. versionadded:: 1.0

       -- |signature|
    """
    args_highlighter(structure, bias, dropout, activation, ctype_option)


def convolutional_neural(conv_structure: list[int], mpl_structure: list[int], activation: Callable = ReLU,
                         in_dimension: int = 2, conv_kernel: dict = None, batch_norm: dict = None,
                         pre_activation: bool = False, pool: dict = None, dropout: float = None,
                         conv_customization: list[dict] = None):
    """
    a configurable convolutional neural network (CNN) module with flexible architecture. This framework provides a
    convolutional neural network architecture comprising configurable convolutional blocks cascaded with a multi-stage
    fully-connected network.  The modular design enables flexible customization of both feature extraction components
    (convolutional operations) and classification modules (MLP layers), supporting both baseline configurations and
    application-specific topological variations through parameterized layer composition.

    .. attribute:: Arguments:

       :param list[int] conv_structure: list specifying the number of output channels for each convolutional block
       :param list[int] mpl_structure: list specifying the layer sizes for the final MLP
       :param Callable activation: global activation function; ``nn.ReLU`` as default
       :param int in_dimension: spatial dimension of input; must be ``1``, ``2``, or ``3``; ``2`` as default to adapt
                                natural images related tasks
       :param dict conv_kernel: parameter dict containing ``'kernel_size'``, ``'stride'``, ``'padding'`` or
                                ``'dilation'``; accepted values can be a positive integer (applied to all dimensions),
                                 or tuple of positive integers specifying per-dimension values matching the input
                                 data's dimensional structure; ``{'kernel_size': 3, 'stride': 1, 'padding': 1}`` as
                                 default configuration
       :param dict batch_norm: batch normalization configuration; ``None`` as default to disable batch normalization;
                               if provided, its accepted value should be a dict with ``'eps'``, ``'momentum'``,
                               ``'affine'``, or ``'track_running_state'`` as keys, and allowable value for its
                               respective key
       :param bool pre_activation: whether to use pre-activation ordering before convolution; ``False`` as default
       :param dict pool: 1-length dict of pooling configuration; key should be one among ``'Max'``,
                         ``'FractionalMax'``, ``'AdaptiveAvg'``, ``'AdaptiveMax'``, ``'Avg'``, ``'LP'``, ``'MaxUn'``,
                         and the value is of the similar form as the ``conv_kernel`` parameter;
                         ``{'Max': {'kernel_size': 2, 'stride': 2}}`` as default to apply conventional max pooling
                         approach
       :param float dropout: dropout probability from 0 to 1; ``None`` as default to disable dropout
       :param list[dict] conv_customization: list of dictionaries to customize each convolutional block's parameters;
                                             each dict can override default conv parameters (from ``activation`` to
                                             ``dropout``); ``None`` as default to apply global configuration; e.g.,
                                             ``[{'pre_activation': True}, {'dropout': 0.4}]`` to specify a
                                             two-convolutional layers with pre-activation the 1st, and 0.4 dropout
                                             the 2nd if the ``conv_structure`` is of ``[16, 32]``
       :return: a convolutional neural network
       :rtype: :py:func:`~info.docfunc.Module`

    .. attribute:: Examples:

       .. code-block:: python
          :caption: convolutional neural network
          :name: convolutional neural network

          import torch as tch
          from info.net import convolutional_neural

          sp1, sp2, nums, n = (128, 128), (64, 64, 32), 20, 10
          x_2d, x_3d, y_c, y_r = (tch.randn(nums, 3, *sp1), tch.randn(nums, 1, *sp2), tch.randint(0, 10, (nums,)),
                                  tch.randn(nums, n))

          # natural image classification task:
          model1 = convolutional_neural(conv_structure=[16, 32], mpl_structure=[128, n])
          with model1.train_session() as md:
              md.solve(train=x_2d, target=y_c, loading_mode='local')

          # 3D image classification task:
          model2 = convolutional_neural(conv_structure=[16, 32], mpl_structure=[128, n], in_dimensions=3)
          with model2.train_session() as md:
              md.solve(train=x_3d, target=y_c, loading_mode='local')

          # online loading for 3D images with customized configuration:
          model3 = convolutional_neural(conv_structure=[16, 32], mpl_structure=[128, n], in_dimensions=3,
                                        pre_activation=True, dropout=0.13)
          with model3.train_session(criterion=tch.nn.HingeEmbeddingLoss()) as md:
              md.solve(train=(_ for _ in x_3d), target=(_ for _ in y_c), stop_conditions={'epochs': 40})

          # or application on regression task:
          model4 = convolutional_neural(conv_structure=[16, 32], mpl_structure=[128, n])
          with model4.train_session(criterion=tch.nn.MSELoss()) as md:
              md.solve(train=x_2d, target=y_r, loading_mode='local')

    .. attribute:: Notes:

       this implementation is featured as:

       - dynamic input dimension handling via lazy layers

       - configurable per-block parameters

       - automatic flattening before MLP

       - default Adam optimizer (lr=0.001) and CrossEntropyLoss

       it employs an MLP-based backend implementation, inheriting its most features such as adaptive capabilities for
       both classification and regression tasks.

    .. attribute:: See Also:

       - :py:class:`~info.docfunc.Module`

       - :py:class:`~info.docfunc.full_connected_neural`

    .. attribute:: Logs:

       .. versionadded:: 1.0

       -- |signature|
    """
    args_highlighter(conv_structure, mpl_structure, activation, in_dimension, conv_kernel, batch_norm,
                     pre_activation, pool, dropout, conv_customization)


def unet(mirrored_channels: list[int], in_dimension: int = 2, activation: Callable = (lambda: ReLU(inplace=True)),
         conv_kernel: dict = None, batch_norm: dict = None, pre_activation: bool = False, pool: dict = None,
         dropout: float = None, export_channel: int = 1):
    """
    a configurable U-Net architecture for semantic segmentation with dynamic dimensionality support. This
    implementation follows the classic U-Net encoder-decoder structure with skip connections, while providing
    extensive customization options through parameterized components.

    .. attribute:: Arguments:

       :param list[int] mirrored_channels: channel dimensions for each level of the encoder-decoder blocks; the
                                           decoder path mirrors the encoder channel structure
       :param int in_dimension: spatial dimension of input; must be ``1``, ``2``, or ``3``; ``2`` as default to adapt
                                natural images related tasks
       :param Callable activation: activation function factory; default uses in-place ReLU for memory efficiency
       :param dict conv_kernel: parameter dict containing ``'kernel_size'``, ``'stride'``, ``'padding'`` or
                                ``'dilation'``; accepted values can be a positive integer (applied to all dimensions),
                                 or tuple of positive integers specifying per-dimension values matching the input
                                 data's dimensional structure; ``{'kernel_size': 3, 'stride': 1, 'padding': 1}`` as
                                 default configuration
       :param dict batch_norm: batch normalization configuration with optional keys; ``None`` as default to disable
                               batch normalization; if provided, its accepted value should be a dict with ``'eps'``,
                               ``'momentum'``, ``'affine'``, or ``'track_running_state'`` as keys, and allowable value
                               for its respective key
       :param bool pre_activation: whether to use pre-activation ordering before convolution; ``False`` as default
       :param dict pool: 1-length dict of pooling configuration; key should be one among ``'Max'``,
                         ``'FractionalMax'``, ``'AdaptiveAvg'``, ``'AdaptiveMax'``, ``'Avg'``, ``'LP'``, ``'MaxUn'``,
                         and the value is of the similar form as the ``conv_kernel`` parameter;
                         ``{'Max': {'kernel_size': 2, 'stride': 2}}`` as default to apply conventional max pooling
                         approach
       :param float dropout: dropout probability from 0 to 1; ``None`` as default to disable dropout
       :param int export_channel: number of output channels; positive integer no greater than ``3``; ``1`` as default
       :return: an U-Net instance
       :rtype: :py:func:`~info.docfunc.Module`

    .. attribute:: Examples:

       .. code-block:: python
          :caption: U-Net demonstration
          :name: U-Net demonstration

          import torch as tch
          from info.net import unet

          # standard 2D U-Net for binary segmentation
          x, y = tch.randn(5, 1, 20, 40), tch.randint(0, 2, (5, 1, 20, 40)).float()
          model1 = unet(mirrored_channels=[64, 128, 256, 512], in_dimensions=2)
          with model1.train_session() as md:
              md.solve(train=x, target=y)

          # 3D U-Net with custom normalization
          x, y = tch.randn(5, 1, 20, 40, 35), tch.randint(0, 2, (5, 1, 20, 40, 35)).float()
          model2 = unet(mirrored_channels=[16, 32], in_dimensions=3, batch_norm={'eps': 1e-6, 'momentum': 0.01},
                        activation=(lambda: tch.nn.LeakyReLU(0.1)))
          with model2.train_session(criterion=net.dice(1e-3)) as md:
              md.solve(train=x, target=y, loading_mode='local')

          # 3D U-Net natively support multimodal fusion
          x_multi, y = tch.randn(5, 4, 20, 40, 35), tch.randint(0, 2, (5, 1, 20, 40, 35)).float()
          model3 = unet(mirrored_channels=[16, 32], in_dimensions=3)
          with model3.train_session() as md:
              md.solve(train=x_multi, target=y)

          # 3D U-Net for multiple segmentations, trained using mixture loss
          x, y_multi = tch.randn(5, 1, 20, 40, 35), tch.randint(0, 2, (5, 3, 20, 40, 35)).float()
          model4 = unet(mirrored_channels=[16, 32], in_dimensions=3, export_channel=3)
          mixture_loss = (lambda m1, m2: 0.9 * dice(1e-3)(m1, m2) + 0.1 * tch.nn.CrossEntropyLoss()(m1, m2))
          with model4.train_session(criterion=_c) as md:
              md.solve(train=x, target=y_multi, loading_mode='local')

    .. attribute:: Notes:

       architectural features:

       - symmetric encoder-decoder structure with skip connection

       - automatic handling of input dimensions (1D/2D/3D)

       - dynamic channel sizing through ``mirrored_channels`` argument

       - lazy initialization for input flexibility

       - nearest-exact interpolation for precise feature map alignment

       default training configuration utilizes Adam optimizer with ``0.001`` learning rate, and dice loss with
       ``1e-5`` smoothing factor; if requires customization, overwrite the ``criterion`` or ``optimizer``
       argument when invoking the train session.

    .. attribute:: See Also:

       - :py:class:`~info.docfunc.Module`

    .. attribute:: Logs:

       .. versionadded:: 1.0

       -- |signature|
    """
    args_highlighter(mirrored_channels, in_dimension, activation, conv_kernel,batch_norm, pre_activation,
                     pool, dropout, export_channel)


def transformer(dimension_model: int, num_heads: int, vocabulary_size: dict[Literal['in', 'out'], int] = None,
                embedding_func: dict[Literal['in', 'out', 'endmost'], Optional[Callable]] = None,
                encoding_meth: Literal['sinusoid', 'trainable', 'relative', 'rotation'] = None,
                encoding_configs: dict = None, dimension_feed_forward: int = 2048, activation: Callable = ReLU,
                num_layers: Union[int, tuple[int, int]] = 6, attn_init: dict = None, attn_forward: dict = None,
                dropout: float = 0.1):
    """
    a highly configurable transformer architecture supporting multiple attention mechanisms and embedding methods.
    this implementation provides dynamic dimensionality handling, flexible positional encoding strategies, and modular
    attention configurations suitable for sequence-to-sequence tasks.

    .. attribute:: Arguments:

       :param int dimension_model: hidden dimension size, must be positive integer
       :param int num_heads: number of attention heads, positive integer; If unable to precisely divide
                             ``dimension_model``, this value will be heuristically adjusted
       :param dict[Literal['in', 'out'], int] vocabulary_size: dictionary specifying input and output vocabulary sizes;
                                                               ``{'in': 10000, 'out': 8000}`` as default
       :param dict[Literal['in', 'out', 'endmost'], Optional[Callable]] embedding_func: custom embedding functions for
                                                                                        input, output, and final layer;
                                                                                        acceptable value is dictionary
                                                                                        containing ``'in'``, ``'out'``
                                                                                        and ``'endmost'`` as keys, and
                                                                                        embedding function as
                                                                                        their respective value; default
                                                                                        configuration uses ``None``
                                                                                        to automatically initialize
                                                                                        the embedding function
       :param Literal['sinusoid', 'trainable', 'relative', 'rotation'] encoding_meth: positional encoding method;
                                                                                      accept value must be one option
                                                                                      among ``'sinusoid'``,
                                                                                      ``'trainable'``, ``'relative'``,
                                                                                      and ``'rotation'``; default uses
                                                                                      ``'sinusoid'`` for canonical
                                                                                      transformer implementation
       :param dict encoding_configs: configuration dict for positional encoding (method-specific parameters); default
                                     configuration uses ``{'max_length': 5000, 'base': 10000}`` for ``'sinusoid'``
                                     encoding, ``{'max_relative': 3}`` for ``'relative'``, and
                                     ``{'theta': 10000.0, 'start_pos': 0}`` for ``'rotation'``
       :param int dimension_feed_forward: dimension of feed forward network; ``2048`` as default
       :param Callable activation: global activation function; ``torch.nn.ReLU`` as default
       :param Union[int, tuple[int, int]] num_layers: encoder and decoder layer counts; support unbalanced encode
                                                      decode architecture via tuple assignment; e.g., ``(6, 3)``
                                                      for unequal encoder and decoder transformer
       :param dict attn_init: initialization parameters for attention layer; standard configuration uses
                              ``{'bias': True, 'add_bias_kv': False, 'add_zero_attn': False, 'batch_first': True}``;
                              as for cross attention, the ``'kdim'`` and ``'vdim'`` will be determined by
                              ``dimension_model`` while ``None`` for self attention in ``'relative'`` and
                              ``'rotation'`` encoding method (``'sinusoid'`` and ``'trainable'`` will be ``None`` in
                              both self and cross); ``'dropout'`` will be adjusted from global dropout
       :param dict attn_forward: configuration passed in attention forward; the standard setting utilizes
                                 ``'need_weights'`` as ``True``, ``'attn_mask'`` as ``None``, ``average_attn_weights``
                                 as ``True``, and ``'is_causal'`` as ``False``; if customized configuration are
                                 provided, the values will be overwrote from default
       :param float dropout: global dropout rate; ``0.1`` as default
       :return: a Transformer model
       :rtype: :py:func:`~info.docfunc.Module`

    .. attribute:: Examples:

       .. code-block:: python
          :caption: transformer demonstration
          :name: transformer demonstration

          import torch as tch
          from info.net import transformer

          batch, seq1, seq2, voc1, voc2 = 32, 20, 15, 10000, 8000
          src, tgt = tch.randint(0, voc1, (batch, seq1)), tch.randint(0, voc2, (batch, seq2))
          src_msk, tgt_msk = tch.randn(src.shape) > 0, tch.randn(tgt.shape) > 0

          # application on basic sequence-to-sequence task (e.g., machine translation):
          model1 = transformer(dimension_model=512, num_heads=8)
          with model1.train_session() as md:
              md.solve(train=(src, src_msk), target=(tgt, tgt_msk))

          # flexibility to support multiple data types input
          src_np, tgt_pt, tgt_msk_gen = src.numpy, tgt, (_ for _ in tgt_msk.clone())
          model2 = transformer(dimension_model=512, num_heads=8)
          with model1.train_session() as md:
              md.solve(train=(src_np, src_msk), target=(tgt_pt, tgt_msk_gen))

          # parameter-reduced memory-efficient model for edge devices, importing locally stored data for training
          model3 = transformer(dimension_model=256, num_heads=4, dimension_feed_forward=1024, num_layers=(4, 2),
                               dropout=0.05)
          with model3.train_session() as md:
              md.solve(train=(src, src_msk), target=(tgt, tgt_msk), loading_mode='local')

          # rotary position embedding to comprehend long-range dependence of sequence
          model4 = transformer(dimension_model=512, num_heads=8, encoding_meth='rotation',
                               encoding_configs={'max_length': 4096, 'theta': 10000.0, 'start_pos': 0})
          with model4.train_session(optimizer=tch.optim.Adam(model3.parameters(), lr=0.005)) as md:
              md.solve(train=(src, src_msk), target=(tgt, tgt_msk))

          # transfer learning using pre-trained embedding function
          emb_func = base_model.from_pretrain(...)
          model5 = transformer(dimension_model=512, num_heads=8, encoding_meth='trainable',
                               embedding_func={'in': emb_func, 'out': None, 'endmost': None})
          with model5.train_session() as md:
              md.solve(train=(src, src_msk), target=(tgt, tgt_msk), stop_conditions={'epochs': 50})

    .. attribute:: Notes:

       architectural features:

       - flexibility on encoding method options

       - dynamic attention mechanism selection

       - configurable encoder-decoder asymmetry

       - expandability for integrating on-going works

    .. attribute:: See Also:

       - `Multi-head Attention <https://pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html>`_

    .. attribute:: Logs:

       .. versionadded:: 1.0

       -- |signature|
    """
    args_highlighter(dimension_model, num_heads, vocabulary_size, embedding_func, encoding_meth,
                     encoding_configs, dimension_feed_forward, activation, num_layers, attn_init, attn_forward,
                     dropout)


if __name__ == '__main__':
    pass
