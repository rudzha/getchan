# getchan
Fourchan thread downloader. Just a little Python experiment, that serves two purposes:
1. It lets me try out FP ideas in Python
2. It lets me grab YLYL threads before they 404 in case I come in late or I pass out

# Requirements
* Python 3.5
* requests
* PyToolz

# Usage
1. python main.py [link to the thread]
2. Wait for the thread to 404
3. Check out the freshly created thread directory

# Roadmap
1. Better url handling
2. Original post handling
3. Incremental timeout
4. Proper Python packaging, setuptools, etc
5. Thread scanning service to check boards for threads containing specific words... like ylyl, pepe, dubs
6. Generate HTML from JSON and images