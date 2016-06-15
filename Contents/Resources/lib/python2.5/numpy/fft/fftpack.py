"""
Discrete Fourier Transforms - FFT.py

The underlying code for these functions is an f2c translated and modified
version of the FFTPACK routines.

fft(a, n=None, axis=-1)
ifft(a, n=None, axis=-1)
rfft(a, n=None, axis=-1)
irfft(a, n=None, axis=-1)
hfft(a, n=None, axis=-1)
ihfft(a, n=None, axis=-1)
fftn(a, s=None, axes=None)
ifftn(a, s=None, axes=None)
rfftn(a, s=None, axes=None)
irfftn(a, s=None, axes=None)
fft2(a, s=None, axes=(-2,-1))
ifft2(a, s=None, axes=(-2, -1))
rfft2(a, s=None, axes=(-2,-1))
irfft2(a, s=None, axes=(-2, -1))
"""
__all__ = ['fft','ifft', 'rfft', 'irfft', 'hfft', 'ihfft', 'rfftn',
           'irfftn', 'rfft2', 'irfft2', 'fft2', 'ifft2', 'fftn', 'ifftn',
           'refft', 'irefft','refftn','irefftn', 'refft2', 'irefft2']

from numpy.core import asarray, zeros, swapaxes, shape, conjugate, \
     take
import fftpack_lite as fftpack
from helper import *

_fft_cache = {}
_real_fft_cache = {}

def _raw_fft(a, n=None, axis=-1, init_function=fftpack.cffti,
             work_function=fftpack.cfftf, fft_cache = _fft_cache ):
    a = asarray(a)

    if n is None:
        n = a.shape[axis]

    if n < 1:
        raise ValueError("Invalid number of FFT data points (%d) specified." % n)

    try:
        wsave = fft_cache[n]
    except(KeyError):
        wsave = init_function(n)
        fft_cache[n] = wsave

    if a.shape[axis] != n:
        s = list(a.shape)
        if s[axis] > n:
            index = [slice(None)]*len(s)
            index[axis] = slice(0,n)
            a = a[index]
        else:
            index = [slice(None)]*len(s)
            index[axis] = slice(0,s[axis])
            s[axis] = n
            z = zeros(s, a.dtype.char)
            z[index] = a
            a = z

    if axis != -1:
        a = swapaxes(a, axis, -1)
    r = work_function(a, wsave)
    if axis != -1:
        r = swapaxes(r, axis, -1)
    return r


def fft(a, n=None, axis=-1):
    """
    Compute the one-dimensional discrete Fourier Transform

    This function computes the one-dimensional *n*-point discrete Fourier
    Transform (DFT) with the efficient Fast Fourier Transform (FFT) algorithm. [CT]

    Parameters
    ----------
    a : array_like
        Input array, can be complex
    n : int, optional
        Length of the transformed axis of the output.
        If `n` is smaller than the length of the input, the input is cropped.
        If it is larger, the input is padded with zeros.  If `n` is not given,
        the length of the input (along the axis specified by `axis`) is used.
    axis : int, optional
        Axis over which to compute the FFT.  If not given, the last axis is
        used.

    Returns
    -------
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axis
        indicated by `axis`, or the last one if `axis` is not specified.

    Raises
    ------
    IndexError
        if `axes` is larger than the last axis of `a`

    See Also
    --------
    numpy.fft : for definition of the DFT and conventions used
    ifft : The inverse of `fft`.
    fft2 : The two-dimensional FFT.
    fftn : The *n*-dimensional FFT.
    rfftn : The *n*-dimensional FFT of real input.
    fftfreq : Frequency bins for given FFT parameters.

    Notes
    -----

    FFT (Fast Fourier Transform) refers to a way the discrete Fourier
    Transform (DFT) can be calculated efficiently, by using symmetries in the
    calculated terms.  The symmetry is highest when `n` is a power of 2, and
    the transform is therefore most efficient for these sizes.

    The DFT is defined, with the conventions used in this implementation, in
    the documentation for the `numpy.fft` module.

    References
    ----------
    .. [CT] Cooley, James W., and John W. Tukey, 1965, "An algorithm for the
            machine calculation of complex Fourier series," *Math. Comput.*
            19: 297-301.

    Examples
    --------

    >>> from numpy import arange, pi, exp
    >>> from numpy.fft import fft
    >>> fft(exp(2j*pi*arange(8)/8))
    array([ -3.44505240e-16 +1.14383329e-17j,
             8.00000000e+00 -5.71092652e-15j,
             2.33482938e-16 +1.22460635e-16j,
             1.64863782e-15 +1.77635684e-15j,
             9.95839695e-17 +2.33482938e-16j,
             0.00000000e+00 +1.66837030e-15j,
             1.14383329e-17 +1.22460635e-16j,
             -1.64863782e-15 +1.77635684e-15j])


    >>> from numpy.fft import fft, fftfreq
    >>> import matplotlib.pyplot as plt
    >>> t = np.arange(256)
    >>> sp = fft(np.sin(t))
    >>> freq = fftfreq(t.shape[-1])
    >>> plt.plot(freq, sp.real, freq, sp.imag)
    >>> plt.show()

    In this example, real input has an FFT which is Hermitian, i.e., symmetric
    in the real part and anti-symmetric in the imaginary part, as described in
    the `numpy.fft` documentation.

    """

    return _raw_fft(a, n, axis, fftpack.cffti, fftpack.cfftf, _fft_cache)


