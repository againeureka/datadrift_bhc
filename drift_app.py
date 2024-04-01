from datetime import datetime, time
import os

import pandas as pd
from sklearn import datasets, ensemble

from evidently import ColumnMapping
from evidently.metrics import DatasetSummaryMetric
from evidently.metrics import ColumnDriftMetric
from evidently.metrics import ColumnSummaryMetric
from evidently.metrics import DatasetDriftMetric
from evidently.metrics import DatasetMissingValuesMetric
from evidently.report import Report
from evidently.test_preset import DataDriftTestPreset
from evidently.test_suite import TestSuite
from evidently.ui.dashboards import CounterAgg
from evidently.ui.dashboards import DashboardPanelCounter
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards import PlotType
from evidently.ui.dashboards import ReportFilter
from evidently.ui.remote import RemoteWorkspace
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import WorkspaceBase

def preprocess_data(cur, ref):
    current = pd.read_csv(os.path.join(".", cur))
    reference = pd.read_csv(os.path.join(".", ref))
    column_mapping = ColumnMapping()

    return current, reference, column_mapping

def create_report(i: int, data):
    pass

    return report

def create_project(workspace: WorkspaceBase, name: str):
    project = workspace.create_project(name)
    pass

    return project

if __name__ == "__main__":
    pass