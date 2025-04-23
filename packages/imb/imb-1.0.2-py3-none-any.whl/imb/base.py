from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import time
import os


class BaseClient:
    def __init__(self, *args, **kwargs):
        self.show_fps: bool = os.environ.get('SHOW_FPS') in {'yes', 'true'}
        self.model_name = ''
        self.fixed_batch = False
        self.max_batch_size = 1
        self.is_async = False
        self.return_dict = True

        self.inputs_names: List[str] = []
        self.inputs_shapes: List[tuple] = []
        self.np_inputs_dtypes: List[np.dtype] = []

        self.outputs_names: List[str] = []
        self.outputs_shapes: List[tuple] = []
        self.np_outputs_dtypes: List[np.dtype] = []

        self.sample_inputs: Optional[List[np.ndarray]] = None
    
    def _load_model_params(self, *args, **kwargs):
        raise NotImplementedError

    def _create_input_sample(self):
        if self.sample_inputs is not None:
            # validate sample inputs
            for sample_array, config_input_shape in zip(self.sample_inputs, self.inputs_shapes):
                for i, (s_dim, t_dim) in enumerate(zip(sample_array.shape, config_input_shape)):
                    if i == 0:
                        if self.fixed_batch:
                            assert s_dim == t_dim, \
                                f'model support fixed batch size {t_dim}, \
                                    sample_inputs has batch size {s_dim}'
                        else:
                            assert s_dim <= t_dim, \
                                f'model support max batch size {t_dim}, \
                                    sample_inputs has batch size {s_dim}'
                        continue
                    assert ((t_dim != -1) and (int(s_dim) == int(t_dim))) or t_dim == -1, \
                        f'incorrect shape in sample_inputs {sample_array.shape}, must be {config_input_shape}'
        else:
            has_dynamic_shapes = any(
                -1 in config_input_shape for config_input_shape in self.inputs_shapes
            )
            if has_dynamic_shapes:
                return
            self.sample_inputs = []
            for config_input_shape, np_input_format in zip(self.inputs_shapes, self.np_inputs_dtypes):
                self.sample_inputs.append(
                    np.ones(config_input_shape).astype(np_input_format)
                )
    
    def _create_batches(self, *inputs_data: np.ndarray) -> Tuple[Dict[str, List[np.ndarray]], List[int]]:
        inputs_batches = dict()
        paddings = []
        for input_data, np_format, input_name in zip(inputs_data, self.np_inputs_dtypes, self.inputs_names):
            input_data = input_data.astype(np_format)
            input_batches, input_paddings = self._split_on_batches(input_data)
            if paddings == []:
                paddings = input_paddings
            inputs_batches[input_name] = input_batches
        return inputs_batches, paddings

    def log(self, text, warn=False, err=False):
        text = f'Model ({self.model_name}) - {text}'
        if err:
            print('error', text)
        elif warn:
            print('warning',text)
        else:
            print('debug', text)

    def warmup_model(self):
        if self.sample_inputs is None:
            print('Model was not warmed up, because sample_inputs didn\'t set or shape is dynamic and cannot auto generate')
            return
        exception = None
        for _ in range(5):
            try:
                _ = self.__call__(*self.sample_inputs)
                exception = None
            except Exception as e:
                print(f'{e} while warmup, repeat inference...')
                exception = e
                time.sleep(2)
        if exception is not None:
            raise exception
    
    def pad_batch(self, batch: np.ndarray):
        padding_size = self.max_batch_size - batch.shape[0]
        if padding_size > 0:
            pad = np.zeros([padding_size, *batch.shape[1:]], dtype=batch.dtype)
            batch = np.concatenate((batch, pad), axis=0)
        return batch, padding_size
    
    def _split_on_batches(self, input_data: np.ndarray):
        batches = []
        paddings = []
        for i in range(0, len(input_data), self.max_batch_size):
            batch = input_data[i:i+self.max_batch_size]
            batches.append(batch)
            paddings.append(0)
        
        if self.fixed_batch:
            batches[-1], paddings[-1] = self.pad_batch(batches[-1])

        return batches, paddings
    
    def forward(self, *input_data):
        raise NotImplementedError
    
    def async_forward(self, *input_data):
        raise NotImplementedError

    def __call__(self, *args, **kwargs) -> Union[Dict[str, np.ndarray], List[np.ndarray]]:
        t1 = time.time()
        forward_func = self.async_forward if self.is_async else self.forward
        output = forward_func(*args, **kwargs)
        if self.return_dict is False:
            output = [output[output_name] for output_name in self.outputs_names]
        t2 = time.time()
        if self.show_fps:
            self.log(f'Model: {self.model_name} fps {int(len(args[0])/(t2-t1))}')
        return output
