=================
Using with Pandas
=================

The `pyquations` library can be seamlessly integrated with Pandas to perform calculations on DataFrames. Below is an example of how to use `pyquations` with a Pandas DataFrame to create calculated columns. It utilizes a `dataframe.apply()` method to apply the Pythagorean theorem to two columns, `a` and `b`, and store the results in a new column called `results`.

.. code-block:: python

    import pandas as pd
    from pyquations import pythagorean_theorem

    dataframe = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    dataframe["results"] = dataframe.apply(
        lambda row: pythagorean_theorem(row["a"], row["b"]), axis=1
    )