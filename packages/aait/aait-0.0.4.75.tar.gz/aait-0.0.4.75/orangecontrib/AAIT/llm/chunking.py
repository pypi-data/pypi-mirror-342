import copy
import re
import Orange
from Orange.data import Domain, Table, StringVariable, ContinuousVariable
from chonkie import TokenChunker, WordChunker, SentenceChunker

def create_chunks(table, model, chunk_size=500, overlap=125, mode="words", progress_callback=None, argself=None):
    """
    Chunk the text contained in the column "content" of an input table, with the help of an embedding model.

    Parameters:
        table (Table): The input table to process
        model (SentenceTransformer): The embeddings model to process the text.
        mode (str): chunking mode

    Returns:
        out_data (Table): The data table with a column "Chunks" (and more rows if several chunks were obtained per text)
    """
    import copy
    from Orange.data import Domain, Table, StringVariable, ContinuousVariable

    data = copy.deepcopy(table)

    # Définir la fonction de chunking selon le mode
    if mode == "tokens":
        chunk_function = chunk_tokens
    elif mode == "words":
        chunk_function = chunk_words
    elif mode == "sentence":
        chunk_function = chunk_sentences
    elif mode == "semantic":
        chunk_function = chunk_semantic
    elif mode == "markdown":
        chunk_function = chunk_markdown
    else:
        raise ValueError(f"Invalid mode: {mode}. Valid modes are: 'tokens', 'words', 'sentence', 'markdown', 'semantic'")

    new_metas = [StringVariable("Chunks"), ContinuousVariable("Chunks index"), StringVariable("Metadata")]
    #new_metas = list(data.domain.metas) + [StringVariable("Chunks"), ContinuousVariable("Chunks index"), StringVariable("Metadata")]
    new_domain = Domain(data.domain.attributes, data.domain.class_vars, new_metas)

    new_rows = []
    for row in data:
        content = row["content"].value
        chunks, metadatas = chunk_function(content, tokenizer=model.tokenizer, chunk_size=chunk_size, chunk_overlap=overlap)

        for i, (chunk, metadata) in enumerate(zip(chunks, metadatas)):
            # Construction de la nouvelle instance avec attributs, classe(s), et nouveaux metas
            attr_values = [row[x] for x in data.domain.attributes]
            class_values = [row[y] for y in data.domain.class_vars]
            metas_values = [chunk, i, metadata]

            new_instance = Orange.data.Instance(new_domain, attr_values + class_values + metas_values)
            new_rows.append(new_instance)

    return Table.from_list(domain=new_domain, rows=new_rows)


def chunk_tokens(content, tokenizer, chunk_size=512, chunk_overlap=128, mode=None):
    chunker = TokenChunker(tokenizer=tokenizer, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = chunker.chunk(content)
    chunks = [chunk.text for chunk in chunks]
    return chunks, []

def chunk_words(content, tokenizer, chunk_size=300, chunk_overlap=100):
    chunker = WordChunker(tokenizer=tokenizer, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = chunker.chunk(content)
    chunks = [chunk.text for chunk in chunks]
    return chunks, []

def chunk_sentences(content, tokenizer, chunk_size=500, chunk_overlap=125):
    chunker = SentenceChunker(tokenizer=tokenizer, chunk_size=chunk_size, chunk_overlap=chunk_overlap,
                              min_sentences_per_chunk=1)
    chunks = chunker.chunk(content)
    chunks = [chunk.text for chunk in chunks]
    return chunks, []

def chunk_markdown(content, tokenizer=None, chunk_size=500, chunk_overlap=125):
    """
    Chunk Markdown en se basant sur les titres #, ##, ###
    Affiche des logs pour le debug.
    """

    header_regex = re.compile(r"^(#{1,6})\s+(.*)", re.MULTILINE)
    matches = list(header_regex.finditer(content))

    if not matches:
        return [], []

    sections = []
    for i, match in enumerate(matches):
        level = len(match.group(1))
        title = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[start:end].strip()
        sections.append((level, title, body))

    chunks, metadatas = [], []
    current_titles = {}

    for level, title, body in sections:
        current_titles[level] = title
        for l in range(level + 1, 7):
            current_titles.pop(l, None)

        metadata = " ; ".join(current_titles[l] for l in sorted(current_titles) if current_titles[l])
        words = body.split()

        if len(words) <= chunk_size:
            chunks.append(body)
            metadatas.append(metadata)
        else:
            for i in range(0, len(words), chunk_size - chunk_overlap):
                chunk = " ".join(words[i:i + chunk_size])
                chunks.append(chunk)
                metadatas.append(metadata)
    return chunks, metadatas

def chunk_semantic():
    pass



# def chunk_text(text):
#
#     # Basic initialization with default parameters
#     local_store_path = get_local_store_path()
#     model_name = "all-mpnet-base-v2"
#     model = os.path.join(local_store_path, "Models", "NLP", model_name)
#     chunker = SemanticChunker(
#         embedding_model=model,  # Default model
#         threshold=0.4,  # Similarity threshold (0-1)
#         similarity_window=3,
#         chunk_size=512,  # Maximum tokens per chunk
#         #min_chunk_size=300  # minimal chunk size
#     )
#
#     chunks = chunker.chunk(text)
#     chunks1 = []
#     for chunk in chunks:
#         chunks1.append(chunk.text)
#     return chunks1


    # @staticmethod
    # def chunk_data(data):
    #     """
    #     Takes a Table, segments the content of each instance into chunks of approximately
    #     400 words, stopping at sentence boundaries, and returns a new Table with the new instances.
    #
    #     :param data: The input Table.
    #     :return: A new Table with the segmented instances.
    #     """
    #
    #     new_instances = []
    #     domain = data.domain
    #
    #     # Créer un nouveau domaine avec une colonne "Chunks"
    #     new_metas = list(domain.metas) + [Orange.data.StringVariable("Chunks")]
    #     new_domain = Orange.data.Domain(domain.attributes, domain.class_vars, new_metas)
    #
    #     for instance in data:
    #         content = instance["content"].value  # Vérifie que "content" existe bien
    #         chunks = chunk_text(content)  # Découpe le texte en segments
    #
    #         for chunk in chunks:
    #             # Construire une nouvelle instance avec le segment
    #             new_metas_values = list(instance.metas) + [chunk]
    #             new_instance = Orange.data.Instance(new_domain, [instance[x] for x in domain.attributes] + [instance[y] for y in domain.class_vars] + new_metas_values)
    #             new_instances.append(new_instance)
    #
    #     # Retourner une nouvelle table avec toutes les instances générées
    #     return Orange.data.Table.from_list(new_domain, new_instances)