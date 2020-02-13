from defs import *
from data_processing import best_model
from utils import *
from scipy import stats
import os

def mahalanobis(x=None, data=None, cov=None):
    """Compute the Mahalanobis Distance between each row of x and the data
    x    : vector or matrix of data with, say, p columns.
    data : ndarray of the distribution from which Mahalanobis distance of each observation of x is to be computed.
    cov  : covariance matrix (p x p) of the distribution. If None, will be computed from data.
    """
    x_minus_mu = x - np.mean(data)
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = sp.linalg.inv(cov)
    left_term = np.dot(x_minus_mu, inv_covmat)
    mahal = np.dot(left_term, x_minus_mu.T)
    return (mahal)

def mahalanobis_pv(md, true_percentiles,df = None):
    if not df:
        df = len(obs)
    pv = 1 - chi2.cdf(md, df) # Compute the P-Values
    vec = get_adequcy_vec(filename4)
    if pv<=0.05:
        vec.append(0)
    else:
        vec.append(1)
    print(genus,"," ,model1,",",model2,",",i,",",round(md,2),",",round(pv,2), ",",",".join(map(str, vec)),",",",".join(map(str, true_percentiles)))

def get_true_percentiles(lst):
    tmp_obs = read_obs_vec(filename3)
    res = []
    for i in range(len(tmp_obs)):
        x = stats.percentileofscore(lst[i],tmp_obs[i], kind = "mean")
        res.append(x)
    with open(filename5,"w") as f:
        res_str = str(res)
        f.write(res_str[1:-1:])
    return(res)


def create_dist_file():
    res_lst = []
    with open(filename1, "r") as dist:
        for line in dist:
            lst = str_to_lst(line,"float")
            res_lst.append(lst)

    true_percentiles = get_true_percentiles(res_lst)

    rows = zip(*res_lst)
    with open(filename2, "w") as out:
        writer = csv.writer(out)
        writer.writerow(["variance", "entropy", "range", "unique", "fitch"])
        for row in rows:
            writer.writerow(row)
    return(true_percentiles)

def read_obs_vec(f):
    with open(f, "r") as obs_vec:
        vec = obs_vec.read()
        vec = vec.strip()
    vec = list(map(float, vec.split(",")))
    return (vec)

def get_adequcy_vec(f):
    with open(f, "r") as ma:
        res = ma.read()
        return(str_to_lst(res,"int"))

def transform_simulations_matrix(sim_trans):
    sim_trans[["variance", "entropy"]] = sim_trans[["variance", "entropy"]] + 1
    sim_trans[["variance", "entropy"]] = sim_trans[["variance", "entropy"]].apply(np.log2)
    sim_trans[["range", "unique", "fitch"]] = sim_trans[["range", "unique", "fitch"]].apply(np.sqrt)
    return(sim_trans)

def transform_vector(obs):
    obs = [round(x + 1, 4) if i == 0 or i == 1 else x for i, x in enumerate(obs)]  # add +1 to variance and entropy
    obs = [round(np.log2(x), 4) if i == 0 or i == 1 else round(np.sqrt(x), 4) for i, x in enumerate(obs)]  # apply log2 and sqrt transformations
    return(obs)

parser = argparse.ArgumentParser()
parser.add_argument('--genera', '-g', help='Genera to get Mahalanobis distance for',required=True)
parser.add_argument('--sanity', '-s', help='Genera to get Mahalanobis distance for',required=True)


args = parser.parse_args()
genera_file = args.genera
sanity_flag = int(args.sanity)

models = ["CONST_RATE","CONST_RATE_NO_DUPL","BASE_NUM","BASE_NUM_DUPL"]

# print header
print("genus,model1,model2,i,distance,pv,variance,entropy,range,unique,fitch,mahalanobis,variance_perc,entropy_perc,range_perc,unique_perc,fitch_perc")

models_d = model_per_genus()

with open (genera_file, "r") as genera:
    for genus in genera:
        genus = genus.strip()
        results_sum = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/result_sum"
        model1 = best_model.get_best_model(results_sum)

        if sanity_flag==1:
            model1 = models_d.get(genus)
            for model2 in models:
                for i in range(50):
                    wd = "/groups/itay_mayrose/annarice/model_adequacy/sanity/" + genus + "/" + model1 + "/adequacy_test/" + str(i) + "/" + model2 + "/adequacy_test/"
                    filename1 = wd + "stats_dist_sims"
                    filename2 = wd + "stats_dist_sims.csv"
                    filename3 = wd + "orig_stats"
                    filename4 = wd + "adequacy_vec"
                    filename5 = wd + "true_percentiles"

                    try:
                        true_percentiles = create_dist_file()
                    except:
                        continue

                    # manipulate simulations matrix
                    sim = pd.read_csv(filename2) # simulations statistics table
                    if os.path.exists(wd + "stats_dist_sims_partially.csv"):
                        os.remove(wd + "stats_dist_sims_partially.csv")
                    sim_trans = transform_simulations_matrix(sim)

                    # manipulate observation vector
                    obs = read_obs_vec(filename3) # observed statistics vector
                    obs_trans = transform_vector(obs)

                    try:
                        mahal_dist = mahalanobis(x= obs_trans, data=sim_trans)
                        #critical_val = chi2.ppf((1 - 0.01), df=len(obs))  # Critical values for two degrees of freedom
                        mahalanobis_pv(mahal_dist,true_percentiles)
                    except:
                        pass
        else:
            model2 = "NOT_SANITY"
            i = "NOT_SANITY"
            wd = "/groups/itay_mayrose/annarice/model_adequacy/genera/" + genus + "/" + model1 + "/adequacy_test/"
            filename1 = wd + "stats_dist_sims"
            filename2 = wd + "stats_dist_sims.csv"
            filename3 = wd + "orig_stats"
            filename4 = wd + "adequacy_vec"
            filename5 = wd + "true_percentiles"

            try:
                true_percentiles = create_dist_file()
            except:
                continue

            # manipulate simulations matrix
            sim = pd.read_csv(filename2) # simulations statistics table
            if os.path.exists(wd + "stats_dist_sims_partially.csv"):
                os.remove(wd + "stats_dist_sims_partially.csv")
            sim_trans = transform_simulations_matrix(sim)

            # manipulate observation vector
            obs = read_obs_vec(filename3) # observed statistics vector
            obs_trans = transform_vector(obs)

            try:
                mahal_dist = mahalanobis(x= obs_trans, data=sim_trans)
                #critical_val = chi2.ppf((1 - 0.01), df=len(obs))  # Critical values for two degrees of freedom
                mahalanobis_pv(mahal_dist,true_percentiles)
            except:
                pass