"""
Class extending functionality of :obj:`gwpy.frequencyseries.frequencyseries.FrequencySeries` from GWpy

Authors:
    | Artem Basalaev <artem[dot]basalaev[at]pm.me>
    | Christian Darsow-Fromm <cdarsowf[at]physnet.uni-hamburg.de>
    | Shreevathsa Chalathadka Subrahmanya <schalath[at]physnet.uni-hamburg.de>
"""
import copy
from warnings import warn
import gwpy.frequencyseries
import numpy as np
from astropy.units import UnitsError
from astropy import units as u


class FrequencySeries(gwpy.frequencyseries.FrequencySeries):
    """
    Class to model spectra of signals (frequency series), inherits from GWpy

    """

    @classmethod
    def from_other(cls, fs):
        """Create FrequencySeries from another FrequencySeries, in particular gwpy.FrequencySeries

        Parameters
        ----------
        fs : FrequencySeries, gwpy.frequencyseries.FrequencySeries
            Other FrequencySeries object
        Returns
        -------
        FrequencySeries
            Copy Spicypy FrequencySeries object
        """
        fs_spicypy = cls(fs.value)
        fs_spicypy.__dict__ = copy.deepcopy(fs.__dict__)
        return fs_spicypy

    def times_iomega(self, omega_exponent=1):
        """Differentiate or integrate spectrum wrt. time

        Parameters
        ----------
        omega_exponent : int
            Power of i*omega in multiplication factor, i.e. spectrum is multiplied by (i*omega)^omega_exponent.

            * values > 0 correspond to differentiation omega_exponent times,
            * values < 0 correspond to integration omega_exponent times.

        Returns
        -------
        FrequencySeries
            Integrate/differentiate frequency series.
        """
        if omega_exponent == 0:
            warn("Specified omega_exponent is 0. Returning as it is")
            return self
        omega = self.frequencies * 2 * np.pi
        dc_bin = False
        if omega[0] == 0.0:  # avoid potential divide by zero
            omega = omega[1:]
            dc_bin = True

        # let's first check if any of the values are complex
        if np.iscomplex(self.value).any():
            omega = (
                1j * omega
            )  # yes, there are complex values -  do it "properly" with i*omega
            # otherwise, ignore the i and apply real omega factor

        # calculate omega factor
        omega_pow = np.power(omega, omega_exponent)

        if dc_bin:
            omega_pow = np.insert(omega_pow, 0, 0.0)
        output = self * omega_pow
        # astropy mixes Hz and s. Manual correction is done below.
        for _ in range(abs(omega_exponent)):
            if omega_exponent > 0:
                output.override_unit(
                    output.unit / u.Hz / u.s  # pylint: disable=no-member
                )  # pylint: disable=no-member
            else:
                output.override_unit(
                    output.unit * u.Hz * u.s  # pylint: disable=no-member
                )  # pylint: disable=no-member
        return output

    def to_displacement(self):
        """Integrate the spectrum once or twice to convert to displacement.
        Input spectrum must have velocity or acceleration units.

        Parameters
        ----------

        Returns
        -------
        FrequencySeries
            Displacement frequency series.
        """

        # first check units - only velocity and acceleration can be converted to displacement
        original_units = ["m*s(-1)/Hz(1/2)", "m*s(-2)/Hz(1/2)"]
        omega_exponents = [
            -1,
            -2,
        ]  # possible exponents to use, depending on whether it is velocity or acceleration
        omega_exponent = None
        for i in range(len(omega_exponents)):
            try:
                self.unit.to(original_units[i])  # pylint: disable=no-member
            except UnitsError:
                continue  # could not convert to this unit, try with another one
            omega_exponent = omega_exponents[
                i
            ]  # converted to this unit - save omega_factor and stop the loop
            break

        if omega_exponent is None:
            raise ValueError(
                "Units of this FrequencySeries ",
                self.unit,
                " cannot be converted to displacement",
            )
        return self.times_iomega(omega_exponent)

    def to_velocity(self):
        """Integrate the spectrum once or differentiate once to convert to velocity.
        Input spectrum must have displacement or acceleration units.

        Parameters
        ----------

        Returns
        -------
        FrequencySeries
            Velocity frequency series.
        """

        # first check units - only displacement and acceleration can be converted to velocity
        original_units = ["m/Hz(1/2)", "m*s(-2)/Hz(1/2)"]
        omega_exponents = [
            1,
            -1,
        ]  # possible exponents to use, depending on whether it is displacement or acceleration
        omega_exponent = None
        for i in range(len(omega_exponents)):
            try:
                self.unit.to(original_units[i])  # pylint: disable=no-member
            except UnitsError:
                continue  # could not convert to this unit, try with another one
            omega_exponent = omega_exponents[
                i
            ]  # converted to this unit - save omega_factor and stop the loop
            break

        if omega_exponent is None:
            raise ValueError(
                "Units of this FrequencySeries ",
                self.unit,
                " cannot be converted to velocity",
            )
        return self.times_iomega(omega_exponent)

    def to_acceleration(self):
        """Differentiate the spectrum once or twice once to convert to acceleration.
        Input spectrum must have displacement or velocity units.

        Parameters
        ----------

        Returns
        -------
        FrequencySeries
            Acceleration frequency series.
        """

        # first check units - only displacement and velocity can be converted to acceleration
        original_units = ["m/Hz(1/2)", "m*s(-1)/Hz(1/2)"]
        omega_exponents = [
            2,
            1,
        ]  # possible exponents to use, depending on whether it is displacement or velocity
        omega_exponent = None
        for i in range(len(omega_exponents)):
            try:
                self.unit.to(original_units[i])  # pylint: disable=no-member
            except UnitsError:
                continue  # could not convert to this unit, try with another one
            omega_exponent = omega_exponents[
                i
            ]  # converted to this unit - save omega_factor and stop the loop
            break

        if omega_exponent is None:
            raise ValueError(
                "Units of this FrequencySeries ",
                self.unit,
                " cannot be converted to acceleration",
            )
        return self.times_iomega(omega_exponent)

    @property
    def is_asd(self):
        """Checks whether the input is ASD or not"""
        if self.unit == "Hz(1/2)":  # only possible for frequency ASD
            return True
        if self.unit == "1/Hz(1/2)":  # only possible for strain (unitless) ASD
            return True
        # let's assume it _is_ ASD, then if we do the following the frequency unit should cancel out
        test_unit = self.unit * u.Unit("Hz (1/2)")
        # now find out which units it had:
        bases = test_unit.decompose().bases
        # now try to force decompose this unit in base units from above _plus_ a frequency unit
        bases.append(u.Hz)  # pylint: disable=no-member
        if "Hz" in test_unit.decompose(bases=bases).bases:
            # as residual frquency unit is still present, not ASD
            return False
        # can be only ASD at this point
        return True

    @property
    def is_psd(self):
        """Checks whether the input is PSD or not"""
        if self.unit == "Hz":  # only possible for frequency PSD
            return True
        if self.unit == "1/Hz":  # only possible for strain (unitless) PSD
            return True
        test_unit = self.unit * u.Unit("Hz (1/2)")
        bases = test_unit.decompose().bases
        if len(bases) == 1 and "s" in bases:
            pass  # bypass for frequency ASD
        else:
            bases.append(u.Hz)  # pylint: disable=no-member
        if "Hz" in test_unit.decompose(bases=bases).bases:
            # as residual frquency unit is still present
            return True
        return False

    def rms(self, start_frequency=None):
        """Calculates the high-to-low RMS of the input spectrum.

        Parameters
        ----------
        start_frequency: float
            frequency to begin accumulating RMS (optional)

        Return
        ------
        rms: FrequencySeries
            High-to-low frequency cumulative RMS
        """
        rms = self.copy()

        # sanity check
        if (self.is_asd is False and self.is_psd is False) or (
            self.is_asd is True and self.is_psd is True
        ):
            raise ValueError(
                "Could not determine from units whether this FrequencySeries is ASD or PSD, cannot calculate RMS!"
            )
        # at this point we know whether it's PSD or ASD (and it can be nothing else)
        # if PSD, first take square root and then proceed with calculation for ASD
        if self.is_psd:
            rms = np.sqrt(rms)
        if start_frequency is not None:
            n_cut = np.where(self.frequencies.value > start_frequency)[0][0]
            rms = self[0:n_cut]

        bin_widths = np.diff(rms.frequencies)
        bin_widths = np.append(bin_widths[0], bin_widths)
        rms = np.sqrt(np.flip(np.cumsum(np.flip(rms * rms * bin_widths))))

        return rms


