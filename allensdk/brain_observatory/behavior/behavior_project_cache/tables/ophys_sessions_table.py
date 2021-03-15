import logging
from typing import Optional, List

import pandas as pd

from allensdk.brain_observatory.behavior.behavior_project_cache.tables\
    .ophys_mixin import \
    OphysMixin
from allensdk.brain_observatory.behavior.behavior_project_cache.tables\
    .project_table import ProjectTable
from allensdk.brain_observatory.behavior.behavior_project_cache.tables\
    .sessions_table import SessionsTable


class BehaviorOphysSessionsTable(ProjectTable, OphysMixin):
    """Class for storing and manipulating project-level data
    at the behavior-ophys session level"""
    def __init__(self, df: pd.DataFrame,
                 sessions_table: SessionsTable,
                 suppress: Optional[List[str]] = None,
                 index_column: str = 'ophys_session_id'):
        """
        Parameters
        ----------
        df
            The behavior-ophys session-level data
        sessions_table
            All session-level data (needed to calculate exposure counts)
        suppress
            columns to drop from table
        index_column
            See description in BehaviorProjectCache.get_session_table
        """

        self._logger = logging.getLogger(self.__class__.__name__)
        self._index_column = index_column
        self._sessions_table = sessions_table
        super().__init__(df=df, suppress=suppress)

    def postprocess_additional(self):
        self._df = self._add_prior_exposures(
            sessions_table=self._sessions_table, df=self._df)

        # Possibly explode and reindex
        self.__explode()

    def __explode(self):
        if self._index_column == "ophys_session_id":
            pass
        elif self._index_column == "ophys_experiment_id":
            self._df = (self._df.reset_index()
                        .explode("ophys_experiment_id")
                        .set_index("ophys_experiment_id"))
        else:
            self._logger.warning(
                f"Invalid value for `by`, '{self._index_column}', passed to "
                f"BehaviorOphysSessionsCacheTable."
                " Valid choices for `by` are 'ophys_experiment_id' and "
                "'ophys_session_id'.")