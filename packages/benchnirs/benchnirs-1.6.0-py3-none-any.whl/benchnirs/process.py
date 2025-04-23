import numpy as np

from scipy.stats import linregress, kurtosis, skew


def process_epochs(mne_epochs, tmin=0, tmax=None, tslide=None, sort=False,
                   reject_criteria=None):
    """
    Perform processing on epochs including baseline cropping, bad epoch
    removal, label extraction and  unit conversion.

    Parameters
    ----------
    mne_epochs : MNE Epochs object
        MNE epochs of filtered data with associated labels. Subject IDs are
        contained in the ``metadata`` property.

    tmin : float | None
        Start time of selection in seconds. Defaults to ``0`` to crop the
        baseline.

    tmax : float | None
        End time of selection in seconds. Defaults to ``None`` to keep the
        initial end time.

    tslide : float | None
        Size of the sliding window in seconds. Will crop the epochs if ``tmax``
        is not a multiple of ``tslide``. Defaults to ``None`` for no window
        sliding.

    sort : boolean
        Whether to sort channels by type (all HbO, all HbR). Defaults to
        ``False`` for no sorting.

    reject_criteria : list of floats | None
        List of the 2 peak-to-peak rejection thresholds for HbO and HbR
        channels respectively in uM. Defaults to ``None`` for no rejection.

    Returns
    -------
    nirs : array of shape (n_samples, n_channels, n_times)
        Processed NIRS data in uM.

    labels : array of integer
        List of labels, starting at 0 and with ranks in the same order as
        the event codes. For example if the MNE event codes are
        ``[5, 2, 5, 1]``, the labels will be ``[2, 1, 2, 0]``. Please note that
        ``999`` is reserved for unlabelled samples and will be unchanged.

    groups : array of integer
        List of groups, starting at 0 and with ranks in the same order as the
        original subject IDs. For example if the subject IDs are
        ``[5, 2, 5, 1]``, the groups will be ``[2, 1, 2, 0]``.
    """
    # Process epochs
    epochs = mne_epochs.copy()
    epochs.baseline = None
    epochs.crop(tmin=tmin, tmax=tmax)
    if reject_criteria is not None:
        reject = {'hbo': reject_criteria[0]*1e-6,
                  'hbr': reject_criteria[1]*1e-6}
        epochs.drop_bad(reject=reject)

    # Extract data
    id_list = epochs.events[:, 2]
    sorted_id_set = sorted(epochs.event_id.values())
    id_to_label = {
        id: (i if id != 999 else 999) for i, id in enumerate(sorted_id_set)
    }
    labels = list(map(id_to_label.get, id_list))
    labels = np.array(labels, dtype=np.int64)
    event_to_label = {
        key: id_to_label[value] for key, value in epochs.event_id.items()
    }
    print(f'Event-to-label mapping: {event_to_label}')
    try:
        subj_list = epochs.metadata['Subject_ID'].to_numpy()
        sorted_subj_set = sorted(set(subj_list))
        subj_to_group = {subj: i for i, subj in enumerate(sorted_subj_set)}
        groups = list(map(subj_to_group.get, subj_list))
        groups = np.array(groups, dtype=np.int64)
        print(f'Subject-to-group mapping: {subj_to_group}')
    except TypeError:
        groups = None
    nirs_epochs = epochs.pick('fnirs')
    if sort:
        hbo_chs = epochs.copy().pick('hbo').ch_names
        hbr_chs = epochs.copy().pick('hbr').ch_names
        nirs_epochs.reorder_channels(hbo_chs + hbr_chs)
    nirs = nirs_epochs.get_data(copy=True)
    nirs *= 1e6  # convert from M to uM

    # Create sliding window
    if tslide is not None:
        sliding_size = int(tslide * nirs_epochs.info['sfreq'])
        r = nirs.shape[-1] % sliding_size
        if r > 0:
            nirs = nirs[:, :, :-r]  # crop to fit window size
        nirs = nirs.reshape(nirs.shape[0], nirs.shape[1], -1, sliding_size)
        labels = labels.repeat(nirs.shape[2])
        if groups is not None:
            groups = groups.repeat(nirs.shape[2])
        nirs = nirs.swapaxes(1, 2)
        nirs = nirs.reshape(-1, nirs.shape[2], nirs.shape[3])

    nirs = np.single(nirs)

    print(f'Dataset shape: {nirs.shape}')

    return nirs, labels, groups


def extract_features(nirs, feature_list):
    """
    Perform feature extraction on NIRS data.

    Parameters
    ----------
    nirs : array of shape (n_samples, n_channels, n_times)
        Processed NIRS data.

    feature_list : list of strings
        List of features to extract. The list can include ``'mean'`` for the
        mean along the time axis, ``'std'`` for standard deviation along the
        time axis and ``'slope'`` for the slope of the linear regression along
        the time axis, ``'skew'`` for the skewness along the time axis,
        ``'kurt'`` for the kurtosis along the time axis, ``'ttp'`` for the time
        to peak (requires channels to have been sorted beforehand: all HbO, all
        HbR), ``'peak'`` for the value of the peak (max value for HbO and min
        value for HbR, requires channels to have been sorted beforehand: all
        HbO, all HbR).

    Returns
    -------
    nirs_features : array of shape (n_samples, n_channels, n_features)
        Features extracted from NIRS data.
    """
    nirs_features = []
    for feature in feature_list:
        if feature == 'mean':
            nirs_feature = np.mean(nirs, axis=-1, keepdims=True)
        elif feature == 'std':
            nirs_feature = np.std(nirs, axis=-1, keepdims=True)
        elif feature == 'slope':
            x = range(nirs.shape[-1])
            nirs_feature = []
            for epoch in nirs:
                ep_slopes = []
                for channel in epoch:
                    ep_slopes.append(linregress(x, channel).slope)
                nirs_feature.append(ep_slopes)
            nirs_feature = np.expand_dims(nirs_feature, -1)
        elif feature == 'skew':
            nirs_feature = skew(nirs, axis=-1, keepdims=True)
        elif feature == 'kurt':
            nirs_feature = kurtosis(nirs, axis=-1, keepdims=True)
        elif feature == 'ttp':
            nirs_hbo, nirs_hbr = np.split(nirs, 2, axis=1)
            hbo_feature = np.argmax(nirs_hbo, axis=-1, keepdims=True)
            hbr_feature = np.argmin(nirs_hbr, axis=-1, keepdims=True)
            nirs_feature = np.concatenate((hbo_feature, hbr_feature), axis=1)
        elif feature == 'peak':
            nirs_hbo, nirs_hbr = np.split(nirs, 2, axis=1)
            hbo_feature = np.max(nirs_hbo, axis=-1, keepdims=True)
            hbr_feature = np.min(nirs_hbr, axis=-1, keepdims=True)
            nirs_feature = np.concatenate((hbo_feature, hbr_feature), axis=1)

        nirs_features.append(nirs_feature)

    nirs_features = np.concatenate(nirs_features, axis=-1)

    nirs_features = np.single(nirs_features)

    return nirs_features
