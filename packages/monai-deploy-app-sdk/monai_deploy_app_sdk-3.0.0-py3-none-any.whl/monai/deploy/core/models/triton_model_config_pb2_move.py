from pathlib import Path

from google.protobuf import text_format
from tritonclient.grpc.model_config_pb2 import DataType, ModelConfig


def parse_triton_config_pbtxt(pbtxt_path) -> ModelConfig:
    """Parse a Triton model config.pbtxt file

    Args:
        config_path: Path to the config.pbtxt file

    Returns:
        ModelConfig object containing parsed configuration

    Raises:
        ValueError: If config file is invalid or missing required fields
        FileNotFoundError: If config file doesn't exist
    """

    if not pbtxt_path.exists():
        raise FileNotFoundError(f"Config file not found: {pbtxt_path}")
    try:
        # Read the config.pbtxt content
        with open(pbtxt_path, "r") as f:
            config_text = f.read()
            # Parse using protobuf text_format
            model_config = ModelConfig()
            text_format.Parse(config_text, model_config)
            return model_config

    except Exception as e:
        raise ValueError(f"Failed to parse config file {pbtxt_path}: {str(e)}")


# Example usage:
if __name__ == "__main__":
    config = parse_triton_config_pbtxt(Path("models/triton_models/spleen_ct/config.pbtxt"))
    print("Model name:", config.name)
    print("Model platform:", config.platform)
    print("Model backend:", config.backend)
    print("Model max batch size:", config.max_batch_size)
    print("Model runtime:", config.runtime)
    print("Model default model filename:", config.default_model_filename)

    print("Model input count:", len(config.input))
    print("Model output count:", len(config.output))
    for inp in config.input:
        print("Input name:", inp.name, "data_type:", DataType.Name(inp.data_type), "dims:", inp.dims)
        print("dims datatype:", type(inp.dims))
        list_dims = list(inp.dims)
        print("list_dims:", list_dims)
        print("list_dims datatype:", type(list_dims))
    for out in config.output:
        print("Output name:", out.name, "data_type:", DataType.Name(out.data_type), "dims:", out.dims)

    print("Model version policy:", config.version_policy)
    print("Model scheduling choice:", config.dynamic_batching)
    print("Model instance group:", config.instance_group)
    print("Model model metrics:", config.model_metrics)
