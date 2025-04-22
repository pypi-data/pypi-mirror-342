import traceback

from typing import Dict, List, Optional

from clipped.utils.np import sanitize_dict, sanitize_np_types

from hypertune.logger import logger
from polyaxon.client import RunClient
from polyaxon.schemas import V1Join
from traceml.artifacts import V1ArtifactKind, V1RunArtifact


def get_iteration_definition(
    client: RunClient,
    iteration: int,
    join: V1Join,
    optimization_metric: str,
    name: Optional[str] = None,
):
    def handler():
        runs = (
            client.list(
                query=join.query,
                sort=join.sort,
                limit=join.limit,
                offset=join.offset,
            ).results
            or []
        )
        configs = []
        metrics = []
        run_uuids = []
        for run in runs:
            if optimization_metric in run.outputs:
                run_uuids.append(run.uuid)
                configs.append(run.inputs)
                metrics.append(run.outputs[optimization_metric])

        if configs or metrics or run_uuids:
            artifact_run = V1RunArtifact.construct(
                name=name or "in-iteration-{}".format(iteration),
                kind=V1ArtifactKind.ITERATION,
                summary={
                    "iteration": iteration,
                    "configs": [sanitize_dict(s) for s in configs],
                    "metrics": [sanitize_np_types(s) for s in metrics],
                    "uuid": run_uuids,
                },
                is_input=True,
            )
            client.log_artifact_lineage(artifact_run)

        return run_uuids, configs, metrics

    try:
        return handler()
    except Exception as e:
        exp = "Polyaxon tuner failed fetching iteration definition: {}\n{}".format(
            repr(e), traceback.format_exc()
        )
        client.log_failed(reason="PolyaxonTunerIteration", message=exp)
        logger.warning(e)


def handle_iteration_failure(client: RunClient, exp: Exception):
    exp = "Polyaxon tuner failed creating suggestions: {}\n{}".format(
        repr(exp), traceback.format_exc()
    )
    client.log_failed(reason="PolyaxonTunerSuggestions", message=exp)


def handle_iteration(
    client: RunClient,
    suggestions: List[Dict] = None,
):
    if not suggestions:
        logger.warning("No new suggestions were created")
        return
    try:
        logger.info("Generated new {} suggestions".format(len(suggestions)))
        client.log_outputs(
            suggestions=[sanitize_dict(s) for s in suggestions], async_req=False
        )
        return
    except Exception as e:
        logger.warning(e)
        exp = e

    if exp:
        message = "Polyaxon tuner failed logging iteration definition: {}\n{}".format(
            repr(exp), traceback.format_exc()
        )
        client.log_failed(reason="PolyaxonTunerIteration", message=message)
        raise exp
