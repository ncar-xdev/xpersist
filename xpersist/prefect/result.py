import os
import typing

os.environ['PREFECT__FLOWS__CHECKPOINTING'] = 'True'

import pendulum
import pydantic
from prefect.engine.result import Result
from slugify import slugify

from ..cache import CacheStore


@pydantic.dataclasses.dataclass
class XpersistResult(Result):
    """A result class used to store the results of a task in a xpersist cache store.

    Parameters
    ----------
    cache_store : :py:class:`xpersist.cache.CacheStore`
        The cache store to use for storing the result.
    serializer : str
        The serializer to use for storing the result. Valid options are:

        - 'auto' (default): automatically chooses the serializer based on the type of the value
        - 'xarray.netcdf': requires xarray and netCDF4
        - 'xarray.zarr': requires xarray and zarr
        - 'pandas.csv' : requires pandas
        - 'pandas.parquet': requires pandas and pyarrow or fastparquet
    serializer_dump_kwargs : dict
        The keyword arguments to pass to the serializer's `dump` method.
    serializer_load_kwargs : dict
        The keyword arguments to pass to the serializer's `load` method.
    kwargs : dict
        Any additional keyword arguments to pass to the `Result` class.
    """

    cache_store: CacheStore
    serializer: str = 'auto'
    serializer_dump_kwargs: typing.Dict[str, typing.Any] = None
    serializer_load_kwargs: typing.Dict[str, typing.Any] = None
    kwargs: typing.Dict[str, typing.Any] = None

    def __post_init_post_parse__(self):
        self.kwargs = self.kwargs or {}
        self._serializer = self.serializer
        super().__init__(**self.kwargs)
        self.serializer = self._serializer
        self.serializer_dump_kwargs = self.serializer_dump_kwargs or {}
        self.serializer_load_kwargs = self.serializer_load_kwargs or {}

    @property
    def default_location(self) -> str:
        return f"prefect-result-{slugify(pendulum.now('utc').isoformat())}"

    def read(self, location: str) -> Result:
        """Reads a result from the cache store and returns the corresponding `Result` instance.

        Parameters
        ----------
        location : str
            the location to read from

        Returns
        -------
        result : Result
            a new result instance with the data represented by the location
        """
        new = self.copy()
        new.location = location

        self.logger.debug('Starting to read result from {}...'.format(location))
        new.value = self.cache_store.get(key=location, load_kwargs=new.serializer_load_kwargs)
        self.logger.debug('Finished reading result from {}...'.format(location))
        return new

    def write(self, value_: typing.Any, **kwargs: typing.Any) -> Result:
        """Writes the result to a location in the cache store and returns a new `Result`
        object with the result's location.

        Parameters
        ----------
        value_ : typing.Any
            the value to write; will then be stored as the `value` attribute
            of the returned `Result` instance
        kwargs : dict
            if provided, will be used to format the location template
            to determine the location to write to

        Returns
        -------
        result : Result
            A new `Result` instance with the location of the written result.

        """

        new = self.format(**kwargs)
        new.value = value_
        assert new.location is not None

        relevant_context_keys = sorted(
            {
                'today',
                'yesterday',
                'tomorrow',
                'flow_name',
                'task_name',
                'map_index',
                'task_full_name',
                'task_slug',
                'task_tags',
                'task_run_name',
                'flow_id',
                'flow_run_id',
                'flow_run_version',
                'flow_run_name',
                'task_id',
                'task_run_id',
                'task_run_version',
            }
        )
        additional_metadata = {key: kwargs.get(key, '') for key in relevant_context_keys}

        self.logger.debug('Starting to upload result to {}...'.format(new.location))
        self.cache_store.put(
            key=new.location,
            value=new.value,
            serializer=self.serializer,
            dump_kwargs=new.serializer_dump_kwargs,
            additional_metadata=additional_metadata,
        )
        self.logger.debug('Finished uploading result to {}.'.format(new.location))
        return new

    def exists(self, location: str, **kwargs: typing.Any) -> bool:
        """Checks whether the target result exists in the cache store.

        Does not validate whether the result is `valid`, only that it is present.

        Parameters
        ----------
        location : str
            Location of the result in the specific result target.
            Will check whether the provided location exists
        kwargs : dict
            string format arguments for `location`

        Returns
        -------
        _ : bool
            whether or not the target result exists
        """
        return location.format(**kwargs) in self.cache_store


# Fixes https://github.com/samuelcolvin/pydantic/issues/704
XpersistResult.__pydantic_model__.update_forward_refs()
