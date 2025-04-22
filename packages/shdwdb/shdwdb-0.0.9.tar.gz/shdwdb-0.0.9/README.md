# The ShdwDB package
package for tables
## Functions
### `make(name, column_names, row_names)`
This creates a new database. `column_names` must be an iterable containing the names of the columns. `row_names` must be also be an iterable with the row names.
### `retrieve(name, filename_saved)`
Retrive a database from local filesystem. Give it a name and specifiy file path, path with be relative to current directory
## Database methods
+ `set(column, row, value)`: Set a value to a cell.
+ `delete_item(column, row)`: Set the cell value to None.
+ `delete_column(column)`: Delete the column.
+ `delete_row(row)`: Delete the row.
+ `get_value(column, row)`: Get the value of a cell.
+ `get_column(column)`: Get a column.
+ `get_row(row)`: Get a row(as a string).
+ `save(filename_to_save)`: save to local filesystem. `filename_to_save` is relative to current path
+ `add_column(name)`: Add a column.
+ `add_row(name)`: Add a row.

Release notes:
+ migrated away from replit db