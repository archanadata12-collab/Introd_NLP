# Data

Three corpora. Notebooks 01 and 03 work on the poems; notebook 02 works on the animal books, which
give every word a subject to keep company with; notebook 03 closes on the shopping baskets, where
the same algorithm runs on something that is not language at all.

## The poems

| File | Contents | Source and licence |
|---|---|---|
| `dickinson_poems.txt` | *Poems by Emily Dickinson, Three Series, Complete* (1890 to 1896), as distributed by Project Gutenberg | [Project Gutenberg eBook #12242](https://www.gutenberg.org/ebooks/12242), public domain in the USA; the Project Gutenberg License is included in the file |
| `whitman_leaves_of_grass.txt` | *Leaves of Grass* by Walt Whitman (1891 to 1892 edition), as distributed by Project Gutenberg | [Project Gutenberg eBook #1322](https://www.gutenberg.org/ebooks/1322), public domain in the USA; the Project Gutenberg License is included in the file |
| `poems.csv` | The 1,082 poems and poem sections of both books, one per row (`author`, `title`, `text`), with straight quotes, no italic underscores and no double hyphens | Derived from the two files above by `build_poems.py` |

## The animal books

Four handbooks, two about whales and two about horses, as distributed by Project Gutenberg.

| File | Contents | Source and licence |
|---|---|---|
| `whales_dolphins_porpoises.txt` | *Whales, Dolphins, and Porpoises of the Western North Atlantic: A Guide to Their Identification* by Leatherwood, Caldwell and Winn (NOAA Technical Report NMFS CIRC-396, 1976) | [Project Gutenberg eBook #33527](https://www.gutenberg.org/ebooks/33527), public domain in the USA; the Project Gutenberg License is included in the file |
| `whale_primer.txt` | *Whale Primer, with Special Attention to the California Gray Whale* by Theodore J. Walker (Cabrillo Historical Association, 1962) | [Project Gutenberg eBook #58695](https://www.gutenberg.org/ebooks/58695), public domain in the country of publication; the Project Gutenberg License is included in the file |
| `domestic_animals.txt` | *Domestic Animals: History and Description of the Horse, Mule, Cattle, Sheep, Swine, Poultry and Farm Dogs* by Richard Lamb Allen (1847). Only chapter V, "The Horse", is used | [Project Gutenberg eBook #34175](https://www.gutenberg.org/ebooks/34175), public domain in the USA; the Project Gutenberg License is included in the file |
| `diseases_of_the_horse.txt` | *Special Report on Diseases of the Horse*, US Department of Agriculture, Bureau of Animal Industry (revised edition, 1916). The index is not used | [Project Gutenberg eBook #23403](https://www.gutenberg.org/ebooks/23403), public domain in the USA; the Project Gutenberg License is included in the file |
| `animals.csv` | The 1,221 paragraphs of those four books, one per row (`subject`, `source`, `text`), with straight quotes, no italic underscores and no double hyphens, the two subjects cut to about the same number of words: 54,994 about whales and 54,928 about horses | Derived from the four files above by `build_animals.py` |

## The shopping baskets

| File | Contents | Source and licence |
|---|---|---|
| `baskets.csv` | 33,653 baskets of a British online gift shop, one per row (`invoice`, `items`), the items being stock codes separated by spaces. Cancelled invoices, returns, single-item baskets and baskets of more than sixty products are left out; 627,978 items remain, median basket 16 | Derived by `build_baskets.py` from the source below |
| `products.csv` | The 4,607 stock codes those baskets contain (`code`, `description`), each under the description it is sold with most often | Derived by `build_baskets.py` from the source below |

Both come from **Online Retail II**, Chen, D. (2019), UCI Machine Learning Repository,
[doi.org/10.24432/C5CG6D](https://doi.org/10.24432/C5CG6D), licensed
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The source spreadsheet is 43 MB and
holds a million order lines over two years; `build_baskets.py` downloads it and keeps only what
notebook 03 reads, so the spreadsheet itself is not part of this repository.
