# PatANN - Pattern-Aware Vector Database / ANN

## Overview
PatANN is a pattern-aware, massively parallel, and distributed vector search framework designed for scalable and efficient nearest neighbor search, operating both in-memory and on-disk. Unlike conventional algorithms, PatANN leverages macro and micro patterns within vectors to drastically reduce search space before performing costly distance computations.

Refer to the website for technical details, algorithm overview, key innovations, benchmarks, and tutorials.  

Website: https://patann.dev

While still in beta, PatANN's pattern-first approach delivers unprecedented performance advantages. As shown in our benchmarks (Figure 1), PatANN consistently outperforms leading ANN libraries including HNSW (hnswlib), Google ScaNN, Facebook FAISS variants, and others in the critical recall-throughput tradeoff.

![PatANN Benchmark](https://patann.dev/plots_light/sift-128-euclidean.png)

## Installation

Install PatANN using pip:

```bash
pip install patann
```

## Usage

PatANN provides Python API as well as a command-line interface to download example code. 

### Command Line Interface

```bash
patann --help
```

Output:
```
PatANN Version: 0.1.0
Python Version: 3.11.5
PatANN - https://github.com/mesibo/patann
usage: patann [-h] [--help-examples] [--list-examples] [--copy-examples [DEST]]
PatANN: Pattern-Aware Approximate Nearest Neighbors Search
options:
  -h, --help            show this help message and exit
  --help-examples       Show information about examples
  --list-examples       List available examples
  --copy-examples [DEST]
                        Copy examples to specified directory (default: current directory)
```

### Examples

PatANN comes with several example scripts to help you get started:

```bash
patann --help-examples
```

This will display information about the included examples:

```
PatANN Version: 0.1.0
Python Version: 3.11.5
PatANN - https://github.com/mesibo/patann
PatANN: Efficient Approximate Nearest Neighbors Search

Example Helper Functions:
-----------------------
patann.help()              - Display this help message
patann.list_examples()     - List all available examples with descriptions
patann.get_examples_dir()  - Get the directory path where examples are located
patann.copy_examples()     - Copy all example files to your current directory

Available Examples:
-----------------
patann_sync_example.py:
- Demonstrates synchronous (blocking) usage of PatANN
- Shows how to create an index, add vectors, and perform queries in a sequential manner
- Suitable for simple applications where asynchronous operation is not needed

patann_async_example.py:
- Demonstrates basic asynchronous usage with a single query
- Shows how to set up callbacks for index building and query results
- Good starting point for understanding PatANN's asynchronous operation

patann_async_parallel_example.py:
- Demonstrates advanced usage with multiple parallel queries
- Shows how to handle multiple unique query vectors simultaneously
- Suitable for high-throughput applications needing parallel processing

To run an example after copying:
$ python patann_sync_example.py

For more information, visit: https://github.com/mesibo/patann
```

To list all available examples:

```bash
patann --list-examples
```

Output:
```
PatANN Version: 0.1.0
Python Version: 3.11.5
PatANN - https://github.com/mesibo/patann
Example files located at: /usr/local/lib/python3.11/site-packages/patann/examples
Available examples:
- patann_sync_example.py: Synchronous (blocking) usage of PatANN
- patann_async_example.py: Basic asynchronous usage with a single query
- patann_async_parallel_example.py: Advanced parallel query processing with multiple vectors
To copy examples to current directory, run: patann.copy_examples()
```

You can copy examples to your current directory either with:

```bash
patann --copy-examples
```

Or from within Python:

```python
	import patann
patann.copy_examples()
	```

### Python API

	PatANN supports both synchronous (blocking) and asynchronous (non-blocking) operation modes:

	1. **Synchronous Mode**: Simple sequential operations, ideal for straightforward applications
	2. **Asynchronous Mode**: High-throughput parallel operations with callbacks, ideal for production systems

## Platforms
	- Linux
- macOS (Apple Silicon)
	- Windows
	- Android
	- iOS

## Code Examples
	Code examples for all platforms (Python, Kotlin, Java, Objective-C, Swift) in both asynchronous and synchronous modes are available at https://github.com/mesibo/patann

## Key Distinguishing Features
	- Novel pattern-based probing for ANN search
	- In-Memory, On-Disk, and Hybrid Index
	- Fully asynchronous operations with built-in support for conventional synchronous execution
	- Refined search, filtering, and pagination algorithms
	- Unlimited scalability without pre-specified capacity
	- Dynamic sharding to load balance across servers
	- Cloud (in-progress) and Serverless
	- SIMD-Accelerated for both x86_64 (SSE*, AVX2, AVX-512) and ARM (NEON, SVE) platforms
- OS-optimized I/O—huge pages (Linux), large pages (Windows), and super pages (macOS)
	- NUMA-aware architecture
