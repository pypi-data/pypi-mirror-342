from importlib.resources import files
from jdk4py import JAVA
from pathlib import Path as P
from subprocess import call, run
from argparse import ArgumentParser, REMAINDER
from tempfile import mkdtemp
import os, sys, shutil, zipfile

_PACKAGE_DIRECTORY = files("walnut_cli")
daenv = os.environ.copy()
daenv["JAVA"] = str(JAVA)
daenv["WALNUT_JAR"] = str(_PACKAGE_DIRECTORY / "aux" / "walnut-6.2.jar")


def gen_dir(whome):
    for s in [
        "Automata Library",
        "Command Files",
        "Custom Bases",
        "Macro Library",
        "Morphism Library",
        "Result",
        "Transducer Library",
        "Word Automata Library",
    ]:
        (whome / s).mkdir(exist_ok=True)


def do_shell(args):
    sys.exit(call("jupyter console --kernel=Walnut", env=daenv, shell=True))


def do_notebook(args):
    sys.exit(call("jupyter notebook", env=daenv, shell=True))


def do_lab(args):
    sys.exit(call("jupyter lab", env=daenv, shell=True))


def do_render(args):
    origdir = P.cwd()
    tmpdir = P(mkdtemp())
    print(f"Going to {tmpdir}")
    inittar = args.init.resolve() if args.init else None
    qmd = args.qmd.resolve()
    qmd_file = qmd.name
    zipdst = qmd.stem + ".zip"
    for file in [qmd] + [P(f).resolve() for f in args.extras]:
        shutil.copy(file, tmpdir)
    gen_dir(tmpdir)
    (tmpdir / "out").mkdir(exist_ok=True)
    if inittar:
        subprocess.run(["tar", "xvf", str(inittar)], cwd=tmpdir / "Walnut", check=True)
    daenv["WALNUT_HOME"] = str(tmpdir / "Walnut")
    run(
        f"quarto add --no-prompt --quiet {str(_PACKAGE_DIRECTORY / 'aux' / 'downloadthis.zip')}",
        cwd=tmpdir,
        shell=True,
        check=True,
    )
    shutil.copy(_PACKAGE_DIRECTORY / "aux" / "walnut.xml", tmpdir)
    run(
        f"quarto render {qmd_file} --output-dir out --execute --cache --execute-daemon 1000000",
        cwd=tmpdir,
        shell=True,
        check=True,
    )
    with zipfile.ZipFile(origdir / zipdst, "w") as zipf:
        for file in (tmpdir / "out").iterdir():
            zipf.write(file, arcname=file.name)
    print("Cleaning")
    shutil.rmtree(tmpdir)


parser = ArgumentParser(prog="walnut", description="Walnut+Jupyter command-line client")
parser.add_argument(
    "-H",
    "--from-here",
    action="store_true",
    help="use current directory as WALNUT_HOME",
)
parser.add_argument(
    "-g",
    "--gen-dir",
    action="store_true",
    help="generate Walnut directories in WALNUT_HOME",
)
parser.add_argument(
    "-M", "--max-memory", default=None, help="maximum Walnut memory (ex: 64g for 64GB)"
)
subparsers = parser.add_subparsers()

parser_shell = subparsers.add_parser("shell")
parser_shell.set_defaults(func=do_shell)

parser_lab = subparsers.add_parser("lab")
parser_lab.set_defaults(func=do_lab)

parser_notebook = subparsers.add_parser("notebook")
parser_notebook.set_defaults(func=do_notebook)

parser_render = subparsers.add_parser("render")
parser_render.set_defaults(func=do_render)
parser_render.add_argument("--init", type=P, help="path to initialization tar archive")
parser_render.add_argument("qmd", type=P, help="path to .qmd file")
parser_render.add_argument("extras", nargs=REMAINDER, help="additional files to copy")

parser.set_defaults(func=do_notebook)


def main() -> None:
    args = parser.parse_args()
    if args.func:
        if args.from_here:
            daenv["WALNUT_HOME"] = os.getcwd()
        if args.gen_dir:
            gen_dir(P(daenv.get("WALNUT_HOME", ".")))
        if args.max_memory is not None:
            daenv["WALNUT_MEM"] = args.max_memory
        if "WALNUT_HOME" not in daenv:
            daenv["WALNUT_HOME"] = os.getcwd()
            gen_dir(P(daenv.get("WALNUT_HOME", ".")))
        args.func(args)
    else:
        parser.print_help()
