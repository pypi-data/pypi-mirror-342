# Troubleshooting Feature Engineering Jobs

We'll cover common problems you may encounter when using Geneva and troubleshooting tips to solve them.

Here are some areas to verify to identify the source of problems with your Geneva deployment.

1. Versions compatibility (Ray, Python, Lance).
2. Remote Ray execution and hardware resource availability.
3. Sufficient permissions to access data.
4. Worker code only returns serializable values (no open files, no GPU resident buffers).

# Confirming dependency versions (Ray, Python, Lance, etc)

Geneva uses Ray for distributed execution.  Ray requires the version deployed cluster services and clients to be exactly the same.   Minor versions of Python must match both on client and cluster services (e.g. 3.10.3 and 3.10.5 are ok, but 3.10.3 and 3.12.1 are not.)

Geneva has been tested with Ray 2.44+ and python 3.10.x and 3.12.x.

You can run this code in your notebook to verify your environment matches your expectations.
```
!python --version
!pip show lancedb  # need 0.22.0b0+
!echo $VIRTUAL_ENV'
```

# Confirming remote Ray execution

Geneva allows you to specify the resources of your worker nodes.  You can verify that your cluster has the resources (e.g. GPUs) available for your jobs and that remote execution is working properly.

You can get some basic information about resources available to your Ray:
```
print(ray.available_resources())
```

You can verify basic remote execution via Ray:
```

@ray.remote
def check_remote():
  return "Hello from a worker"

print(ray.get(check_remote.remote()))
```

For GPU-dependent UDFs and jobs, you can verify that GPU worker nodes have the cuda library 
```
# does ray have cuda?
@ray.remote(num_gpus=1)
def check_cuda():
    import torch
    return torch.version.cuda, torch.cuda.is_available()

print(ray.get(check_cuda.remote()))
```

# Confirming sufficient permissions

While your notebook or working environment may have credentials to read and write to particular buckets, your jobs need sufficient rights to read and write to them as well.    Adding a `import geneva` to any remote function can help verify that your workers have sufficient grants.

Here we add `import geneva` to help trigger potential permissions problems:
```
@ray.remote(num_gpus=1)
def check_cuda():
    import geneva # this is currently required before other imports
    import torch
    return torch.version.cuda, torch.cuda.is_available()

print(ray.get(check_cuda.remote()))
```

## GCE Permissions errors in job logs

If are using geneva managed ray deployed on GKE, the errors may look like this:

```
PermissionError: [Errno 13] google::cloud::Status(PERMISSION_DENIED: Permanent error, with a last message of Caller does not have storage.objects.get access to the Google Cloud Storage object. Permission 'storage.objects.get' denied on resource (or it may not exist). error_info={reason=forbidden, domain=global, metadata={gcloud-cpp.retry.function=GetObjectMetadata, gcloud-cpp.retry.reason=permanent-error, gcloud-cpp.retry.original-message=Caller does not have storage.objects.get access to the Google Cloud Storage object. Permission 'storage.objects.get' denied on resource (or it may not exist)., http_status_code=403}}). Detail: [errno 13] Permission denied
```

THis indicates that your workers and or head node are not being run with the correct service account or with an account that has sufficient access.  Please double check the service account's accesses and make sure to add your service account that has access to the buckets as a parameter to your this to your Head and Worker specs. See `service_account="geneva-integ-test"` below.

```
raycluster =  RayCluster(
    name= k8s_name,
    namespace=k8s_namespace,
    head_group=_HeadGroupSpec(
        num_cpus=8,
        service_account="geneva-integ-test"
    ),
    worker_groups=[
        _WorkerGroupSpec(
            name="cpu",
            num_cpus=60,
            memory="120G",
            service_account="geneva-integ-test",
        ),
        _WorkerGroupSpec(
            name="gpu",
            num_cpus=8,
            memory="32G",
            num_gpus=1,
            service_account="geneva-integ-test",
        ),
    ],
)

```

