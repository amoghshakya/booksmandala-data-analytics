
import pandas as pd

def get_recommendations(title, similarity_df, df, n=5):
    idx = similarity_df.index.get_loc(title)
    sim_scores = list(enumerate(similarity_df.iloc[idx]))

    # sort the books based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:n+1]  # exclude the first one as it's the book itself

    # get the book indices
    book_indices = [i[0] for i in sim_scores]

    # top n most similar books
    return df[['Title', 'Author']].iloc[book_indices]
