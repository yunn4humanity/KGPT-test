import random

unit_operations = {
    "abs": {"inputs": (2, 2), "outputs": (2, 2), "tags": ["bin", "tin", "bout", "tout"]},
    "blwr": {"inputs": (1, 1), "outputs": (1, 1), "tags": []},
    "centr": {"inputs": (1, 1), "outputs": (1, 2), "tags": []},
    "comp": {"inputs": (1, 1), "outputs": (1, 1), "tags": []},
    "cond": {"inputs": (1, 1), "outputs": (2, 2), "tags": ["bout", "tout"]},
    "cycl": {"inputs": (1, 1), "outputs": (2, 2), "tags": []},
    "dist": {"inputs": (1, 2), "outputs": (2, 2), "tags": ["bout", "tout"]},
    "expand": {"inputs": (1, 1), "outputs": (1, 1), "tags": []},
    "extr": {"inputs": (2, 2), "outputs": (2, 2), "tags": []},
    "flash": {"inputs": (1, 1), "outputs": (2, 2), "tags": []},
    "gfil": {"inputs": (1, 1), "outputs": (2, 2), "tags": []},
    "hex": {"inputs": (1, 2), "outputs": (1, 2), "tags": ["he"]},
    "lfil": {"inputs": (1, 1), "outputs": (2, 2), "tags": []},
    "mix": {"inputs": (2, 2), "outputs": (1, 1), "tags": []},
    "r": {"inputs": (1, 1), "outputs": (1, 1), "tags": []},
    "pp": {"inputs": (1, 1), "outputs": (1, 1), "tags": []},
    "splt": {"inputs": (1, 1), "outputs": (2, 2), "tags": []},
    "v": {"inputs": (1, 1), "outputs": (1, 1), "tags": []},
}

def random_unit():
    return random.choice([unit for unit in unit_operations.keys()])

def gen_tag(unit, input_output, tag_index, total_io):
    unit_prefix = unit[:2]
    if total_io > 1:
        return {unit_prefix: [f"{tag_index}_{input_output}"]}
    return None

def gen_flowsheet(num_operations):
    sfiles_string = ""
    
    num_inputs = random.randint(1, 4)
    num_outputs = random.randint(1, 4)
    
    inputs = [f"raw-{i+1}" for i in range(num_inputs)]
    available_inputs = inputs[:]

    outputs = [f"prod-{i+1}" for i in range(num_outputs)]
    
    nodes = set(inputs)
    edges = []
    available_outputs = []

    for i in range(num_operations):
        unit = random_unit()
        unit_inputs_range = unit_operations[unit]["inputs"]
        unit_outputs_range = unit_operations[unit]["outputs"]
        
        unit_inputs = random.randint(unit_inputs_range[0], unit_inputs_range[1])
        unit_outputs = random.randint(unit_outputs_range[0], unit_outputs_range[1])
        
        if unit_inputs > len(available_inputs):
            unit_inputs = len(available_inputs)
            
        unit_name = f"{unit}-{i+1}" # 각 unit마다 넘버링이 순차적으로 가야 하는데 그렇게 되는 건가? 

        used_inputs = [available_inputs.pop(0) for _ in range(unit_inputs)]
        sfiles_string += ''.join(f"({inp})" for inp in used_inputs)
        sfiles_string += f"({unit_name})"

        new_outputs = [f"{unit_name}" for _ in range(unit_outputs)]
        for out in new_outputs:
            available_inputs.append(out)

        available_outputs.extend(new_outputs)

        nodes.add(unit_name)
        tag_index = 1
        for inp in used_inputs:
            tags = gen_tag(unit, "in", tag_index, unit_inputs)
            if tags:
                edges.append((inp, unit_name, {'tags': tags}))
            else:
                edges.append((inp, unit_name))
            tag_index += 1
        tag_index = 1
        for out in new_outputs:
            if out != unit_name:
                tags = gen_tag(unit, "out", tag_index, unit_outputs)
                if tags:
                    edges.append((unit_name, out, {'tags': tags}))
                else:
                    edges.append((unit_name, out))
            tag_index += 1

    for output_stream in outputs:
        if available_inputs:
            sfiles_string += f"({output_stream})"
            nodes.add(output_stream)
            edges.append((available_inputs.pop(0), output_stream))

    return sfiles_string, list(nodes), edges

num_operations = random.randint(5, 20)
sfiles_string, nodes, edges = gen_flowsheet(num_operations)

print(f"SFILES string: {sfiles_string}\n")
print(f"Nodes: {nodes}\n")
print(f"Edges: {edges}\n")
