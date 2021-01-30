import dataclasses
import datetime
import json
import multiprocessing
import os
import platform
import socket
import subprocess
import sys
import time
import typing

import psutil

CACHE_TIMEOUT = 7200
CONDA_EXE = os.environ.get('CONDA_EXE', 'conda')


@dataclasses.dataclass
class Environment:
    cache_timeout: int = CACHE_TIMEOUT
    conda_list_cache_expiry: float = dataclasses.field(init=False, default=None, repr=False)
    info: typing.Dict[str, typing.Any] = dataclasses.field(init=False)
    _info: typing.Dict[str, typing.Any] = dataclasses.field(init=False, repr=False)

    def __post_init__(self):
        self.hostname = socket.gethostname()
        self.sys_info = self._get_sysinfo()

    @property
    def info(self) -> typing.Dict[str, typing.Any]:

        self._info = {
            'sys_info': self.sys_info,
            'process_info': self._get_process_info(),
            'hostname': self.hostname,
            'conda_list_info': self._get_conda_list_info(),
        }

        return self._info

    @info.setter
    def info(self, info: typing.Dict[str, typing.Any] = {}):
        self._info = info

    def _get_sysinfo(self):
        return {
            'compiler': platform.python_compiler(),
            'operating_system': platform.system(),
            'release': platform.release(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'cpu_cores': multiprocessing.cpu_count(),
            'architecture': platform.architecture()[0],
            'python_implementation': platform.python_implementation(),
            'python_version': platform.python_version(),
        }

    def _get_commit_hash(self):
        raise NotImplementedError()

    def _get_git_remote_origin(self):
        raise NotImplementedError()

    def _get_git_branch(self):
        raise NotImplementedError()

    def _get_process_info(self):
        pid = os.getpid()
        p = psutil.Process(pid)
        dt = datetime.datetime.fromtimestamp(p.create_time())
        iso_dt = dt.astimezone(tz=datetime.timezone.utc).isoformat()
        return {
            'cmdline': p.cmdline(),
            'cwd': p.cwd(),
            'exe': p.exe(),
            'name': p.name(),
            'iso_dt': iso_dt,
        }

    def _get_conda_list_info(self):
        """
        Get and parse the whole conda list output
        Caches the information for CACHE_TIMEOUT seconds, as this is relatively expensive

        Note
        ----
        Adapted from https://github.com/Anaconda-Platform/nb_conda_kernels/blob/master/nb_conda_kernels/manager.py#L112
        """

        expiry = self.conda_list_cache_expiry
        if expiry is None or expiry < time.time():
            print('refreshing conda list info')
            # This is to make sure that subprocess can find 'conda' even if
            # it is a Windows batch file---which is the case in non-root
            # conda environments.
            shell = CONDA_EXE == 'conda' and sys.platform.startswith('win')
            try:
                env_name = os.environ['CONDA_DEFAULT_ENV']
                # conda list --json uses the standard JSON escaping
                # mechanism for non-ASCII characters. So it is always
                # valid to decode here as 'ascii', since the JSON loads()
                # method will recover any original Unicode for us.

                p = subprocess.check_output(
                    [CONDA_EXE, 'list', '--name', env_name, '--json'], shell=shell
                ).decode('ascii')
                conda_info = json.loads(p)

            except Exception as exc:
                conda_info = None
                print(f"couldn't get conda environment list info:\n{exc}")

            self.conda_list_info = conda_info
            self.conda_list_cache_expiry = time.time() + self.cache_timeout

        return self.conda_list_info