def ifft(a, n=None, axis=-1):
    """
    Compute the one-dimensional inverse discrete Fourier Transform

    This function computes the inverse of the one-dimensional *n*-point
    discrete Fourier transform computed by `fft`.  In other words,
    `ifft(fft(a)) == a` to within numerical accuracy.
    For a general description of the algorithm and definitions,
    see `numpy.fft`.

    The input should be ordered in the same way as is returned by `fft`,
    i.e., `a[0]` should contain the zero frequency term,
    `a[1:n/2+1]` should contain the positive-frequency terms, and
    `a[n/2+1:]` should contain the negative-frequency terms, in order of
    decreasingly negative frequency.  See `numpy.fft` for details.

    Parameters
    ----------
    a : array_like
        Input array, can be complex
    n : int, optional
        Length of the transformed axis of the output.
        If `n` is smaller than the length of the input, the input is cropped.
        If it is larger, the input is padded with zeros.  If `n` is not given,
        the length of the input (along the axis specified by `axis`) is used.
        See notes about padding issues.
    axis : int, optional
        Axis over which to compute the inverse DFT.  If not given, the last
        axis is used.

    Returns
    -------
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axis
        indicated by `axis`, or the last one if `axis` is not specified.

    Raises
    ------
    IndexError
        if `axes` is larger than the last axis of `a`

    See Also
    --------
    numpy.fft : An introduction, with definitions and general explanations
    fft : The one-dimensional (forward) FFT, of which `ifft` is the inverse
    ifft2 : The two-dimensional inverse FFT
    ifftn : The n-dimensional inverse FFT

    Notes
    -----

    If the input parameter `n` is larger than the size of the input, the input
    is padded by appending zeros at the end.  Even though this is the common
    approach, it might lead to surprising results.  If a different padding is
    desired, it must be performed before calling `ifft`.

    Examples
    --------

    >>> from numpy.fft import ifft
    >>> ifft([0, 4, 0, 0])
    array([ 1.+0.j,  0.+1.j, -1.+0.j,  0.-1.j])

    >>> from numpy import exp, pi, arange, zeros
    >>> import matplotlib.pyplot as plt
    >>> t = arange(400)
    >>> n = zeros((400,), dtype=complex)
    >>> n[40:60] = exp(1j*np.random.uniform(0, 2*pi, (20,)))
    >>> s = np.fft.ifft(n)
    >>> plt.plot(t, s.real, 'b-', t, s.imag, 'r--')
    >>> plt.legend(('real', 'imaginary'))
    >>> plt.show()

    Creates and plots a band-limited signal with random phases.

    """

    a = asarray(a).astype(complex)
    if n is None:
        n = shape(a)[axis]
    return _raw_fft(a, n, axis, fftpack.cffti, fftpack.cfftb, _fft_cache) / n


