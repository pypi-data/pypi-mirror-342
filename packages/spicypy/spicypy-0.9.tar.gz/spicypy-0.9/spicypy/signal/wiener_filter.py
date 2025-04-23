"""
Class creating Wiener filter from reference time series to signal time series.

Wiener filter gives an estimate of target channel from one or more references, based on linear coherence.
This estimate is optimal for linear and stationary signals. The most common application is to have reference(s) for
noise which enables then subtraction of this noise from target channel. More generally, Wiener filter generates
a time-domain filter that is equivalent to frequency-domain transfer function between two channels, or several such
transfer functions if more than one reference is used (one per reference).

The most common Wiener filter algorithm available (e.g. in image processing etc) relies on one reference, or
even no reference if noise is being estimated directly in the target channel. In other words it is a single-input,
single-output Wiener filter, or sometimes the output has higher dimensionality, such as the case with filtering
images (2D). MISO filter (based on algorithm in https://dcc.ligo.org/LIGO-T070192/public), where multiple references
can be supplied to estimate target channel. See also `J. Harms, Terrestrial gravity fluctuations, Living Reviews in
Relativity 22, 6 (2019)`.

This complicates the calculation as the matrix to invert is no longer a simple Toeplitz matrix,
but a block-Toeplitz matrix. This structure however is still exploited to speed up calculation significantly compared
to general matrix inversion. Implementation is based on iterative solvers from `scipy.sparse.linalg` that don't require
full matrix knowledge for every iteration and `scipy.sparse.linalg.LinearOperator` to generate matrix elements based on
a rule (operator), which permits exploiting symmetries of the matrix. In case of longer time series than necessary for
filter generation, several filters will be generated and the best automatically selected. Application of the filter
to references is also optimized using `numpy` arrays and optionally can be done with `multiprocessing`.

Authors:
    | Artem Basalaev <artem[dot]basalaev[at]pm.me>
"""
from warnings import warn
from copy import deepcopy
import multiprocessing
import os
import json

import numpy as np
from gwpy.timeseries import TimeSeriesDict

# import LinearOperator and all sorts of different solvers
from scipy.sparse.linalg import (
    LinearOperator,
    gmres,
    cgs,
    cg,
    gcrotmk,
    tfqmr,
    bicgstab,
    lgmres,
    minres,
)
from scipy.signal import correlate, correlation_lags
from scipy.linalg import matmul_toeplitz
from scipy import optimize
from spicypy.signal.time_series import TimeSeries

_solver_list = {
    "gmres": gmres,
    "cgs": cgs,
    "cg": cg,
    "gcrotmk": gcrotmk,
    "tfqmr": tfqmr,
    "bicgstab": bicgstab,
    "lgmres": lgmres,
    "minres": minres,
}