class SpectralVariance(gwpy.frequencyseries.SpectralVariance):
    """
    Class to model spectral variance (frequency series), copy from GWpy with fix for LPSD averaging method.

    """

    @classmethod
    def from_spectrogram(
        cls, *spectrograms, **kwargs
    ):  # pylint: disable=too-many-branches
        """Calculate a new `SpectralVariance` from a
        :class:`~gwpy.spectrogram.Spectrogram`.

        Parameters
        ----------
        spectrogram : `~gwpy.spectrogram.Spectrogram`
            input `Spectrogram` data

        bins : `~np.ndarray`, optional
            array of histogram bin edges, including the rightmost edge

        low : `float`, optional
            left edge of lowest amplitude bin, only read
            if ``bins`` is not given

        high : `float`, optional
            right edge of highest amplitude bin, only read
            if ``bins`` is not given

        nbins : `int`, optional
            number of bins to generate, only read if ``bins`` is not
            given, default: `500`

        log : `bool`, optional
            calculate amplitude bins over a logarithmic scale, only
            read if ``bins`` is not given, default: `False`

        norm : `bool`, optional
            normalise bin counts to a unit sum, default: `False`

        density : `bool`, optional
            normalise bin counts to a unit integral, default: `False`

        Returns
        -------
        specvar : `SpectralVariance`
            2D-array of spectral frequency-amplitude counts

        See also
        --------
        np.histogram
            The histogram function
        """
        # parse args and kwargs
        if not spectrograms:
            raise ValueError("Must give at least one Spectrogram")
        bins = kwargs.pop("bins", None)
        low = kwargs.pop("low", None)
        high = kwargs.pop("high", None)
        nbins = kwargs.pop("nbins", 500)
        log = kwargs.pop("log", False)
        norm = kwargs.pop("norm", False)
        density = kwargs.pop("density", False)
        if norm and density:
            raise ValueError(
                "Cannot give both norm=True and density=True, please pick one"
            )

        # get data and bins
        spectrogram = spectrograms[0]
        data = np.vstack([s.value for s in spectrograms])
        if bins is None:
            if low is None and log:
                low = np.log10(data.min() / 2)
            elif low is None:
                low = data.min() / 2
            elif log:
                low = np.log10(low)
            if high is None and log:
                high = np.log10(data.max() * 2)
            elif high is None:
                high = data.max() * 2
            elif log:
                high = np.log10(high)
            if log:
                bins = np.logspace(low, high, num=nbins + 1)
            else:
                bins = np.linspace(low, high, num=nbins + 1)
        nbins = bins.size - 1
        qbins = bins * spectrogram.unit

        # loop over frequencies
        out = np.zeros((data.shape[1], nbins))
        for i in range(data.shape[1]):
            out[i, :], bins = np.histogram(data[:, i], bins, density=density)
            if norm and out[i, :].sum():  # normalise
                out[i, :] /= out[i, :].sum()

        # return SpectralVariance
        name = f"{spectrogram.name} variance"
        try:
            new = cls(
                out,
                qbins,
                epoch=spectrogram.epoch,
                name=name,
                channel=spectrogram.channel,
                f0=spectrogram.f0,
                df=spectrogram.df,
            )
        except AttributeError:
            new = cls(
                out,
                qbins,
                epoch=spectrogram.epoch,
                name=name,
                channel=spectrogram.channel,
                f0=spectrogram.f0,
                frequencies=spectrogram.frequencies,
            )
        return new
