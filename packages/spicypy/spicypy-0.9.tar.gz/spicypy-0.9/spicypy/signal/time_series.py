"""
Class extending functionality of :obj:`gwpy.timeseries.timeseries.TimeSeries` from GWpy.

Authors:
    | Artem Basalaev <artem[dot]basalaev[at]pm.me>
    | Christian Darsow-Fromm <cdarsowf[at]physnet.uni-hamburg.de>
    | Abhinav Patra <patraa1[at]cardiff.ac.uk>
    | Octavio Vega <vega00087[at]gmail[dot]com>
    | Jonathan Perry <j.w.perry[at]vuDOTnl>
"""
from functools import wraps
import copy
from warnings import warn
import numpy as np
import gwpy.timeseries
import gwpy.frequencyseries
import gwpy.spectrogram
from gwpy.signal import spectral

from spicypy.signal.spectral import daniell, lpsd
from spicypy.signal.coherent_subtraction import (
    coherent_subtraction,
    coherent_subtraction_spectrogram,
)

spectral.register_method(daniell)
spectral.register_method(lpsd)


def check_not_implemented_method(func):
    """Decorate a method to check if user tries to do LPSD or Daniell averaging method
    where we haven't implemented it yet.
    """

    @wraps(func)
    def wrapped_func(*args, **kwargs):
        """Wrap method to check if user tries to do LPSD or Daniell averaging method
        where we haven't implemented it yet.
        """
        if "method" in kwargs and (
            kwargs["method"] == "daniell" or kwargs["method"] == "lpsd"
        ):
            raise NotImplementedError(
                "LPSD/Daniell averaging is not supported for this method"
            )
        return func(*args, **kwargs)

    return wrapped_func


def fix_window_argument(func):
    """Decorate a method to fix "window" argument for Spicypy"""

    @wraps(func)
    def wrapped_func(*args, **kwargs):
        """Wrap method to fix "window" argument for Spicypy"""
        # work-around to propagate 'window' argument intact for custom averaging methods
        window = kwargs.get("window")
        if "method" in kwargs and (
            kwargs["method"] == "daniell" or kwargs["method"] == "lpsd"
        ):
            kwargs["window_"] = window
        elif window is None:
            # default to 'hann' for standard GWpy methods
            kwargs["window"] = "hann"

        return func(*args, **kwargs)

    return wrapped_func


def fix_return_object(func):
    """Decorate a method to always return Spicypy object if available"""

    @wraps(func)
    def wrapped_func(*args, **kwargs):
        """Wrap method to always return Spicypy object if available"""
        res = func(*args, **kwargs)
        # convert to Spicypy object
        if isinstance(res, gwpy.frequencyseries.frequencyseries.FrequencySeries):
            from spicypy.signal import FrequencySeries

            return FrequencySeries.from_other(res)
        elif isinstance(res, gwpy.timeseries.timeseries.TimeSeries):
            return TimeSeries.from_other(res)
        elif isinstance(res, gwpy.spectrogram.Spectrogram):
            from spicypy.signal import Spectrogram

            return Spectrogram.from_other(res)
        return res

    return wrapped_func


def _psd(bundle):
    """Calculate a PSD for a spectrogram.

    Parameters
    ----------
    bundle : `tuple`
        ts: `TimeSeries`
            input time series
        kwargs : `dict`
            additional arguments for PSD

    Returns
    -------
    psd_ : FrequencySeries
        a PSD of these time series
    """
    ts, kwargs = bundle
    psd_ = ts.psd(**kwargs)
    return psd_