def rfft(a, n=None, axis=-1):
    """
    Compute the one-dimensional discrete Fourier Transform for real input.

    This function computes the one-dimensional *n*-point discrete Fourier
    Transform (DFT) of a real-valued array by means of an efficient algorithm
    called the Fast Fourier Transform (FFT).

    Parameters
    ----------
    a : array_like
        Input array
    n : int, optional
        Number of points along transformation axis in the input to use.
        If `n` is smaller than the length of the input, the input is cropped.
        If it is larger, the input is padded with zeros.  If `n` is not given,
        the length of the input (along the axis specified by `axis`) is used.
    axis : int, optional
        Axis over which to compute the FFT.  If not given, the last axis is
        used.

    Returns
    -------
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axis
        indicated by `axis`, or the last one if `axis` is not specified.
        The length of the transformed axis is `n/2+1`.

    Raises
    ------
    IndexError
        if `axis` is larger than the last axis of `a`

    See Also
    --------
    numpy.fft : for definition of the DFT and conventions used
    irfft : The inverse of `rfft`
    fft : The one-dimensional FFT of general (complex) input
    fftn : The *n*-dimensional FFT.
    rfftn : The *n*-dimensional FFT of real input.

    Notes
    -----

    When the DFT is computed for purely real input, the output is
    Hermite-symmetric, i.e. the negative frequency terms are just the complex
    conjugates of the corresponding positive-frequency terms, and the
    negative-frequency terms are therefore redundant.  This function does not
    compute the negative frequency terms, and the length of the transformed
    axis of the output is therefore `n/2+1`.

    When `A = rfft(a)`, `A[0]` contains the zero-frequency term, which must be
    purely real due to the Hermite symmetry.

    If `n` is even, `A[-1]` contains the term for frequencies `n/2` and `-n/2`,
    and must also be purely real.  If `n` is odd, `A[-1]` contains the term
    for frequency `A[(n-1)/2]`, and is complex in the general case.

    If the input `a` contains an imaginary part, it is silently discarded.

    Examples
    --------

    >>> from numpy.fft import fft, rfft
    >>> fft([0, 1, 0, 0])
    array([ 1.+0.j,  0.-1.j, -1.+0.j,  0.+1.j])
    >>> rfft([0, 1, 0, 0])
    array([ 1.+0.j,  0.-1.j, -1.+0.j])

    Notice how the final element of the `fft` output is the complex conjugate
    of the second element, for real input.  For `rfft`, this symmetry is
    exploited to compute only the nonnegative frequency terms.

    """

    a = asarray(a).astype(float)
    return _raw_fft(a, n, axis, fftpack.rffti, fftpack.rfftf, _real_fft_cache)


def irfft(a, n=None, axis=-1):
    """
    Compute the inverse of the n-point DFT for real input.

    This function computes the inverse of the one-dimensional *n*-point
    discrete Fourier Transform of real input computed by `rfft`.
    In other words, `irfft(rfft(a), len(a)) == a` to within numerical accuracy.
    (See Notes below for why `len(a)` is necessary here.)

    The input is expected to be in the form returned by `rfft`, i.e. the
    real zero-frequency term followed by the complex positive frequency terms
    in order of increasing frequency.  Since the discrete Fourier Transform of
    real input is Hermite-symmetric, the negative frequency terms are taken
    to be the complex conjugates of the corresponding positive frequency terms.

    Parameters
    ----------
    a : array_like
        Input array
    n : int, optional
        Length of the transformed axis of the output.
        For `n` output points, `n/2+1` input points are necessary.  If the
        input is longer than this, it is cropped.  If it is shorter than this,
        it is padded with zeros.  If `n` is not given, it is determined from
        the length of the input (along the axis specified by `axis`)
        as explained below.
    axis : int, optional
        Axis over which to compute the inverse FFT.

    Returns
    -------
    out : real ndarray
        The truncated or zero-padded input, transformed along the axis
        indicated by `axis`, or the last one if `axis` is not specified.
        The length of the transformed axis is `n`, or, if `n` is not given,
        `2*(m-1)` where `m` is the length of the transformed axis of the input.
        To get an odd number of output points, `n` must be specified.

    Raises
    ------
    IndexError
        if `axis` is larger than the last axis of `a`

    See Also
    --------
    numpy.fft : for definition of the DFT and conventions used
    rfft : The one-dimensional FFT of real input, of which `irfft` is inverse.
    fft : The one-dimensional FFT
    irfft2 : The inverse of the two-dimensional FFT of real input.
    irfftn : The inverse of the *n*-dimensional FFT of real input.

    Notes
    -----

    Returns the real valued `n`-point inverse discrete Fourier transform
    of `a`, where `a` contains the nonnegative frequency terms of a
    Hermite-symmetric sequence. `n` is the length of the result, not the
    input.

    If you specify an `n` such that `a` must be zero-padded or truncated, the
    extra/removed values will be added/removed at high frequencies. One can
    thus resample a series to `m` points via Fourier interpolation by:
    `a_resamp = irfft(rfft(a), m)`.


    Examples
    --------

    >>> from numpy.fft import ifft, irfft
    >>> ifft([1, -1j, -1, 1j])
    array([ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j])
    >>> irfft([1, -1j, -1])
    array([ 0.,  1.,  0.,  0.])

    Notice how the last term in the input to the ordinary `ifft` is the
    complex conjugate of the second term, and the output has zero imaginary
    part everywhere.  When calling `irfft`, the negative frequencies are not
    specified, and the output array is purely real.

    """

    a = asarray(a).astype(complex)
    if n is None:
        n = (shape(a)[axis] - 1) * 2
    return _raw_fft(a, n, axis, fftpack.rffti, fftpack.rfftb,
                    _real_fft_cache) / n


