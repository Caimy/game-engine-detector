#!/usr/bin/env python
import sys
import os
import traceback

import common
import detector


def main():
    print("main entry!")

    workspace = os.getcwd()
    print("workspace: " + workspace)

    from optparse import OptionParser

    parser = OptionParser(usage="./main.py csv_path")

    parser.add_option("-c", "--configfile",
                      action="store", type="string", dest="config_file", default=None,
                      help="The config file path")

    parser.add_option("-z", "--zip",
                      action="store", type="string", dest="seven_zip_path", default=None,
                      help="7z path")

    parser.add_option("-p", "--pkg_dir",
                      action="store", type="string", dest="pkg_dir", default=None,
                      help="Directory that contains packages")

    (opts, args) = parser.parse_args()

    if opts.config_file is None:
        opts.config_file = "config.json"

    cfg = common.read_object_from_json_file(opts.config_file)

    cfg["7z_path"]= opts.seven_zip_path

    if opts.pkg_dir is not None:
        cfg["package_dirs"]= [opts.pkg_dir]

    d = detector.GameEngineDetector(workspace, cfg)
    d.run()
    r = d.get_all_results()

    common.result_csv_output(r, args[0])

    for e in r:
        str = "package: " + e["file_name"] + ", engine: " + e["engine"]
        if e["sub_type"]:
            str += ", subtype: " + e["sub_type"]

        if len(e["error_info"]) > 0:
            str += ", error info: " + e["error_info"]

        print(str)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
