import sys

from metrics.query_set import QUERIES
from metrics.metrics import ranking_correlation, query_response_time


metric_to_func = {
    'timing': query_response_time,
    'ranking_correlation': ranking_correlation
}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Wrong number of CL args. Should be 1: the metric type. {} given.'.format(len(sys.argv)-1))
        sys.exit(1)

    if not sys.argv[1] in metric_to_func.keys():
        print('Metric type not existent. Try one of {}'.format(str(metric_to_func.keys())))
        sys.exit(1)

    func = metric_to_func[sys.argv[1]]
    func(QUERIES)
    

    