def hfft(a, n=None, axis=-1):
    """
    Compute the fft of a signal which spectrum has Hermitian symmetry.

    Parameters
    ----------
    a : array
        input array
    n : int
        length of the hfft
    axis : int
        axis over which to compute the hfft

    See also
    --------
    rfft
    ihfft

    Notes
    -----
    These are a pair analogous to rfft/irfft, but for the
    opposite case: here the signal is real in the frequency domain and has
    Hermite symmetry in the time domain. So here it's hermite_fft for which
    you must supply the length of the result if it is to be odd.

    ihfft(hfft(a), len(a)) == a
    within numerical accuracy.

    """

    a = asarray(a).astype(complex)
    if n is None:
        n = (shape(a)[axis] - 1) * 2
    return irfft(conjugate(a), n, axis) * n


def ihfft(a, n=None, axis=-1):
    """
    Compute the inverse fft of a signal whose spectrum has Hermitian symmetry.

    Parameters
    ----------
    a : array_like
        Input array.
    n : int, optional
        Length of the ihfft.
    axis : int, optional
        Axis over which to compute the ihfft.

    See also
    --------
    rfft, hfft

    Notes
    -----
    These are a pair analogous to rfft/irfft, but for the
    opposite case: here the signal is real in the frequency domain and has
    Hermite symmetry in the time domain. So here it's hermite_fft for which
    you must supply the length of the result if it is to be odd.

    ihfft(hfft(a), len(a)) == a
    within numerical accuracy.

    """

    a = asarray(a).astype(float)
    if n is None:
        n = shape(a)[axis]
    return conjugate(rfft(a, n, axis))/n


def _cook_nd_args(a, s=None, axes=None, invreal=0):
    if s is None:
        shapeless = 1
        if axes is None:
            s = list(a.shape)
        else:
            s = take(a.shape, axes)
    else:
        shapeless = 0
    s = list(s)
    if axes is None:
        axes = range(-len(s), 0)
    if len(s) != len(axes):
        raise ValueError, "Shape and axes have different lengths."
    if invreal and shapeless:
        s[axes[-1]] = (s[axes[-1]] - 1) * 2
    return s, axes


def _raw_fftnd(a, s=None, axes=None, function=fft):
    a = asarray(a)
    s, axes = _cook_nd_args(a, s, axes)
    itl = range(len(axes))
    itl.reverse()
    for ii in itl:
        a = function(a, n=s[ii], axis=axes[ii])
    return a


def fftn(a, s=None, axes=None):
    """
    Compute the N-dimensional discrete Fourier Transform

    This function computes the *N*-dimensional discrete Fourier Transform over
    any number of axes in an *M*-dimensional array by means of the Fast Fourier
    Transform (FFT).

    Parameters
    ----------
    a : array_like
        Input array, can be complex
    s : sequence of ints, optional
        Shape (length of each transformed axis) of the output
        (`s[0]` refers to axis 0, `s[1]` to axis 1, etc.).
        This corresponds to `n` for `fft(x, n)`.
        Along any axis, if the given shape is smaller than that of the input,
        the input is cropped.  If it is larger, the input is padded with zeros.
        if `s` is not given, the shape of the input (along the axes specified
        by `axes`) is used.
    axes : sequence of ints, optional
        Axes over which to compute the FFT.  If not given, the last `len(s)`
        axes are used, or all axes if `s` is also not specified.
        Repeated indices in `axes` means that the transform over that axis is
        performed multiple times.

    Returns
    -------
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axes
        indicated by `axes`, or by a combination of `s` and `a`,
        as explained in the parameters section above.

    Raises
    ------
    ValueError
        if `s` and `axes` have different length.
    IndexError
        if an element of `axes` is larger than than the number of axes of `a`.

    See Also
    --------
    numpy.fft : Overall view of discrete Fourier transforms, with definitions
        and conventions used.
    ifftn : The inverse of `fftn`, the inverse *n*-dimensional FFT.
    fft : The one-dimensional FFT, with definitions and conventions used.
    rfftn : The *n*-dimensional FFT of real input.
    fft2 : The two-dimensional FFT.
    fftshift : shifts zero-frequency terms to centre of array

    Notes
    -----

    The output, analogously to `fft`, contains the term for zero frequency in
    the low-order corner of all axes, the positive frequency terms in the
    first half of all axes, the term for the Nyquist frequency in the middle
    of all axes and the negative frequency terms in the second half of all
    axes, in order of decreasingly negative frequency.

    See `numpy.fft` for details, definitions and conventions used.

    Examples
    --------
    >>> from numpy import mgrid
    >>> from numpy.fft import fftn
    >>> a = mgrid[:3,:3,:3][0]
    >>> fftn(a, axes=(1,2))
    array([[[  0.+0.j,   0.+0.j,   0.+0.j],
            [  0.+0.j,   0.+0.j,   0.+0.j],
            [  0.+0.j,   0.+0.j,   0.+0.j]],
           [[  9.+0.j,   0.+0.j,   0.+0.j],
            [  0.+0.j,   0.+0.j,   0.+0.j],
            [  0.+0.j,   0.+0.j,   0.+0.j]],
           [[ 18.+0.j,   0.+0.j,   0.+0.j],
            [  0.+0.j,   0.+0.j,   0.+0.j],
            [  0.+0.j,   0.+0.j,   0.+0.j]]])
    >>> fftn(a, (2,2), axes=(0,1))
    array([[[ 2.+0.j,  2.+0.j,  2.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j]],
           [[-2.+0.j, -2.+0.j, -2.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j]]])


    >>> from numpy import meshgrid, pi, arange, sin, cos, log, abs
    >>> from numpy.fft import fftn, fftshift
    >>> import matplotlib.pyplot as plt
    >>> [X, Y] = np.meshgrid(2*pi*arange(200)/12, 2*pi*arange(200)/34)
    >>> S = np.sin(X) + np.cos(Y) + np.random.uniform(0, 1, X.shape)
    >>> FS = np.fft.fftn(S)
    >>> plt.imshow(np.log(np.abs(fftshift(FS))**2))
    >>> plt.show()

    """

    return _raw_fftnd(a,s,axes,fft)

