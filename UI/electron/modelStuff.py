# infer.py
from openvino.inference_engine import IECore

def load_model(model_xml, model_bin):
    ie = IECore()
    net = ie.read_network(model=model_xml, weights=model_bin)
    exec_net = ie.load_network(network=net, device_name='CPU')
    return exec_net

def infer(exec_net, input_data):
    input_blob = next(iter(exec_net.input_info))
    output_blob = next(iter(exec_net.outputs))
    res = exec_net.infer({input_blob: input_data})
    return res[output_blob]

if __name__ == "__main__":
    model = load_model('path_to_model.xml', 'path_to_weights.bin')
    # Assume input_data is prepared appropriately
    results = infer(model, input_data)
    print(results)
