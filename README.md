# Intro to NLP

Before a model can learn from text, the text has to be turned into numbers. In these notebooks you build a bag of words by hand, classify the poems of Emily Dickinson and Walt Whitman by author with TF-IDF and logistic regression, train word embeddings with a small Keras network on four handbooks about whales and horses, and work with pretrained vectors trained on six billion words — then run the same algorithm on shopping baskets, where there are no words at all.

## Learning Objectives

By the end of this repository, you should be able to:

- Tokenize text with a regular expression, normalize word forms by stemming and lemmatization, and build a bag-of-words matrix by hand and with `CountVectorizer`.
- Calculate TF-IDF weights by hand, and compare two authors' vocabularies in a word cloud of each.
- Score a text classifier with cross-validation, search the choices of the vectorizer and the classifier with `GridSearchCV`, and identify the words that decide the best model's predictions.
- Build skip-gram pairs with a sliding window, train word embeddings with a Keras network, extract them from its weights, and rank a word's neighbors by cosine distance.
- Identify the three changes that make word2vec fast enough for a whole vocabulary where notebook 02's network is not, and decide when to load pretrained vectors rather than train your own.
- Load pretrained word vectors, rank a word's neighbors by cosine similarity, solve analogies by adding and subtracting vectors, and recommend products by training word2vec on shopping baskets instead of on text.

## Learning Path

Work through the notebooks in this order.

**Scope** marks the core path every student is expected to complete. Optional lessons stay in
the repository and are worth returning to, but the day does not depend on them. **Units** are
indicative pacing, where one unit is 45 minutes.

| File / Folder | Description | Scope | Units |
|---|---|---|---|
| [**01 - Text Classification with the Bag of Words**](01_text_classification.ipynb) | Build a bag of words by hand, stem and lemmatize it, and tell Dickinson from Whitman with TF-IDF, logistic regression and a grid search. | Core | 3.5 |
| [**02 - Word Embeddings**](02_word_embeddings.ipynb) | Build skip-gram pairs from four handbooks about whales and horses, train two-dimensional embeddings for the 500 most frequent words with a small Keras network and read them from its weights. | Core | 2.75 |
| [**03 - Word2vec**](03_word2vec.ipynb) | Load pretrained GloVe vectors, look at what they know and do not, solve analogies with vector arithmetic, and recommend products by running word2vec on shopping baskets. | Core | 1.75 |

### Additional Folders and Files

| File / Folder | Description |
|---|---|
| [**Solutions**](solutions/) | Worked solutions for all three notebooks. |
| [**Data**](data/) | The two books of poems and the four animal handbooks, the tables derived from them and the scripts that build those, with their sources. |
| [**Assets**](assets/) | The figures used in the notebooks and the scripts that draw them. |
| [**pyproject.toml**](pyproject.toml) | Project configuration and dependencies. |
| [**uv.lock**](uv.lock) | Dependency lock file. |

## Setup

> [!NOTE]
> Throughout these steps, text in angle brackets like `<repo-name>` is a
> **placeholder**. Replace it, including the `< >` brackets, with your own
> value. For example, `cd <repo-name>` becomes `cd amle-intro-to-nlp`.

### 1. Create the Repository from the Template

Click **Use this template** on GitHub.

When creating the repository:

- Set yourself as the **Owner**
- Choose a repository name
- Disable **Include all branches**
- Click **Create repository**

> [!IMPORTANT]
> If you are working in pairs or groups, only **one person** should complete this step.

---

### 2. Add Collaborators (Pairs/Groups Only)

If working with teammates:

1. Open the repository on GitHub
2. Go to **Settings → Collaborators**
3. Add your teammates as collaborators
4. Share the repository link with your team

Teammates should accept the invitation before continuing.

---

### 3. Clone the Repository

Copy the SSH URL from the **Code** button on GitHub, then run:

```bash
git clone <copied-ssh-url>
```

The copied SSH URL will look like `git@github.com:<your-username>/<repo-name>.git`.

---

### 4. Move into the Project Folder and Install Dependencies

This installs all dependencies, including TensorFlow, Keras, gensim, NLTK and wordcloud, and creates a virtual environment in `.venv/`. TensorFlow is a large package, so the first install takes a few minutes. The first run of notebook 01 also downloads two NLTK corpora, WordNet for the lemmatizer and the English stop word list: 11 MB together, into a `nltk_data/` folder inside the project rather than your home directory, because NLTK refuses to read corpora from a folder other accounts can write to. It is gitignored.

```bash
cd <repo-name>
uv sync
```

