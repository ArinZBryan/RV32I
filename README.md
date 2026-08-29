# Requirements
- Python 3 (tested with python 3.13.9)
- Python 3 Venv
- Verilator (Must be locatable from `$PATH`)
- riscv32-unknown-elf-xxxx toolchain (Must be locatable from `$PATH`)

Once Python 3, Python 3 Venv, Verilator and a RV32 toolchain have been installed, the rest of the python requirements can be installed via:
```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install .
```

# Running Testbenches
To run the testbenches using `cocotb` (building with `verilator`), simply run `pytest` from within the virtual environment. As long as you are in the root of the project or `tb/`, then the tests will be discovered and ran. Alternatively, to run a specific testbench, run `python test_<testbench name>.py` from the `tb/` directory.

# Building & Running Code
A functional C toolchain has been set up within the `c/` directory. Simply copy the `c/example/` directory and start writing C code in `main.c`. If more source files are desired, make sure to add them to the makefile. 
- `make` - If a `riscv32-unknown-elf-xxxx` toolchain is available in `$PATH`, it will be invoked and your code will be compiled with the `start.s` initialiser script into an executable `program.bin`.
- `make objdump` - If a `program.elf` executable has been created by running `make`, this will create a file `objdump.txt` the contains the dump of the compiled ELF.
- `make clean` - Remove all build artefacts

Once an executable binary file `program.bin` has been created, build the RISCV core with `verilator` (if needed) and run the program from the root directory using the following command:
```
$ python tb/run_program.py -p <absolute path to program.bin> -t <timeout for program in CPU cycles>
```
For more command-line options, refer to `python tb/run_program.py --help`

![Design Overview](./image.png)