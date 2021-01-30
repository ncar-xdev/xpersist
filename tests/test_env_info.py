from xpersist import Environment

env = Environment()


def test_get_sys_info():
    assert set(env.info['sys_info'].keys()) == set(
        [
            'compiler',
            'operating_system',
            'release',
            'machine',
            'processor',
            'cpu_cores',
            'architecture',
            'python_implementation',
            'python_version',
        ]
    )


def test_info():
    assert set(env.info.keys()) == set(['sys_info', 'process_info', 'hostname', 'conda_list_info'])


def test_process_info():
    assert set(env.info['process_info'].keys()) == set(['cmdline', 'cwd', 'exe', 'name', 'iso_dt'])


def test_conda_list_info():
    assert isinstance(env.info['conda_list_info'], list)
    item = env.info['conda_list_info'][0]
    assert isinstance(item, dict)
    assert set(item.keys()) == set(
        [
            'base_url',
            'build_number',
            'build_string',
            'channel',
            'dist_name',
            'name',
            'platform',
            'version',
        ]
    )
