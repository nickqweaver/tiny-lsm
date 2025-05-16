# Tiny LSM Storage Engine

A lightweight, educational implementation of an LSM (Log-Structured Merge-Tree) storage engine in Python. This project is built for learning purposes to understand how LSM trees work in real-world databases like RocksDB, LevelDB, and others.

## Features

- Simple key-value store with PUT, GET, DELETE operations
- In-memory memtable with configurable capacity
- Automatic flushing of memtable to disk as SSTable when full
- SSTable compaction to handle disk space efficiency
- REPL interface for interactive usage

## How It Works

This implementation follows the standard LSM tree architecture:

1. Writes go to an in-memory memtable first
2. When the memtable reaches capacity, it's sorted and flushed to disk as an SSTable
3. Read operations check the memtable first, then scan through SSTables (newest to oldest)
4. Periodic compaction merges SSTables to reclaim space and improve read performance

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run the REPL interface
python main.py
```

### Commands

In the REPL interface:

- `PUT key%value` - Store a key-value pair
- `GET key` - Retrieve a value by key
- `DELETE key` - Delete a key-value pair
- `help` - Display available commands
- `quit` - Exit the program

Example:
```
> PUT fruit%apple
Added fruit, apple successfully
> GET fruit
GET fruit -> apple
```

## Project Structure

- `main.py` - REPL interface and command parsing
- `tiny_lsm/` - Core implementation
  - `engine.py` - Main storage engine implementation
  - `memtable.py` - In-memory table implementation
  - `tests/` - Test suite

## Limitations

This is a toy implementation meant for educational purposes:
- No real concurrency controls
- Simple file format for SSTables
- Linear search through SSTables (no indexing or bloom filters)
- Basic compaction strategy
- No recovery mechanism

## Running Tests

```bash
pytest
```