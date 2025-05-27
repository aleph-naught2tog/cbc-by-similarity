import json
import numpy as np

import pandas as pd

import matplotlib.pyplot as plt
import math

from tslearn.clustering import TimeSeriesKMeans

# next: https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py

def nan_counter(list_of_series):
    nan_polluted_series_counter = 0
    for series in list_of_series:
        if series.isnull().sum().sum() > 0:
            nan_polluted_series_counter+=1

    print(nan_polluted_series_counter)

"""
NOTE: we are coercing None to -1
"""
# https://www.kaggle.com/code/izzettunc/introduction-to-time-series-clustering/notebook#1.-Introduction
def another_kmeans():
    input_filename = "data/raw/bird_map_as_json.json"

    # bird_data = translate_json_to_bird_data(input_filename)
    all_bird_series = []
    bird_names = []

    with open(input_filename) as j:
        d = json.load(j)

        # out: {  bird_name: bird_name, x_years: [...years], y_how_many: [...howMany], y_by_party_hours: [...partyHours]}
        for bird_name, itemsByYear in d.items():
            byYearItems = itemsByYear.items()
            bird_dict = {
                # "bird_name": bird_name,
                "x_years": [year for (year, _datum) in byYearItems],
                "y_how_many": [
                    (-1 if datum["howMany"] is None else datum["howMany"]) for (_year, datum) in byYearItems
                ],
                # "y_by_party_hours": [
                #     datum["numberByPartyHours"]
                #     for (_year, datum) in byYearItems
                # ],
            }

            bird_df = pd.DataFrame(bird_dict)
            bird_df.loc[:, ["x_years", "y_how_many"]]
            bird_df.set_index("x_years", inplace=True)

            all_bird_series.append(bird_df)
            bird_names.append(bird_name)

    # how_many_tall = 20
    # how_many_wide = 10
    # # fig, axs = plt.subplots(how_many_tall, how_many_wide, figsize=(50, 50))
    # fig, axs = plt.subplots(how_many_tall, how_many_wide, figsize=(50, 50))


    # # datum = all_birds_dict[42]

    # # print(datum)

    # # datum.plot()

    # for i in range(how_many_tall):
    #     for j in range(how_many_wide):
    #         if i * how_many_wide + j + 1 > len(all_bird_series):
    #             continue

    #         di = i * how_many_wide + j
    #         datum = all_bird_series[di]
    #         print(datum)

    #         axs[i, j].plot(datum.values)
    #         axs[i, j].set_title(bird_names[di])


    # plt.show()

#    # check to see if every series has the same length
#     series_lengths = {len(series) for series in all_bird_series}
#     # print(series_lengths)

#     # the answer is no!
#     ind = 0
#     for series in all_bird_series:
#         # print("["+str(ind)+"] "+series.index[0]+" "+series.index[len(series)-1])

#         ind+=1

#     # for this particular dataset we can actually see the error, BUT
#     # find the maximum length
#     max_len = max(series_lengths)
#     longest_series = None
#     for series in all_bird_series:
#         if len(series) == max_len:
#             longest_series = series

#     # FIND_MISMATCHED_SERIES
#     # we need every series to have the same length
#     # some of these have tons of nans

#     # reindex everything
#     problems_index = []

#     for i in range(len(all_bird_series)):
#         if len(all_bird_series[i])!= max_len:
#             problems_index.append(i)
#             all_bird_series[i] = all_bird_series[i].reindex(longest_series.index)

#     nan_counter(all_bird_series)
#     # KMEANS https://www.kaggle.com/code/izzettunc/introduction-to-time-series-clustering?scriptVersionId=56314361&cellId=54
    cluster_count = math.ceil(math.sqrt(len(all_bird_series)))
    # kmeans = TimeSeriesKMeans(n_clusters=cluster_count, metric="dtw")
    kmeans = TimeSeriesKMeans(n_clusters=cluster_count)
    print(all_bird_series[0])
    # dimension error here
    # example says we need to use things as a single datum
    # and doesn't really say how
    # TODO: @NEXT try the other one?
    labels = kmeans.fit_predict(all_bird_series)

    ## graph clusters
    plot_count = math.ceil(math.sqrt(cluster_count))

    fig, axs = plt.subplots(plot_count,plot_count,figsize=(25,25))
    fig.suptitle('Clusters')
    row_i=0
    column_j=0
    # For each label there is,
    # plots every series with that label
    for label in set(labels):
        cluster = []
        for i in range(len(labels)):
            if(labels[i]==label):
                axs[row_i, column_j].plot(all_bird_series[i],c="gray",alpha=0.4)
                cluster.append(all_bird_series[i])

        if len(cluster) > 0:
            axs[row_i, column_j].plot(np.average(np.vstack(cluster),axis=0),c="red")

        axs[row_i, column_j].set_title("Cluster "+str(row_i * 10 + column_j))

        column_j+=1

        if column_j%plot_count == 0:
            row_i+=1
            column_j=0

    plt.show()


def main():
    another_kmeans()


if __name__ == "__main__":
    main()
