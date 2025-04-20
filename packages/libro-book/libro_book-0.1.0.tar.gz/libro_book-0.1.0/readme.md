# Libro

📚 Libro: A simple command-line tool to track your reading history, with your data stored locally in a SQLite database.

## Usage

Add new book: `libro add`

Show books read by year: `libro show --year 2024`

Show book details by id: `libro show 123`

Show books read by year: `libro report`

Show books read by author: `libro report --author`

## Install

Libro is packaged as `libro-book` on PyPI.

```
pip install libro-book
```

You can also clone this repository and install it locally:

```
git clone https://github.com/mkaz/libro.git
cd libro
pip install -e .
```

## Setup

On first run, libro will create a `libro.db` database file based on database location. It will prompt for confirmation to proceed which also shows the location where the file will be created.

**Database locations:**

The following order is used to determine the database location:

1. Using the `--db` flag on command-line.

2. `libro.db` in current directory

3. Environment variable `LIBRO_DB` to specify custom file/location

4. Finally, the user's platform-specific data directory
    * Linux: `~/.local/share/libro/libro.db`
    * macOS: `~/Library/Application Support/libro/libro.db`
    * Windows: `%APPDATA%\libro\libro.db`


For example, if you want to create a new database file in the current directory, you can use the following command:

```
libro --db ./libro.db
```

### Import from Goodreads

Libro can import your reading history from a Goodreads export CSV file.

```
libro import goodreads_library_export.csv
```

There is a `genre` field for fiction and nonfiction, but this data is not available in the Goodreads export. I still need to build the edit book functionality to change the genre.

# Database Schema

## Books table

| Field | Type | Description |
|-------|------|-------------|
| id | primary key | Unique identifier |
| title | string | Book title |
| author | string | Book author |
| pages | int | Number of pages in book |
| pub_year | int | Year book was published |
| genre | string | Fiction or nonfiction |

## Reviews table

| Field | Type | Description |
|-------|------|-------------|
| id | primary key | Unique identifier |
| book_id | foreign key | Book identifier |
| date_read | date | Date book was read |
| rating | float | Number between 0 and 5 |
| review | text | Review of book |

# Packaging

Notes to self, I forget how to do this stuff.

Libro is packaged as `libro-book` on PyPI.

Packaging is done with `hatchling`, [see Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

```
# install tools
py -m pip install --upgrade build twine
```

```
# build
py -m build
```

```
# upload
py -m twine upload dist/*
```
