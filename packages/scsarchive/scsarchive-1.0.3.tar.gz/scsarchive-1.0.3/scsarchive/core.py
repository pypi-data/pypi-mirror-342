# scsarchive.py
#pylint: disable-all

import os
import shutil
import zipfile as scsfile

def make_scsfile(base_name, base_dir, verbose=0, dry_run=0, owner=None, group=None, logger=None):
    scs_filename = base_name + ".scs"
    archive_dir = os.path.dirname(base_name)

    if archive_dir and not os.path.exists(archive_dir):
        if logger:
            logger.info(f"creating {archive_dir}")
        if not dry_run:
            os.makedirs(archive_dir)

    if logger:
        logger.info(f"creating '{scs_filename}' and adding '{base_dir}' to it")

    if not dry_run:
        with scsfile.ZipFile(scs_filename, "w", compression=scsfile.ZIP_STORED) as sf:
            path = os.path.normpath(base_dir)
            if path != os.curdir and os.path.relpath(path, base_dir) != '.':
                sf.write(path, os.path.relpath(path, base_dir))
                if logger:
                    logger.info(f"adding '{path}'")
            for dirpath, dirnames, filenames in os.walk(base_dir):
                for name in sorted(dirnames):
                    path = os.path.normpath(os.path.join(dirpath, name))
                    sf.write(path, os.path.relpath(path, base_dir))
                    if logger:
                        logger.info(f"adding '{path}'")
                for name in filenames:
                    path = os.path.normpath(os.path.join(dirpath, name))
                    if os.path.isfile(path):
                        sf.write(path, os.path.relpath(path, base_dir))
                        if logger:
                            logger.info(f"adding '{path}'")
    return scs_filename

def register_scs_format():
    # Avoid double registration
    if "scs" not in shutil.get_archive_formats():
        shutil.register_archive_format("scs", make_scsfile, description="Uncompressed SCS file")

def unregister_scs_format():
    if "scs" in shutil.get_archive_formats():
        shutil.unregister_archive_format("scs")