def ifftn(a, s=None, axes=None):
    """
    Compute the N-dimensional inverse discrete Fourier Transform

    This function computes the inverse of the N-dimensional discrete
    Fourier Transform over any number of axes in an M-dimensional array by
    means of the Fast Fourier Transform (FFT).  In other words,
    `ifftn(fftn(a)) == a` to within numerical accuracy.
    For a description of the definitions and conventions used, see `numpy.fft`.

    The input, analogously to `ifft`, should be ordered in the same way as is
    returned by `fftn`, i.e. it should have the term for zero frequency
    in all axes in the low-order corner, the positive frequency terms in the
    first half of all axes, the term for the Nyquist frequency in the middle
    of all axes and the negative frequency terms in the second half of all
    axes, in order of decreasingly negative frequency.

    Parameters
    ----------
    a : array_like
        Input array, can be complex
    s : sequence of ints, optional
        Shape (length of each transformed axis) of the output
        (`s[0]` refers to axis 0, `s[1]` to axis 1, etc.).
        This corresponds to `n` for `ifft(x, n)`.
        Along any axis, if the given shape is smaller than that of the input,
        the input is cropped.  If it is larger, the input is padded with zeros.
        if `s` is not given, the shape of the input (along the axes specified
        by `axes`) is used.  See notes for issue on ifft zero padding.
    axes : sequence of ints, optional
        Axes over which to compute the IFFT.  If not given, the last `len(s)`
        axes are used, or all axes if `s` is also not specified.
        Repeated indices in `axes` means that the inverse transform over that
        axis is performed multiple times.

    Returns
    -------
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axes
        indicated by `axes`, or by a combination of `s` or `a`,
        as explained in the parameters section above.

    Raises
    ------
    ValueError
        if `s` and `axes` have different length.
    IndexError
        if an element of `axes` is larger than than the number of axes of `a`.

    See Also
    --------
    numpy.fft : Overall view of discrete Fourier transforms, with definitions
         and conventions used.
    fftn : The forward *n*-dimensional FFT, of which `ifftn` is the inverse.
    ifft : The one-dimensional inverse FFT.
    ifft2 : The two-dimensional inverse FFT.
    ifftshift : undoes `fftshift`, shifts zero-frequency terms to beginning
        of array

    Notes
    -----

    See `numpy.fft` for definitions and conventions used.

    Zero-padding, analogously with `ifft`, is performed by appending zeros to
    the input along the specified dimension.  Although this is the common
    approach, it might lead to surprising results.  If another form of zero
    padding is desired, it must be performed before `ifftn` is called.

    Examples
    --------
    >>> from numpy import eye
    >>> from numpy.fft import ifftn, fftn
    >>> a = eye(4)
    >>> ifftn(fftn(a, axes=(0,)),axes=(1,))
    array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
           [ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j],
           [ 0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
           [ 0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j]])

    >>> from numpy import zeros, exp
    >>> from numpy.random import uniform
    >>> from numpy.fft import ifftn
    >>> import matplotlib.pyplot as plt
    >>> n = np.zeros((200,200), dtype=complex)
    >>> n[60:80,20:40] = exp(1j*uniform(0, 2*pi, (20,20)))
    >>> im = np.fft.ifftn(n).real
    >>> plt.imshow(im)
    >>> plt.show()

    Creates and plots an image with band-limited frequency content

    """

    return _raw_fftnd(a, s, axes, ifft)


