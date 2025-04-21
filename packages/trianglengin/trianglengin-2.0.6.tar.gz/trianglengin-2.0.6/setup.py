# File: setup.py
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Import pybind11 BEFORE setuptools
import pybind11
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext
from setuptools.command.develop import develop as _develop

# REMOVED: Unused PLAT_TO_CMAKE dictionary
# PLAT_TO_CMAKE = {
#     "win32": "Win32",
#     "win-amd64": "x64",
#     "win-arm32": "ARM",
#     "win-arm64": "ARM64",
# }


# A CMakeExtension needs a sourcedir instead of a file list.
class CMakeExtension(Extension):
    def __init__(self, name: str, sourcedir: str = "") -> None:
        super().__init__(name, sources=[])
        self.sourcedir = os.fspath(Path(sourcedir).resolve())


class CMakeBuild(build_ext):
    def build_extension(self, ext: CMakeExtension) -> None:
        ext_fullpath = Path(self.get_ext_fullpath(ext.name)).resolve()
        extdir = ext_fullpath.parent.resolve()

        cmake_generator = os.environ.get("CMAKE_GENERATOR", "")
        cfg = "Debug" if self.debug else "Release"
        python_executable = sys.executable
        pybind11_cmake_dir = pybind11.get_cmake_dir()

        if not Path(pybind11_cmake_dir).exists():
            raise RuntimeError(
                f"Could not find Pybind11 CMake directory: {pybind11_cmake_dir}"
            )
        print(f"Found Pybind11 CMake directory: {pybind11_cmake_dir}")

        is_multi_config = any(x in cmake_generator for x in {"Visual Studio", "Xcode"})
        cmake_library_output_dir = extdir
        if is_multi_config and self.compiler.compiler_type == "msvc":
            cmake_library_output_dir = extdir.joinpath(cfg)
            cmake_library_output_dir.mkdir(parents=True, exist_ok=True)

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={cmake_library_output_dir}",
            f"-DPython_EXECUTABLE={python_executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",
            f"-Dpybind11_DIR={pybind11_cmake_dir}",
        ]

        if sys.platform.startswith("darwin"):
            archs = re.findall(r"-arch (\S+)", os.environ.get("ARCHFLAGS", ""))
            if archs:
                cmake_args += ["-DCMAKE_OSX_ARCHITECTURES={}".format(";".join(archs))]

        if "CMAKE_ARGS" in os.environ:
            cmake_args += [item for item in os.environ["CMAKE_ARGS"].split(" ") if item]

        cmake_args += [f"-DTRIANGLENGIN_VERSION_INFO={self.distribution.get_version()}"]

        build_args = ["--config", cfg]

        # Combine nested ifs using 'and'
        if self.compiler.compiler_type == "msvc" and not any(
            x in cmake_generator for x in {"NMake", "Ninja"}
        ):
            # REMOVED: Do not force architecture with -A; let cibuildwheel/CMake handle it.
            # cmake_args += ["-A", PLAT_TO_CMAKE[self.plat_name]]
            build_args += ["--", "/m"]  # Keep multi-process build for MSVC

        # Combine nested ifs using 'and'
        if (
            "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ
            and hasattr(self, "parallel")
            and self.parallel
        ):
            build_args += [f"-j{self.parallel}"]

        build_temp = Path(self.build_temp) / ext.name
        build_temp.mkdir(parents=True, exist_ok=True)

        print("-" * 10, "Running CMake prepare", "-" * 40)
        print(f"CMake command: cmake {ext.sourcedir} {' '.join(cmake_args)}")
        subprocess.run(
            ["cmake", ext.sourcedir, *cmake_args],
            cwd=build_temp,
            check=True,
        )

        print("-" * 10, "Building extension", "-" * 43)
        print(f"Build command: cmake --build . {' '.join(build_args)}")
        subprocess.run(
            ["cmake", "--build", ".", *build_args],
            cwd=build_temp,
            check=True,
        )
        print("-" * 10, "Finished building extension", "-" * 36)

        # Fallback copy mechanism (adapted from trimcts)
        if not ext_fullpath.exists():
            print(f"Extension not found at expected path: {ext_fullpath}")
            print(f"Searching in build temp: {build_temp}")
            module_name = ext.name.split(".")[-1]
            found = False
            for suffix in (".so", ".dylib", ".pyd"):
                candidates = list(build_temp.rglob(f"*{module_name}*{suffix}"))
                if candidates:
                    built = candidates[0]
                    print(f"Found candidate in build temp: {built}")
                    print(f"Copying built extension from: {built} -> {ext_fullpath}")
                    ext_fullpath.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(built, ext_fullpath)
                    found = True
                    break
            if not found:
                print(f"Searching in extdir: {extdir}")
                for suffix in (".so", ".dylib", ".pyd"):
                    candidates = list(extdir.rglob(f"{module_name}*{suffix}"))
                    if candidates:
                        built = candidates[0]
                        print(f"Found candidate in extdir: {built}")
                        print(
                            f"Copying built extension from: {built} -> {ext_fullpath}"
                        )
                        ext_fullpath.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(built, ext_fullpath)
                        found = True
                        break

            if not found:
                raise RuntimeError(
                    f"Could not find built extension {module_name}.* in {extdir} or {build_temp}"
                )
        else:
            print(f"Found built extension at target: {ext_fullpath}")


class Develop(_develop):
    """Run CMake build_ext as part of 'python setup.py develop'."""

    def run(self) -> None:
        self.run_command("build_ext")
        super().run()


setup(
    # Metadata defined in pyproject.toml
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "trianglengin": ["py.typed", "cpp/*.h"]
    },  # Include headers and py.typed
    ext_modules=[
        CMakeExtension(
            "trianglengin.trianglengin_cpp", sourcedir="src/trianglengin/cpp"
        )
    ],
    cmdclass={
        "build_ext": CMakeBuild,
        "develop": Develop,
    },
    zip_safe=False,
)
