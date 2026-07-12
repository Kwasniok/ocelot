import subprocess
import shlex
import os
from sys import platform, path
import shutil
import tempfile
from pathlib import Path


def remove_file(path_to_folder, filename):
    if not os.path.isdir(path_to_folder):
        return
    files = os.listdir(path_to_folder)
    if filename in files:
        os.remove(path_to_folder + "/" + filename)

def move_file(source_folder, filename, destin_folder):
    os.makedirs(destin_folder, exist_ok=True)
    files = os.listdir(source_folder)
    if filename in files:
        shutil.move(source_folder+"/" + filename,destin_folder)

def compiler_supports_openmp(compiler):
    source = "#include <omp.h>\nint main(){return 0;}\n"
    with tempfile.TemporaryDirectory() as tmpdir:
        source_path = Path(tmpdir) / "openmp_check.cpp"
        binary_path = Path(tmpdir) / "openmp_check"
        source_path.write_text(source)
        cmd = [compiler, "-fopenmp", str(source_path), "-o", str(binary_path)]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def compile(dir_path, *, compiler, openmp_supported):
    os.chdir(dir_path)
    print ("platform = ", platform, "  os.name = ", os.name)
    if os.name == "nt":
        cmd = 'c:/MinGW/bin/mingw32-make -f Makefile'
        args = shlex.split(cmd)
    else:
        args = ["make", "-f", "Makefile", f"COMPILER={compiler}"]
        if not openmp_supported:
            args.append("OPENMP_FLAGS=")
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(p.stdout)
    if p.returncode != 0:
        raise RuntimeError(
            "genera C++ build failed in {dir_path}. "
            "Install an OpenMP-capable compiler or check the compiler output above."
            .format(dir_path=dir_path)
        )

# clean
def clean_folder(dir_path):
    """
    it does not need
    """
    print (dir_path)
    os.chdir(dir_path)
    cmd = "make clean"
    if os.name == "nt":
        cmd = 'c:/MinGW/bin/mingw32-make -f Makefile'
    args = shlex.split(cmd)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.communicate()[0]
    print (result)

# move lib to genera_libs
home_path = path[0]
#print "compile ", home_path
import ocelot
#print ocelot.__file__
import os
path_to_ocelot = os.path.dirname(ocelot.__file__)


#indx = path[0].find("siberia2")

#xcode_path = home_path[:indx]
gen_path = path_to_ocelot + "/lib/genera/"

libs_path = gen_path + "build/genera_libs"

cpp_path = gen_path + "src/cpp"
os.makedirs(libs_path, exist_ok=True)

compiler = os.environ.get("CXX", "g++")
openmp_supported = compiler_supports_openmp(compiler) if os.name != "nt" else True
if not openmp_supported:
    print("OpenMP is not available for", compiler, "- building genera C++ libraries without OpenMP")

for dirname in ["undulator", "radiation", "convolution"]:
    dir_path = cpp_path + "/" + dirname

    compile(dir_path, compiler=compiler, openmp_supported=openmp_supported)

    filename = dirname +".so"

    remove_file(libs_path, filename)

    move_file(dir_path, filename, libs_path)

#shutil.move(dir_path+"/undulator.so",libs_path)
