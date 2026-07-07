# Fuzzer

A simple custom fuzzer (fuzzer.py) for testing target binaries.

- **Brute-force mode** - sends randomly generated arguments/input to the target.
- **Bit-flipping mode** - mutates random bytes in an input file, then runs the target.
- Detects crashes (segfaults) and logs the crashing input, arguments, and mutation indices.
