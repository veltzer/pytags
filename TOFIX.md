# TOFIX

Findings from a code scan on 2026-10-04.

## High

- `src/pytags/cmdline.py:121` - `pytags.config.ns_op.p_force = ...` assigns an attribute on a dict (`ns_op` is a dict, `src/pytags/config.py:40`), so every invocation crashes with `AttributeError` before any command runs (verified with `pytags --showconfig`); same at line 122 for `ns_mgr.p_dir`. Use item assignment.
- `src/pytags/config.py:41` - `ns_op` has keys `force`/`debug`, but the code reads `ns_op["p_force"]` (`src/pytags/mgr.py:114`, `:248`) and `ns_op["p_debug"]` (`src/pytags/mgr.py:33`), so these raise `KeyError`; use one consistent key set.
- `src/pytags/mgr.py:19` - `mysql.connector.Connect({})` passes a positional dict, which raises `TypeError` (verified), and the configured host/user/password/db in `ns_db` are never used; `connect()` and `connectNodb()` (line 22) are identical. Pass the `ns_db` values as keyword arguments (and the database only in `connect()`).
- `pyproject.toml:39` - the dependency `mysql.connector` resolves to the abandoned `mysql-connector` 2.2.9 (2019, `uv.lock:412`), not Oracle's maintained `mysql-connector-python`; switch the dependency name.

## Medium

- `src/pytags/mgr.py:98` - rows are read as `row["f_id"]` / `row["f_name"]` (also line 208), but the default cursor (`getCursor`, line 86) returns tuples, so `loadTags`/`taglist` raise `TypeError`; use `conn.cursor(dictionary=True)` or index by position.
- `src/pytags/mgr.py:75` - `conn.insert_id()` is a MySQLdb API that mysql.connector connections do not have; use the cursor's `lastrowid`.
- `src/pytags/mgr.py:56` - SQL is built with f-strings / `%` formatting from file and directory names (also line 11/71, 120, 129, 244), so a name containing a quote breaks the query or injects SQL; use parameterized `cursor.execute(query, params)`.
- `src/pytags/config.py:19` - `show()` iterates `locals()` of the function (empty) and then calls `d.__dict__` on a dict, so `--showconfig` prints only the header; iterate the module globals and print the dict items.
- `src/pytags/config.py:10` - the user config files (`~/.pytags.cfg.py`, `pytags.cfg.py`) are never loaded (the `imp.load_source` calls are commented out and `imp` is removed in current Python), so `ns_db` stays all `None` and no DB command can connect; implement config loading (e.g. `importlib` or a TOML file).

## Low

- `src/pytags/mgr.py:181` - `scan()` only loads tags and does nothing else, although `--scan` is advertised as "scan a folder recursivly"; implement it or remove the option.
- `src/pytags/mgr.py:106` - `dropTables` runs `DROP DATABASE IF EXISTS TbFileTag` (a table name) and the method is never called; delete it or fix it.
- `src/pytags/utils/boot.py:2` - leftover module from pdmt ("should never use pdmt classes"), unused anywhere in pytags; delete it.
- `rsconstruct.toml:50` - sphinx `dep_inputs = ["src/pytags/*.py"]` misses the `src/pytags/utils/` subpackage documented in `sphinx/pytags.utils.rst`; include it.
- `pyproject.toml:89` - `mypy_path = "src:python:scripts"` names `python` and `scripts` directories that do not exist; reduce to `src`.
- `src/pytags/mgr.py:50` - `# pylint: disable=...` comment is a leftover; pylint is not part of the build (ruff is).
