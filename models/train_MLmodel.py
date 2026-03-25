'''
## Data models from Fonkoze - Pistache Thomonde
## objectives:
#   1) what is the distribution of yield?
#   2) what factors result in good yield ==== are some cost elements more important? : ML train
#   3) what clusters exist? and characteristics  : k clusters
#
#   ACTION:
#   1 - describe yields
#   cross tab of cost and yield: did those who spent more generate more yield?
#   determining factors - cost === yield
'''

import pandas as pd
from sklearn import tree
# import hierarchical clustering libraries
from sklearn.cluster import AgglomerativeClustering
#import KMeans clustering
from sklearn.cluster import KMeans
import joblib



#def load_housing_data(housing_path=HOUSING_PATH):
def load_data():
    print(f"Begin: read data from file...")
    #####return pd.read_csv("RapportFinalpilotepistacheThomonde.csv", sep='\t')
    try:
        #return pd.read_csv("LetsTryThis.csv", sep='\t')
        return pd.read_csv('Data_final.csv')
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None


def AgglomerativeCluster_model(data, num_clusters):
    hc = AgglomerativeClustering(n_clusters=num_clusters,
                                 #affinity='euclidean',
                                 linkage='ward')
    print("=============== Agglomerative Cluster Model ==============")
    print(data.head())

    y_hc = hc.fit_predict(data)
    print(f"AggClustering labels: {hc.labels_}")
    return hc.labels_  # return labels to add to original dataframe



def DecisionTree(X, y, num_clusters: int):
    from sklearn.neighbors import KNeighborsClassifier
    import pickle
    try:
        neigh = KNeighborsClassifier(n_neighbors=num_clusters)
        model = neigh.fit(X, y)
        joblib.dump(model, 'ag_model.pkl')
        #pickle.dump(model, open('ag_model.pickle', 'wb'))
        response = True
    except Exception as e:
        print(f"Exception occurred: {e}")
        response = False


def controller():
    print("in controller")
    pistachepd = load_data()
    print(f"data: {pistachepd.head()}")
    clusterdata = pistachepd.filter(
        ['Gender', 'CLMclient', 'SeedPrice', 'Prep_Plow', 'Plant', 'Labor', 'Weed', 'Harvest_Labor',
         'MarmitesHarvested'], axis=1)
    clusterdata.rename(columns={'Gender': 'gender',
                                'CLMclient': 'clm_client',
                                'SeedPrice': 'seed_price',
                                'Prep_Plow': 'prep_plow',
                                'Plant': 'plant',
                                'Labor': 'labor',
                                'Weed': 'weed',
                                'Harvest_Labor': 'harvest_labor',
                                'MarmitesHarvested': 'marmites_harvested'},
                                inplace=True
    )
    #create cluster list: returns list of clusters associated with data
    clusterlist = AgglomerativeCluster_model(data=clusterdata, num_clusters=2)
    print(f"list of clusters: {clusterlist}")
    print('==== add the cluster to the initial df ====')

    pistachepd['Cluster'] = clusterlist  # add the cluster to the dataframe
    print("=== create a model basedon the clustering")

    if DecisionTree(X=clusterdata, y=clusterlist, num_clusters=2):
        print("model successfully created")
    else:
        print("model not created or saved")



if __name__ == '__main__':
    controller()