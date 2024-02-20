# yeso-compiler
A compiler for yeso, a language i created for fun.

## Documentation
Documentation and examples can be found in  the docs folder.
## Try it

To generate asembly run:
```bash
python3 src/main.py path/to/source/file.yeso
```
This will generate a file named `out.asm`

Then to compile the generated assembly run:
```bash
./scripts/compile.sh out
```

Finally to run the program run 
```bash
./out
```

Alternativly you can compile and run the program by running:
```bash
./c.sh path/to/source/file.yeso
```