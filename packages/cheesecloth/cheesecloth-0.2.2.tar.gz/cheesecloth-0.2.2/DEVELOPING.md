
# Initial Setup

```bash
$ maturin new --mixed --bindings pyo3 cheesecloth
$ cd cheesecloth
$ uv venv --seed
$ maturin develop
```

# Running

## Build

```bash
maturin develop --uv
```


## Tests

```bash
uv run pytest
```