def fft2(a, s=None, axes=(-2,-1)):
    """
    Compute the 2-dimensional discrete Fourier Transform

    This function computes the *n*-dimensional discrete Fourier Transform
    over any axes in an *M*-dimensional array by means of the
    Fast Fourier Transform (FFT).  By default, the transform is computed over
    the last two axes of the input array, i.e., a 2-dimensional FFT.

    Parameters
    ----------
    a : array_like
        Input array, can be complex
    s : sequence of ints, optional
        Shape (length of each transformed axis) of the output
        (`s[0]` refers to axis 0, `s[1]` to axis 1, etc.).
        This corresponds to `n` for `fft(x, n)`.
        Along each axis, if the given shape is smaller than that of the input,
        the input is cropped.  If it is larger, the input is padded with zeros.
        if `s` is not given, the shape of the input (along the axes specified
        by `axes`) is used.
    axes : sequence of ints, optional
        Axes over which to compute the FFT.  If not given, the last 2
        axes are used.  A repeated index in `axes` means the transform over
        that axis is performed multiple times.  A one-element sequence means
        that a one-dimensional FFT is performed.

    Returns
    -------
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axes
        indicated by `axes`, or the last two axes if `axes` is not given.

    Raises
    ------
    ValueError
        if `s` and `axes` have different length, or
        `axes` not given and `len(s) != 2`
    IndexError
        if an element of `axes` is larger than than the number of axes of `a`.

    See Also
    --------
    numpy.fft : Overall view of discrete Fourier transforms, with definitions
         and conventions used.
    ifft2 : The inverse two-dimensional FFT
    fft : The one-dimensional FFT
    fftn : The *n*-dimensional FFT
    fftshift : shifts zero-frequency terms to centre of array.
        For two-dimensional input, swaps first and third quadrants, and second
        and fourth quadrants.

    Notes
    -----

    `fft2` is just `fftn` with a different default for `axes`.

    The output, analogously to `fft`, contains the term for zero frequency in
    the low-order corner of the transformed axes, the positive frequency terms
    in the first half of these axes, the term for the Nyquist frequency in the
    middle of the axes and the negative frequency terms in the second half of
    the axes, in order of decreasingly negative frequency.

    See `fftn` for details and a plotting example, and `numpy.fft` for
    definitions and conventions used.


    Examples
    --------
    >>> from numpy import mgrid
    >>> from numpy.fft import fft2
    >>> a = mgrid[:5, :5][0]
    >>> fft2(a)
    array([[  0.+0.j,   0.+0.j,   0.+0.j,   0.+0.j,   0.+0.j],
           [  5.+0.j,   0.+0.j,   0.+0.j,   0.+0.j,   0.+0.j],
           [ 10.+0.j,   0.+0.j,   0.+0.j,   0.+0.j,   0.+0.j],
           [ 15.+0.j,   0.+0.j,   0.+0.j,   0.+0.j,   0.+0.j],
           [ 20.+0.j,   0.+0.j,   0.+0.j,   0.+0.j,   0.+0.j]])

    """

    return _raw_fftnd(a,s,axes,fft)


def ifft2(a, s=None, axes=(-2,-1)):
    """
    Compute the 2-dimensional inverse discrete Fourier Transform

    This function computes the inverse of the 2-dimensional discrete Fourier
    Transform over any number of axes in an M-dimensional array by means of
    the Fast Fourier Transform (FFT).  In other words, `ifft2(fft2(a)) == a`
    to within numerical accuracy.  By default, the inverse transform is
    computed over the last two axes of the input array.

    The input, analogously to `ifft`, should be ordered in the same way as is
    returned by `fft2`, i.e. it should have the term for zero frequency
    in the low-order corner of the two axes, the positive frequency terms in
    the first half of these axes, the term for the Nyquist frequency in the
    middle of the axes and the negative frequency terms in the second half of
    both axes, in order of decreasingly negative frequency.

    Parameters
    ----------
    a : array_like
        Input array, can be complex
    s : sequence of ints, optional
        Shape (length of each axis) of the output (`s[0]` refers to axis 0,
        `s[1]` to axis 1, etc.).  This corresponds to `n` for `ifft(x, n)`.
        Along each axis, if the given shape is smaller than that of the input,
        the input is cropped.  If it is larger, the input is padded with zeros.
        if `s` is not given, the shape of the input (along the axes specified
        by `axes`) is used.  See notes for issue on ifft zero padding.
    axes : sequence of ints, optional
        Axes over which to compute the FFT.  If not given, the last 2
        axes are used.  A repeated index in `axes` means the transform over
        that axis is performed multiple times.  A one-element sequence means
        that a one-dimensional FFT is performed.

    Returns
    -------
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axes
        indicated by `axes`, or the last two axes if `axes` is not given.

    Raises
    ------
    ValueError
        if `s` and `axes` have different length, or
        `axes` not given and `len(s) != 2`
    IndexError
        if an element of `axes` is larger than than the number of axes of `a`.

    See Also
    --------
    numpy.fft : Overall view of discrete Fourier transforms, with definitions
         and conventions used.
    fft2 : The forward 2-dimensional FFT, of which `ifft2` is the inverse.
    ifftn : The inverse of the *n*-dimensional FFT.
    fft : The one-dimensional FFT
    ifft : The one-dimensional inverse FFT.

    Notes
    -----

    `ifft2` is just `ifftn` with a different default for `axes`.

    See `ifftn` for details and a plotting example, and `numpy.fft` for
    definition and conventions used.

    Zero-padding, analogously with `ifft`, is performed by appending zeros to
    the input along the specified dimension.  Although this is the common
    approach, it might lead to surprising results.  If another form of zero
    padding is desired, it must be performed before `ifft2` is called.

    Examples
    --------
    >>> from numpy import eye
    >>> from numpy.fft import ifft2
    >>> a = 4*eye(4)
    >>> ifft2(a)
    array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
           [ 0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j],
           [ 0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
           [ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j]])

    """

    return _raw_fftnd(a, s, axes, ifft)


