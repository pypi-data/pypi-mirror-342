# Vecworks

Vecworks is an open-source framework build on top of Pypeworks to procedurally query vector
stores in Python. It offers the following features:

* Standardized access to various vectorization platforms, like OpenAI's, SBERT and fastText
* Mixing and matching of vectorization procedures, reducable to a single output using ensemblers
* Remote serving of custom vectorization procedures using the built-in server


## Install

Vecworks is available through the PyPI repository and can be installed using `pip`:

```bash
pip install vecworks
```

## Quickstart

Vecworks' key concept is that of the `Retriever`. A retriever is a specialised Pypeworks node 
that vectorizes inputs, allowing to cross-reference these inputs with data in a vector store. As 
nodes retrievers may be embedded in Pypeworks pipeworks, enabling various applications, including 
semantic text matching, document classification, and RAG (when combined with Langworks).

Assuming a vector store has been set-up on a PostgreSQL-database, a retriever may be instantiated as
follows:

```python
import vecworks

from vecworks.retrievers.pgvector import (
    pgvectorRetriever
)

from vecworks.vectorizers.sbert import (
    sbertVectorizer
)

match = pgvectorRetriever(

    url   = "postgresql://127.0.0.1:5432/rag-mini-wikipedia",
    # Populated using https://huggingface.co/datasets/rag-datasets/rag-mini-wikipedia

    authenticator = vecworks.auth.UsernameCredentials("username", "password"),

    table = '"text-corpus"',

    index = [

        vecworks.Index(

            name         = "passage-e5-ml-large-q",
            # Column derived from 'passage', populated with vectorized contents of 'passage'.

            bind         = "input",

            distance     = vecworks.DISTANCES.cosine,
            max_distance = 0.2,
            top_k        = 5,

            vectorizer   = sbertVectorizer.create_from_string(

                "intfloat/multilingual-e5-large",

                prompt_format = "query: "
                normalize     = True

            ),

            density      = vecworks.DENSITY.dense

        ),

    ],

    return_columns = ["passage", "id"]

    top_k       = 3

) 
```