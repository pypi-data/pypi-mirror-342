from collections import defaultdict
from typing import Dict, List
from .base import BaseClient
import onnxruntime as rt
import numpy as np


class OnnxClient(BaseClient):
    def __init__(self, model_path: str, 
                 model_name: str, 
                 providers: List[str] = ['CUDAExecutionProvider', 'CPUExecutionProvider'], 
                 max_batch_size: int = 1,
                 return_dict: bool = True,
                 fixed_batch: bool = False,
                 warmup: bool = False
                 ):
        super().__init__()
        self.model_name = model_name
        self.model_path = model_path
        self.providers = providers
        self.return_dict = return_dict
        self.max_batch_size = max_batch_size
        self.fixed_batch = fixed_batch

        self._load_model_params(max_batch_size)

        self.sample_inputs = [np.zeros((*shape,), dtype=dtype) for shape, dtype in zip(self.inputs_shapes, self.np_inputs_dtypes)]

        if warmup:
            self.warmup_model()

    def _load_model_params(self, max_batch_size: int = 1):
        """
        Load model parameters from onnx model

        Args:
            max_batch_size (int, optional): max batch size. Defaults to 1.

        Raises:
            ValueError: not support dynamic batch
        """
        sess_options = rt.SessionOptions()
        self.onnx_model = rt.InferenceSession(
            self.model_path,
            providers=self.providers,
            sess_options=sess_options
        )

        model_inputs = self.onnx_model.get_inputs()
        data_dtype = np.float16 if 'float16' in model_inputs[0].type else np.float32
        self.inputs_names = [model_inputs[i].name for i in range(len(model_inputs))]
        self.np_inputs_dtypes = [data_dtype for _ in range(len(self.inputs_names))]
        self.inputs_shapes = [model_inputs[i].shape for i in range(len(model_inputs))] 
        for i_input, shape in enumerate(self.inputs_shapes):
            new_shape = []
            for i_dim, value in enumerate(shape):
                if isinstance(value, int):
                    if i_dim == 0:
                        self.max_batch_size = value
                        self.log(f'set batch size {value} from model metadata')
                    new_shape.append(value)
                elif isinstance(value, str) and 'batch' in value:
                    new_shape.append(max_batch_size)
                    self.log(f'set batch size {value} from user settings')
                else:
                    raise ValueError(f'not support value {value} in input shape {shape}')
            self.inputs_shapes[i_input] = new_shape            

        model_outputs = self.onnx_model.get_outputs()
        self.outputs_names = [model_outputs[i].name for i in range(len(model_outputs))]
        self.np_outputs_dtypes = [data_dtype for _ in range(len(self.outputs_names))]
    
    def forward(self, *inputs_data: np.ndarray) -> Dict[str, np.ndarray]:
        inputs_batches, batches_paddings = self._create_batches(*inputs_data)

        result = defaultdict(list)
        count_batches = len(next(iter(inputs_batches.values())))

        for i_batch in range(count_batches):
            batch = dict()
            for input_name, np_dtype in zip(self.inputs_names, self.np_inputs_dtypes):
                batch[input_name] = inputs_batches[input_name][i_batch].astype(np_dtype)

            batch_result = self.onnx_model.run(self.outputs_names, batch)
            batch_result = {
                self.outputs_names[i]: batch_result[i].astype(self.np_outputs_dtypes[i])
                for i in range(len(self.outputs_names))
            }
            
            padding_size = batches_paddings[i_batch]
            for output_name, output_value in batch_result.items():
                result[output_name].append(
                    output_value if padding_size == 0 else output_value[:-padding_size]
                    )

        for output_name, output_values in result.items(): 
            result[output_name] = np.concatenate(output_values)

        return result
