# Fuzzer

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Fuzzing](https://img.shields.io/badge/-Fuzzing-F26D50?style=flat-square)

A simple custom fuzzer (fuzzer.py) for testing target binaries.

- **Brute-force mode** - sends randomly generated arguments/input to the target.
- **Bit-flipping mode** - mutates random bytes in an input file, then runs the target.
- Detects crashes (segfaults) and logs the crashing input, arguments, and mutation indices.
