import numpy as np
import matplotlib.pyplot as plt
import hashlib

from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from sklearn.utils.extmath import fast_dot

from python_analysis_toolkit.machine_learning import clustering

_colors = ['r', 'b', 'g', 'k', 'm', 'c', 'y']  

def pca_biplot_with_clustering(data_matrix, feature_labels, K = 5, n_components=2, f_out = "foo"):
    """
    Inputs:
        data_matrix- numpy array of shape n x f where n is the number of samples and f is the number of features (variables)
        feature_labels - the list of human-interpretable labels for the rows in data_matrix. Used for the biplot
        n_components: the number of PCA vectors you want. 
        f_out: the path to write the graph (as PDF) to
        
        NOTE: the graph currently only supports n=2. 
    
    Outputs:
        None, but writes to a file on disk
    
        References:
        http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
        https://github.com/teddyroland/python-biplot/blob/master/biplot.py
        http://stackoverflow.com/questions/21217710/factor-loadings-using-sklearn
        http://stackoverflow.com/questions/14716965/r-principle-component-analysis-label-of-component
        http://nxn.se/post/36838219245/loadings-with-scikit-learn-pca
    """    
    
    data_matrix = np.nan_to_num(data_matrix) #clustering does not allow infs, nans
    rows, variables = np.shape(data_matrix)
    pca = PCA(n_components=n_components)
    transformed_matrix = pca.fit_transform(data_matrix)
    
    r_loadings = np.matrix.transpose(pca.components_) #components is n_components x f; transpase to get rows as features, like R does it 
    
    loading_vectors = []
    loading_labels = []
            
    for i in range(0, variables):
        loading_vectors.append((list(r_loadings[i])))
        loading_labels.append(str(feature_labels[i]))
    
    #Run KM
    centroids, labels = clustering.kmpp(transformed_matrix, K)
    
    #do the plot
    fig, ax = plt.subplots()

    for l in range(0, K):
        transformed_matrix_i = [transformed_matrix[i] for i in range(0, rows) if labels[i] == l]                     
        ax.scatter([x[0] for x in transformed_matrix_i], 
                   [x[1] for x in transformed_matrix_i], 
                   color = _colors[l % len(_colors)],
                   label = "cluster" + str(l))

    pxs = [i[0] for i in loading_vectors]
    pys =  [i[1] for i in loading_vectors]    
    for xindex, x in enumerate(pxs):     
        ax.arrow(0, 0, pxs[xindex], pys[xindex], width=0.0005, head_width=0.0025, color="r")
        ax.text(pxs[xindex], pys[xindex], loading_labels[xindex], color="r")
    
    x0,x1 = ax.get_xlim()
    y0,y1 = ax.get_ylim()
    ax.set_xlim(min(x0, y0), max(x1,y1))
    ax.set_ylim(min(x0, y0), max(x1,y1))      
    ax.set_xlabel("PCA[0]")
    ax.set_ylabel("PCA[1]") 
    ax.set_title("", fontsize = 20)
    ax.grid(b=True, which='major', color='k', linestyle='--')

    fig.savefig(f_out + "{0}".format(K) + ".pdf", format="pdf")    
    plt.close() #THIS IS CRUCIAL SEE:  http://stackoverflow.com/questions/26132693/matplotlib-saving-state-between-different-uses-of-io-bytesio
    


