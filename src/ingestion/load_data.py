from sklearn.datasets import fetch_20newsgroups

def load_dataset(categories):
    ds = fetch_20newsgroups(
        subset="train",
        categories=categories,
        remove=("headers", "footers", "quotes"),
    )
    return ds.data, ds.target, ds.target_names
