"""
Class wrapping :obj:`gwpy.spectrogram.spectrogram.Spectrogram` from GWpy

Authors:
    | Artem Basalaev <artem[dot]basalaev[at]pm.me>
"""
import copy
import gwpy.spectrogram
import gwpy.frequencyseries
import gwpy.timeseries
import numpy as np


class Spectrogram(gwpy.spectrogram.Spectrogram):
    """
    Class wrapping :obj:`gwpy.spectrogram.spectrogram.Spectrogram` from GWpy

    """

    @classmethod
    def from_other(cls, sgram):
        """Create Spectrogram from another Spectrogram, in particular gwpy.Spectrogram

        Parameters
        ----------
        sgram : Spectrogram, gwpy.Spectrogram
            Other Spectrogram object
        Returns
        -------
        Spectrogram
            Copy Spicypy Spectrogram object
        """
        sgram_spicypy = cls(
            sgram.value,
            unit=sgram.unit,
            xindex=sgram.xindex,
            yindex=sgram.yindex,
            name=sgram.name,
            channel=sgram.channel,
        )
        sgram_spicypy.__dict__ = copy.deepcopy(sgram_spicypy.__dict__)
        return sgram_spicypy

    @classmethod
    def from_spectra(cls, *spectra, **kwargs):
        """Build a new `Spectrogram` from a list of spectra.

        Parameters
        ----------
        *spectra
            any number of `~gwpy.frequencyseries.FrequencySeries` series
        dt : `float`, `~astropy.units.Quantity`, optional
            stride between given spectra

        Returns
        -------
        Spectrogram
            a new `Spectrogram` from a vertical stacking of the spectra
            The new object takes the metadata from the first given
            `~gwpy.frequencyseries.FrequencySeries` if not given explicitly

        Notes
        -----
        Each `~gwpy.frequencyseries.FrequencySeries` passed to this
        constructor must be the same length.
        """
        data = np.vstack([s.value for s in spectra])
        spec1 = list(spectra)[0]
        if not all(s.f0 == spec1.f0 for s in spectra):
            raise ValueError("Cannot stack spectra with different f0")
        if not all(np.array_equal(s.frequencies, spec1.frequencies) for s in spectra):
            raise ValueError("Cannot stack spectra with different df")
        kwargs.setdefault("name", spec1.name)
        kwargs.setdefault("channel", spec1.channel)
        kwargs.setdefault("epoch", spec1.epoch)
        try:
            kwargs.setdefault("df", spec1.df)
            kwargs.setdefault("f0", spec1.f0)
        except AttributeError:  #  in case of irregular frequency axis, e.g. if using LPSD
            kwargs.setdefault("frequencies", spec1.frequencies)
        kwargs.setdefault("unit", spec1.unit)
        if not ("dt" in kwargs or "times" in kwargs):
            try:
                kwargs.setdefault("dt", spectra[1].epoch.gps - spec1.epoch.gps)
            except (AttributeError, IndexError) as exc:
                raise ValueError from exc(
                    "Cannot determine dt (time-spacing) for Spectrogram from inputs"
                )
        return Spectrogram(data, **kwargs)

    def variance(  # pylint: disable=too-many-positional-arguments
        self,
        bins=None,
        low=None,
        high=None,
        nbins=500,
        log=False,
        norm=False,
        density=False,
    ):
        """Calculate the `SpectralVariance` of this `Spectrogram`.
        Overriding GWpy method to make it work for LPSD averaging method.

        Parameters
        ----------
        bins : `~numpy.ndarray`, optional, default `None`
            array of histogram bin edges, including the rightmost edge
        low : `float`, optional, default: `None`
            left edge of lowest amplitude bin, only read
            if ``bins`` is not given
        high : `float`, optional, default: `None`
            right edge of highest amplitude bin, only read
            if ``bins`` is not given
        nbins : `int`, optional, default: `500`
            number of bins to generate, only read if ``bins`` is not
            given
        log : `bool`, optional, default: `False`
            calculate amplitude bins over a logarithmic scale, only
            read if ``bins`` is not given
        norm : `bool`, optional, default: `False`
            normalise bin counts to a unit sum
        density : `bool`, optional, default: `False`
            normalise bin counts to a unit integral

        Returns
        -------
        specvar : `SpectralVariance`
            2D-array of spectral frequency-amplitude counts

        See also
        --------
        numpy.histogram
            for details on specifying bins and weights
        """
        from .frequency_series import SpectralVariance

        return SpectralVariance.from_spectrogram(
            self,
            bins=bins,
            low=low,
            high=high,
            nbins=nbins,
            log=log,
            norm=norm,
            density=density,
        )

    def _wrap_function(self, *args, **kwargs):
        """Wrap the wrap function from gwpy.Spectrogram, to return Spicypy objects"""
        out = super()._wrap_function(*args, **kwargs)
        if isinstance(out, gwpy.frequencyseries.FrequencySeries):
            # convert to Spicypy object
            from spicypy.signal import FrequencySeries

            return FrequencySeries.from_other(out)
        elif isinstance(out, gwpy.timeseries.TimeSeries):
            # convert to Spicypy object
            from spicypy.signal import TimeSeries

            return TimeSeries.from_other(out)
