# Part 3, Option A: Terminal Interface Using Rich
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from .trie import Trie
from .crawler import build_index
import time


console = Console()


def main():
    # initialize
    exit_program = False
    # main loop
    while not exit_program:
        # Step1: build up a trie
        trie = build_up_trie()
        # exit the program when needed
        if trie == "quit":
            break
        # Step2: query
        query(trie)
        exit_program = wait_for_next()
    # exit
    console.print("\n"*100)
    console.print("[bold green]Goodbye![/bold green]")


def build_up_trie() -> Trie | str:
    '''
    Build a trie based on a user-provided URL and maximum depth.

    The user is prompted to input a URL and depth repeatedly until a valid trie
    is created or the user chooses to quit the program by typing "Q" for the
    URL or entering a negative integer for depth.

    Helper functions:
        wait_for_input()
        process()

    Output:
        trie: - a constructed trie
              - a string "quit" if the user chooses to exit.
    '''
    trie = None
    # loop until create a trie or type to exit the program
    while trie is None:
        # new page asking for url & depth
        console.print("\n"*100)
        # get url & depth
        start_url, max_depth = wait_for_input()
        # if type "Q" or negative number to quit the program
        if start_url is None:
            return "quit"
        # create a trie
        trie = process(start_url, max_depth)
    return trie


def wait_for_input() -> tuple:
    '''
    Prompt the user to input a valid URL and depth for crawling.

    Outputs:
        (url, depth): A tuple containing the valid URL and depth.
                      Returns (None, None) if the user chooses to quit.
    '''
    # loop until getting a valid url or getting "Q" to quit
    while True:
        url = Prompt.ask("[bold cyan]Please enter a valid URL (starting with 'https://').[/]\n(Type 'Q' to quit)\n")
        # break the loop when getting a valid url
        if url.startswith("https://"):
            break
        # type "Q" to quit
        elif url == "Q":
            return None, None
        # prompt invalid information and ask for next input
        else:
            console.print("[bold red]Invalid input. URL must start with 'https://'![/]\n")
    # prompt valid information
    console.print("[bold green]URL accepted![/]\n")

    # loop until getting a valid integer or getting an negative integer to quit
    while True:
        try:
            depth = IntPrompt.ask("[bold cyan]Please enter the crawling depth (a positive integer).[/] \n(Type a negative integer to quit)\n")
            # type a negative integer to quit
            if depth < 0:
                return None, None
            # loop until getting a valid integer
            break
        except ValueError:
            # prompt invalid infomation and ask for next input
            console.print("[bold red]Invalid input. Please enter an integer.[/]\n")
    # prompt valid information
    console.print("[bold green]Depth accepted![/]\n")

    return url, depth


def process(start_url, max_depth):
    '''
    Crawl a given URL up to a specified depth and build a trie.

    This function displays a progress animation while crawling. If the crawling
    or trie creation fails, the user is prompted to retry.

    Inputs:
        start_url (str): The starting URL for crawling.
        max_depth (int): The maximum depth for crawling.

    Outputs:
        trie: The constructed trie, or None if the crawling fails.
    '''
    # to show a progerss animation
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}")
    )
    with progress:
        # text shown when collecting data
        task = progress.add_task("[bold green]Crawling the URL and building a trie... Please wait...\n[/]", total=None)
        # create a trie
        try:
            trie = build_index(start_url, max_depth)
            # text shown after completion
            progress.update(task, description="[bold green]Trie completed!\n[/]")
            time.sleep(0.7)  # time for prompting 'Trie completed!'
        except Exception:
            # deal with failed crwaling
            progress.update(task, description="[bold red]:( Crwaling failed. Try it again!\n[/]")
            time.sleep(2)  # time for prompting 'Crwaling failed!'
            return
    return trie


def query(trie: Trie):
    '''
    Query a trie with wildcard searches for matching keyword-URL pairs.

    This function allows the user to repeatedly search the trie until they
    choose to exit.

    Helper functions:
        get_results()
        show_results()

    Input:
        trie (Trie): The trie to query
    '''
    while True:
        # Prompt the user to enter a query
        results = get_results(trie)
        # exit query on the current trie
        if results == "Q":
            console.print("[bold green]Exiting the current search session...[/]")
            break
        show_results(results)
        console.input("[bold cyan]Press the ENTER key to continue searching.[/]")


def get_results(trie: Trie):
    '''
    Perform a wildcard search on the trie for matching keyword-URL pairs.

    Input:
        trie (Trie): The trie to search.

    Output:
        results: A generator of keyword-URL pairs that match the search string.
                 Returns "Q" if the user chooses to quit the search.
    '''
    while True:
        console.print("\n"*100)
        # ask for input
        key_word = Prompt.ask('''[bold cyan]Enter a string with wildcard '*' to search.[/bold cyan]
Tips: A '*' can represent any character.
      Enter lowercase letters only.
      Type 'Q' to quit the current search session. \n''')
        # exit when asked
        if key_word == "Q":
            return key_word
        # Search the trie for matching words
        results = trie.wildcard_search(key_word)
        return results


def show_results(results):
    '''
    Display search results in a table format.

    Input:
        results: A generator of keyword-URLs(set) pairs.
    '''
    console.print("\n"*100)
    # Create a table for the current result
    table = Table(title="[bold]Search Results[/bold]")
    table.add_column("Matched Word", justify="left", style="bold cyan", no_wrap=True)
    table.add_column("Entries of Pages", justify="left", style="green")

    # add rows of data to the table
    for key_word, urls in results:
        urls = list(urls)
        # each word is shown once
        table.add_row(key_word, urls[0])
        # show the following urls
        for idx in range(1, len(urls)):
            table.add_row(None, urls[idx])

    if table.rows:
        # print table if not empty
        console.print(table)
    else:
        # Prompt to search again if no results
        console.print("[bold red]No results found.\n[/bold red]")


def wait_for_next():
    '''
    Prompt the user to decide whether to exit current session or continue.

    Args:
        prompt (str): The prompt message to display.

    Returns:
        bool: True if the user chooses to exit, False to continue.
    '''
    prompt = "[bold cyan]Would you like to exit the program or create another trie? (Q - quit / N - continue)[/bold cyan]\n"
    next_step = Prompt.ask(prompt, choices=['Q', 'N'])
    if next_step in ('Q', 'N'):
        return True if next_step == "Q" else False


if __name__ == "__main__":
    main()
