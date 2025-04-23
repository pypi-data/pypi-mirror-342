import argparse
import sys

import gevent.ssl
import numpy as np
import torch
import tritonclient.http as httpclient
from tritonclient.utils import InferenceServerException


def test_infer_torch(
    model_name,
    input0_data,
    input1_data,
    headers=None,
    request_compression_algorithm=None,
    response_compression_algorithm=None,
):
    inputs = []
    outputs = []
    inputs.append(httpclient.InferInput("INPUT0", [1, 16], "INT32"))
    inputs.append(httpclient.InferInput("INPUT1", [1, 16], "INT32"))

    # Convert PyTorch tensors to numpy arrays
    input0_data_np = input0_data.numpy()
    input1_data_np = input1_data.numpy()

    # Initialize the data
    inputs[0].set_data_from_numpy(input0_data_np, binary_data=False)
    inputs[1].set_data_from_numpy(input1_data_np, binary_data=True)

    outputs.append(httpclient.InferRequestedOutput("OUTPUT0", binary_data=True))
    outputs.append(httpclient.InferRequestedOutput("OUTPUT1", binary_data=False))
    query_params = {"test_1": 1, "test_2": 2}
    results = triton_client.infer(
        model_name,
        inputs,
        outputs=outputs,
        query_params=query_params,
        headers=headers,
        request_compression_algorithm=request_compression_algorithm,
        response_compression_algorithm=response_compression_algorithm,
    )

    return results


def test_infer_spleen_ct(
    model_name,
    input0_data,
    triton_client,
    headers=None,
    request_compression_algorithm=None,
    response_compression_algorithm=None,
):
    inputs = []
    outputs = []
    inputs.append(httpclient.InferInput("INPUT_0", [4, 1, 96, 96, 96], "FP32"))

    # Convert PyTorch tensors to numpy arrays
    input0_data_np = input0_data.detach().cpu().numpy()
    print(f"input0_data_np.shape: {input0_data_np.shape}")

    # Initialize the data
    inputs[0].set_data_from_numpy(input0_data_np, binary_data=False)

    outputs.append(httpclient.InferRequestedOutput("OUTPUT_0", binary_data=True))

    query_params = {"test_1": 1}
    results = triton_client.infer(
        model_name,
        inputs,
        outputs=outputs,
        query_params=query_params,
        headers=headers,
        request_compression_algorithm=request_compression_algorithm,
        response_compression_algorithm=response_compression_algorithm,
    )

    print(f"Got results{results.get_response()}")
    output0_data = results.as_numpy("OUTPUT_0")
    print(f"as_numpy output0_data.shape: {output0_data.shape}")
    print(f"as_numpy output0_data.dtype: {output0_data.dtype}")

    # Convert numpy array to torch tensor as expected by the anticipated clients,
    # e.g. monai cliding window inference
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.as_tensor(output0_data).to(device)  # from_numpy is fine too.


