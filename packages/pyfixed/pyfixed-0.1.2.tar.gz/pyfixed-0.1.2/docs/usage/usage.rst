Usage
=====

Converting to NumPy and mpmath
------------------------------

:py:mod:`!pyfixed` supports conversion to and from the following types:

- :py:class:`!bool`
- :py:class:`!int`
- :py:class:`!float`
- :py:class:`!complex`
- :py:class:`!numpy.integer`
- :py:class:`!numpy.floating`
- :py:class:`!numpy.complexfloating`
- :py:class:`!mpmath.mpf`
- :py:class:`!mpmath.mpc`

Converting to and from native Python types and NumPy is done via the conventional methods:

::

  pyfixed.Fixed(True)
  pyfixed.Fixed(1.0)
  pyfixed.ComplexFixed(1j)
  numpy.single(pyfixed.Fixed(1.5))
  ...

Conversion to mpmath is problematic though, since it forces conversion when performing arithmetic
operations (e.g. ``mpmath.mpf(1) + pyfixed.Fixed(1)`` will convert ``pyfixed.Fixed(1)`` to mpmath).

Therefore, the native conversion can't be implemented, and instead :py:mod:`!pyfixed` provides
:py:func:`!mpmath`, which converts a fixed-point number (:py:mod:`!pyfixed.Fixed` or :py:mod:`!pyfixed.ComplexFixed`)
to mpmath (:py:class:`!mpmath.mpf` or :py:class:`!mpmath.mpc`).

Conversion from mpmath still works the same as regular conversions.

Returned Types
--------------

Unlike C integers and floats, :py:mod:`!pyfixed` can have many configurations of the same bit width.

Therefore, when performing calculations which involve multiple configurations as inputs, an output configuration needs to be determined.

The default logic is as following:

- Any operation taking a single argument will return an output with the input's configuration.
- Any operation taking multiple arguments will return an output with the highest precision configuration.
  If configurations conflict (e.g. one has the highest fraction bits, while the other has the highest integer bits),
  a new configuration is composed such that it has the highest configuration elements.
- Any operation taking multiple arguments that is performed in-place (e.g. ``a += b``) will return an output with the
  configuration of the variable which performs the operation (e.g. the configuration of ``a`` for ``a += b``).
- The returned value is always :py:mod:`!pyfixed.Fixed` or :py:mod:`!pyfixed.ComplexFixed`, even when any of the inputs are floats.

Straying from the defaults are rounding functions (:py:func:`!floor`, :py:func:`!ceil`, :py:func:`!trunc` and :py:func:`!round`),
which round to integers, and return :py:class:`!int` (except for :py:func:`!round` with a ``ndigits`` argument).

.. note::
  Although results are always fixed-point, the calculations themselves don't convert the arguments in order to preserve accuracy
  (unlike ``1.0 + 1``, which will convert ``1`` to :py:class:`!float`).

Rounding Modes
--------------

:py:mod:`!pyfixed` offers 10 rounding modes, as described in :py:class:`pyfixed.fixed.FixedRounding`.

Each rounding mode can be used for regular arithmetics and for the rounding in modulo.

Some functions perform explicit rounding:

- :py:func:`!floor`, :py:func:`!ceil` and :py:func:`!trunc`: round in the specified mode,
  regardless of the current rounding mode.
- :py:func:`!round`: round to integer according to the current rounding mode.
  Note that ``ndigits`` is in base 2, unlike Python's base 10.
- :py:meth:`floordiv` (``//``): divide and floor the result, regardless of the current rounding mode.
  The result is returned as fixed-point.
- :py:meth:`mod` (``%``): divide and return the remainder.
  The rounding mode used is the current modulo rounding mode.
- :py:func:`divmod`: divide and return a rounded result and a remainder.
  The rounding mode used is the current modulo rounding mode.

Comparisons
-----------

Unlike C and NumPy comparisons, and similar to Python and mpmath, :py:mod:`!pyfixed` performs accurate comparisons without casting/converting between types.

| For example, ``numpy.float32(2 ** 25) == 2 ** 25 - 1`` is true, even though the numbers are different.
| That's because C and NumPy convert the integer to :py:class:`!float32`.

Another key difference is complex comparisons - :py:mod:`!pyfixed` allows for ordered comparisons when two components are equal.

| For example, ``pyfixed.ComplexFixed(1 + 1j)`` is greater than ``pyfixed.ComplexFixed(1 - 1j)``, since the real components are equal, and ``1j`` is greater than ``-1j``;
| ``pyfixed.ComplexFixed(1 + 1j)`` is less than ``pyfixed.ComplexFixed(2 + 1j)``, since the imaginary components are equal, and ``1`` is less than ``2``.

However, comparing ``pyfixed.ComplexFixed(1 + 1j)`` and ``pyfixed.ComplexFixed(2 - 1j)`` is unordered, since they don't share a common axis to compare on.

Both :py:class:`!pyfixed.Fixed` and :py:class:`!pyfixed.ComplexFixed` provide the :py:meth:`!cmp` method, which returns the ordering of the compared numbers.

Exceptions and Sticky Flags
---------------------------

| :py:mod:`!pyfixed` supports numeric error exceptions.
| These exceptions are raised when a mathematical error occurs (e.g. division by 0), or when :py:mod:`!pyfixed` can't correctly represent a value (e.g. overflow).
| All exceptions can be disabled (i.e. ignored).

| :py:mod:`!pyfixed` also offers sticky flags, which are silent exceptions - they aren't raised, but rather set a flag, which can later be read by the user.
| Note that the sticky flags are only cleared when modifying the current state, or via :py:func:`pyfixed.fixed.get_sticky`.

There are some special cases regarding exceptions:

- :py:meth:`!cmp` performs a lossless comparison, so it won't raise overflow or underflow, and it handles undefined scenarios by returning unordered.
- All rounding functions: never raise overflow, underflow and undefined, as they round a valid value and return an integer.
  :py:func:`!round` might raise overflow when ``ndigits`` is given.
- :py:meth:`!floordiv` never raises underflow, as the result is floored.
- :py:meth:`!mod` and :py:func:`!divmod` (and reverse variants) raise undefined when
  given float values that are too small/big (``fixed % float`` / ``float % float``).
  The division in :py:func:`!divmod` and :py:func:`!rdivmod` also ignore underflow (like :py:meth:`!floordiv`).
- :py:class:`!pyfixed.ComplexFixed` returns :py:obj:`!NotImplemented` when given complex floats,
  as these values cannot be accurately computed without using large fixed-point configurations
  (e.g. ``Fixed<149, 127, True>`` to support ``float32``).
