"""AutoArchiver - an automatic archive generator.
Generates an archive out of files in the same directory as script is.

Author: wofiku
https://github.com/wofiku/autoarchiver"""


# MODULES
# Logger
import logging
# Paths and files handler
from pathlib import Path
import sys
# Subprocess runner
from subprocess import run as subprocess_run


# LOGGER
logging.basicConfig(level=logging.INFO)
logging.info("Starting creating a new archive file")


# VARS
# Version
version: str = 'v1.0'
# Script
# Name
script_name: str = str(__file__).split('\\')[-1]
# Path: Determine, if running as script or compiled file
script_path: Path = Path(sys._MEIPASS) if getattr(sys, 'frozen', False) else Path('.')


# Archiver
# Uses compiled 7-Zip for command line usage (Windows)
# 7-Zip: All rights reserved by Igor Pavlov. Get 7-Zip on https://www.7-zip.org/
arch_exe: str = str(script_path / '7z.exe')
arch_exe_keys: str = '-tzip -ssw -mx{compression_level}'
arch_exe_keys_pass: str = arch_exe_keys + ' -p{password}'
arch_exe_template: str = f'{arch_exe} a {arch_exe_keys}' + ' \'{arch_name}\' \'{input_file}\''
arch_exe_template_pass: str = f'{arch_exe} a {arch_exe_keys_pass}' + ' "{arch_name}" "{input_file}"'


# FUNCTIONS
def create_archive(files: str | list | tuple | set | Path, arch_name: str | Path, password: str | None = None,
                   compression_level: int = 9) -> None:
    """Creating an archive

    :param files: Files to archive
    :param arch_name: Name of the archive (with archive format/extension)
    :param password: (not mandatory) Password for the archive
    :param compression_level: (not mandatory) Level of compression for the files in archive
    :return: New archive
    """

    logging.info("Starting creating archive, please wait")

    # VARS
    # Convert files to list, as pyminizip works with lists
    logging.info("Getting all files")
    if isinstance(files, Path):
        files: list = list(str(files))
    else:
        files: list = list(str(_f) if isinstance(_f, Path) else
                           _f.replace('/', '\\').replace('\\\\', '\\') for _f in files)

    logging.info(f"Files selected: {', '.join(_fi for _fi in files)}")

    logging.info("Separating folders of files...")

    # Path of files for the archive to create
    folders: list = []
    for file in files:
        file: tuple = tuple(file.split('\\'))
        file_path: str = str('\\'.join(file[:-1])) if len(file) > 1 else ''
        folders.append(file_path)
    logging.info(f"Folders: {', '.join(set(_fo for _fo in folders if _fo != ''))}")

    # Convert arch_name to str, as pyminizip works with strings only
    arch_name: str = str(arch_name.resolve()) if isinstance(arch_name, Path) else str(arch_name)
    # Adding ZIP extension for the output archive, if none is declared
    arch_name: str = arch_name if '.' in arch_name else arch_name.split('.')[0] + '.zip'
    # Creating path for the archive
    arch_path: Path = (Path('.') / arch_name).resolve()

    logging.info(f"Output archive name: {arch_name} at {arch_path}")

    # Dummy check for password
    password: str = str(password) if password else None

    logging.info("Got secret password for the archive") if password else logging.info("No password selected")

    # Compression level of output archive - from scale of 0 to 9
    compression_level: int = int(compression_level)

    logging.info(f"Compression level: {compression_level}")

    # MAIN
    logging.info("Creating archive now, please wait")

    formatted_archiver_cmd_to_run = arch_exe_template_pass.format(
        compression_level=compression_level, password=password, arch_name=arch_path,
        input_file='" "'.join(str(_f) for _f in files)
    )
    subprocess_run(formatted_archiver_cmd_to_run, shell=True)
    logging.info(f"Archive {arch_name} has been created at {arch_path}")


def create_archive_from_files(directory: str | Path = '.') -> None:
    """Automatically creating archive <first_file>.zip from files in directory with password.
    Password will be saved in <first_file>.zip_password.txt file at the same directory

    :param directory: Working directory/path, where archive will gather files from
    :return: New archive
    """

    logging.info("Started creating an archive from all files from the directory")
    # VARS
    # Normalizing directory to the pathlib.Path format, so it's easier for further usage
    directory: Path = Path(directory) if isinstance(directory, str) else directory

    logging.info(f"Working directory: {directory.resolve()}")

    # Listing all files in directory (raw)
    files_in_directory: tuple = tuple(str(_dir) for _dir in (directory.glob('**/*')))
    # Listing found files in directory, but excluding the script itself
    to_exclude: tuple = (script_name, script_name.replace('.py', '.exe'), arch_exe)
    files: tuple = tuple(str(x) for x in files_in_directory if Path(x).is_file() and str(x) not in to_exclude)
    logging.info(f"Files selected: {', '.join(_fi for _fi in files)}")

    # Create archive name out of first found file
    archive_name: str = str(files[0]).split('\\')[-1].split('.')[-2] + '.zip'

    logging.info(f"Name of future archive: {archive_name}")

    # MAIN
    # Creating archive of <first_file>.zip
    create_archive(files=files, arch_name=archive_name, password=None)


if __name__ == '__main__':
    logging.info("Semi-auto running mode detected")
else:
    logging.info("External usage detected")

create_archive_from_files()