class TimeSeries(gwpy.timeseries.TimeSeries):
    """
    Class to model signals (time series)

    """

    @classmethod
    def from_other(cls, ts):
        """Create TimeSeries from another TimeSeries, in particular gwpy.TimeSeries

        Parameters
        ----------
        ts : TimeSeries, gwpy.timeseries.TimeSeries
            Other TimeSeries object
        Returns
        -------
        TimeSeries
            Copy Spicypy TimeSeries object
        """
        ts_spicypy = cls(ts.value)
        ts_spicypy.__dict__ = copy.deepcopy(ts.__dict__)
        return ts_spicypy

    @fix_window_argument
    @fix_return_object
    def asd(self, fftlength=None, overlap=None, window=None, **kwargs):
        """Calculate the ASD `FrequencySeries` of this `TimeSeries`

        Parameters
        ----------
        fftlength : `float`, optional
            number of seconds in single FFT. Default behavior:

            * For Daniell averaging method (`method='daniell'`): user-specified value ignored, calculates single FFT covering full duration and then performs averaging in frequency domain.
            * For LPSD averaging method (`method='lpsd'`): user-specified value ignored, algorithm calculates optimal segment lengths.
            * For other averaging methods: defaults to a single FFT covering the full duration

        overlap : `float`, optional
            number of seconds of overlap between FFTs. Default behavior:

            * For Daniell averaging method (`method='daniell'`): user-specified value ignored, no overlap possible because a single FFT is calculated.
            * For other averaging methods: defaults to the recommended overlap for the given window (if given), or 0

        window : `str`, `numpy.ndarray`, optional
            Window function to apply to timeseries prior to FFT. Behavior depends on averaging method:

            * For LPSD averaging method (`method='lpsd'`): only `str` type is allowed. Possible values: 'hann', 'hanning', 'ham', 'hamming', 'bartlett', 'blackman', 'kaiser'. Defaults to 'kaiser'.
            * For other averaging methods: see :func:`scipy.signal.get_window` for details on acceptable formats. Defaults to 'hann'.

        **kwargs
            method : `str`, optional
                FFT-averaging method (default: ``'median'``). The accepted ``method`` arguments are:

                - ``'bartlett'`` : a mean average of non-overlapping periodograms
                - ``'median'`` : a median average of overlapping periodograms
                - ``'welch'`` : a mean average of overlapping periodograms
                - ``'lpsd'`` :  average of overlapping periodograms binned logarithmically in frequency
                - ``'daniell'`` : calculates single fft for the whole time series and averages in frequency domain

            any other keyword arguments accepted by the respective averaging methods. See definitions of corresponding method (`method` keyword). If `method` is not specified, defaults to :class:`gwpy.signal.spectral.csd`

        Returns
        -------
        asd :  FrequencySeries
            a data series containing the ASD
        """
        return super().asd(fftlength, overlap, window, **kwargs)

    @fix_window_argument
    @fix_return_object
    def psd(self, fftlength=None, overlap=None, window=None, **kwargs):
        """Calculate the PSD `FrequencySeries` of this `TimeSeries`

        Parameters
        ----------
        fftlength : `float`, optional
            number of seconds in single FFT. Default behavior:

            * For Daniell averaging method (`method='daniell'`): user-specified value ignored, calculates single FFT covering full duration and then performs averaging in frequency domain.
            * For LPSD averaging method (`method='lpsd'`): user-specified value ignored, algorithm calculates optimal segment lengths.
            * For other averaging methods: defaults to a single FFT covering the full duration

        overlap : `float`, optional
            number of seconds of overlap between FFTs. Default behavior:

            * For Daniell averaging method (`method='daniell'`): user-specified value ignored, no overlap possible because a single FFT is calculated.
            * For other averaging methods: defaults to the recommended overlap for the given window (if given), or 0

        window : `str`, `numpy.ndarray`, optional
            Window function to apply to timeseries prior to FFT. Behavior depends on averaging method:

            * For LPSD averaging method (`method='lpsd'`): only `str` type is allowed. Possible values: 'hann', 'hanning', 'ham', 'hamming', 'bartlett', 'blackman', 'kaiser'. Defaults to 'kaiser'.
            * For other averaging methods: see :func:`scipy.signal.get_window` for details on acceptable formats. Defaults to 'hann'.

        **kwargs
            method : `str`, optional
                FFT-averaging method (default: ``'median'``). The accepted ``method`` arguments are:

                - ``'bartlett'`` : a mean average of non-overlapping periodograms
                - ``'median'`` : a median average of overlapping periodograms
                - ``'welch'`` : a mean average of overlapping periodograms
                - ``'lpsd'`` :  average of overlapping periodograms binned logarithmically in frequency
                - ``'daniell'`` : calculates single fft for the whole time series and averages in frequency domain

            any other keyword arguments accepted by the respective averaging methods.
            See definitions of corresponding method (`method` keyword). If `method` is not specified,
            defaults to gwpy.signal.spectral.csd

        Returns
        -------
        psd :  FrequencySeries
            a data series containing the PSD
        """
        return super().psd(fftlength, overlap, window, **kwargs)

    @fix_window_argument
    @fix_return_object
    def csd(self, other, fftlength=None, overlap=None, window=None, **kwargs):
        """Calculate the CSD `FrequencySeries` for two `TimeSeries`

        Parameters
        ----------
        other : `TimeSeries`
            the second `TimeSeries` in this CSD calculation

        fftlength : `float`, optional
            number of seconds in single FFT. Default behavior:

            * For Daniell averaging method (`method='daniell'`): user-specified value ignored, calculates single FFT covering full duration and then performs averaging in frequency domain.
            * For LPSD averaging method (`method='lpsd'`): user-specified value ignored, algorithm calculates optimal segment lengths.
            * For other averaging methods: defaults to a single FFT covering the full duration

        overlap : `float`, optional
            number of seconds of overlap between FFTs. Default behavior:

            * For Daniell averaging method (`method='daniell'`): user-specified value ignored, no overlap possible because a single FFT is calculated.
            * For other averaging methods: defaults to the recommended overlap for the given window (if given), or 0

        window : `str`, `numpy.ndarray`, optional
            Window function to apply to timeseries prior to FFT. Behavior depends on averaging method:

            * For LPSD averaging method (`method='lpsd'`): only `str` type is allowed. Possible values: 'hann', 'hanning', 'ham', 'hamming', 'bartlett', 'blackman', 'kaiser'. Defaults to 'kaiser'.
            * For other averaging methods: see :func:`scipy.signal.get_window` for details on acceptable formats. Defaults to 'hann'.

        **kwargs
            method: `str`, optional
                averaging method for coherence calculation (default: ``'median'``). See above for important difference in arguments. The accepted ``method`` arguments are:

                - ``'bartlett'`` : a mean average of non-overlapping periodograms
                - ``'median'`` : a median average of overlapping periodograms
                - ``'welch'`` : a mean average of overlapping periodograms
                - ``'lpsd'`` :  average of overlapping periodograms binned logarithmically in frequency
                - ``'daniell'`` : calculates single fft for the whole time series and averages in frequency domain

            any other keyword arguments accepted by the respective averaging methods.
            See definitions of corresponding method (`method` keyword).

        Returns
        -------
        csd :  FrequencySeries
            a data series containing the CSD.
        """

        method_func = spectral.csd
        method = kwargs.pop("method", None)
        if method == "daniell":
            method_func = daniell
        elif method == "lpsd":
            method_func = lpsd
        elif method is None:
            # using default GWpy method; in that case, default fftlength will may also be used
            # inform the user of dangers
            if fftlength is None:
                warn(
                    "No 'fftlength' specified, note that in this case single FFT covering whole time series is used"
                )
        else:
            raise NotImplementedError(
                "Only 'daniell' and 'lpsd' averaging methods are currently implemented in addition to default"
            )

        return spectral.psd(
            (self, other),
            method_func,
            fftlength=fftlength,
            overlap=overlap,
            window=window,
            **kwargs,
        )

    def coherent_subtract_spectrogram(self, reference, stride, window=None, **kwargs):
        """Calculate the residual spectrogram (using coherent subtraction) between this `TimeSeries` and references.

        Parameters
        ----------
        reference: list or  `TimeSeriesDict`
            reference time series

        stride: `float`
            stride for spectrogram, in seconds

        window : `str`, `numpy.ndarray`, optional
            Window function to apply to timeseries prior to FFT.

            see :func:`scipy.signal.get_window` for details on acceptable formats. Defaults to 'hann'.

        **kwargs
            method: `str`, optional
                averaging method for coherence calculation. Currently only 'daniell' is supported

            any other keyword arguments accepted by 'daniell' averaging method

        Returns
        -------
        residual_spectrogram : Spectrogram
            residual spectrogram after frequency-domain subtraction of reference time series
        """

        method = kwargs.pop("method", "daniell")
        if method != "daniell":
            raise NotImplementedError(
                "Coherent subtraction is currently implemented only with Daniell averaging "
                "method."
            )
        if kwargs.get("overlap"):
            raise ValueError(
                "overlap argument is not supported by Daniell averaging method; "
                "single FFT covering the full duration is calculated, with averaging performed in frequency domain."
            )
        if kwargs.get("fftlength"):
            raise ValueError(
                "fftlength argument is not supported by Daniell averaging method; "
                "single FFT covering the full duration is calculated, with averaging performed in frequency domain."
            )
        kwargs["window_"] = window
        return coherent_subtraction_spectrogram(self, reference, stride, **kwargs)

    def coherent_subtract(self, reference, window=None, **kwargs):
        """Calculate the residual PSD (using coherent subtraction) between this `TimeSeries` and references.

        Parameters
        ----------
        reference: list or  `TimeSeriesDict`
            reference time series

        window : `str`, `numpy.ndarray`, optional
            Window function to apply to timeseries prior to FFT.

            see :func:`scipy.signal.get_window` for details on acceptable formats. Defaults to 'hann'.

        **kwargs
            method: `str`, optional
                averaging method for coherence calculation. Currently only 'daniell' is supported

            any other keyword arguments accepted by 'daniell' averaging method

        Returns
        -------
        residual_psd : FrequencySeries
            residual PSD after frequency-domain subtraction of reference time series
        """

        # No overlap for Daniell method.
        if kwargs.get("overlap"):
            raise ValueError(
                "overlap argument is not supported by Daniell averaging method; "
                "single FFT covering the full duration is calculated, with averaging performed in frequency domain."
            )
        if kwargs.get("fftlength"):
            raise ValueError(
                "fftlength argument is not supported by Daniell averaging method; "
                "single FFT covering the full duration is calculated, with averaging performed in frequency domain."
            )
        kwargs["window_"] = window
        return coherent_subtraction(self, reference, **kwargs)

    @fix_window_argument
    @fix_return_object
    def coherence(self, other, fftlength=None, overlap=None, window=None, **kwargs):
        """Calculate the frequency-coherence between this `TimeSeries` and another.

        Parameters
        ----------
        other : `TimeSeries`
            `TimeSeries` signal to calculate coherence with

        fftlength : `float`, optional
            number of seconds in single FFT. Default behavior:

            * For Daniell averaging method (`method='daniell'`): user-specified value ignored, calculates single FFT covering full duration and then performs averaging in frequency domain.
            * For LPSD averaging method (`method='lpsd'`): user-specified value ignored, algorithm calculates optimal segment lengths.
            * For other averaging methods: defaults to a single FFT covering the full duration (**NOTE**: THIS DEFAULT VALUE IN COHERENCE CALCULATION DOES NOT MAKE SENSE FOR MOST REAL APPLICATIONS!)

        overlap : `float`, optional
            number of seconds of overlap between FFTs. Default behavior:

            * For Daniell averaging method (`method='daniell'`): user-specified value ignored, no overlap possible because a single FFT is calculated.
            * For other averaging methods: defaults to the recommended overlap for the given window (if given), or 0

        window : `str`, `numpy.ndarray`, optional
            Window function to apply to timeseries prior to FFT. Behavior depends on averaging method:

            * For LPSD averaging method (`method='lpsd'`): only `str` type is allowed. Possible values: 'hann', 'hanning', 'ham', 'hamming', 'bartlett', 'blackman', 'kaiser'. Defaults to 'kaiser'.
            * For other averaging methods: see :func:`scipy.signal.get_window` for details on acceptable formats. Defaults to 'hann'.

        **kwargs
            method: `str`, optional
                averaging method for coherence calculation. See above for important difference in arguments.
                Defaults to gwpy.signal.spectral.coherence

            any other keyword arguments accepted by the respective averaging methods.
            See definitions of corresponding method (`method` keyword). If `method` is not specified,
            defaults to gwpy.signal.spectral.coherence

        Returns
        -------
        coherence : FrequencySeries
            the coherence `FrequencySeries` of this `TimeSeries` with the other
        """

        method = kwargs.pop("method", None)

        # calculate coherence
        if method == "daniell" or method == "lpsd":
            coherence = self._coherence(
                other,
                window=window,
                method=method,
                **kwargs,
            )
        elif method is None:
            # using default GWpy method; in that case, default fftlength will may also be used
            # inform the user of dangers
            if fftlength is None:
                warn(
                    "No 'fftlength' specified, note that in this case single FFT covering whole time series is used"
                )

            coherence = spectral.psd(
                (self, other),
                spectral.coherence,
                fftlength=fftlength,
                overlap=overlap,
                window=window,
                **kwargs,
            )
        else:
            raise NotImplementedError(
                "Only 'daniell' and 'lpsd' averaging methods are currently implemented in addition to default"
            )
        return coherence

    def _coherence(
        self,
        other,
        window=None,
        method="daniell",
        **kwargs,
    ):
        """Calculate the frequency-coherence between this `TimeSeries` and another with "custom" averaging methods. This method then calculates coherence using the formula:

        `coherence = np.abs(csd) ** 2 / psd1 / psd2`

        Parameters
        ----------
        other : `TimeSeries`
            `TimeSeries` signal to calculate coherence with

        window : `str`, `numpy.ndarray`, optional
            Window function to apply to timeseries prior to FFT. Behavior depends on averaging method:

            * For LPSD averaging method (`method='lpsd'`): only `str` type is allowed. Possible values: 'hann', 'hanning', 'ham', 'hamming', 'bartlett', 'blackman', 'kaiser'. Defaults to 'kaiser'.
            * For other averaging methods: see :func:`scipy.signal.get_window` for details on acceptable formats. Defaults to 'hann'.

        **kwargs
            any other keyword arguments accepted by the respective averaging methods.
            See definitions of corresponding method (`method` keyword).

        Returns
        -------
        coherence : FrequencySeries
            the coherence `FrequencySeries` of this `TimeSeries` with the other
        """

        if method == "daniell":
            method_func = daniell
        elif method == "lpsd":
            method_func = lpsd
        else:
            raise NotImplementedError(
                "Custom coherence calculation is only implemented for 'daniell' and 'lpsd' "
                "averaging methods."
            )
        if kwargs.get("overlap"):
            raise ValueError(
                "overlap argument is not supported by custom averaging methods; "
                "For Daniell averaging method: no overlap possible because a single FFT is calculated."
                "For LPSD averaging method: defaults to the recommended overlap for the given window (if given), or 0"
            )
        if kwargs.get("fftlength"):
            raise ValueError(
                "fftlength argument is not supported by custom averaging methods; "
                "For Daniell averaging method: single FFT is calculated and then averaging performed in frequency domain."
                "For LPSD averaging method: algorithm calculates optimal segment lengths."
            )
        csd = spectral.psd(
            (self, other),
            method_func=method_func,
            fftlength=None,
            overlap=None,
            window=window,
            **kwargs,
        )
        psd1 = spectral.psd(
            self,
            method_func=method_func,
            fftlength=None,
            overlap=None,
            window=window,
            **kwargs,
        )
        psd2 = spectral.psd(
            other,
            method_func=method_func,
            fftlength=None,
            overlap=None,
            window=window,
            **kwargs,
        )
        coherence = np.abs(csd) ** 2 / psd1 / psd2
        coherence.name = f"Coherence between {self.name} and {other.name}"

        return coherence

    @check_not_implemented_method
    @fix_return_object
    def fft(self, *args, **kwargs):
        """Compute the one-dimensional discrete Fourier transform of this `TimeSeries`.
        Simply wrapping GWpy method, see GWpy docs for details.
        """
        return super().fft(*args, **kwargs)

    def fetch(*args, **kwargs):  # pylint: disable=no-self-argument
        """Fetch time series (e.g. from NDS server).
        Simply wrapping GWpy method, see GWpy docs for details.
        """
        #  note this is not a method, but rather just a function,
        #  so have to wrap differently than other methods
        return TimeSeries.from_other(gwpy.timeseries.TimeSeries.fetch(*args, **kwargs))

    @check_not_implemented_method
    @fix_return_object
    def average_fft(self, *args, **kwargs):
        """Compute the averaged one-dimensional DFT of this `TimeSeries`.
        Simply wrapping GWpy method, see GWpy docs for details.
        """
        return super().average_fft(*args, **kwargs)

    def chunk(self, stride):
        """Split these time series in several chunks and return a list.

        Parameters
        ----------
        stride: `float`
            stride for spectrogram, in seconds

        Returns
        -------
        list : `list` of `TimeSeries`
            Chunks of TimeSeries in a list
        """
        from gwpy.signal.spectral._ui import seconds_to_samples

        n_stride = seconds_to_samples(stride, self.sample_rate)
        n_samples = len(self.value)
        if n_stride > n_samples:
            raise ValueError("Specified stride is longer than time series length.")

        n_chunks = (
            int(n_samples / n_stride)
            if n_samples % n_stride == 0
            else int(n_samples / n_stride) + 1
        )
        chunks = []
        for i in range(n_chunks):
            chunk = self[i * n_stride : (i + 1) * n_stride]
            chunks.append(chunk)
        return chunks

    @fix_return_object
    def spectrogram(self, stride, **kwargs):
        """Calculate the average power spectrogram of this `TimeSeries`.

        Parameters
        ----------
        stride: `float`
            stride for spectrogram, in seconds

        **kwargs
            method : `str`, optional
                FFT-averaging method (default: ``'median'``). The accepted ``method`` arguments are:

                - ``'bartlett'`` : a mean average of non-overlapping periodograms
                - ``'median'`` : a median average of overlapping periodograms
                - ``'welch'`` : a mean average of overlapping periodograms
                - ``'lpsd'`` :  average of overlapping periodograms binned logarithmically in frequency
                - ``'daniell'`` : calculates single fft for the whole time series and averages in frequency domain

            any other keyword arguments accepted by GWpy TimeSeries.Spectrogram method,
            and the respective averaging methods.
            See definitions of corresponding method (`method` keyword). If `method` is not specified,
            defaults to gwpy.signal.spectral.csd

        Returns
        -------
        spectrogram :  Spectrogram
            average power spectrogram of this `TimeSeries`
        """
        #  enable multiprocessing for spectrogram
        from gwpy.utils import mp
        from .spectrogram import Spectrogram

        if "method" not in kwargs or (
            kwargs["method"] != "lpsd" and kwargs["method"] != "daniell"
        ):
            return super().spectrogram(stride, **kwargs)

        # form list of inputs for each PSD calculation
        chunks = self.chunk(stride)

        # bundle inputs for _psd
        inputs = [(chunk, kwargs) for chunk in chunks]

        # calculate spectrogram
        n_proc = kwargs.pop("n_proc", 1)
        psds = mp.multiprocess_with_queues(n_proc, _psd, inputs)
        epoch = self.t0.value
        return Spectrogram.from_spectra(*psds, epoch=epoch, dt=stride)

    @check_not_implemented_method
    @fix_return_object
    def spectrogram2(self, *args, **kwargs):
        """Calculate the non-averaged power `Spectrogram` of this `TimeSeries`
        Simply wrapping GWpy method, see GWpy docs for details.
        """
        return super().spectrogram2(*args, **kwargs)

    @check_not_implemented_method
    @fix_return_object
    def fftgram(self, *args, **kwargs):
        """Calculate the Fourier-gram of this `TimeSeries`.
        Simply wrapping GWpy method, see GWpy docs for details.
        """
        return super().fftgram(*args, **kwargs)

    @check_not_implemented_method
    @fix_return_object
    def spectral_variance(self, *args, **kwargs):
        """Calculate the `SpectralVariance` of this `TimeSeries`.
        Simply wrapping GWpy method, see GWpy docs for details.
        """
        return super().spectral_variance(*args, **kwargs)

    @check_not_implemented_method
    @fix_return_object
    def rayleigh_spectrum(self, *args, **kwargs):
        """Calculate the Rayleigh `FrequencySeries` for this `TimeSeries`.
        Simply wrapping GWpy method, see GWpy docs for details.
        """
        return super().rayleigh_spectrum(*args, **kwargs)

    @check_not_implemented_method
    @fix_return_object
    def rayleigh_spectrogram(self, *args, **kwargs):
        """Calculate the Rayleigh statistic spectrogram of this `TimeSeries`.
        Simply wrapping GWpy method, see GWpy docs for details.
        """
        return super().rayleigh_spectrogram(*args, **kwargs)

    @check_not_implemented_method
    @fix_return_object
    def csd_spectrogram(self, *args, **kwargs):
        """Calculate the cross spectral density spectrogram of this`TimeSeries` with 'other'.
        Simply wrapping GWpy method, see GWpy docs for details.
        """
        return super().csd_spectrogram(*args, **kwargs)

    @fix_window_argument
    @fix_return_object
    def transfer_function(
        self, other, fftlength=None, overlap=None, window="hann", **kwargs
    ):
        """Calculate the transfer function between this `TimeSeries` and
        another.

        This `TimeSeries` is the 'A-channel', serving as the reference
        (denominator) while the other time series is the test (numerator)

        Parameters
        ----------
        other : `TimeSeries`
            `TimeSeries` signal to calculate the transfer function with

        fftlength : `float`, optional
            number of seconds in single FFT. Default behavior:

            * For Daniell averaging method (`method='daniell'`): user-specified value ignored, calculates single FFT covering full duration and then performs averaging in frequency domain.
            * For LPSD averaging method (`method='lpsd'`): user-specified value ignored, algorithm calculates optimal segment lengths.
            * For other averaging methods: defaults to a single FFT covering the full duration

        overlap : `float`, optional
            number of seconds of overlap between FFTs. Default behavior:

            * For Daniell averaging method (`method='daniell'`): user-specified value ignored, no overlap possible because a single FFT is calculated.
            * For other averaging methods: defaults to the recommended overlap for the given window (if given), or 0

        window : `str`, `numpy.ndarray`, optional
            Window function to apply to timeseries prior to FFT. Behavior depends on averaging method:

            * For LPSD averaging method (`method='lpsd'`): only `str` type is allowed. Possible values: 'hann', 'hanning', 'ham', 'hamming', 'bartlett', 'blackman', 'kaiser'. Defaults to 'kaiser'.
            * For other averaging methods: see :func:`scipy.signal.get_window` for details on acceptable formats. Defaults to 'hann'.

        **kwargs
            method : `str`, optional
                FFT-averaging method (default: ``'mean'``). The accepted ``method`` arguments are:

                - ``'bartlett'`` : a mean average of non-overlapping periodograms
                - ``'median'`` : a median average of overlapping periodograms
                - ``'welch'`` : a mean average of overlapping periodograms
                - ``'lpsd'`` :  average of overlapping periodograms binned logarithmically in frequency
                - ``'daniell'`` : calculates single fft for the whole time series and averages in frequency domain

            average : `str`, optional
                FFT-averaging method for scipy (default: ``'mean'``) passed to underlying csd() and psd() methods,
                unless "daniell" or "lpsd" is used.

        Returns
        -------
        transfer_function : `FrequencySeries`
            the transfer function `FrequencySeries` of this `TimeSeries`
            with the other

        Notes
        -----
        If `self` and `other` have difference
        :attr:`TimeSeries.sample_rate` values, the higher sampled
        `TimeSeries` will be down-sampled to match the lower.
        """
        average = kwargs.pop(
            "average", "mean"
        )  # apply gwpy default ("mean") if none specified
        return super().transfer_function(
            other,
            fftlength=fftlength,
            overlap=overlap,
            window=window,
            average=average,
            **kwargs,
        )

    @check_not_implemented_method
    @fix_return_object
    def coherence_spectrogram(self, *args, **kwargs):
        """Calculate the coherence spectrogram between this `TimeSeries` and other.
        Simply wrapping GWpy method, see GWpy docs for details.
        """
        return super().coherence_spectrogram(*args, **kwargs)
