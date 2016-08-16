import numpy as np
from allensdk.core.brain_observatory_nwb_data_set import BrainObservatoryNwbDataSet
import pytest
import os


@pytest.fixture
def data_set():
    nwb_file = '/projects/neuralcoding/vol1/prod6/specimen_497258322/ophys_experiment_506954308/506954308.nwb'
    data_set = BrainObservatoryNwbDataSet(nwb_file)
    return data_set


@pytest.mark.skipif(not os.path.exists('/projects/neuralcoding'),
                    reason="test NWB file not available")
def test_acceptance(data_set):
    ids = data_set.get_cell_specimen_ids()
    data_set.get_session_type()
    data_set.get_metadata()
    data_set.get_running_speed()
    data_set.get_motion_correction()


@pytest.mark.skipif(not os.path.exists('/projects/neuralcoding'),
                    reason="test NWB file not available")
def test_get_roi_ids(data_set):
    ids = data_set.get_roi_ids()
    assert len(ids) == len(data_set.get_cell_specimen_ids())


@pytest.mark.skipif(not os.path.exists('/projects/neuralcoding'),
                    reason="test NWB file not available")
def test_get_cell_specimen_indices(data_set):
    inds = data_set.get_cell_specimen_indices([])
    assert len(inds) == 0

    ids = data_set.get_cell_specimen_ids()

    inds = data_set.get_cell_specimen_indices(ids)
    assert np.all(np.array(inds) == np.arange(len(inds)))

    inds = data_set.get_cell_specimen_indices([ids[0]])
    assert inds[0] == 0


@pytest.mark.skipif(not os.path.exists('/projects/neuralcoding'),
                    reason="test NWB file not available")
def test_get_fluorescence_traces(data_set):
    ids = data_set.get_cell_specimen_ids()

    timestamps, traces = data_set.get_fluorescence_traces()
    assert len(timestamps) == traces.shape[1]
    assert len(ids) == traces.shape[0]

    timestamps, traces = data_set.get_fluorescence_traces(ids)
    assert len(ids) == traces.shape[0]

    timestamps, traces = data_set.get_fluorescence_traces([ids[0]])
    assert traces.shape[0] == 1


@pytest.mark.skipif(not os.path.exists('/projects/neuralcoding'),
                    reason="test NWB file not available")
def test_get_neuropil_traces(data_set):
    ids = data_set.get_cell_specimen_ids()

    timestamps, traces = data_set.get_neuropil_traces()
    assert len(timestamps) == traces.shape[1]
    assert len(ids) == traces.shape[0]

    timestamps, traces = data_set.get_neuropil_traces(ids)
    assert len(ids) == traces.shape[0]

    timestamps, traces = data_set.get_neuropil_traces([ids[0]])
    assert traces.shape[0] == 1


@pytest.mark.skipif(not os.path.exists('/projects/neuralcoding'),
                    reason="test NWB file not available")
def test_get_dff_traces(data_set):
    ids = data_set.get_cell_specimen_ids()

    timestamps, traces = data_set.get_dff_traces()
    #assert len(timestamps) == traces.shape[1]
    assert len(ids) == traces.shape[0]

    timestamps, traces = data_set.get_dff_traces(ids)
    assert len(ids) == traces.shape[0]

    timestamps, traces = data_set.get_dff_traces([ids[0]])
    assert traces.shape[0] == 1


@pytest.mark.skipif(not os.path.exists('/projects/neuralcoding'),
                    reason="test NWB file not available")
def test_get_corrected_fluorescence_traces(data_set):
    ids = data_set.get_cell_specimen_ids()

    timestamps, traces = data_set.get_corrected_fluorescence_traces()
    assert len(timestamps) == traces.shape[1]
    assert len(ids) == traces.shape[0]

    timestamps, traces = data_set.get_corrected_fluorescence_traces(ids)
    assert len(ids) == traces.shape[0]

    timestamps, traces = data_set.get_corrected_fluorescence_traces([ids[0]])
    assert traces.shape[0] == 1


@pytest.mark.skipif(not os.path.exists('/projects/neuralcoding'),
                    reason="test NWB file not available")
def test_get_roi_mask(data_set):
    ids = data_set.get_cell_specimen_ids()
    roi_masks = data_set.get_roi_mask()
    assert len(ids) == len(roi_masks)

    max_projection = data_set.get_max_projection()
    for roi_mask in roi_masks:
        mask = roi_mask.get_mask_plane()
        assert mask.shape[0] == max_projection.shape[0]
        assert mask.shape[1] == max_projection.shape[1]

    roi_masks = data_set.get_roi_mask([ids[0]])
    assert len(roi_masks) == 1


@pytest.mark.skipif(not os.path.exists('/projects/neuralcoding'),
                    reason="test NWB file not available")
def test_get_roi_mask_array(data_set):
    ids = data_set.get_cell_specimen_ids()
    arr = data_set.get_roi_mask_array()
    assert arr.shape[0] == len(ids)

    arr = data_set.get_roi_mask_array([ids[0]])
    assert arr.shape[0] == 1

    try:
        arr = data_set.get_roi_mask_array([0])
    except ValueError as e:
        assert str(e).startswith("Cell specimen not found")