def rfftn(a, s=None, axes=None):
    """
    Compute the N-dimensional discrete Fourier Transform for real input.

    This function computes the N-dimensional discrete Fourier Transform over
    any number of axes in an M-dimensional real array by means of the Fast
    Fourier Transform (FFT).  By default, all axes are transformed, with the
    real transform performed over the last axis, while the remaining
    transforms are complex.

    Parameters
    ----------
    a : array_like
        Input array, taken to be real
    s : sequence of ints, optional
        Shape (length along each transformed axis) to use from the input.
        (`s[0]` refers to axis 0, `s[1]` to axis 1, etc.).
        The final element of `s` corresponds to `n` for `rfft(x, n)`, while
        for the remaining axes, it corresponds to `n` for `fft(x, n)`.
        Along any axis, if the given shape is smaller than that of the input,
        the input is cropped.  If it is larger, the input is padded with zeros.
        if `s` is not given, the shape of the input (along the axes specified
        by `axes`) is used.
    axes : sequence of ints, optional
        Axes over which to compute the FFT.  If not given, the last `len(s)`
        axes are used, or all axes if `s` is also not specified.

    Returns
    -------
    out : complex ndarray
        The truncated or zero-padded input, transformed along the axes
        indicated by `axes`, or by a combination of `s` and `a`,
        as explained in the parameters section above.
        The length of the last axis transformed will be `s[-1]//2+1`,
        while the remaining transformed axes will have lengths according to
        `s`, or unchanged from the input.

    Raises
    ------
    ValueError
        if `s` and `axes` have different length.
    IndexError
        if an element of `axes` is larger than than the number of axes of `a`.

    See Also
    --------
    irfftn : The inverse of `rfftn`, i.e. the inverse of the n-dimensional FFT
         of real input.
    fft : The one-dimensional FFT, with definitions and conventions used.
    rfft : The one-dimensional FFT of real input.
    fftn : The n-dimensional FFT.
    rfft2 : The two-dimensional FFT of real input.

    Notes
    -----

    The transform for real input is performed over the last transformation
    axis, as by `rfft`, then the transform over the remaining axes is
    performed as by `fftn`.  The order of the output is as for `rfft` for the
    final transformation axis, and as for `fftn` for the remaining
    transformation axes.

    See `fft` for details, definitions and conventions used.

    Examples
    --------
    >>> from numpy import ones
    >>> from numpy.fft import rfftn
    >>> a = ones((3,3,3))
    >>> rfftn(a)
    array([[[ 27.+0.j,   0.+0.j],
            [  0.+0.j,   0.+0.j],
            [  0.+0.j,   0.+0.j]],
           [[  0.+0.j,   0.+0.j],
            [  0.+0.j,   0.+0.j],
            [  0.+0.j,   0.+0.j]],
           [[  0.+0.j,   0.+0.j],
            [  0.+0.j,   0.+0.j],
            [  0.+0.j,   0.+0.j]]])
    >>> rfftn(a, axes=(2,0))
    array([[[ 9.+0.j,  0.+0.j,  0.+0.j],
            [ 9.+0.j,  0.+0.j,  0.+0.j],
            [ 9.+0.j,  0.+0.j,  0.+0.j]],
           [[ 0.+0.j,  0.+0.j,  0.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j],
            [ 0.+0.j,  0.+0.j,  0.+0.j]]])

    """

    a = asarray(a).astype(float)
    s, axes = _cook_nd_args(a, s, axes)
    a = rfft(a, s[-1], axes[-1])
    for ii in range(len(axes)-1):
        a = fft(a, s[ii], axes[ii])
    return a