class WienerFilter:  # pylint: disable=too-many-instance-attributes
    """
    Class creating Wiener filter from reference time series to signal time series.

        Parameters
        ----------
        test: `TimeSeries`
            input time series
        reference: `list`, `TimeSeriesDict`
            reference time series
        kwargs : `dict`
            n_taps : `int`
                Number of taps for this Wiener filter, should be less than time series length.
            zero_padding : `bool`, optional
                Whether to use zero padding; if set to true, resulting time series will begin at the same time as input time series, but will be filled with zeros for n_taps (default: true).
            use_multiprocessing : `bool`, optional
                Whether to use multiprocessing to apply filters (default:false).
            n_proc: `int`, optional
                Number of parallel processes to use. Defaults to number of CPUs.
            subtract_mean: `bool`, optional
                Subtract mean from data for internal processing, to ensure that floating point numbers are not too large. For the output time series operation is inverted, therefore besides improving numerical stability it is not affecting the results. Defaults to true.
            normalize_data: `bool`, optional
                Divide data by its standard deviation for internal processing, to ensure that floating point numbers are not too large. For the output time series operation is inverted, therefore besides improving numerical stability it is not affecting the results. Defaults to true.
            use_norm_factor: `bool`, optional
                Renormalize resulting Wiener filter by finding the best-fitting normalization coefficient for ASD on training data. May result in improvement in case of MISO filter with noisy references, otherwise not recommended. Defaults to false.
            verbose: `bool`, optional
                Enable verbose output (default: false).
            solver: `str`, optional
                Solver to use for Wiener-Hopf equations. Default: `tfqmr`. Other available: `gmres`, `cgs`, `cg`, `gcrotmk`, `tfqmr`, `bicgstab`, `lgmres`, `minres`.
    """

    def __init__(self, test, reference, **kwargs):
        """Init method for Wiener filter"""

        self.test = test
        self.reference = reference
        if isinstance(reference, TimeSeriesDict):
            self.reference = []
            for channel in reference.keys():
                self.reference.append(reference[channel])
        elif not isinstance(reference, list):
            raise TypeError(
                "only TimeSeriesDict or list of TimeSeries are supported types for reference time series"
            )
        self.test_array = None
        self.reference_array = None
        self.kwargs = kwargs

        self.unique_rmi = {}
        self.P = {}
        self.labels = {}
        self.W = {}
        self.norm_factor = {}
        self.test_std = 1.0
        self.test_mean = 0.0
        self.refs_std = []
        self.refs_mean = []
        self.best_filter_index = 0

        self._check_inputs()
        # Note for following attributes: they are needed only to be able to use pool.map(..) function and
        # pass information which normally would be done with function arguments. Maybe there's a nicer way to do it.
        self.parallel_idx = None
        self.parallel_slice_length = None
        self.parallel_filter_index = None
        self.parallel_refs = None

    def save(self, path):
        """Save Wiener filter to file.

        Parameters
        ----------
        path: `str`
            Save path with file name. If file name does not end on `.json`, it will be appended to the end.
        """

        path = path.replace("\\", "/")  # get rid of Windows-only path separator if any
        filename = os.path.basename(path)
        if filename != path:  # got a full path, check that folder exists
            folder = path.split(filename)[0]
            if not os.path.exists(folder):
                raise ValueError("Save path is invalid")
        if not path.endswith(".json"):
            path += ".json"

        W_lists_dict = {}
        for idx, value in self.W.items():
            W_lists_dict[idx] = value.tolist()
        save_dict = {
            "kwargs": self.kwargs,
            "W": W_lists_dict,
            "norm_factor": self.norm_factor,
            "test_std": self.test_std,
            "test_mean": self.test_mean,
            "refs_std": self.refs_std,
            "refs_mean": self.refs_mean,
            "best_filter_index": self.best_filter_index,
            "n_taps": self.n_taps,
            "zero_padding": self.zero_padding,
            "subtract_mean": self.subtract_mean,
            "normalize": self.normalize,
            "use_norm_factor": self.use_norm_factor,
            "solver": self.solver_arg,
            "sample_rate": self.sample_rate,
            "n_references": self.n_references,
            "unit": self.unit,
        }

        with open(path, "w", encoding="utf-8") as out_file:
            json.dump(save_dict, out_file, default=str)

    @classmethod
    def load(cls, filename):
        """Load Wiener filter from a file.

        Parameters
        ----------
        filename: `str`
            Load path with file name.
        """

        if not os.path.isfile(filename):
            if os.path.isfile(filename + ".json"):
                filename = filename + ".json"
            else:
                raise ValueError("Load path is invalid")
        dummy_ts = TimeSeries([0.0, 0.0])
        kwargs_dict = {"loaded_from_file": True}
        wf = cls(dummy_ts, [], **kwargs_dict)
        wf.test = None
        wf.reference = None

        with open(filename, "r", encoding="utf-8") as in_file:
            data_dict = json.load(in_file)

        try:
            wf.kwargs = data_dict["kwargs"]
            wf.W = {}
            W_lists_dict = data_dict["W"]
            for idx in W_lists_dict.keys():
                wf.W[int(idx)] = np.array(W_lists_dict[idx])
            norm_factor_dict = data_dict["norm_factor"]
            wf.norm_factor = {}
            for idx in norm_factor_dict.keys():
                wf.norm_factor[int(idx)] = np.array(norm_factor_dict[idx])
            wf.test_std = data_dict["test_std"]
            wf.test_mean = data_dict["test_mean"]
            wf.refs_std = data_dict["refs_std"]
            wf.refs_mean = data_dict["refs_mean"]
            wf.best_filter_index = int(data_dict["best_filter_index"])
            wf.n_taps = data_dict["n_taps"]
            wf.zero_padding = data_dict["zero_padding"]
            wf.subtract_mean = data_dict["subtract_mean"]
            wf.normalize = data_dict["normalize"]
            wf.use_norm_factor = data_dict["use_norm_factor"]
            solver = data_dict["solver"]
            if solver in _solver_list:
                wf.solver = _solver_list[solver]
            else:
                raise NotImplementedError(
                    "Requested solver " + solver + "is not supported"
                )
            wf.sample_rate = (data_dict["sample_rate"],)
            wf.n_references = (data_dict["n_references"],)
            wf.unit = data_dict["unit"]
        except KeyError as exc:
            raise KeyError(
                "Data file is corrupted or in wrong format, missing required keys in the dictionary."
            ) from exc
        # for unknown reason, two class members become tuples with one element
        if isinstance(wf.sample_rate, tuple):
            wf.sample_rate = wf.sample_rate[0]
        if isinstance(wf.n_references, tuple):
            wf.n_references = wf.n_references[0]

        # set some args to default values - they have to be set by a user in explicit calls if required
        # another solution would be extra kwargs in `load` method... but maybe it's confusing
        wf.use_multiprocessing = False
        wf.n_proc = multiprocessing.cpu_count()
        wf.verbose = False
        return wf

    def _check_timeseries_consistency(self, inputs_list):
        """Check input time series consistency (sampling rates, start time, length, etc.).

        Parameters
        ----------
        inputs_list: `list` of `TimeSeries`
            input time series
        """

        sample_rate = inputs_list[0].sample_rate.value
        epoch = inputs_list[0].epoch
        n_samples = len(inputs_list[0])

        # test time series for consistency
        for input_time_series in inputs_list:
            if len(input_time_series) != n_samples:
                raise ValueError(
                    "All time series must have the same length (number of samples)!"
                )
            if input_time_series.sample_rate.value != sample_rate:
                raise ValueError("All time series must have the same sampling rate!")
            if (
                input_time_series.epoch is not None
                and epoch is not None
                and input_time_series.epoch != epoch
            ):
                raise ValueError(
                    "All time series must be aligned in time (same time_series.epoch)!"
                )
            if np.iscomplexobj(input_time_series.value):
                raise NotImplementedError(
                    "Wiener filtering for complex time series is not implemented"
                )

    def _check_inputs(self):
        """Parse input arguments for this Wiener filter."""

        self.loaded_from_file = self.kwargs.pop("loaded_from_file", False)
        if self.loaded_from_file:  # Do nothing; no inputs to check if loaded from file
            return
        # make a list of all inputs and compare values to test
        inputs_list = self.reference + [self.test]
        self._check_timeseries_consistency(inputs_list)
        self.sample_rate = self.test.sample_rate.value
        self.n_references = len(self.reference)
        self.unit = self.test.unit.to_string()

        # get parameters for Wiener filter calculation
        self.n_taps = self.kwargs.pop("n_taps", len(self.test) - 1)
        if self.n_taps + 1 > len(self.test):
            warn(
                "Cannot set more taps than input time series length - 1. Setting n_taps to time series length - 1. "
            )
            self.n_taps = len(self.test) - 1
        if self.n_taps <= 0:
            raise ValueError(
                "You must specify a non-zero number of taps for Wiener filter."
            )
        if self.n_taps >= 15000:
            warn(
                "Creating Wiener filter with 15000 or more taps requested. This is A LOT. Depending on number of "
                "references and available resources, calculation may fail!"
            )
        self.zero_padding = self.kwargs.pop("zero_padding", True)
        self.use_multiprocessing = self.kwargs.pop("use_multiprocessing", False)
        self.n_proc = self.kwargs.pop("n_proc", multiprocessing.cpu_count())
        if self.n_proc == 1:
            self.use_multiprocessing = False
        self.subtract_mean = self.kwargs.pop("subtract_mean", True)
        self.normalize = self.kwargs.pop("normalize_data", True)
        self.use_norm_factor = self.kwargs.pop("use_norm_factor", False)
        self.verbose = self.kwargs.pop("verbose", False)

        self.solver = tfqmr
        self.solver_arg = self.kwargs.pop("solver", "tfqmr")
        if self.solver_arg in _solver_list:
            self.solver = _solver_list[self.solver_arg]
        else:
            raise NotImplementedError(
                "Requested solver " + self.solver_arg + " is not supported"
            )
        if self.use_norm_factor and self.normalize:
            raise NotImplementedError(
                "Additional norm factor can only be derived"
                " when Wiener filter is applied to already normalized data"
            )

    def create_filters(self):
        """Calculate Wiener filter(s) based on inputs."""

        if self.loaded_from_file:
            raise NotImplementedError(
                "Cannot generate filters because this Wiener filter was loaded from file;"
                " filters are already generated earlier. Try calling `.apply(..)` instead."
            )
        self._prepare_data()
        # each filter requires n_taps + 1 time steps to create
        if (
            len(self.test) > 2 * self.n_taps
        ):  # will create multiple filters and choose the best one
            # first calculate how many times n_taps
            n_filters = int(np.floor(len(self.test) / self.n_taps))
            # then check if there's one more time step for last filter, if not make one less
            if len(self.test) <= n_filters * self.n_taps:
                n_filters -= 1
            print("Creating Wiener Filters...")
            for i in range(n_filters):
                self._create_filter(
                    i,
                    self.test_array,
                    self.reference_array,
                    i * self.n_taps,
                    (i + 1) * self.n_taps,
                )
            self.determine_best_filter()
        else:  # create one filter
            self._create_filter(
                0, self.test_array, self.reference_array, 0, self.n_taps
            )

    def determine_best_filter(self):
        """Find the best-performing Wiener Filter on input data."""

        if self.loaded_from_file:
            raise NotImplementedError(
                "Cannot determine the best filter because this Wiener filter was "
                "loaded from file; best filters are already found earlier. "
                "Try calling `.apply(..)` instead."
            )

        print("Determining the best filter...")
        mse_arr = np.zeros(len(self.W))
        test_asd = self.test.asd(method="lpsd")
        for idx in self.W:
            result_ts = self.apply(
                inputs_list=None,
                index=idx,
                zero_padding=True,
                normalized_output=True,
                to_training_data=True,
            )
            result_asd = result_ts.asd(method="lpsd")
            mse = 0.0
            if self.use_norm_factor:

                def MSE_to_minimize(norm_factor):
                    return MSE(
                        test_asd.value,
                        norm_factor
                        * result_asd.value,  # pylint: disable=cell-var-from-loop
                    )

                norm = optimize.minimize_scalar(MSE_to_minimize)
                self.norm_factor[idx] = norm.x
                mse = MSE_to_minimize(norm.x)
                if self.verbose:
                    print(
                        idx,
                        "MSE:",
                        MSE_to_minimize(norm.x),
                        "normalization factor:",
                        norm.x,
                    )
            else:
                mse = MSE(test_asd.value, result_asd.value)
                if self.verbose:
                    print(idx, "MSE:", mse)
            mse_arr[idx] = mse
        self.best_filter_index = np.argmin(mse_arr)
        print("Done. Best filter index:", self.best_filter_index)

    def _create_filter(
        self, index, tot_signal, tot_refs, start, end
    ):  # pylint: disable=too-many-positional-arguments
        """Calculate individual Wiener filter

        Parameters
        ----------
        index: `int`
            Current filter index.
        tot_signal: `np.array` of `float`
            Target time series, which filter should recreate.
        tot_refs: `np.array` of `float`
            One or multiple reference time series.
        start: `int`
            First index in the array for this filter.
        end: `int`
            Last index in the array for this filter.
        """

        if self.verbose:
            print("Creating Wiener filter: ", index)
        signal = tot_signal[start : end + 1]
        refs = tot_refs[start : end + 1]
        n_refs = refs.shape[1]

        self._wiener_components(refs, signal, index)
        unique_rmi = self.unique_rmi[index]
        unique_colrows = unique_rmi.shape[0]
        labels = self.labels[index]

        def R_block_times_vec(q, r, vec):
            colrow_idx = None
            transpose = False
            for i in range(unique_colrows):
                if labels[i][0] == q and labels[i][1] == r:
                    colrow_idx = i
                    break
                if q != r and labels[i][0] == r and labels[i][1] == q:
                    colrow_idx = i
                    transpose = True
                    break
            if colrow_idx is None:
                raise ValueError("Block ", q, r, "is out of bounds!")
            rmi_left = unique_rmi[colrow_idx][0 : self.n_taps + 1]
            rmi_right = unique_rmi[colrow_idx][self.n_taps :]
            if transpose:
                return matmul_toeplitz((rmi_right, np.flip(rmi_left)), vec)
            return matmul_toeplitz((np.flip(rmi_left), rmi_right), vec)

        def R_times_vec(vec):
            vec = np.ndarray.flatten(vec)
            outvec = np.zeros(shape=vec.shape[0])
            for i in range(n_refs):
                for j in range(n_refs):
                    outvec[
                        i * (self.n_taps + 1) : (i + 1) * (self.n_taps + 1)
                    ] = outvec[
                        i * (self.n_taps + 1) : (i + 1) * (self.n_taps + 1)
                    ] + R_block_times_vec(
                        i, j, vec[j * (self.n_taps + 1) : (j + 1) * (self.n_taps + 1)]
                    )
            return outvec

        operator_dim = (self.n_taps + 1) * refs.shape[1]
        Rv = LinearOperator(shape=(operator_dim, operator_dim), matvec=R_times_vec)
        if self.verbose:
            print("inverting the matrix")
        W = self.solver(Rv, self.P[index])
        self.W[index] = W[0]

    def _wiener_components(self, refs, signal, index):
        """Prepare components for the Wiener-Hopf equations: covariance matrix, cross-corr vector.

        Parameters
        ----------
        refs: `np.array` of `float`
            One or multiple reference time series.
        signal: `np.array` of `float`
            Target time series, which filter should recreate.
        index: `int`
            Current filter index.
        """

        n_refs = refs.shape[1]
        n_time_steps = refs.shape[0]

        # unique components ("rmi") rows/cols of covariance matrix
        unique_colrows = 0
        for m in range(n_refs):
            for i in range(m, n_refs):
                unique_colrows = unique_colrows + 1
        colrow_length = 2 * (self.n_taps + 1) - 1
        unique_rmi = np.zeros(shape=(unique_colrows, colrow_length))

        # input covariance matrix
        lags = correlation_lags(n_time_steps, n_time_steps)
        max_lag = np.where(np.abs(lags) <= self.n_taps)
        k = 0
        for m in range(n_refs):
            for i in range(m, n_refs):
                if self.verbose:
                    print("calculating R" + str(m) + str(i))
                rmi = correlate(refs[:, m], refs[:, i])
                rmi = np.ndarray.flatten(np.take(rmi, max_lag))
                unique_rmi[k, :] = rmi
                k = k + 1

        # cross−correlation vector
        P = np.zeros(n_refs * (self.n_taps + 1))
        if self.verbose:
            print("calculating cross-corr vector")
        for i in range(n_refs):
            top = i * (self.n_taps + 1)
            bottom = (i + 1) * (self.n_taps + 1)
            p = correlate(signal, refs[:, i])
            p = np.ndarray.flatten(np.take(p, max_lag))
            P[top:bottom] = np.conjugate(p[self.n_taps :])

        k = 0
        labels = np.zeros(shape=(unique_colrows, 2), dtype=np.int8)
        for m in range(n_refs):
            for i in range(m, n_refs):
                labels[k] = [m, i]
                k = k + 1

        self.unique_rmi[index] = unique_rmi
        self.P[index] = P
        self.labels[index] = labels

    def _prepare_data(self):
        """Normalize input time series to values close to 1, for better numerical stability."""

        self.test_array = deepcopy(self.test.value)  # need to copy time series
        # or else normalization will affect original values
        self.test_mean = np.mean(self.test_array)
        self.test_std = np.std(self.test_array)

        self.reference_array = deepcopy(self.reference[0].value).reshape(
            (self.test_array.shape[0], 1)
        )
        self.refs_mean = [np.mean(self.reference[0].value)]
        self.refs_std = [np.std(self.reference[0].value)]
        if len(self.reference) > 1:
            for i in range(1, len(self.reference)):
                self.reference_array = np.column_stack(
                    (self.reference_array, deepcopy(self.reference[i].value))
                )
                self.refs_mean += [np.mean(self.reference[i].value)]
                self.refs_std += [np.std(self.reference[i].value)]

        if self.subtract_mean:
            self.test_array -= self.test_mean
            for i in range(self.reference_array.shape[1]):
                self.reference_array[:, i] -= self.refs_mean[i]
        if self.normalize:
            self.test_array /= self.test_std
            for i in range(self.reference_array.shape[1]):
                self.reference_array[:, i] /= self.refs_std[i]

    def _apply_parallel(self, i):
        """Apply Wiener filter to partial data by one parallel process.
        Can be called once to apply to all data by a single process.

        Parameters
        ----------
        i: `int`
            index of the parallel process (default: 0 for single process)
        """

        n_time_steps = self.parallel_refs.shape[0]
        n_refs = self.parallel_refs.shape[1]
        W = self.W[self.parallel_filter_index]
        indices = self.parallel_idx[
            self.parallel_slice_length * i : self.parallel_slice_length * (i + 1)
        ]
        result_timeseries = np.zeros(n_time_steps)

        for n in indices:  # time steps for which we can calculate
            # output signal
            if self.verbose and n % 50000 == 0:
                print(
                    "Applying filter " + str(self.parallel_filter_index) + ": step",
                    n - self.n_taps,
                    "out of",
                    n_time_steps - self.n_taps,
                )
            for m in range(n_refs):  # number of ref channels
                result_timeseries[n] = result_timeseries[n] + W[
                    (self.n_taps + 1) * m : (self.n_taps + 1) * (m + 1)
                ].dot(np.flip(self.parallel_refs[n - self.n_taps : n + 1, m]))
        return indices, result_timeseries

    def _preprocess_data(self, to_training_data, inputs_list):
        """Preprocess data (check, normalize, subtract mean, etc) before applying the filter.

        Parameters
        ----------
        to_training_data: `bool`
            Whether the filter is applied to training data.
        inputs_list: `np.array` of `float`
            Array of inputs (references) to which this filter is applied.
        """

        if (inputs_list is None and not to_training_data) or (
            inputs_list is not None and to_training_data
        ):
            raise ValueError(
                "Require either reference time series specified, or 'to_training_data' set to 'True'"
            )

        if to_training_data:
            return self.reference_array

        if self.n_taps >= len(inputs_list[0]):
            raise ValueError(
                "Input time series have less time steps than number of filter taps! Cannot apply filter"
            )

        # check consistency
        self._check_timeseries_consistency(inputs_list)
        if inputs_list[0].sample_rate.value != self.sample_rate:
            raise ValueError(
                "Reference sample rate is not the same as sample rate used to generate this filter!"
            )

        if len(inputs_list) != self.n_references:
            raise ValueError("Wrong number of references for this Wiener Filter")
        refs = deepcopy(inputs_list[0].value).reshape(
            (inputs_list[0].value.shape[0], 1)
        )
        if len(inputs_list) > 1:
            for i in range(1, len(inputs_list)):
                refs = np.column_stack((refs, deepcopy(inputs_list[i].value)))

        for i in range(refs.shape[1]):
            if self.normalize:
                refs[:, i] /= self.refs_std[i]
                if self.verbose:
                    print("Dividing ref" + str(i) + " by std=", self.refs_std[i])
            if self.subtract_mean:
                refs[:, i] -= self.refs_mean[i]
                if self.verbose:
                    print("Subtracting ref" + str(i) + " mean=", self.refs_mean[i])
        return refs

    def _post_process_data(  # pylint: disable=too-many-positional-arguments
        self,
        result_timeseries,
        zero_padding,
        to_training_data,
        normalized_output,
        index,
        inputs_list,
    ):
        """Post-process data (revert normalization, package as `TimeSeries`, etc.).

        Parameters
        ----------
        result_timeseries: `np.array` of `float`
            Raw time series - result of the applied filter
        zero_padding: `bool`
            Whether to add zeros in front (results in time series of same length as input).
        to_training_data: `bool`
            Whether the filter was applied to training data.
        normalized_output: `bool`
            Whether the data were normalized before creating filter - in that case inverse should be applied to the result.
        index: `int`
            Index of the applied filter, in case it has individual norm factor to be applied.
        inputs_list: `np.array` of `float`
            Array of inputs (references) to which this filter is applied.
        """

        if not zero_padding:
            result_timeseries = result_timeseries[self.n_taps :]

        unit = self.unit
        if to_training_data:
            t0 = self.test.t0
            sample_rate = self.test.sample_rate
        else:
            t0 = inputs_list[0].t0
            sample_rate = inputs_list[0].sample_rate

        if not zero_padding:  # advance start time by filter length
            t0 += self.n_taps / sample_rate

        if not normalized_output:
            norm_factor = 1.0
            if index in self.norm_factor:
                norm_factor = self.norm_factor[index]
                if self.verbose:
                    print("Multiplying by norm factor=", norm_factor)
            result_timeseries *= norm_factor
            if self.normalize:
                result_timeseries = result_timeseries * self.test_std
                if self.verbose:
                    print("Multiplying by test std=", self.test_std)
            if self.subtract_mean:
                result_timeseries += self.test_mean
                if self.verbose:
                    print("Adding mean=", self.test_mean)

        return TimeSeries(
            result_timeseries,
            sample_rate=sample_rate,
            unit=unit,
            t0=t0,
            name="Wiener filter output",
        )

    def apply(  # pylint: disable=too-many-positional-arguments
        self,
        inputs_list=None,
        index=None,
        zero_padding=None,
        normalized_output=False,
        to_training_data=False,
        use_multiprocessing=None,
    ):
        """Apply Wiener filter to data.

        Parameters
        ----------
        inputs_list: `list` of `TimeSeries`, optional
            time series to apply Wiener filter to, not needed if applying to training data
        index: `int`, optional
            use specific Wiener filter by index, by default using the best filter determined earlier
        zero_padding: `bool`, optional
            if true, return time series of the same length as inputs,
            with zeros in the beginning (Wiener filter needs to "accumulate" data equal to its n_taps first);
            if false, returned time series will be shorter and with shifted t0 by n_taps/sample_rate
        normalized_output: `bool`, optional
            if true, do not add mean and multiply by standard deviation, as if the data were already normalized
        to_training_data: `bool`, optional
            apply filters to training data - runs after filter creation to de3termine best filter,
            but can also be called explicitly
        use_multiprocessing: `bool`, optional
            use multiprocessing (with number of parallel processes set with `self.n_proc`)
        """

        if to_training_data and self.loaded_from_file:
            raise NotImplementedError(
                "Cannot apply filter to training data because this Wiener filter "
                "was loaded from file; filters are already applied to training data earlier. "
                "Try calling `.apply(..)` without `to_training_data` argument."
            )

        if use_multiprocessing is None:
            use_multiprocessing = self.use_multiprocessing

        if index is None:  # apply the best filter
            index = self.best_filter_index

        refs = self._preprocess_data(to_training_data, inputs_list)

        n_time_steps = refs.shape[0]
        idx = np.arange(
            self.n_taps, n_time_steps
        )  # time steps for which we can calculate output signal
        self.parallel_idx = idx
        self.parallel_filter_index = index
        self.parallel_refs = refs

        if use_multiprocessing and len(idx) < self.n_proc:
            print(
                "Requested multiprocessing but time series is not long enough to benefit from it. "
                "You can try to set n_proc to lower values to run on fewer processes than "
                + str(self.n_proc)
                + ". Running in single process mode."
            )
        if use_multiprocessing and len(idx) > self.n_proc:
            print(
                "Using multiprocessing. Your computer may become unresponsive due to load, this is expected. Please "
                "wait until the operation is complete."
            )
            self.parallel_slice_length = int(np.ceil(len(idx) / float(self.n_proc)))
            n_slices = int(np.ceil(len(idx) / float(self.parallel_slice_length)))
            result_timeseries = np.zeros(self.parallel_refs.shape[0])

            with multiprocessing.Pool(processes=self.n_proc) as pool:
                result_list = pool.map(self._apply_parallel, range(n_slices))
            for indices, ts in result_list:
                result_timeseries[indices[0] : indices[-1]] = ts[
                    indices[0] : indices[-1]
                ]

        else:
            self.parallel_slice_length = len(idx)
            _, result_timeseries = self._apply_parallel(0)

        if zero_padding is None:
            zero_padding = self.zero_padding

        return self._post_process_data(
            result_timeseries,
            zero_padding,
            to_training_data,
            normalized_output,
            index,
            inputs_list,
        )


def MSE(sig_asd, pred_asd):
    """Calculate mean squared error on FrequencySeries

    Parameters
    ----------
    sig_asd: `FrequencySeries`
        "signal" frequency series
    pred_asd: `FrequencySeries`
        "prediction" frequency series

    Returns
    -------
    mse :  float
        mean squared error
    """
    squared_residuals = 0.0
    for i in range(len(sig_asd)):
        squared_residuals = squared_residuals + (sig_asd[i] - pred_asd[i]) ** 2
    return np.sqrt(1.0 / float(len(sig_asd)) * squared_residuals)