---

### 5. Open the Notebooks

> [!NOTE]
> Make sure you open VS Code from the project root so it automatically detects the environment created by `uv sync`.

Launch VS Code in the project root folder:

```bash
code .
```

Then open a notebook and select the Python environment created by `uv sync` as the kernel.

## Data and Credits

All data is part of the repository, in `data/` (9 MB); [data/README.md](data/README.md) lists every file with its licence. Notebook 03 additionally downloads the pretrained GloVe vectors, **66 MB**, the first time it runs, and stores them in `~/gensim-data` outside this repository.

- **Poems by Emily Dickinson** and **Leaves of Grass** by Walt Whitman: [Project Gutenberg](https://www.gutenberg.org/) eBooks [#12242](https://www.gutenberg.org/ebooks/12242) and [#1322](https://www.gutenberg.org/ebooks/1322), public domain in the USA.
- **The four animal handbooks** of notebook 02: Project Gutenberg eBooks [#33527](https://www.gutenberg.org/ebooks/33527), [#58695](https://www.gutenberg.org/ebooks/58695), [#34175](https://www.gutenberg.org/ebooks/34175) and [#23403](https://www.gutenberg.org/ebooks/23403), public domain in the USA.
- **The shopping baskets** of notebook 03: Online Retail II, Chen, D. (2019), UCI Machine Learning Repository, [doi.org/10.24432/C5CG6D](https://doi.org/10.24432/C5CG6D), licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- **`glove-wiki-gigaword-50`**: Pennington, J., Socher, R. and Manning, C. D. (2014), [GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/projects/glove/), loaded through [gensim-data](https://github.com/piskvorky/gensim-data).
- Notebook 03 follows chapter 2 of **Jay Alammar and Maarten Grootendorst, *Hands-On Large Language Models*** (O'Reilly, 2024) — its pretrained vectors and its recommender; the book's [companion code](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models) is Apache-2.0. The book recommends songs from playlists, which cannot be redistributed; this repository uses shopping baskets instead.
- The bag of words by hand in notebook 01 follows the Bag of Words notebook of the Classical NLP lesson.
- The network of notebook 02 follows the embeddings notebook of the neuefische Intro to NLP repository.

## References & Further Reading

- [**RegexOne**](https://regexone.com/): Interactive lessons on regular expressions, for the patterns of notebook 01 and beyond.
- [**regex101**](https://regex101.com/): Test a regular expression on your own text and read an explanation of each part.
- [**Speech and Language Processing**](https://web.stanford.edu/~jurafsky/slp3/): Jurafsky and Martin's free textbook; chapters 2 (regular expressions and tokenization), 5 (logistic regression) and 6 (TF-IDF and embeddings).
- [**scikit-learn: Text feature extraction**](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction): The bag of words, TF-IDF and the options of the vectorizers.
- [**word_cloud**](https://amueller.github.io/word_cloud/): The documentation and gallery of the `wordcloud` package.
- [**The Illustrated Word2vec**](https://jalammar.github.io/illustrated-word2vec/): Jay Alammar's visual explanation of embeddings, skip-gram and negative sampling.
- [**Gensim Word2Vec tutorial**](https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html): Train, inspect and save word2vec models.
- [**Embedding Projector**](https://projector.tensorflow.org/): Explore pretrained word embeddings in 3D in the browser.

### The papers behind the notebooks

- Mikolov, T., Chen, K., Corrado, G. and Dean, J. (2013). [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781): skip-gram and CBOW, the second of which notebook 02 builds.
- Mikolov, T., Sutskever, I., Chen, K., Corrado, G. and Dean, J. (2013). [Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546): negative sampling and the subsampling of frequent words, the two of the three speed-ups in notebook 03's table that have names.
- Pennington, J., Socher, R. and Manning, C. D. (2014). [GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/projects/glove/): the pretrained vectors notebook 03 loads, and how counting co-occurrences differs from sliding a window.
- Mosteller, F. and Wallace, D. L. (1963). [Inference in an Authorship Problem](https://www.jstor.org/stable/2283270): the classic study that identified the authors of the disputed Federalist Papers from the frequencies of function words such as *upon* and *by* — the effect notebook 01 finds in the coefficients.
- Firth, J. R. (1957). A synopsis of linguistic theory 1930-1955. In *Studies in Linguistic Analysis*, 1-32. Oxford: Blackwell. The source of *"You shall know a word by the company it keeps."*
- scikit-learn example. [Classification of text documents using sparse features](https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html): TF-IDF and several classifiers on newsgroup posts.
