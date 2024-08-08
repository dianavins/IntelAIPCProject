import openvino
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from openvino.runtime import Core, Tensor
import transformers
import torch

################ load model ################

model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]

outputs = pipeline(
    messages,
    max_new_tokens=256,
)
print(outputs[0]["generated_text"][-1])

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

################ openvino & optimum ################

core = Core()
optimum = core.create_optimum()
optimum.set_model(model)
optimum.optimize()
optimum.save_model("optimized_model.xml")

# OR

core = Core()
model = core.read_network(model=model, weights=model)
model = core.load_network(model=model, device="CPU")
input = Tensor("input", "FP32", [1, 1])
output = Tensor("output", "FP32", [1, 1])
model.reshape({"input": input, "output": output})
model.optimize()
model.export("model.xml", "model.bin")