class TritonRemoteModel:
    def __call__(self, data, **kwds):
        print(f"TritonRemoteModel.__call__: {self._model_name}")
        return test_infer_spleen_ct(self._model_name, data, self._triton_client, **kwds)

    def __init__(self, model_name, headers=None):
        self._headers = headers
        self._request_compression_algorithm = None
        self._response_compression_algorithm = None
        self._model_name = model_name
        self._model_version = None

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            required=False,
            default=False,
            help="Enable verbose output",
        )
        parser.add_argument(
            "-u",
            "--url",
            type=str,
            required=False,
            default="localhost:8000",
            help="Inference server URL. Default is localhost:8000.",
        )
        parser.add_argument(
            "-s",
            "--ssl",
            action="store_true",
            required=False,
            default=False,
            help="Enable encrypted link to the server using HTTPS",
        )
        parser.add_argument(
            "--key-file",
            type=str,
            required=False,
            default=None,
            help="File holding client private key. Default is None.",
        )
        parser.add_argument(
            "--cert-file",
            type=str,
            required=False,
            default=None,
            help="File holding client certificate. Default is None.",
        )
        parser.add_argument(
            "--ca-certs",
            type=str,
            required=False,
            default=None,
            help="File holding ca certificate. Default is None.",
        )
        parser.add_argument(
            "--insecure",
            action="store_true",
            required=False,
            default=False,
            help="Use no peer verification in SSL communications. Use with caution. Default is False.",
        )
        parser.add_argument(
            "-H",
            dest="http_headers",
            metavar="HTTP_HEADER",
            required=False,
            action="append",
            help="HTTP headers to add to inference server requests. " + 'Format is -H"Header:Value".',
        )
        parser.add_argument(
            "--request-compression-algorithm",
            type=str,
            required=False,
            default=None,
            help="The compression algorithm to be used when sending request body to server. Default is None.",
        )
        parser.add_argument(
            "--response-compression-algorithm",
            type=str,
            required=False,
            default=None,
            help="The compression algorithm to be used when receiving response body from server. Default is None.",
        )

        FLAGS = parser.parse_args()
        try:
            if FLAGS.ssl:
                ssl_options = {}
                if FLAGS.key_file is not None:
                    ssl_options["keyfile"] = FLAGS.key_file
                if FLAGS.cert_file is not None:
                    ssl_options["certfile"] = FLAGS.cert_file
                if FLAGS.ca_certs is not None:
                    ssl_options["ca_certs"] = FLAGS.ca_certs
                ssl_context_factory = None
                if FLAGS.insecure:
                    ssl_context_factory = gevent.ssl._create_unverified_context
                self._triton_client = httpclient.InferenceServerClient(
                    url=FLAGS.url,
                    verbose=FLAGS.verbose,
                    ssl=True,
                    ssl_options=ssl_options,
                    insecure=FLAGS.insecure,
                    ssl_context_factory=ssl_context_factory,
                )
            else:
                self._triton_client = httpclient.InferenceServerClient(url=FLAGS.url, verbose=FLAGS.verbose)
                print(f"Created triton client: {self._triton_client}")
        except Exception as e:
            print("channel creation failed: " + str(e))
            sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        required=False,
        default=False,
        help="Enable verbose output",
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=False,
        default="localhost:8000",
        help="Inference server URL. Default is localhost:8000.",
    )
    parser.add_argument(
        "-s",
        "--ssl",
        action="store_true",
        required=False,
        default=False,
        help="Enable encrypted link to the server using HTTPS",
    )
    parser.add_argument(
        "--key-file",
        type=str,
        required=False,
        default=None,
        help="File holding client private key. Default is None.",
    )
    parser.add_argument(
        "--cert-file",
        type=str,
        required=False,
        default=None,
        help="File holding client certificate. Default is None.",
    )
    parser.add_argument(
        "--ca-certs",
        type=str,
        required=False,
        default=None,
        help="File holding ca certificate. Default is None.",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        required=False,
        default=False,
        help="Use no peer verification in SSL communications. Use with caution. Default is False.",
    )
    parser.add_argument(
        "-H",
        dest="http_headers",
        metavar="HTTP_HEADER",
        required=False,
        action="append",
        help="HTTP headers to add to inference server requests. " + 'Format is -H"Header:Value".',
    )
    parser.add_argument(
        "--request-compression-algorithm",
        type=str,
        required=False,
        default=None,
        help="The compression algorithm to be used when sending request body to server. Default is None.",
    )
    parser.add_argument(
        "--response-compression-algorithm",
        type=str,
        required=False,
        default=None,
        help="The compression algorithm to be used when receiving response body from server. Default is None.",
    )

    FLAGS = parser.parse_args()
    try:
        if FLAGS.ssl:
            ssl_options = {}
            if FLAGS.key_file is not None:
                ssl_options["keyfile"] = FLAGS.key_file
            if FLAGS.cert_file is not None:
                ssl_options["certfile"] = FLAGS.cert_file
            if FLAGS.ca_certs is not None:
                ssl_options["ca_certs"] = FLAGS.ca_certs
            ssl_context_factory = None
            if FLAGS.insecure:
                ssl_context_factory = gevent.ssl._create_unverified_context
            triton_client = httpclient.InferenceServerClient(
                url=FLAGS.url,
                verbose=FLAGS.verbose,
                ssl=True,
                ssl_options=ssl_options,
                insecure=FLAGS.insecure,
                ssl_context_factory=ssl_context_factory,
            )
        else:
            triton_client = httpclient.InferenceServerClient(url=FLAGS.url, verbose=FLAGS.verbose)
    except Exception as e:
        print("channel creation failed: " + str(e))
        sys.exit(1)

    model_name = "spleen_ct"  # "simple"
    input0_data = torch.zeros(4, 1, 96, 96, 96)
    print(f"Dummy input0_data.shape: {input0_data.shape}")
    # Create the data for the two input tensors using PyTorch. Initialize the first
    # to unique integers and the second to all ones.
    # input0_data = torch.arange(start=0, end=16, dtype=torch.int32).unsqueeze(0)
    # input1_data = torch.full((1, 16), -1, dtype=torch.int32)

    if FLAGS.http_headers is not None:
        headers_dict = {l.split(":")[0]: l.split(":")[1] for l in FLAGS.http_headers}
    else:
        headers_dict = None

    # # Infer with requested Outputs
    # results = test_infer_torch(
    #     model_name,
    #     input0_data,
    #     input1_data,
    #     headers_dict,
    #     FLAGS.request_compression_algorithm,
    #     FLAGS.response_compression_algorithm,
    # )
    results = test_infer_spleen_ct(
        model_name,
        input0_data,
        triton_client,
        headers_dict,
        FLAGS.request_compression_algorithm,
        FLAGS.response_compression_algorithm,
    )
    # print(f"Got results{results.get_response()}")

    statistics = triton_client.get_inference_statistics(model_name=model_name, headers=headers_dict)
    print(statistics)
    if len(statistics["model_stats"]) != 1:
        print("FAILED: Inference Statistics")
        sys.exit(1)

    # Validate the results by comparing with precomputed values.
    # output0_data = results.as_numpy("OUTPUT_0")
    # print(f"as_numpy output0_data.shape: {output0_data.shape}")
    # print(f"as_numpy output0_data.dtype: {output0_data.dtype}")
    # #print(output0_data)
    # for i in range(16):
    #     print(str(input0_data[0][i].item()) + " + " + str(input1_data[0][i].item()) + " = " + str(output0_data[0][i]))
    #     print(str(input0_data[0][i].item()) + " - " + str(input1_data[0][i].item()) + " = " + str(output1_data[0][i]))
    #     if (input0_data[0][i].item() + input1_data[0][i].item()) != output0_data[0][i]:
    #         print("sync infer error: incorrect sum")
    #         sys.exit(1)
    #     if (input0_data[0][i].item() - input1_data[0][i].item()) != output1_data[0][i]:
    #         print("sync infer error: incorrect difference")
    #         sys.exit(1)
