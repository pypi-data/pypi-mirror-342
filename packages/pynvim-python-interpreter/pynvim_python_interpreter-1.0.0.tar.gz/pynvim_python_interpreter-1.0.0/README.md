# `pynvim-python-interpreter`

## Introduction

`pynvim-python-interpreter` is a thin wrapper designed to expose the Python
interpreter associated with Neovim's `pynvim` library. When placed on the
executable `PATH`, `pynvim-python-interpreter` chains to the Python interpreter
associated with `pynvim`, essentially providing a renamed Python interpreter
that won't collide with other Python interpreters on `PATH`.

NOTE: Ideally, `pynvim` and Neovim would adopt this idea to make a
zero-configuration solution.  For that reason, this project leaves the shorter
name `pynvim-python` available in case the Neovim project would like to
implement this idea in some form.

## Installation

Typical installation uses `uv`[^1] or `pipx`[^2] to install
`pynvim-python-interpreter` on the `PATH`, e.g.:

- For `uv`:

  ```sh
  uv tool install pynvim-python-interpreter
  ```

- For `pipx`:

  ```sh
  pipx install pynvim-python-interpreter
  ```

## Post-installation Neovim configuration

After installing `pynvim-python-interpreter`, configure Neovim to use it by
setting the global variable `python3_host_prog` to be the string
`pynvim-python-interpreter`:

- Via Vimscript in `init.vim`:

  ```vim
  let g:python3_host_prog = 'pynvim-python-interpreter'
  ```

- Via Lua in `init.lua`:

  ```lua
  vim.g.python3_host_prog = 'pynvim-python-interpreter'
  ```

## References

[^1]: https://docs.astral.sh/uv/
[^2]: https://pipx.pypa.io/stable/
