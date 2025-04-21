import os
import shutil
import subprocess


def clean_directory(dir: str) -> None:
    """Remove directory if it exists."""
    if os.path.exists(dir):
        shutil.rmtree(dir)


def collect_structure(base_dir: str) -> dict[str, list[str]]:
    """Walk through the base directory and collect packages and modules."""
    structure: dict[str, list[str]] = {}

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [
            d
            for d in dirs
            if d != "__pycache__"
            and not d.endswith(
                ".egg-info",
            )
        ]

        rel_path = os.path.relpath(root, base_dir)

        if rel_path == ".":
            rel_path = ""

        py_files = [
            f
            for f in files
            if f.endswith(
                ".py",
            )
            and f != "__init__.py"
        ]

        if py_files:
            structure[rel_path] = py_files

    return structure


def write_main_modules_rst(
    modules_rst_file: str, structure: dict[str, list[str]]
) -> None:
    """Write the main modules.rst file."""
    with open(modules_rst_file, "w") as f:
        f.write("API Reference\n")
        f.write("=============\n\n")
        f.write(".. include:: ../_templates/api_index.rst\n\n")
        f.write(".. toctree::\n")
        f.write("   :maxdepth: 2\n")
        f.write("   :hidden:\n\n")
        for package, modules in sorted(structure.items()):
            if package:
                f.write(f"   {package}/index\n")
            else:
                for module in sorted(modules):
                    module_name = module[:-3]
                    f.write(f"   {module_name}\n")


def write_package_index(
    package_dir: str, package_name: str, modules: list[str]
) -> None:
    """Write the index.rst file for a package."""
    os.makedirs(package_dir, exist_ok=True)
    package_index_file = os.path.join(package_dir, "index.rst")
    package_name = package_name.replace("_", " ").title()
    with open(package_index_file, "w") as f:
        f.write("=" * len(package_name) + "\n")
        f.write(f"{package_name}\n")
        f.write("=" * len(package_name) + "\n\n")
        f.write(".. toctree::\n")
        f.write("   :maxdepth: 1\n\n")
        for module in sorted(modules):
            module_name = module[:-3]
            f.write(f"   {module_name}\n")


def write_module_rst(
    module_file: str,
    module_name: str,
    module_path: str,
) -> None:
    """Write the .rst file for a module."""
    module_name = module_name.replace("_", " ").title()
    with open(module_file, "w") as f:
        f.write("=" * len(module_name) + "\n")
        f.write(f"{module_name}\n")
        f.write("=" * len(module_name) + "\n\n")
        f.write(f".. automodule:: {module_path}\n")
        f.write("   :noindex:\n")
        f.write("   :members:\n")
        f.write("   :undoc-members:\n")
        f.write("   :show-inheritance:\n\n")


def generate_modules_rst(base_dir: str, output_dir: str) -> None:
    """Generate the modules.rst file and all package/module RST files."""
    subprocess.run(
        [
            "sphinx-apidoc",
            "-o",
            output_dir,
            base_dir,
        ],
        check=True,
    )
    structure = collect_structure(base_dir)
    modules_rst_file = os.path.join(output_dir, "modules.rst")
    write_main_modules_rst(modules_rst_file, structure)

    for package, modules in structure.items():
        if package:
            package_name = package.replace("/", ".")
            package_dir = os.path.join(output_dir, package)
            write_package_index(package_dir, package_name, modules)
            for module in modules:
                module_name = module[:-3]
                module_file = os.path.join(package_dir, f"{module_name}.rst")
                module_path = f"pyquations.{package_name}.{module_name}"
                write_module_rst(module_file, module_name, module_path)
        else:
            for module in modules:
                module_name = module[:-3]
                module_file = os.path.join(output_dir, f"{module_name}.rst")
                module_path = f"pyquations.{module_name}"
                write_module_rst(module_file, module_name, module_path)

    for file in os.listdir(output_dir):
        if file.endswith(".rst") and file != "modules.rst":
            os.remove(os.path.join(output_dir, file))


def make_docs(docs_dir: str) -> None:
    """Make the HTML documentation."""
    subprocess.run(
        [
            "sphinx-build",
            "-b",
            "html",
            docs_dir,
            os.path.join(docs_dir, "_build", "html"),
            "-W",
            "-n",
            "-a",
        ],
        check=True,
    )


def build_docs() -> None:
    """Build the Sphinx documentation."""
    # Setup Directories
    docs_dir: str = os.path.dirname(os.path.abspath(__file__))
    package_dir: str = os.path.abspath(os.path.join(docs_dir, "../pyquations"))
    rst_dir: str = os.path.join(docs_dir, "api")
    html_dir: str = os.path.join(docs_dir, "_build")

    # Update Python Path with Package
    os.environ["PYTHONPATH"] = os.pathsep.join(
        [os.environ.get("PYTHONPATH", ""), package_dir]
    )

    # Remove Coverage Environment Variable
    os.environ.pop("COVERAGE_PROCESS_START", None)

    # Clean the Build Directory
    clean_directory(html_dir)

    # Clean the Output Directory
    clean_directory(rst_dir)

    # Generate RST Files
    generate_modules_rst(package_dir, rst_dir)

    # Make the Documentation
    make_docs(docs_dir)


if __name__ == "__main__":
    build_docs()
