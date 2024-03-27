import datetime
import pandas as pd
import numpy as np
import requests
import zipfile
import io

from sklearn import datasets, ensemble

from evidently import ColumnMapping
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, RegressionPreset, DataQualityPreset

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


## adult dataset
# adult_data = datasets.fetch_openml(name="adult", version=2, as_frame="auto")
# adult = adult_data.frame

# adult_ref = adult[~adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]
# adult_cur = adult[adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]


## bicycle demand dataset
content = requests.get("https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip", verify=False).content
with zipfile.ZipFile(io.BytesIO(content)) as arc:
    raw_data = pd.read_csv(arc.open("hour.csv"), header=0, sep=',', parse_dates=['dteday'], index_col='dteday')

raw_data.index = raw_data.apply(
    lambda row: datetime.datetime.combine(row.name, datetime.time(hour=int(row['hr']))), axis = 1)

ref = raw_data.loc['2011-01-01 00:00:00':'2011-12-31 23:00:00']
cur = raw_data.loc['2012-01-01 00:00:00':'2012-12-31 23:00:00']

column_mapping = ColumnMapping()
column_mapping.target = 'cnt'

# ref = ref.reset_index()
# cur = cur.reset_index()

WORKSPACE = "workspace"

YOUR_PROJECT_NAME = "New Project 6"
YOUR_PROJECT_DESCRIPTION = "Test project using Bicycle dataset."


def create_report(i: int):
    data_drift_report = Report(
        metrics=[
            DataDriftPreset()
        ],
        timestamp=datetime.datetime.now() + datetime.timedelta(days=i),
    )
    data_quality_report = Report(
        metrics=[
            DataQualityPreset()
        ],
        timestamp=datetime.datetime.now() + datetime.timedelta(days=i),
    )
    target_drift_report = Report(
        metrics=[
            TargetDriftPreset()
        ],
        timestamp=datetime.datetime.now() + datetime.timedelta(days=i),
    )

    data_drift_report.run(reference_data=ref, current_data=cur)
    data_quality_report.run(reference_data=ref, current_data=cur)
    target_drift_report.run(reference_data=ref, current_data=cur, column_mapping=column_mapping)
    return data_drift_report, data_quality_report, target_drift_report


def create_test_suite(i: int):
    data_drift_test_suite = TestSuite(
        tests=[DataDriftTestPreset()],
        timestamp=datetime.datetime.now() + datetime.timedelta(days=i),
    )

    data_drift_test_suite.run(reference_data=ref, current_data=cur)
    return data_drift_test_suite


def create_project(workspace: WorkspaceBase):
    project = workspace.create_project(YOUR_PROJECT_NAME)
    project.description = YOUR_PROJECT_DESCRIPTION

    project.save()
    return project


def create_demo_project(workspace: str):
    ws = Workspace.create(workspace)
    project = create_project(ws)

    i = 0

    df_report, dq_report, td_report = create_report(i=i)
    ws.add_report(project.id, df_report)
    ws.add_report(project.id, dq_report)
    ws.add_report(project.id, td_report)

    test_suite = create_test_suite(i=i)
    ws.add_test_suite(project.id, test_suite)


if __name__ == "__main__":
    create_demo_project(WORKSPACE)