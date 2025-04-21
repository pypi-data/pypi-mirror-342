# InferenceMultiBackend

Python library for run inference of deep learning models in different backends

## Installation

For use triton inference client:
```pip install imb[triton]```

For use onnxruntime-gpu client:
```pip install imb[onnxgpu]```

For use onnxruntime client:
```pip install imb[onnxcpu]```

For support all implemented clients:
```pip install imb[all]```

## Usage

OnnxClient usage example
```
onnx_client = OnnxClient(
    model_path='model.onnx',
    model_name='any name',
    providers=['CUDAExecutionProvider', 'CPUExecutionProvider'],
    max_batch_size=16,
    return_dict=True,
    fixed_batch=True,
    warmup=True
)
# if model has fixed input size (except batch size) then sample_inputs will be created
sample_inputs = onnx_client.sample_inputs
print('inputs shapes', [o.shape for o in sample_inputs])
outputs = onnx_client(*sample_inputs)
print('outputs shapes', [(o_name, o_value.shape) for o_name, o_value in outputs.items()])
```

TritonClient usage example
```
triton_client = TritonClient(
    url='localhost:8000',
    model_name='arcface',
    max_batch_size=16,
    timeout=10,
    resend_count=10,
    fixed_batch=True,
    is_async=False,
    cuda_shm=False,
    max_shm_regions=2,
    scheme='http',
    return_dict=True,
    warmup=False
)
# if model has fixed input size (except batch size) then sample_inputs will be created
sample_inputs = triton_client.sample_inputs
print('inputs shapes', [o.shape for o in sample_inputs])
outputs = triton_client(*sample_inputs)
print('outputs shapes', [(o_name, o_value.shape) for o_name, o_value in outputs.items()])
```

## Notes

max_batch_size - maximum batch size for inference. If input data larger that max_batch_size, then input data will be splitted to several batches.

fixed_batch - if fixed batch is True, then each batch will have fixed size (padding the smallest batch to max_batch_size).

warmup - if True, model will run several calls on sample_inputs while initialization. 

return_dict - if True, __call__ return dict {'output_name1': output_value1, ...}, else [output_value1, ...]