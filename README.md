# README

Web Crawler and Search Deck Based on Trie

Project Overview

	This project implements a web crawler and a search tool built on the Trie
	data structure. It allows users to efficiently crawl web pages and construct
	a searchable index through a command-line interface.

File Descriptions

	•	crawler.py
		Handles the web crawling functionality. This module retrieves web
		content from specified URLs, recursively crawling pages to extract
		valuable information.
	•	trie.py
		Implements the Trie data structure for storing and efficiently
		retrieving keywords and content extracted during the web crawling
		process.
	•	tui.py
		Provides a simple Text User Interface (TUI) for interacting with the
		project's features via the command line.
	•	utils.py
		Contains utility functions and helper modules for data processing,
		string manipulation, and other auxiliary tasks.

Requirements

	Before running the project, ensure the following requirements are met:

	1.	Python
		This project requires the latest version of Python. It is recommended
		to use Python 3.10 or higher.
	2.	Dependencies
		If any third-party libraries are needed, install them using the
		following command:
			---------------------------------
			pip install -r requirements.txt
			---------------------------------
		If no requirements.txt is provided, manually install the required
		libraries as needed.

Usage

	1.	Download the Project
		Download the project files to your local machine. Ensure all modules
		are in the same directory.
	2.	Run the Command-Line Interface
		Open a terminal in the project directory, navigate to the directory
		named 'Web Crawler and Search Deck based on Trie', and run:
			---------------------------------
			uv run python -m trie_search.tui
			---------------------------------
	3.	Interactive Operation
		Follow the prompts in the command-line interface to perform web
		crawling, build indices, and search for keywords.

Notes

	•	Ensure that the target websites allow crawling, and comply with
		robots.txt guidelines and relevant laws and regulations.
	•	For large-scale crawling, implement delays to avoid overwhelming the
		servers and risking IP bans.

Author & License
	Author: Fengshi Teng
	© 2025 All Rights Reserved
