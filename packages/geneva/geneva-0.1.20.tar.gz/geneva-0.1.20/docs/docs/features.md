# Feature Engineering

Geneva improves the productivity of AI engineers by streamlining feature engineering tasks.  It is designed to reduce the time required to prototype, perform experiments, scale up, and move to production.

Geneva uses Python User Defined Functions (**UDFs**) to define features as columns in a Lance dataset.  Adding a feature is straightforward:

1. Prototype your Python function in your favorite environment.
2. Wrap the function with small UDF decorator.
3. Register the UDF as a virtual column using `Table.add_columns()`.
4. Trigger a backfill operation.

## Prototyping your Python function

Build your Python feature generator function in an IDE or notebook using your project's Python versions and dependencies.

*That's it.*

Geneva will automate much of the dependency and version management needed to move from prototype to scale and production.

## Converting functions into UDFs

Converting your Python code to a Geneva UDF is simple.  There are three kinds of UDFs that you can provide — scalar UDFs, batched UDFs and stateful UDFs.

In all cases, Geneva uses Python type hints from your functions to infer the input and output
[arrow data types](https://arrow.apache.org/docs/python/api/datatypes.html) that LanceDB uses.

### Scalar UDFs

The **simplest** form is a scalar UDF, which processes one row at a time:

```python
from geneva import udf

@udf
def simple_udf(x: int, y: float) -> float:
    return x * y
```

This UDF will take the value of x and value of y from each row and return the product.  The `@udf` wrapper is all that is needed.

### Batched UDFs

For **better performance**, you can also define batch UDFs that process multiple rows at once using `pyarrow.RecordBatch`:

```python

import pyarrow as pa

from geneva import udf

@udf(data_type=pa.int32(), input_columns=["prompt"])
def batch_str_len(batch: pa.RecordBatch) -> pa.Array:
    return pa.compute.utf8_length(batch["prompt"])
```

!!! note

    It is required to specify `data_type` in the ``@udf`` decorator for batched UDFs,
    which defines `pyarrow.DataType` of the returned `pyarrow.Array`.

    Optionally, user can specify `input_columns` to scan more efficiently,
    because [Lance is a columnar format](https://github.com/lancedb/lance).

For example, you can specify the data type of an embedding function:

```python

@udf(data_type=pa.list_(pa.float32(), 1536), input_columns=["prompt"])
def openai_embedding(batch: pa.RecordBatch) -> pa.Array:
    resp = self.client.embeddings.create(
        model=self.model, input=batch["prompt"].to_pylist())
    return pa.array(resp.data[0].embedding)
```

### Stateful UDFs

You can also define a **stateful** UDF that retains its state across calls.  This can be used to **optimize expensive initialization** that may require heavy resource on the distributed workers.  For example, this can be used to load an model to the GPU once for all records sent to a worker instead of fonce per record or per batch of records.

A stateful UDF is a `Callable` class, with `__call__()` method.

!!! warning

    Unstable API.

```python
from typing import Callable
from openai import OpenAI

@udf(data_type=pa.list_(pa.float32(), 1536))
class OpenAIEmbedding(Callable):
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        # Per-worker openai client
        self.client: OpenAI | None = None

    def __call__(self, text: str) -> pa.Array:
        if self.client is None:
            self.client = OpenAI()

        resp = self.client.embeddings.create(model=self.model, input=text)
        return pa.array(resp.data[0].embeddings)
```

??? note

    The state is will be independently managed on each distributed Worker.


## Registering Features with UDFs

!!! warning

    Unstable API.

Registering a feature is done by providing the `Table.add_columns()` function a new column name and the Geneva UDF.

Let's start by obtaining the table `tbl`
```python
import geneva

db = geneva.connect("db://my_video")
tbl = db.open_table("youtube-1000")
```

Here's how to register a simple UDF:
```python
@udf
def simple_udf(x: int, y: float) -> float:
    ...

# {'new column name': <udf>}
# simple_udf's arguments are `x` and `y` so the input columns are
# inferred to be columns `x` amd `y`
tbl.add_columns({"xy_product": simple_udf})
```

Batched UDFs require input columns to be specified with the `udf` annotation

```python
@udf(data_type=pa.int32(), input_columns=["prompt"])
def batch_str_len(batch: pa.RecordBatch) -> pa.Array:
    ...

# {'new column name': <udf>}
# batch_str_len's input, `prompt` is specified by the UDF.
tbl.add_columns({"batch_str_len": batch_str_len})
```

Similarly, a stateful UDF is registered the same way.  The call method may be a per-record function or a batch function.
```python
@udf(data_type=pa.list_(pa.float32(), 1536))
class OpenAIEmbedding(Callable):
    ...
    def __call__(self, text: str) -> pa.Array:
        ...

# OpenAIEbmedding's call method input is inferred to be 'text' of
# type string, and its output is specified as list of float32.
tbl.add_columns({"openai": OpenAIEmbedding})
```

## Triggering backfill

Triggering backfill creates a distributed job to run the UDF and populate the column values in your LanceDB table. The Geneva framework simplifies several aspects of distributed execution.

* **Dependency management**:  Geneva automatically packages and deployes your Python execution environment to worker nodes.  This ensures that distributed execution occurs in the same environment and depedencies as your prototype.
* **Checkpoints**:  Each batch of UDF execution is checkpointed so that partial results are not lost in case of job failures.  Jobs can resume and avoid most of the expense of having to recalculate values.

We currently support one processing backend: [Ray](https://www.anyscale.com/product/open-source/ray).  This is deployed on an existing Ray cluster or on a kubernetes cluster on demand.

=== "Ray on Kubernetes"

    Geneva uses KubeRay to deploy Ray on Kubernetes.  You can define a `RayCluster` by specifying the pod name, the Kubernetes namespace, credentials to use for deploying Ray, and characteristics of your workers.

    This approach makes it easy to tailor resource requirements to your particular UDFs.

    You can then wrap your table backfill call with the RayCluster context.

    ```python
    from geneva.runners.ray.raycluster import RayCluster, _HeadGroupSpec, _WorkerGroupSpec

    tbl = db.open_table("my_table")
    with RayCluster(
            name= k8s_name,  # prefix of your k8s pod
            namespace=k8s_namespace,
            use_port_forward=True,
            head_group=_HeadGroupSpec(
                service_account="geneva-integ-test",
                num_cpus=8,
            ),
            worker_groups=[
                _WorkerGroupSpec(  # cpu only nodes
                    name="cpu",
                    num_cpus=60,
                    memory="120G",
                    service_account="geneva-integ-test",
                ),
                _WorkerGroupSpec( # nodes with gpus
                    name="gpu",
                    num_cpus=8,
                    memory="32G",
                    num_gpus=1,
                    service_account="geneva-integ-test",
                ),
            ],
        ):
        tbl.backfill(["xy_product"])
    ```

    For more interactive usage, you can use this pattern:

    ```python
    # this is a k8s pod spec.
    raycluster =  RayCluster(...)
    raycluster.__enter__() # equivalent of ray.init()

    # add column 'text_len' and trigger the job
    tbl.backfill("table_len")  # trigger the job

    raycluster.__exit__()
    ```

    Whne you become more confident with your feature, you can trigger the backfill by specifying the `backfill` kwarg on `Table.add_column()`.

    ```python
    tbl.add_column({"text_len": text_len}, ["prompt"], backfill=True)
    ```

=== "Existing Ray Cluster"

    !!! Warning

        This is a work in progress


=== "Ray Auto Connect"

    To use ray, you can just trigger the `Table.backfill` method or the `Table.add_columns(..., backfill=True)` method.   This will autocreate a local Ray cluster and is only suitable prototyping on small datasets.

    ```python
    tbl.backfill(["xy_product"])

    ...

    # add column 'text_len' and trigger the job
    tbl.backfill(["table_len"])  # trigger the job

    ...

    tbl.add_column({"text_len": text_len}, ["prompt"], backfill=True)
    ```

## UDF API

All UDFs are decorated by ``@geneva.udf``.

::: geneva.udf
    options:
      annotations_path: brief
      show_source: false
