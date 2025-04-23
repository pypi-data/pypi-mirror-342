from django.urls import path
from .views import (
    pip_manager_view,
    reqcheck_view,
    export_json,
    export_csv,
    export_txt,
)

urlpatterns = [
    # Main views
    path("pipfreezesnapshot/", pip_manager_view, name="pipfreezesnapshot"),
    path("requirementscheck/", reqcheck_view, name="requirementscheck"),

    # Snapshot exports
    path("export/snapshot/json/<int:snapshot_id>/", export_json, {"mode": "snapshot"}, name="export_snapshot_json"),
    path("export/snapshot/csv/<int:snapshot_id>/", export_csv, {"mode": "snapshot"}, name="export_snapshot_csv"),
    path("export/snapshot/txt/<int:snapshot_id>/", export_txt, {"mode": "snapshot"}, name="export_snapshot_txt"),

    # Requirements exports
    path("export/requirements/json/", export_json, {"mode": "requirements"}, name="export_requirements_json"),
    path("export/requirements/csv/", export_csv, {"mode": "requirements"}, name="export_requirements_csv"),
    path("export/requirements/txt/", export_txt, {"mode": "requirements"}, name="export_requirements_txt"),

    # Run pip freeze exports
    path("export/freeze/json/", export_json, {"mode": "freeze"}, name="export_freeze_json"),
    path("export/freeze/csv/", export_csv, {"mode": "freeze"}, name="export_freeze_csv"),
    path("export/freeze/txt/", export_txt, {"mode": "freeze"}, name="export_freeze_txt"),

    # Snapshot compare exports
    path("export/compare/json/", export_json, {"mode": "compare"}, name="export_compare_json"),
    path("export/compare/csv/", export_csv, {"mode": "compare"}, name="export_compare_csv"),
    path("export/compare/txt/", export_txt, {"mode": "compare"}, name="export_compare_txt"),

]
