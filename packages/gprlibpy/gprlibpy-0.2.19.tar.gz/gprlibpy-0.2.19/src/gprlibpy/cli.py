import json
import logging
import os
from pathlib import Path
from typing import Optional

import pandas as pd
import typer
from dotenv import load_dotenv, find_dotenv
from lgopy.core import LgoPipeline, BlockHub
from typer import Argument, Option
from gprlibpy.core import Dataset

logger = logging.getLogger(__name__)


try:
    from gprblocks import * # noqa
except ImportError:
    logger.warning("GPR blocks not found. Please install the gprblocks package to use GPR blocks.")
    pass

load_dotenv(find_dotenv())

app = typer.Typer()


@app.command(name="run-pipeline")
def run_pipeline(
        pipeline: str = Argument(..., help="Path to pipeline JSON file"),
        src_dataset: str = Option(..., help="Path to source dataset"),
        verbose: bool = Option(True, help="Enable verbose mode"),
        output_path: str = Option(..., help="Path to output artifact"),
        log_path: Optional[str] = Option(..., help="Path to log file"),
):
    """
    Executes a data processing pipeline from a JSON file.
    """

    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if os.path.isfile(pipeline):
            with open(pipeline, "r") as f:
                pipeline = f.read()
        pipeline = LgoPipeline.from_json(pipeline, verbose=verbose)
        src_ds = Dataset.from_path(src_dataset)
        pipeline_out = pipeline(src_ds)

        if isinstance(pipeline_out, Dataset):
            pipeline_type = "processing"
            pipeline_out.save(output_path.with_suffix(".zarr"), safe_chunks=False, mode="w")
        elif isinstance(pipeline_out, pd.DataFrame):
            pipeline_type = "features"
            pipeline_out.to_csv(output_path.with_suffix(".csv"), index=True)
        else:
            raise ValueError("Output type not supported for saving yet")

        status_message = f"Pipeline executed successfully. Output saved to {output_path}"
        typer.echo(status_message)
        if log_path:
            with open(log_path, "w") as json_file:
                json_file.write(json.dumps({
                    "status": "SUCCESS",
                    "message": status_message,
                    "pipeline_type": pipeline_type
                }, indent=4))

    except Exception as e:
        error_message = f"Error running the pipeline: {e}"
        typer.echo(error_message, err=True)

        if log_path:
            with open(log_path, "w") as json_file:
                json_file.write(json.dumps({
                    "status": "FAILED",
                    "message": error_message,
                    "pipeline_type": ""
                }, indent=4))

        #raise typer.Abort()


@app.command(name="list-blocks")
def list_blocks():
    """
    List all available blocks
    :return:
    """
    typer.echo(BlockHub.blocks_json())


if __name__ == '__main__':
    app()
    # json_pipeline = '[{"block": "BackgroundCorrection", "args": {}}]'
    # ds_src = "./../../data/test.zarr"
    # output_artifact = "./../../data/test"
    #
    # runner = CliRunner()
    # result = runner.invoke(app, [ "run-pipeline",
    #                               json_pipeline,
    #                              "--src-dataset", ds_src,
    #                              "--output-path", output_artifact,
    #                               "--log-path", "log"])
    # print(result.output)