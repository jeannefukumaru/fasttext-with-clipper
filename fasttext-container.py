from __future__ import print_function

import rpc
import os
import fasttext

class fasttextContainer(rpc.ModelContainerBase):
    def __init__(self, path):
	self.model = fasttext.load_model(path + '.bin')

    def predict_func(self, reviews):
        preds = self.model.predict(reviews)
	return [str(p) for p in preds]

if __name__ == "__main__":
    print("Starting fasttext container")
    try:
        model_name = os.environ["CLIPPER_MODEL_NAME"]
    except KeyError:
        print(
            "ERROR: CLIPPER_MODEL_NAME environment variable must be set",
            file=sys.stdout)
        sys.exit(1)
    try:
        model_version = os.environ["CLIPPER_MODEL_VERSION"]
    except KeyError:
        print(
            "ERROR: CLIPPER_MODEL_VERSION environment variable must be set",
            file=sys.stdout)
        sys.exit(1)

    ip = "127.0.0.1"
    if "CLIPPER_IP" in os.environ:
        ip = os.environ["CLIPPER_IP"]
    else:
        print("Connecting to Clipper on localhost")

    port = 7000
    if "CLIPPER_PORT" in os.environ:
        port = int(os.environ["CLIPPER_PORT"])
    else:
        print("Connecting to Clipper with default port: 7000")

    input_type = "doubles"
    model_dir_path = os.environ["CLIPPER_MODEL_PATH"]
    model_files = os.listdir(model_dir_path)
    assert len(model_files) >= 2
    fname = os.path.splitext(model_files[0])[0]
    full_fname = os.path.join(model_dir_path, fname)
    print(full_fname)
    model = TfCifarContainer(full_fname)
    rpc_service = rpc.RPCService()
    rpc_service.start(model, ip, port, model_name, model_version, input_type)