def rfft2(a, s=None, axes=(-2,-1)):
    """
    Compute the 2-dimensional fft of a real array.

    Parameters
    ----------
    a : array (real)
        input array
    s : sequence (int)
        shape of the fft
    axis : int
        axis over which to compute the fft

    Notes
    -----
    The 2-D fft of the real valued array a. This is really just rfftn with
    different default behavior.

    """

    return rfftn(a, s, axes)

def irfftn(a, s=None, axes=None):
    """
    Compute the inverse of the N-dimensional FFT of real input.

    This function computes the inverse of the N-dimensional discrete
    Fourier Transform for real input over any number of axes in an
    M-dimensional array by means of the Fast Fourier Transform (FFT).  In
    other words, `irfftn(rfftn(a), a.shape) == a` to within numerical accuracy.
    (The `a.shape` is necessary like `len(a)` is for `irfft`, and for the same
    reason.)

    The input should be ordered in the same way as is returned by `rfftn`,
    i.e. as for `irfft` for the final transformation axis, and as for `ifftn`
    along all the other axes.

    Parameters
    ----------
    a : array_like
        Input array.
    s : sequence of ints, optional
        Shape (length of each transformed axis) of the output
        (`s[0]` refers to axis 0, `s[1]` to axis 1, etc.).  `s` is also the
        number of input points used along this axis, except for the last axis,
        where `s[-1]//2+1` points of the input are used.
        Along any axis, if the shape indicated by `s` is smaller than that of
        the input, the input is cropped.  If it is larger, the input is padded
        with zeros.  if `s` is not given, the shape of the input (along the
        axes specified by `axes`) is used.
    axes : sequence of ints, optional
        Axes over which to compute the inverse FFT.  If not given, the last
        `len(s)` axes are used, or all axes if `s` is also not specified.
        Repeated indices in `axes` means that the inverse transform over that
        axis is performed multiple times.

    Returns
    -------
    out : real ndarray
        The truncated or zero-padded input, transformed along the axes
        indicated by `axes`, or by a combination of `s` or `a`,
        as explained in the parameters section above.
        The length of each transformed axis is as given by the corresponding
        element of `s`, or the length of the input in every axis except for the
        last one if `s` is not given.  In the final transformed axis the length
        of the output when `s` is not given is `2*(m-1)` where `m` is the
        length of the final transformed axis of the input.  To get an odd
        number of output points in the final axis, `s` must be specified.

    Raises
    ------
    ValueError
        if `s` and `axes` have different length.
    IndexError
        if an element of `axes` is larger than than the number of axes of `a`.

    See Also
    --------
    rfftn : The forward n-dimensional FFT of real input,
            of which `ifftn` is the inverse.
    fft : The one-dimensional FFT, with definitions and conventions used.
    irfft : The inverse of the one-dimensional FFT of real input.
    irfft2 : The inverse of the two-dimensional FFT of real input.

    Notes
    -----

    See `fft` for definitions and conventions used.

    See `rfft` for definitions and conventions used for real input.

    Examples
    --------
    >>> from numpy import zeros
    >>> from numpy.fft import irfftn, zeros
    >>> a = zeros((4,4,3); a[0,0,0] = 64;
    >>> irfftn(a)
    array([[[ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.]],
           [[ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.]],
           [[ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.]],
           [[ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.]]])

    """

    a = asarray(a).astype(complex)
    s, axes = _cook_nd_args(a, s, axes, invreal=1)
    for ii in range(len(axes)-1):
        a = ifft(a, s[ii], axes[ii])
    a = irfft(a, s[-1], axes[-1])
    return a

def irfft2(a, s=None, axes=(-2,-1)):
    """
    Compute the 2-dimensional inverse fft of a real array.

    Parameters
    ----------
    a : array (real)
        input array
    s : sequence (int)
        shape of the inverse fft
    axis : int
        axis over which to compute the inverse fft

    Notes
    -----
    This is really irfftn with different default.

    """

    return irfftn(a, s, axes)

# Deprecated names
from numpy import deprecate
refft = deprecate(rfft, 'refft', 'rfft')
irefft = deprecate(irfft, 'irefft', 'irfft')
refft2 = deprecate(rfft2, 'refft2', 'rfft2')
irefft2 = deprecate(irfft2, 'irefft2', 'irfft2')
refftn = deprecate(rfftn, 'refftn', 'rfftn')
irefftn = deprecate(irfftn, 'irefftn', 'irfftn')
