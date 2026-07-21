# Fuzzer

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Fuzzing](https://img.shields.io/badge/-Fuzzing-F26D50?style=flat-square)

A simple custom fuzzer (fuzzer.py) for testing target binaries.

- **Brute-force mode** - sends randomly generated arguments/input to the target.
- **Bit-flipping mode** - mutates random bytes in an input file, then runs the target.
- Detects crashes (segfaults) and logs the crashing input, arguments, and mutation indices.

## Usage

### Requirements

- Python 3
- A Linux environment (crash detection relies on catching `Segmentation` faults from the OS)
- An executable target binary to fuzz

### Environment setup

The fuzzer writes mutated files, crashing samples, and logs into three folders. Create them in the working directory before running:

```bash
mkdir -p tmp crash Logs
```

- `tmp/` - stores mutated executables while fuzzing (removed automatically when no crash occurs)
- `crash/` - stores the target files that triggered a crash
- `Logs/` - stores the arguments/input passed to each crashing (or fuzzed) file

Make sure the target binary is executable:

```bash
chmod +x ./target
```

### Running

```bash
python3 fuzzer.py
```

The script is interactive. It first prints a menu and then asks for the target file:

```
1. brute_force_fuzzing
2. bit_flipping_fuzzing
select menu > 1
Input filename > ./target
```

- Enter `1` for brute-force mode or `2` for bit-flipping mode.
- Enter the path to the target binary at `Input filename >` (e.g. `./target`).

The fuzzer then loops continuously until you stop it (`Ctrl + C`).

### How arguments are passed

Both modes generate a random option in the form `-<letter>` (a single letter after a dash) plus a random value string of up to 100 characters (`MAX_COMMAND_LENGTH`).

- **Brute-force mode** runs `target -<letter>` and feeds the random value on stdin.
- **Bit-flipping mode** creates a mutated copy of the target in `tmp/`, then runs `mutated_file -<letter> <value>`, passing the value both as a command-line argument and on stdin. The bit-flip ratio is `0.0001` of the file's bytes.

When a crash (segfault) is detected, the crashing file is moved to `crash/`, and the option, value, and (for bit-flipping) the flipped byte indices are written to a file under `Logs/`.
