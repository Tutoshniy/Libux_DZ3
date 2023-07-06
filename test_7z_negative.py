import yaml

from checkout import checkout_negative

with open("config.yaml") as f:
    data = yaml.safe_load(f)


def test_step1(clear_folders, make_files, make_bad_arx):
    # test1
    assert checkout_negative("cd {}; 7z e badarx.7z -o{} -y".format(data['folder_badarx'], data['folder_ext']), "ERROR"), "Test4 Fail"


def test_step2(clear_folders, make_files, make_bad_arx):
    # test2
    assert checkout_negative("cd {}; 7z t badarx.7z".format(data['folder_badarx']), "ERROR"), "Test5 Fail"
