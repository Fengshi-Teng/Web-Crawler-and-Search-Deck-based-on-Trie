from .utils import get_links, get_text, fetch_html, ALLOWED_DOMAINS
from .trie import Trie
from collections import deque


def crawl_site(start_url: str, max_depth: int) -> dict[str, list[str]]:
    """
    Given a starting URL, return a mapping of URLs mapped to words that
    appeared on that page.

    Important: In addition to following max_depth rule, pages must not be
    visited twice
    from a single call to crawl_site.

    Parameters:

        start_url - URL of page to start crawl on.
        max_depth - Maximum link depth into site to visit.
                    Links from the start page would be depth=1, links from
                    those depth=2, and so on.

    Returns:
        Dictionary mapping strings to lists of strings.

        Dictionary keys: URLs of pages visited.
        Dictionary values: lists of all words that appeared on a given page.
    """
    # BFS
    queue = deque()
    results = {}
    depths = {}  # record depth of each url

    queue.append(start_url)
    depths[start_url] = 0
    while queue:
        current_url = queue.popleft()
        # check depth
        if depths[current_url] > max_depth:
            break
        # deal with data
        raw_html = fetch_html(current_url)
        links = get_links(raw_html, current_url)
        text = get_text(raw_html)
        # add new url within domains
        for next_url in links:
            if next_url not in depths and next_url.startswith(ALLOWED_DOMAINS):
                queue.append(next_url)
                depths[next_url] = depths[current_url] + 1
        # collect words
        words = extract_words(text)
        results[current_url] = list(words)
    return results


def extract_words(text) -> set:
    '''
    Extract unique words from a given string.
    This function processes a text string to extract all unique words.
    It retains only alphanumeric characters and apostrophes ('), replacing
    other characters (e.g., punctuation, special symbols) with spaces. The
    resulting words are returned as a set to ensure uniqueness.

    Input:
        text (str): The input string from which to extract words.

    Output:
        words: A set of unique words extracted from the input text. Words are
               split by spaces and cleaned of non-alphanumeric characters
               (except apostrophes).
    '''
    result = ""
    for char in text:
        if char.isalnum() or char == "'":
            # only numbers, characters and apostrophes can be remained
            result += char
        else:
            result += " "
    # strip the blank space
    words = {word for word in result.split() if word}
    return words


def build_index(site_url: str, max_depth: int) -> Trie:
    """
    Given a starting URL, build a `Trie` of all words seen mapped to
    the page(s) they appeared upon.

    Parameters:

        start_url - URL of page to start crawl on.
        max_depth - Maximum link depth into site to visit.

    Returns:
        `Trie` where the keys are words seen on the crawl, and the
        value associated with each key is a set of URLs that word
        appeared on.
    """
    t = Trie()
    url_words = crawl_site(site_url, max_depth)
    for url, words in url_words.items():
        for word in words:
            if word not in t:
                t[word] = set()
            t[word].add(url)
    return t
