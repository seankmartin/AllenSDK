import pytest

import numpy as np
import pandas as pd
from allensdk.brain_observatory.behavior.session_apis.data_transforms import BehaviorOphysDataTransforms  # noqa: E501


@pytest.mark.parametrize("roi_ids,expected", [
    [
        1,
        np.array([
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ])
    ],
    [
        None,
        np.array([
            [
                [1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ]
        ])
    ]
])
# cell_specimen_table_api fixture from allensdk.test.brain_observatory.conftest
def test_get_roi_masks_by_cell_roi_id(roi_ids, expected,
                                      cell_specimen_table_api):
    api = cell_specimen_table_api
    obtained = api.get_roi_masks_by_cell_roi_id(roi_ids)
    assert np.allclose(expected, obtained.values)
    assert np.allclose(obtained.coords['row'],
                       [0.5, 1.5, 2.5, 3.5, 4.5])
    assert np.allclose(obtained.coords['column'],
                       [0.25, 0.75, 1.25, 1.75, 2.25])


def test_get_rewards(monkeypatch):
    """
    Test that BehaviorOphysDataTransforms.get_rewards() returns
    expected results (main nuance is that timestamps should be
    determined by applying the reward frame as an index to
    stimulus_timestamps)
    """

    def dummy_init(self):
        pass

    def dummy_stimulus_timestamps(self):
        return np.arange(0, 2.0, 0.01)

    def dummy_stimulus_file(self):
        trial_log = []
        trial_log.append({'rewards': [(0.001, -1.0, 4)],
                          'trial_params': {'auto_reward': True}})
        trial_log.append({'rewards': []})
        trial_log.append({'rewards': [(0.002, -1.0, 10)],
                          'trial_params': {'auto_reward': False}})
        data = {}
        data['items'] = {}
        data['items']['behavior'] = {}
        data['items']['behavior']['trial_log'] = trial_log
        return data

    with monkeypatch.context() as ctx:
        ctx.setattr(BehaviorOphysDataTransforms,
                    '__init__',
                    dummy_init)

        ctx.setattr(BehaviorOphysDataTransforms,
                    'get_stimulus_timestamps',
                    dummy_stimulus_timestamps)

        ctx.setattr(BehaviorOphysDataTransforms,
                    '_behavior_stimulus_file',
                    dummy_stimulus_file)

        xforms = BehaviorOphysDataTransforms()

        rewards = xforms.get_rewards()

        expected_dict = {'volume': [0.001, 0.002],
                         'timestamps': [0.04, 0.1],
                         'autorewarded': [True, False]}
        expected_df = pd.DataFrame(expected_dict)
        expected_df = expected_df.set_index('timestamps', drop=True)
        assert expected_df.equals(rewards)