# UDF Serialization errors

## Disconnect or serialization errors with GPU dependent UDFs

When using GPU code, the typical process loads some values and tensors from CPU memory to GPU memory.  Even after moving data (`data.cpu().tolist()`), there may be references to GPU memory.  While this is not a problem with local execution, when doing a distributed job it may cause problems because the GPU references are not serializable and not needed.  You must take steps to eliminate references to structures in GPU memory since they can not be serialized
and sent between workers.  This can be achieved by explicitly disconnecting references to the GPU memory (`data.cpu().detach().tolist()`) to get only-CPU resident fully serializable objects.

Here are some typical error messages.

```
Exception in thread Thread-27 (_proxy):
Traceback (most recent call last):
  File "/home/jon/.pyenv/versions/3.10.16/lib/python3.10/threading.py", line 1016, in _bootstrap_inner
    self.run()
  File "/home/jon/proj/geneva-deepseek-vl2/.venv/lib/python3.10/site-packages/ipykernel/ipkernel.py", line 772, in run_closure
    _threading_Thread_run(self)
  File "/home/jon/.pyenv/versions/3.10.16/lib/python3.10/threading.py", line 953, in run
    self._target(*self._args, **self._kwargs)
  File "/home/jon/proj/geneva-deepseek-vl2/src/geneva/runners/ray/_portforward.py", line 172, in _proxy
    {s1: s2, s2: s1}[s].sendall(data)
BrokenPipeError: [Errno 32] Broken pipe
Log channel is reconnecting. Logs produced while the connection was down can be found on the head node of the cluster in `ray_client_server_[port].out`
2025-04-11 02:25:21 INFO Starting proxy from pod to client
2025-04-11 02:25:21 INFO Proxy started
2025-04-11 02:25:21 INFO Proxying between <kubernetes.stream.ws_client.PortForward._Port._Socket object at 0x70b2bf9033a0> and <socket.socket fd=230, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 59979), raddr=('127.0.0.1', 32956)>
2025-04-11 02:25:21 INFO Waiting for client connection
2025-04-11 02:25:21,828	ERROR dataclient.py:330 -- Unrecoverable error in data channel.
---------------------------------------------------------------------------
...
```


```
File ~/proj/geneva-deepseek-vl2/.venv/lib/python3.10/site-packages/grpc/_channel.py:1006, in _end_unary_response_blocking(state, call, with_call, deadline)
   1004         return state.response
   1005 else:
-> 1006     raise _InactiveRpcError(state)

_InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.NOT_FOUND
	details = "Failed to serialize response!"
	debug_error_string = "UNKNOWN:Error received from peer  {created_time:"2025-04-11T02:25:22.209209484+00:00", grpc_status:5, grpc_message:"Failed to serialize response!"}"
>

Unexpected exception:
Traceback (most recent call last):
  File "/home/jon/proj/geneva-deepseek-vl2/.venv/lib/python3.10/site-packages/ray/util/client/logsclient.py", line 67, in _log_main
    for record in log_stream:
  File "/home/jon/proj/geneva-deepseek-vl2/.venv/lib/python3.10/site-packages/grpc/_channel.py", line 543, in __next__
    return self._next()
  File "/home/jon/proj/geneva-deepseek-vl2/.venv/lib/python3.10/site-packages/grpc/_channel.py", line 969, in _next
    raise self
grpc._channel._MultiThreadedRendezvous: <_MultiThreadedRendezvous of RPC that terminated with:
	status = StatusCode.NOT_FOUND
	details = "Logstream proxy failed to connect. Channel for client bd854100340640fb8b5770d2bf173197 not found."
	debug_error_string = "UNKNOWN:Error received from peer  {grpc_message:"Logstream proxy failed to connect. Channel for client bd854100340640fb8b5770d2bf173197 not found.", grpc_status:5, created_time:"2025-04-11T02:25:32.223710374+00:00"}"
>
```