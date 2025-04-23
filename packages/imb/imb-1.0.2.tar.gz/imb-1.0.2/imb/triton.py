from collections import defaultdict
from typing import Any, Dict, List, Literal, Optional, Tuple
import tritonclient.http as httpclient
import tritonclient.grpc as grpcclient
import tritonclient.utils.cuda_shared_memory as cudashm
import tritonclient.utils.shared_memory as shm
from google.protobuf.json_format import MessageToJson
from tritonclient import utils
from .base import BaseClient
import numpy as np
import json
import time


class ShmHandlerWrapper:
    def __init__(self, handler: Any, name: str, size: int):
        self.handler = handler
        self.name = name
        self.size = size



class TritonClient(BaseClient):
    def __init__(self, url: str,
                 model_name: str,
                 max_batch_size: int = 0,
                 sample_inputs: Optional[List[np.ndarray]] = None,
                 timeout: int = 10,
                 resend_count: int = 10,
                 fixed_batch: bool = True,
                 is_async: bool = False,
                 use_cuda_shm: bool = False,
                 use_system_shm: bool = False,
                 max_shm_regions: int = 0,
                 scheme: Literal["http", "grpc"] = "http",
                 return_dict: bool = True,
                 warmup: bool = False
                 ):
        """_summary_

        Args:
            url (str): url of the triton server
            model_name (str): name of the model endpoint
            max_batch_size (int, optional): max batch size. Defaults to 0 (get value from triton config).
            sample_inputs (Optional[List[np.ndarray]], optional): samples for warmup. Defaults to None (zeros array).
            timeout (int, optional): triton client timeout. Defaults to 10.
            resend_count (int, optional): triton client resend count. Defaults to 10.
            fixed_batch (bool, optional): use fixed batch size, using padding for smaller batch. Defaults to True.
            is_async (bool, optional): async inference. Defaults to False.
            use_cuda_shm (bool, optional): use cuda shared memory. Defaults to False.
            use_system_shm (bool, optional): use system shared memory. Defaults to False.
            max_shm_regions (int, optional): max clients for shared memory. Will unregister old regions. Defaults to 0.
            scheme (Literal["http", "grpc"], optional): scheme for triton client. Defaults to "http".
            return_dict (bool, optional): return dict or list of values. Defaults to True.
            warmup (bool, optional): warmup model. Defaults to False.
        """
        super().__init__()
        assert not (use_cuda_shm and use_system_shm), 'shm and cuda_shm are mutually exclusive'
        self.model_name = model_name
        self.scheme = scheme
        self.client_module = httpclient if scheme == "http" else grpcclient
        self.url = url
        self.is_async = is_async
        self.use_cuda_shm = use_cuda_shm
        self.use_system_shm = use_system_shm
        self.triton_timeout = timeout
        self.resend_count = resend_count
        self.max_shm_regions = max_shm_regions
        self.return_dict = return_dict

        self.triton_client = None
        self._init_triton()

        self.triton_inputs_dtypes = None
        self.np_inputs_dtypes = None
        
        self.inputs_shapes = None
        self.fixed_batch = fixed_batch
        
        self.inputs_names = None
        self.outputs_names = None
        
        self.sample_inputs = sample_inputs       
        
        self._load_model_params(max_batch_size) 
        self._create_input_sample()
        if warmup:
            self.warmup_model()

        self.input_shm_handlers: List[Optional[ShmHandlerWrapper]] = \
            [None for _ in range(len(self.inputs_names))]
        self.output_shm_handlers: List[Optional[ShmHandlerWrapper]] = \
            [None for _ in range(len(self.outputs_names))]

        if self.use_cuda_shm or self.use_system_shm:
            assert is_async == False and fixed_batch == True
            self._fill_output_dynamic_axis()
            self._create_input_output_shm_handles()
            self._register_shm_regions()

    def io_summary(self):
        return {
            "model_name": self.model_name,
            "url": self.url,
            "scheme": self.scheme,

            "inputs_shapes": self.inputs_shapes,
            "inputs_names": self.inputs_names,
            "triton_inputs_dtypes": self.triton_inputs_dtypes,
            "np_inputs_dtypes": self.np_inputs_dtypes,

            "outputs_shapes": self.outputs_shapes,
            "outputs_names": self.outputs_names,
            "triton_outputs_dtypes": self.triton_outputs_dtypes,
            "np_outputs_dtypes": self.np_outputs_dtypes,

            "fixed_batch": self.fixed_batch,
            "async": self.is_async,
            "cuda_shm": self.use_cuda_shm,
            "shm": self.use_system_shm,
            "max_shm_regions": self.max_shm_regions,
        }

    def _init_triton(self):
        if self.triton_client is not None:
            # reinit
            self.triton_client.close()
            time.sleep(3)

        self.triton_client = self.client_module.InferenceServerClient(
                                url=self.url,
                                verbose=False,
                                ssl=False,
                                network_timeout=self.triton_timeout,
                                connection_timeout=self.triton_timeout
                            )

    def _load_model_params(self, user_max_batch_size: int) -> None:
        """
        Load the model config from Triton Inferernce Server and update the class attributes.

        Args:
            user_max_batch_size (int): max_batch_size defined by user
        """
        if self.scheme == "grpc":
            config = self.triton_client.get_model_config(self.model_name, as_json=True)
            config = config["config"]
        else:
            config = self.triton_client.get_model_config(self.model_name)
        
        self.triton_inputs_dtypes, self.np_inputs_dtypes, \
            self.inputs_shapes, self.inputs_names \
                = self._parse_io_params(config['input'])
        
        self.triton_outputs_dtypes, self.np_outputs_dtypes, \
            self.outputs_shapes, self.outputs_names \
                = self._parse_io_params(config['output'])
        
        not_support_dynamic_batch = config['max_batch_size'] == 0
        if not_support_dynamic_batch:
            # use batch size from config
            self.max_batch_size = config['input'][0]['dims'][0]
            self.fixed_batch = True
        else:
            # user can decrease max_batch_size from config
            if user_max_batch_size > 0:
                self.max_batch_size = min(config['max_batch_size'], user_max_batch_size)
            else:
                self.max_batch_size = config['max_batch_size']
            # in config's shape has no batch size
            self.inputs_shapes = self._insert_batch_size_to_shapes(
                self.inputs_shapes, self.max_batch_size
                )
            self.outputs_shapes = self._insert_batch_size_to_shapes(
                self.outputs_shapes, self.max_batch_size
                )
    
    def _fill_output_dynamic_axis(self) -> None:
        """
        Fill real values in the dynamic axis of the output shapes.
        """
        has_dynamic_shapes = any(
                -1 in output_shape for output_shape in self.outputs_shapes
            )
        if has_dynamic_shapes:
            start_cuda_shm_flag = self.use_cuda_shm
            start_system_shm_flag = self.use_system_shm
            self.use_cuda_shm = False
            self.use_system_shm = False
            outputs = self.forward(*self.sample_inputs)
            self.outputs_shapes = [
                list(outputs[output_name].shape) for output_name in self.outputs_names
                ]
            self.use_cuda_shm = start_cuda_shm_flag
            self.use_system_shm = start_system_shm_flag

    @staticmethod
    def _parse_io_params(io_params: List[Dict]) -> Tuple[List[str], List[np.dtype], List[List[int]], List[str]]:
        """
        Parse the input/output parameters from the model config.

        Args:
            io_params (List[Dict]): The input/output parameters.

        Returns:
            Tuple[List[str], List[np.dtype], List[List[int]], List[str]]: The input/output dtypes, shapes, and names.
        """
        triton_dtypes = []
        np_dtypes = []
        shapes = []
        names = []
        for params in io_params:
            triton_dtypes.append(params['data_type'].replace('TYPE_', ''))
            np_dtypes.append(utils.triton_to_np_dtype(triton_dtypes[-1]))
            shapes.append(params['dims'])
            names.append(params['name'])

        return triton_dtypes, np_dtypes, shapes, names

    @staticmethod
    def _insert_batch_size_to_shapes(shapes: List[List], insert_batch_size: int) -> List[List[int]]:
        """
        Insert the batch size to the shapes.

        Args:
            shapes (List[List]): Shapes from config
            insert_batch_size (int): Value for insert batch size to shape

        Returns:
            List[List[int]]: Result shape
        """
        return [[insert_batch_size] + shape for shape in shapes]

    def _generate_shm_name(self, ioname: str) -> str:
        """
        Generate shared region name

        Args:
            ioname (str): Input/output name

        Returns:
            str: Shared region name
        """
        return f'{self.model_name}_{ioname}_{time.time()}'

    def _get_old_regions_names(self, regions_statuses: list, new_triton_shm_name: str) -> List[str]:
        """
        Get old regions names for unregister

        Args:
            regions_statuses (list): responce of get_shared_memory_status from triton
            new_triton_shm_name (str): name of new region

        Returns:
            List[str]: old regions names for unregister
        """
        if self.max_shm_regions < 1:
            return []
        i_sep = len(new_triton_shm_name) - new_triton_shm_name[::-1].index('_') - 1
        region_name = new_triton_shm_name[:i_sep]
        registrated_regions = [
            (region['name'], float(region['name'][i_sep+1:])) 
            for region in regions_statuses if region['name'].startswith(region_name)
        ]
        registrated_regions.sort(key=lambda x: x[1])
        count_old_regions = len(registrated_regions) - self.max_shm_regions + 1
        old_regions = []
        if count_old_regions > 0:
            old_regions = [name for name, _ in registrated_regions[:count_old_regions]]
        return old_regions

    def _create_shm_handle(self, shape: List[int], dtype: np.dtype, name: str) -> ShmHandlerWrapper:
        """
        Create shared memory handle

        Args:
            shape (List[int]): Shape of shared memory region
            dtype (np.dtype): Data type of input/output data
            name (str): Input/output name

        Returns:
            Any: shared memory handle
        """
        byte_size = int(np.prod(shape) * np.dtype(dtype).itemsize)
        shm_name = self._generate_shm_name(name)
        if self.use_cuda_shm:
            shm_handle = cudashm.create_shared_memory_region(
                shm_name, byte_size, 0
                )
        else:
            shm_handle = shm.create_shared_memory_region(
                shm_name, shm_name, byte_size
                )
        return ShmHandlerWrapper(shm_handle, shm_name, byte_size)

    def _create_shm_handles_for_io(self, shapes: List[List[int]], 
                                        dtypes: List[np.dtype], 
                                        names: List[str]) -> List[ShmHandlerWrapper]:
        """
        Create shared memory handles for inputs or outputs

        Args:
            shapes (List[List[int]]): Shapes of cuda shared memory regions
            dtypes (List[np.dtype]): Data types of input/output data
            names (List[str]): Input/output names

        Returns:
            List[ShmHandlerWrapper]: shared memory handles
        """
        return [self._create_shm_handle(shape, dtype, name) 
                for shape, dtype, name in zip(shapes, dtypes, names)]

    def _create_input_output_shm_handles(self) -> None:
        """
        Create shared memory handles for inputs and outputs
        """
        self.input_shm_handlers = self._create_shm_handles_for_io(
            self.inputs_shapes, self.np_inputs_dtypes, self.inputs_names
        )
        self.output_shm_handlers = self._create_shm_handles_for_io(
            self.outputs_shapes, self.np_outputs_dtypes, self.outputs_names
        )

    def _create_triton_input(self, input_data: np.ndarray, input_name: str, 
                             config_input_format: str, shm_handler: Optional[ShmHandlerWrapper] = None) -> Any:
        """
        Create triton InferInput

        Args:
            input_data (np.ndarray): data for send to model
            input_name (str): name of input
            config_input_format (str): triton input format
            shm_handler (ShmHandlerWrapper, optional): shared memory handler. Defaults to None.

        Returns:
            Any: triton InferInput for sending request
        """
        infer_input = self.client_module.InferInput(input_name, input_data.shape, config_input_format)
        if self.use_cuda_shm or self.use_system_shm:
            shm_utils = cudashm if self.use_cuda_shm else shm
            shm_utils.set_shared_memory_region(shm_handler.handler, [input_data])
            infer_input.set_shared_memory(shm_handler.name, shm_handler.size)
        else:
            infer_input.set_data_from_numpy(input_data)
        return infer_input

    def _create_triton_output(self, output_name: str, binary: bool = True, shm_handler: Optional[ShmHandlerWrapper] = None) -> Any:
        """
        Create triton InferRequestedOutput

        Args:
            output_name (str): output name
            binary (bool, optional): Whether the output is binary. Defaults to True.
            shm_handler (ShmHandlerWrapper, optional): shared memory handler. Defaults to None.

        Returns:
            Any: triton InferRequestedOutput for receiving response
        """
        if self.scheme == "grpc":
            infer_output = self.client_module.InferRequestedOutput(output_name)
        else:
            infer_output = self.client_module.InferRequestedOutput(output_name, binary_data=binary)
        if self.use_cuda_shm or self.use_system_shm:
            infer_output.set_shared_memory(shm_handler.name, shm_handler.size)
        return infer_output

    def _register_shm_regions(self):
        """
        Register shared memory regions in Triton
        """
        get_shared_memory_status = self.triton_client.get_cuda_shared_memory_status \
            if self.use_cuda_shm else self.triton_client.get_system_shared_memory_status
        
        unregister_shared_memory = self.triton_client.unregister_cuda_shared_memory \
            if self.use_cuda_shm else self.triton_client.unregister_system_shared_memory
        
        if self.scheme == "grpc":
            regions_statuses = get_shared_memory_status(as_json=True)['regions']
        else:
            regions_statuses = get_shared_memory_status()

        for shm_handler in self.input_shm_handlers + self.output_shm_handlers:
            old_regions_names = self._get_old_regions_names(regions_statuses, shm_handler.name)
            for old_region_name in old_regions_names:
                unregister_shared_memory(old_region_name)
            
            if self.use_cuda_shm:
                self.triton_client.register_cuda_shared_memory(
                    shm_handler.name, cudashm.get_raw_handle(shm_handler.handler), 0, shm_handler.size
                )
            else:
                self.triton_client.register_system_shared_memory(
                    shm_handler.name, shm_handler.name, shm_handler.size
                )

    def _postprocess_triton_result(self, triton_response: Any, padding_size: int) -> Dict[str, np.ndarray]:
        """
        Postprocess triton response.

        Args:
            triton_response (Any): triton response
            padding_size (int): padding size for unpad output data

        Returns:
            Dict[str, np.ndarray]: dict of output name and output data
        """
        result = dict()
        for output_name, shm_op_handle in zip(self.outputs_names, self.output_shm_handlers):
            if self.use_cuda_shm or self.use_system_shm:
                if self.scheme == "grpc":
                    # output = triton_response.get_output(output_name, as_json=True) # WARN: bug in tritonclient library, return None
                    output = json.loads(MessageToJson(triton_response.get_output(output_name)))
                else:
                    output = triton_response.get_output(output_name)
                    
                shm_utils = shm if self.use_system_shm else cudashm
                result[output_name] = shm_utils.get_contents_as_numpy(
                    shm_op_handle.handler,
                    utils.triton_to_np_dtype(output["datatype"]),
                    output["shape"],
                )
            else:
                result[output_name] = triton_response.as_numpy(output_name)

            if padding_size != 0:
                result[output_name] = result[output_name][:-padding_size]
                
        return result

    def forward(self, *inputs_data: np.ndarray) -> Dict[str, np.ndarray]:
        assert len(inputs_data) == len(self.inputs_names), 'inputs number is not equal to model inputs'
        inputs_batches, batches_paddings = self._create_batches(*inputs_data)

        result = defaultdict(list)
        count_batches = len(next(iter(inputs_batches.values())))
        
        for i_batch in range(count_batches):
            triton_inputs = []
            for input_name, config_input_format, shm_ip_handler in \
                    zip(self.inputs_names, self.triton_inputs_dtypes, self.input_shm_handlers):
                triton_input = self._create_triton_input(
                    inputs_batches[input_name][i_batch], input_name, config_input_format, shm_ip_handler
                    )
                triton_inputs.append(triton_input)

            triton_outputs = []
            for output_name, shm_op_handlers in zip(self.outputs_names, self.output_shm_handlers):
                triton_output = self._create_triton_output(
                    output_name, binary=True, shm_handler=shm_op_handlers
                    )
                triton_outputs.append(triton_output)

            triton_response = self.triton_client.infer(
                model_name=self.model_name, 
                inputs=triton_inputs, 
                outputs=triton_outputs
                )
            
            batch_result = self._postprocess_triton_result(triton_response, batches_paddings[i_batch])

            for output_name, output_value in batch_result.items():
                result[output_name].append(output_value)

        for output_name, output_values in result.items(): 
            result[output_name] = np.concatenate(output_values)

        return result

    def send_async_requests(self, inputs_batches: Dict):
        count_batches = len(next(iter(inputs_batches.values())))
        
        triton_response_handles = []

        for i_batch in range(count_batches):
            triton_inputs = []
            for input_name, config_input_format, shm_ip_handle in \
                    zip(self.inputs_names, self.triton_inputs_dtypes, self.input_shm_handlers):
                triton_input = self._create_triton_input(
                    inputs_batches[input_name][i_batch], input_name, config_input_format, shm_ip_handle
                    )
                triton_inputs.append(triton_input)

            triton_outputs = []
            for output_name, shm_op_handle in zip(self.outputs_names, self.output_shm_handlers):
                triton_output = self._create_triton_output(
                    output_name, binary=True, shm_handle=shm_op_handle
                    )
                triton_outputs.append(triton_output)
            
            triton_response_handle = self.triton_client.async_infer(
                        model_name=self.model_name, 
                        inputs=triton_inputs, 
                        outputs=triton_outputs
                        )
            triton_response_handles.append(triton_response_handle)
        
        return triton_response_handles
    
    def get_async_results(self, triton_response_handles, batches_paddings):
        result = defaultdict(list)
        for i_batch, triton_response_handle in enumerate(triton_response_handles):
            triton_response = triton_response_handle.get_result()
            batch_result = self._postprocess_triton_result(triton_response, batches_paddings[i_batch])

            for output_name, output_value in batch_result.items():
                result[output_name].append(output_value)

        for output_name, output_values in result.items(): 
            result[output_name] = np.concatenate(output_values)
        
        return result
    
    def async_forward(self, *inputs_data: np.ndarray):
        assert len(inputs_data) == len(self.inputs_names), 'inputs number is not equal to model inputs'
        inputs_batches, batches_paddings = self._create_batches(*inputs_data)
        
        triton_response_handles = self.send_async_requests(inputs_batches)

        result = self.get_async_results(triton_response_handles, batches_paddings)

        return result
