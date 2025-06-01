from plotters import render_elbows


import pandas as pd
from tslearn.clustering import TimeSeriesKMeans


import math





def timeserieskmeans_over_dataframes(
    all_bird_series: list[pd.DataFrame],
    dataframe_titles: list[str],
    cluster_count: int | None,
) -> None:
    # NOTE: this is honestly prob much higher than we need
    # elbows....
    cluster_count = cluster_count or int(math.sqrt(len(all_bird_series)))

    render_elbows(all_bird_series)

    # OKAY -- the dimension error was that all the series weren't the same length
    # happily I could fix that manually
    _tskmeans = TimeSeriesKMeans(n_clusters=cluster_count, metric="dtw")

    # labels = tskmeans.fit_predict(all_bird_series)

    # render_bird_graphs(all_bird_series, bird_names=dataframe_titles)

    # ## graph clusters
    # render_clusters(
    #     labels=labels,
    #     cluster_count=cluster_count,
    #     all_bird_series=all_bird_series,
    # )

    # render_cluster_counts(cluster_count, labels)

    # labeled_cluster_df = (
    #     pd.DataFrame(
    #         zip(dataframe_titles, labels),
    #         columns=["Bird", "Cluster"],
    #     )
    #     .sort_values(by="Cluster")
    #     .set_index("Bird")
    # )

    # labeled_cluster_df.to_csv("birds_and_cluster_indices-byPartyHour.csv")

