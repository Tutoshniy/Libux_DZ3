import random
import string
import pytest
import yaml
import time

from checkout import checkout_positive

with open("config.yaml") as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout_positive(
        "mkdir {} {} {} {}".format(data['folder_in'], data['folder_out'], data['folder_ext'], data['folder_badarx']),
        "")


@pytest.fixture()
def clear_folders():
    return checkout_positive(
        "rm -rf {}/* {}/* {}/* {}/*".format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                            data['folder_badarx']), "")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(5):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=data['count_files']))
        if checkout_positive(
                "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data['folder_in'], filename,
                                                                                       data['size_file']),
                ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout_positive("cd {}; mkdir {}".format(data['folder_in'], subfoldername), ""):
        return None, None
    if not checkout_positive(
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data['folder_in'], subfoldername,
                                                                                      testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx():
    checkout_positive("cd {}; 7z a {}/arxbad".format(data['folder_in'], data['folder_out']), 'Everything is Ok')
    checkout_positive('truncate -s 1 {}/arxbad.7z'.format(data['folder_out']), 'Everything is Ok')
    yield 'arxbad'
    checkout_positive('rm -f {}/arxbad.7z'.format(data['folder_out']), '')


@pytest.fixture(autouse=True)
def write_stat():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    with open(data['stat_file'], 'r') as f:
        cpu_stats = f.read()

    stat_info = '{}, {}, {}, {}\n'.format(current_time, data['count_files'], data['size_file'], cpu_stats)

    with open(data['output_file'], 'a') as f:
        f.write(stat_info)
