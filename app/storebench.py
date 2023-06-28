import argparse
import os
import shutil
import subprocess
import pathlib
HEREPATH = pathlib.Path(__file__).parent.absolute()
import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def generate_libs(nb_libs, store_path, template_lib_path, verbose=False):
    """
    Generate nb_libs libs, each in their folder in store_path  
    """
    for lib in range(nb_libs):
        folder_path = os.path.join(store_path, f"hash-lib{lib}")
        folder_lib_path = os.path.join(folder_path, f"lib")
        if os.path.exists(folder_path):
            if verbose:
                logging.info(f"{folder_path} exists! removing")
            shutil.rmtree(folder_path)
        os.mkdir(folder_path)
        os.mkdir(folder_lib_path)
        so_path = os.path.join(folder_lib_path, f"lib{lib}.so")
        if verbose:
            logging.info(f"Compiling {so_path}")
        subprocess.run(["gcc", "-shared", "-o", so_path, f"-Wl,-soname,lib{lib}.so", "-x", "c", "-fPIC", template_lib_path])

def generate_rpaths(nb_libs, store_path):
    """
    Generate the rpaths for the libs
    """
    return ":".join(f"{store_path}/hash-lib{lib_id}/lib/" for lib_id in range(nb_libs))

def generate_app(nb_libs, store_path, template_app_path, verbose=False):
    """
    Generate the binary linking all the libs
    """
    cflags = " ".join(f"-l{lib_id}" for lib_id in range(nb_libs))
    rpaths = generate_rpaths(nb_libs, store_path)
    cpaths = " ".join(f"-L{store_path}/hash-lib{lib_id}/lib/" for lib_id in range(nb_libs))

    folder_path = os.path.join(store_path, f"app-{nb_libs}")
    folder_bin_path = os.path.join(folder_path, f"bin")
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.mkdir(folder_path)
    os.mkdir(folder_bin_path)
    app_path = os.path.join(folder_bin_path, f"app")

    command = ["gcc", "-o", app_path, cpaths, cflags, f"-Wl,-rpath,{rpaths}", "-x", "c", template_app_path]
    command_str = " ".join(command)
    if verbose:
        logging.info(f"Compiling app: {command_str}")
    subprocess.run(command_str, shell=True)

def main():
    parser = argparse.ArgumentParser(description="Generate a binary loading a given number of libraries")
    parser.add_argument("action", choices=["build", "ld_library_path"])
    parser.add_argument("--nb_libs", type=int, help="Number of libs to link")
    parser.add_argument("--store", help="Location of the 'store'")
    parser.add_argument("-v", "--verbose", action="store_true") 

    args = parser.parse_args()

    nb_libs = args.nb_libs
    store_path = args.store
    verbose = args.verbose

    template_lib_path = f"{HEREPATH}/template.c"
    template_app_path = f"{HEREPATH}/main.c"

    if args.action == "build":
        generate_libs(nb_libs, store_path, template_lib_path, verbose)
        generate_app(nb_libs, store_path, template_app_path, verbose)
    elif args.action == "ld_library_path":
        rpaths = generate_rpaths(nb_libs, store_path)
        print(rpaths)

if __name__ == "__main__":
    main()
