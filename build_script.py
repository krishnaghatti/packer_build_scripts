"""script that builds cloud images with customisation with packer"""
import argparse
import json
import logging
import os
import subprocess
import sys
import shutil
# import stackprinter

import sentry_sdk
sentry_sdk.init("https://c026e5599baf40b7bb721f3e32c3b015@sentry.io/1451024")

# stackprinter.set_excepthook(style='color')

logging.basicConfig(level=logging.INFO)
WORK_DIR = "/home/gsri/workspace/packer_scripts"


def list_without_hidden(WORK_DIR):
    """List dirs in a given folder with out the hidden folders"""
    list_without_hidden = []
    for each in [name for name in os.listdir(WORK_DIR) if os.path.isdir(os.path.join(WORK_DIR, name))]:
        if not each.startswith('.'):
            list_without_hidden.append(each)
    return list_without_hidden


def get_ami_id(item):
    """Gives the AMI IDs from specific manifest file"""
    json_file = os.path.join(WORK_DIR, item, 'manifest.json')
    if os.path.isfile(json_file):
        try:
            with open(json_file, 'r') as stream:
                data = json.load(stream)
                ami_id = (data['builds'][-1]['artifact_id'])
                # print(json.dumps(data, indent=4))
                logging.info(f'ami_id for {item} is {ami_id}')
        except ValueError:
            # stackprinter.show()
            logging.info('invalid json')
    else:
        # stackprinter.show()
        logging.info('manifest file not present')


def get_all_ami_ids():
    """Gives the AMI IDs from all the manifest files"""
    path_list = list_without_hidden(WORK_DIR)
    for each in path_list:
        get_ami_id(each)


def pre_checks():
    """Checks all pre required elements"""
    if not which('packer'):
        logging.info('Packer utility is not installed or is not available in the path')
        return False
    return True


def which(program):
    """checks if a OS command is present in the PATH"""
    return shutil.which(program) is not None


def main():
    """Main program execution."""
    args = parse_args()
    if pre_checks():
        decide_action(args)
    logging.info('Pre checks failed. Please check!')


def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Packer template utils.")
    parser.add_argument(
        "action", help="Define action to take", choices=[
            'build_all', 'build_specific', 'get_all_ami_ids'])
    parser.add_argument('--ami_to_build', required=False,
                        help='name of the folder from where the AMI needs to be built', type=validate_ami_to_build)
    args = parser.parse_args()
    if args.action == 'build_specific' and args.ami_to_build is None:
        parser.error('--ami_to_build is REQUIRED!')
    args = parser.parse_args()
    return args


def decide_action(args):
    """Make decision on what to do from arguments being passed."""
    if args.action == 'build_all':
        build_all()
    elif args.action == 'build_specific':
        build_specific(args)
    elif args.action == 'get_all_ami_ids':
        get_all_ami_ids()


def build_specific(ami_to_build):
    """Builds the image from the specific folder given"""
    args = parse_args()
    ami_to_build = args.ami_to_build
    logging.info(f'building AMI for {ami_to_build}')
    os.chdir(WORK_DIR)
    if validte_dir(ami_to_build) and validate_json(ami_to_build):
        os.chdir(ami_to_build)
        packer_build()


def build_all():
    """Looks for build script in each directory and then executes it."""
    logging.info('Building all images.')
    os.chdir(WORK_DIR)
    for each in list_without_hidden(WORK_DIR):
        build_specific(each)
        os.chdir(WORK_DIR)


def packer_build():
    """Builds the image with packer"""
    process = subprocess.Popen(['packer', 'build', 'baseAmi.json'])
    logging.info('AMIs are being prepared...Please wait and do not stop this program')
    logging.info('The output of the packer command is below...It will take a while to complete. be patient!')
    process.wait()
    if process.returncode != 0:
        sys.exit(1)


def validte_dir(directory):
    """Checks if a given dir exists"""
    # os.chdir(WORK_DIR)
    return bool(os.path.isdir(directory))


def validate_json(directory):
    """Checks if the baseAmi.json exists"""
    return bool(os.path.isfile(os.path.join(directory, 'baseAmi.json')))


def validate_ami_to_build(ami_to_build):
    """Validates the input argument - ami_to_build"""
    if not ami_to_build:
        raise argparse.ArgumentTypeError(f'{ami_to_build} can not be empty')
    return ami_to_build


if __name__ == '__main__':
    main()
