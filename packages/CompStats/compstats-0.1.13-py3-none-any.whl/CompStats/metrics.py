# Copyright 2025 Sergio Nava Muñoz and Mario Graff Guerrero

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from functools import wraps
from sklearn import metrics
from scipy import stats
from CompStats.interface import Perf
from CompStats.utils import metrics_docs


########################################################
#################### Classification ####################
########################################################


@metrics_docs(hy_name='y_pred', attr_name='score_func')
def accuracy_score(y_true, *y_pred,
                   normalize=True, sample_weight=None,
                   num_samples: int=500,
                   n_jobs: int=-1, 
                   use_tqdm=True,
                   **kwargs):
    """accuracy_score"""

    @wraps(metrics.accuracy_score)
    def inner(y, hy):
        return metrics.accuracy_score(y, hy,
                                      normalize=normalize,
                                      sample_weight=sample_weight)
    return Perf(y_true, *y_pred, score_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='score_func')
def balanced_accuracy_score(y_true, *y_pred,
                            sample_weight=None, adjusted=False,
                            num_samples: int=500,
                            n_jobs: int=-1,
                            use_tqdm=True,
                            **kwargs):
    """balanced_accuracy_score"""

    @wraps(metrics.balanced_accuracy_score)
    def inner(y, hy):
        return metrics.balanced_accuracy_score(y, hy,
                                               adjusted=adjusted,
                                               sample_weight=sample_weight)
    return Perf(y_true, *y_pred, score_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_score', attr_name='score_func')
def top_k_accuracy_score(y_true, *y_score, k=2,
                         normalize=True, sample_weight=None,
                         labels=None,
                         num_samples: int=500,
                         n_jobs: int=-1,
                         use_tqdm=True,
                         **kwargs):
    """top_k_accuracy_score"""

    @wraps(metrics.top_k_accuracy_score)
    def inner(y, hy):
        return metrics.top_k_accuracy_score(y, hy, k=k,
                                            normalize=normalize, sample_weight=sample_weight,
                                            labels=labels)
    return Perf(y_true, *y_score, score_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_score', attr_name='score_func')
def average_precision_score(y_true, *y_score,
                            average='macro',
                            sample_weight=None,
                            num_samples: int=500,
                            n_jobs: int=-1,
                            use_tqdm=True,
                            **kwargs):
    """average_precision_score"""

    @wraps(metrics.average_precision_score)
    def inner(y, hy):
        return metrics.average_precision_score(y, hy,
                                               average=average,
                                               sample_weight=sample_weight)
    return Perf(y_true, *y_score, score_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_proba', attr_name='error_func')
def brier_score_loss(y_true, *y_proba,
                     sample_weight=None,
                     pos_label=None,
                     num_samples: int=500,
                     n_jobs: int=-1,
                     use_tqdm=True,
                     **kwargs                     
                     ):
    """brier_score_loss"""

    @wraps(metrics.brier_score_loss)
    def inner(y, hy):
        return metrics.brier_score_loss(y, hy,
                                        sample_weight=sample_weight,
                                        pos_label=pos_label)
    return Perf(y_true, *y_proba, score_func=None, error_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='score_func')
def f1_score(y_true, *y_pred, labels=None, pos_label=1,
             average='binary', sample_weight=None,
             zero_division='warn', num_samples: int=500,
             n_jobs: int=-1, use_tqdm=True,
             **kwargs):
    """f1_score"""

    @wraps(metrics.f1_score)
    def inner(y, hy):
        return metrics.f1_score(y, hy, labels=labels,
                                pos_label=pos_label,
                                average=average,
                                sample_weight=sample_weight,
                                zero_division=zero_division)
    return Perf(y_true, *y_pred, score_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='error_func')
def log_loss(y_true, *y_pred,
             normalize=True,
             sample_weight=None,
             labels=None,
             num_samples: int=500,
             n_jobs: int=-1,
             use_tqdm=True,
             **kwargs):
    """log_loss"""

    @wraps(metrics.log_loss)
    def inner(y, hy):
        return metrics.log_loss(y, hy, normalize=normalize,
                                sample_weight=sample_weight,
                                labels=labels)
    return Perf(y_true, *y_pred, error_func=inner, score_func=None,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='score_func')
def precision_score(y_true,
                    *y_pred,
                    labels=None,
                    pos_label=1,
                    average='binary',
                    sample_weight=None,
                    zero_division='warn',
                    num_samples: int=500,
                    n_jobs: int=-1,
                    use_tqdm=True,
                    **kwargs):
    """precision_score"""

    @wraps(metrics.precision_score)
    def inner(y, hy):
        return metrics.precision_score(y, hy,
                                       labels=labels,
                                       pos_label=pos_label,
                                       average=average,
                                       sample_weight=sample_weight,
                                       zero_division=zero_division)
    return Perf(y_true, *y_pred, score_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='score_func')
def recall_score(y_true,
                 *y_pred,
                 labels=None,
                 pos_label=1,
                 average='binary',
                 sample_weight=None,
                 zero_division='warn',
                 num_samples: int=500,
                 n_jobs: int=-1,
                 use_tqdm=True,
                 **kwargs):
    """recall_score"""

    @wraps(metrics.recall_score)
    def inner(y, hy):
        return metrics.recall_score(y, hy,
                                    labels=labels,
                                    pos_label=pos_label,
                                    average=average,
                                    sample_weight=sample_weight,
                                    zero_division=zero_division)
    return Perf(y_true, *y_pred, score_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='score_func')
def jaccard_score(y_true,
                  *y_pred,
                  labels=None,
                  pos_label=1,
                  average='binary',
                  sample_weight=None,
                  zero_division='warn',
                  num_samples: int=500,
                  n_jobs: int=-1,
                  use_tqdm=True,
                  **kwargs):
    """jaccard_score"""

    @wraps(metrics.jaccard_score)
    def inner(y, hy):
        return metrics.jaccard_score(y, hy,
                                     labels=labels,
                                     pos_label=pos_label,
                                     average=average,
                                     sample_weight=sample_weight,
                                     zero_division=zero_division)
    return Perf(y_true, *y_pred, score_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_score', attr_name='score_func')
def roc_auc_score(y_true,
                  *y_score,
                  average='macro',
                  sample_weight=None,
                  max_fpr=None,
                  multi_class='raise',
                  labels=None,
                  num_samples: int=500,
                  n_jobs: int=-1,
                  use_tqdm=True,
                  **kwargs):
    """roc_auc_score"""

    @wraps(metrics.roc_auc_score)
    def inner(y, hy):
        return metrics.roc_auc_score(y, hy,
                                     average=average,
                                     sample_weight=sample_weight,
                                     max_fpr=max_fpr,
                                     multi_class=multi_class,
                                     labels=labels)
    return Perf(y_true, *y_score, score_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_proba', attr_name='score_func')
def d2_log_loss_score(y_true, *y_proba,
                      sample_weight=None,
                      labels=None,
                      num_samples: int=500,
                      n_jobs: int=-1,
                      use_tqdm=True,
                      **kwargs):
    """d2_log_loss_score"""

    @wraps(metrics.d2_log_loss_score)
    def inner(y, hy):
        return metrics.d2_log_loss_score(y, hy,
                                        sample_weight=sample_weight,
                                        labels=labels)
    return Perf(y_true, *y_proba, score_func=inner, error_func=None,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


def macro_f1(y_true, *y_pred, labels=None,
             sample_weight=None, zero_division='warn',
             num_samples: int=500, n_jobs: int=-1, use_tqdm=True,
             **kwargs):
    """:py:class:`~CompStats.interface.Perf` with :py:func:`~sklearn.metrics.f1_score` (as :py:attr:`score_func`) with the parameteres needed to compute the macro score. The parameters not described can be found in :py:func:`~sklearn.metrics.macro_f1`

    :param y_true: True measurement or could be a pandas.DataFrame where column label 'y' corresponds to the true measurement. 
    :type y_true: numpy.ndarray or pandas.DataFrame 
    :param y_pred: Predictions, the algorithms will be identified with alg-k where k=1 is the first argument included in :py:attr:`y_pred.` 
    :type y_pred: numpy.ndarray 
    :param kwargs: Predictions, the algorithms will be identified using the keyword  
    :type kwargs: numpy.ndarray 
    :param num_samples: Number of bootstrap samples, default=500. 
    :type num_samples: int 
    :param n_jobs: Number of jobs to compute the statistic, default=-1 corresponding to use all threads. 
    :type n_jobs: int 
    :param use_tqdm: Whether to use tqdm.tqdm to visualize the progress, default=True 
    :type use_tqdm: bool     
    """
    return f1_score(y_true, *y_pred, labels=labels, average='macro',
                    sample_weight=sample_weight, zero_division=zero_division,
                    num_samples=num_samples, n_jobs=n_jobs,
                    use_tqdm=use_tqdm, **kwargs)


def macro_recall(y_true, *y_pred, labels=None,
                 sample_weight=None, zero_division='warn',
                 num_samples: int=500, n_jobs: int=-1, use_tqdm=True,
                 **kwargs):
    """:py:class:`~CompStats.interface.Perf` with :py:func:`~sklearn.metrics.recall_score` (as :py:attr:`score_func`) with the parameteres needed to compute the macro score. The parameters not described can be found in :py:func:`~sklearn.metrics.macro_recall`

    :param y_true: True measurement or could be a pandas.DataFrame where column label 'y' corresponds to the true measurement. 
    :type y_true: numpy.ndarray or pandas.DataFrame 
    :param y_pred: Predictions, the algorithms will be identified with alg-k where k=1 is the first argument included in :py:attr:`y_pred.` 
    :type y_pred: numpy.ndarray 
    :param kwargs: Predictions, the algorithms will be identified using the keyword  
    :type kwargs: numpy.ndarray 
    :param num_samples: Number of bootstrap samples, default=500. 
    :type num_samples: int 
    :param n_jobs: Number of jobs to compute the statistic, default=-1 corresponding to use all threads. 
    :type n_jobs: int 
    :param use_tqdm: Whether to use tqdm.tqdm to visualize the progress, default=True 
    :type use_tqdm: bool     
    """
    return recall_score(y_true, *y_pred, labels=labels, average='macro',
                        sample_weight=sample_weight, zero_division=zero_division,
                        num_samples=num_samples, n_jobs=n_jobs,
                        use_tqdm=use_tqdm, **kwargs)


def macro_precision(y_true, *y_pred, labels=None,
                    sample_weight=None, zero_division='warn',
                    num_samples: int=500, n_jobs: int=-1, use_tqdm=True,
                    **kwargs):
    """:py:class:`~CompStats.interface.Perf` with :py:func:`~sklearn.metrics.precision_score` (as :py:attr:`score_func`) with the parameteres needed to compute the macro score. The parameters not described can be found in :py:func:`~sklearn.metrics.macro_precision`

    :param y_true: True measurement or could be a pandas.DataFrame where column label 'y' corresponds to the true measurement. 
    :type y_true: numpy.ndarray or pandas.DataFrame 
    :param y_pred: Predictions, the algorithms will be identified with alg-k where k=1 is the first argument included in :py:attr:`y_pred.` 
    :type y_pred: numpy.ndarray 
    :param kwargs: Predictions, the algorithms will be identified using the keyword  
    :type kwargs: numpy.ndarray 
    :param num_samples: Number of bootstrap samples, default=500. 
    :type num_samples: int 
    :param n_jobs: Number of jobs to compute the statistic, default=-1 corresponding to use all threads. 
    :type n_jobs: int 
    :param use_tqdm: Whether to use tqdm.tqdm to visualize the progress, default=True 
    :type use_tqdm: bool     
    """
    return precision_score(y_true, *y_pred, labels=labels, average='macro',
                           sample_weight=sample_weight, zero_division=zero_division,
                           num_samples=num_samples, n_jobs=n_jobs,
                           use_tqdm=use_tqdm, **kwargs)


########################################################
#################### Regression ########################
########################################################


@metrics_docs(hy_name='y_pred', attr_name='score_func')
def explained_variance_score(y_true,
                             *y_pred,
                             sample_weight=None,
                             multioutput='uniform_average',
                             force_finite=True,
                             num_samples: int=500,
                             n_jobs: int=-1,
                             use_tqdm=True,
                             **kwargs):
    """explained_variance_score"""

    @wraps(metrics.explained_variance_score)
    def inner(y, hy):
        return metrics.explained_variance_score(y, hy,
                                                sample_weight=sample_weight,
                                                multioutput=multioutput,
                                                force_finite=force_finite)
    return Perf(y_true, *y_pred, score_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='error_func')
def max_error(y_true, *y_pred, 
              num_samples: int=500,
              n_jobs: int=-1,
              use_tqdm=True,
              **kwargs):
    """max_error"""

    @wraps(metrics.max_error)
    def inner(y, hy):
        return metrics.max_error(y, hy)
    return Perf(y_true, *y_pred, score_func=None, error_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='error_func')
def mean_absolute_error(y_true,
                        *y_pred,
                        sample_weight=None,
                        multioutput='uniform_average',
                        num_samples: int=500,
                        n_jobs: int=-1,
                        use_tqdm=True,
                        **kwargs):
    """mean_absolute_error"""

    @wraps(metrics.mean_absolute_error)
    def inner(y, hy):
        return metrics.mean_absolute_error(y, hy,
                                           sample_weight=sample_weight,
                                           multioutput=multioutput)

    return Perf(y_true, *y_pred, score_func=None, error_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='error_func')
def mean_squared_error(y_true,
                       *y_pred,
                       sample_weight=None,
                       multioutput='uniform_average',
                       num_samples: int=500,
                       n_jobs: int=-1,
                       use_tqdm=True,
                       **kwargs):
    """mean_squared_error"""

    @wraps(metrics.mean_squared_error)
    def inner(y, hy):
        return metrics.mean_squared_error(y, hy,
                                          sample_weight=sample_weight,
                                          multioutput=multioutput)

    return Perf(y_true, *y_pred, score_func=None, error_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='error_func')
def root_mean_squared_error(y_true,
                            *y_pred,
                            sample_weight=None,
                            multioutput='uniform_average',
                            num_samples: int=500,
                            n_jobs: int=-1,
                            use_tqdm=True,
                            **kwargs):
    """root_mean_squared_error"""

    @wraps(metrics.root_mean_squared_error)
    def inner(y, hy):
        return metrics.root_mean_squared_error(y, hy,
                                               sample_weight=sample_weight,
                                               multioutput=multioutput)

    return Perf(y_true, *y_pred, score_func=None, error_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='error_func')
def mean_squared_log_error(y_true,
                           *y_pred,
                           sample_weight=None,
                           multioutput='uniform_average',
                           num_samples: int=500,
                           n_jobs: int=-1,
                           use_tqdm=True,
                           **kwargs):
    """mean_squared_log_error"""

    @wraps(metrics.mean_squared_log_error)
    def inner(y, hy):
        return metrics.mean_squared_log_error(y, hy,
                                              sample_weight=sample_weight,
                                              multioutput=multioutput)

    return Perf(y_true, *y_pred, score_func=None, error_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='error_func')
def root_mean_squared_log_error(y_true,
                                *y_pred,
                                sample_weight=None,
                                multioutput='uniform_average',
                                num_samples: int=500,
                                n_jobs: int=-1,
                                use_tqdm=True,
                                **kwargs):
    """root_mean_squared_log_error"""

    @wraps(metrics.root_mean_squared_log_error)
    def inner(y, hy):
        return metrics.root_mean_squared_log_error(y, hy,
                                                   sample_weight=sample_weight,
                                                   multioutput=multioutput)

    return Perf(y_true, *y_pred, score_func=None, error_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='error_func')
def median_absolute_error(y_true,
                          *y_pred,
                          sample_weight=None,
                          multioutput='uniform_average',
                          num_samples: int=500,
                          n_jobs: int=-1,
                          use_tqdm=True,
                          **kwargs):
    """median_absolute_error"""

    @wraps(metrics.median_absolute_error)
    def inner(y, hy):
        return metrics.median_absolute_error(y, hy,
                                             sample_weight=sample_weight,
                                             multioutput=multioutput)

    return Perf(y_true, *y_pred, score_func=None, error_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='score_func')
def r2_score(y_true,
             *y_pred,
             sample_weight=None,
             multioutput='uniform_average',
             force_finite=True,
             num_samples: int=500,
             n_jobs: int=-1,
             use_tqdm=True,
             **kwargs):
    """r2_score"""

    @wraps(metrics.r2_score)
    def inner(y, hy):
        return metrics.r2_score(y, hy,
                                sample_weight=sample_weight,
                                multioutput=multioutput,
                                force_finite=force_finite)

    return Perf(y_true, *y_pred, score_func=inner, error_func=None,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='error_func')
def mean_poisson_deviance(y_true,
                          *y_pred,
                          sample_weight=None,
                          num_samples: int=500,
                          n_jobs: int=-1,
                          use_tqdm=True,
                          **kwargs):
    """mean_poisson_deviance"""

    @wraps(metrics.mean_poisson_deviance)
    def inner(y, hy):
        return metrics.mean_poisson_deviance(y, hy,
                                             sample_weight=sample_weight)

    return Perf(y_true, *y_pred, score_func=None, error_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='error_func')
def mean_gamma_deviance(y_true,
                        *y_pred,
                        sample_weight=None,
                        num_samples: int=500,
                        n_jobs: int=-1,
                        use_tqdm=True,
                        **kwargs):
    """mean_gamma_deviance"""

    @wraps(metrics.mean_gamma_deviance)
    def inner(y, hy):
        return metrics.mean_gamma_deviance(y, hy,
                                           sample_weight=sample_weight)

    return Perf(y_true, *y_pred, score_func=None, error_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


@metrics_docs(hy_name='y_pred', attr_name='error_func')
def mean_absolute_percentage_error(y_true,
                                   *y_pred,
                                   sample_weight=None,
                                   multioutput='uniform_average',
                                   num_samples: int=500,
                                   n_jobs: int=-1,
                                   use_tqdm=True,
                                   **kwargs):
    """mean_absolute_percentage_error"""

    @wraps(metrics.mean_absolute_percentage_error)
    def inner(y, hy):
        return metrics.mean_absolute_percentage_error(y, hy,
                                                      sample_weight=sample_weight,
                                                      multioutput=multioutput)

    return Perf(y_true, *y_pred, score_func=None, error_func=inner,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


def d2_absolute_error_score(y_true,
                            *y_pred,
                            sample_weight=None,
                            multioutput='uniform_average',
                            num_samples: int=500,
                            n_jobs: int=-1,
                            use_tqdm=True,
                            **kwargs):
    """d2_absolute_error_score"""

    @wraps(metrics.d2_absolute_error_score)
    def inner(y, hy):
        return metrics.d2_absolute_error_score(y, hy,
                                               sample_weight=sample_weight,
                                               multioutput=multioutput)

    return Perf(y_true, *y_pred, score_func=inner, error_func=None,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)


def pearsonr(y_true, *y_pred,
             alternative='two-sided', method=None,
             num_samples: int=500,
             n_jobs: int=-1,
             use_tqdm=True,
             **kwargs):
    """:py:class:`~CompStats.interface.Perf` with :py:func:`~scipy.stats.pearsonr` as :py:attr:`score_func.`

    :param y_true: True measurement or could be a pandas.DataFrame where column label 'y' corresponds to the true measurement. 
    :type y_true: numpy.ndarray or pandas.DataFrame 
    :param y_pred: Predictions, the algorithms will be identified with alg-k where k=1 is the first argument included in :py:attr:`y_pred.` 
    :type y_pred: numpy.ndarray 
    :param kwargs: Predictions, the algorithms will be identified using the keyword  
    :type kwargs: numpy.ndarray 
    :param num_samples: Number of bootstrap samples, default=500. 
    :type num_samples: int 
    :param n_jobs: Number of jobs to compute the statistic, default=-1 corresponding to use all threads. 
    :type n_jobs: int 
    :param use_tqdm: Whether to use tqdm.tqdm to visualize the progress, default=True 
    :type use_tqdm: bool 
    """

    @wraps(stats.pearsonr)
    def inner(y, hy):
        return stats.pearsonr(y, hy,
                              alternative=alternative,
                              method=method).statistic
    
    return Perf(y_true, *y_pred, score_func=inner, error_func=None,
                num_samples=num_samples, n_jobs=n_jobs,
                use_tqdm=use_tqdm,
                **kwargs)
