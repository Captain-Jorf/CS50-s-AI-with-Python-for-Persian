import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.
    """
    dist = {}
    pages = list(corpus.keys())
    n = len(pages)
    links = corpus[page]

    if len(links) == 0:
        for p in pages:
            dist[p] = 1 / n
        return dist

    base = (1 - damping_factor) / n
    share = damping_factor / len(links)

    for p in pages:
        dist[p] = base
        if p in links:
            dist[p] += share

    return dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    """
    counts = {p: 0 for p in corpus}
    pages = list(corpus.keys())

    cur = random.choice(pages)
    counts[cur] += 1

    for _ in range(n - 1):
        dist = transition_model(corpus, cur, damping_factor)
        keys = list(dist.keys())
        weights = [dist[k] for k in keys]
        cur = random.choices(keys, weights=weights, k=1)[0]
        counts[cur] += 1

    return {p: counts[p] / n for p in counts}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    """
    n = len(corpus)
    ranks = {p: 1 / n for p in corpus}

    adjusted = {}
    for p, links in corpus.items():
        if len(links) == 0:
            adjusted[p] = set(corpus.keys())
        else:
            adjusted[p] = links

    incoming = {p: [] for p in corpus}
    for p, links in adjusted.items():
        for q in links:
            incoming[q].append(p)

    while True:
        new_ranks = {}
        for p in corpus:
            total = 0
            for i in incoming[p]:
                total += ranks[i] / len(adjusted[i])
            new_ranks[p] = (1 - damping_factor) / n + damping_factor * total

        s = sum(new_ranks.values())
        for p in new_ranks:
            new_ranks[p] /= s

        diff = max(abs(new_ranks[p] - ranks[p]) for p in corpus)
        ranks = new_ranks
        if diff < 0.001:
            break

    return ranks


if __name__ == "__main__":
    main()