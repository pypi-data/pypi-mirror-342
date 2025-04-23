# scsarchive.py
#pylint: disable-all

import os
import shutil
import zipfile as scsfile

def _make_scsfile(base_name, base_dir, verbose=0, dry_run=0, owner=None, group=None, logger=None):
    """#### The function defining SCS archive format registration.
    ##### Only for use by `register_scs_format()`"""
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
    """Registers `scs` as an archive format in `shutil.get_archive_formats()`, if not already present."""
    # Avoid double registration
    if "scs" not in shutil.get_archive_formats():
        shutil.register_archive_format("scs", _make_scsfile, description="Uncompressed SCS file")

def unregister_scs_format():
    """Removes `scs` from the registered archive formats in `shutil.get_archive_formats()`, if present."""
    if "scs" in shutil.get_archive_formats():
        shutil.unregister_archive_format("scs")


def make_scs(base_name: str,
             root_dir: str,
             base_dir: str,
             verbose: bool = bool(0),
             dry_run: bool = bool(0)
            ) -> str :
    """## Create an SCS archive file.

### `base_name`:
The name of the file to create, minus any format-specific extension. This is required input.

### `root_dir`:
The directory that will be the root directory of the archive. This is required input.

### `base_dir`:
The directory where we start archiving from. This is required input.

#### `verbose`:
toggles detailed output in the console; set to `True` for detailed output. Defaults to `False`.

#### `dry_run`:
toggles creation of the SCS archive; set to `True` for testing purposes. Defaults to `False`.
    """
    if "scs" not in shutil.get_archive_formats():
        register_scs_format()
        shutil.make_archive(base_name, 'scs', root_dir, base_dir, verbose, dry_run, owner=None, group=None, logger=None)
        unregister_scs_format()
    else:
        shutil.make_archive(base_name, 'scs', root_dir, base_dir, verbose, dry_run, owner=None, group=None, logger=None)
        
