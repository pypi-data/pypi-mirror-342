from luminarycloud._proto.client.simulation_pb2 import SimulationParam
from luminarycloud._helpers.cond import params_to_dict
from google.protobuf.json_format import ParseDict
import json

json_file = "/sdk/testdata/transient_param.json"
with open(json_file, "r") as f:
    sim_dict = json.load(f)
sim = SimulationParam()
_ = ParseDict(sim_dict, sim)
clean_sim_dict = params_to_dict(sim)
print(clean_sim_dict)
