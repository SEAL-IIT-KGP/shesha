import xml.etree.ElementTree as ET
import argparse
import os
import subprocess
import random
import numpy as np
from datetime import datetime
import re
############## Set up relevant instruction extensions ###################
parser = argparse.ArgumentParser(description = "Fuzzer to explore transient execution paths for instruction extensions")
parser.add_argument('-avx', action='store_true')
parser.add_argument('-avx2', action='store_true')
parser.add_argument('-sse', action='store_true')
parser.add_argument('-sse2', action='store_true')
parser.add_argument('-ssse3', action='store_true')
parser.add_argument('-sse4', action='store_true')
parser.add_argument('--num-instructions', required=True)
parser.add_argument('-aes', action='store_true')
parser.add_argument('-bmi1', action='store_true')
parser.add_argument('-bmi2', action='store_true')
parser.add_argument('-cet', action='store_true')
parser.add_argument('-clflushopt', action='store_true')
parser.add_argument('-clwb', action='store_true')
parser.add_argument('-invpcid', action='store_true')
parser.add_argument('-sse3', action='store_true')
parser.add_argument('-sse4a', action='store_true')
parser.add_argument('-wbnoinvd', action='store_true')
parser.add_argument('-x87', action='store_true')
parser.add_argument('-xsave', action='store_true')
parser.add_argument('-xsavec', action='store_true')
parser.add_argument('-xsaveopt', action='store_true')
parser.add_argument('-xsaves', action='store_true')
parser.add_argument('-avxaes', action='store_true')
args = parser.parse_args()
#########################################################################


class Particle:
    def __init__(self):
        self.position_vector = None
        self.fitness = None
        self.asm = None

    def set_asm(self, asm):
        self.asm = asm
    
    def get_asm(self):
        return self.asm

    def choose_supported_instruction(self, extension, enabled_instructions):
        while(1):
            instruction = enabled_instructions[extension][random.randint(0, len(enabled_instructions[extension]) - 1)]
            for operandNode in instruction.iter('operand'):
                if(operandNode.attrib['type'] != "reg"):
                    continue
            return instruction

    def construct_instruction_asm(self, instruction):
        instruction_name = instruction.attrib['asm']
        if(instruction_name.find("load") >= 0 or instruction_name.find("store") >= 0):
            instruction_name = instruction_name.split(" ")[1].strip()
        instruction_asm = instruction_name + " "
        for operandNode in instruction.iter('operand'):
            ###### handle reg operands ######################
            if(operandNode.attrib['type'] == "reg"):
                registers = operandNode.text.split(',')
                register = registers[random.randint(0, len(registers) -1)]
                if not operandNode.attrib.get('opmask', '') == '1':
                    instruction_asm += register + ", "
                else:
                    instruction_asm += '{' + register + '}, '
                    if instruction.attrib.get('zeroing', '') == '1':
                        instruction_asm += '{z}, '
        instruction_asm = instruction_asm.strip()
        if(instruction_asm[-1] == ','):
            return instruction_asm[0:len(instruction_asm)-1]
        else:
            return instruction_asm

    def choose_replacement_instruction(self, enabled_extensions, enabled_instructions):
        extension = enabled_extensions[random.randint(0, len(enabled_extensions) - 1)]
        instruction = self.choose_supported_instruction(extension, enabled_instructions)
        instruction_asm = self.construct_instruction_asm(instruction)
        return instruction_asm

    def initialize_particle(self, enabled_extensions, enabled_instructions, num_instructions_to_fuzz):
        particle_asm = ""
        particle_asm += "global fuzz_instruction_extensions\n"
        particle_asm += "align 64\n"
        particle_asm += "fuzz_instruction_extensions:\n"
        for _ in range(num_instructions_to_fuzz):
            extension = enabled_extensions[random.randint(0, len(enabled_extensions) - 1)]
            instruction = self.choose_supported_instruction(extension, enabled_instructions)
            instruction_asm = self.construct_instruction_asm(instruction)
            particle_asm += instruction_asm + "\n"
        particle_asm += "ret\n"
        return particle_asm

    def set_position_vector(self, position_vector):
        self.position_vector = position_vector

    def update_position(self, velocity_vector):
        self.position_vector = self.position_vector + velocity_vector

    def return_single_instruction(self):
        particle_asm = self.get_asm()
        particle_asm = particle_asm.split("\n")
        chosen_instruction = None
        while(1):
            chosen_index = random.randint(0, len(particle_asm) - 1)
            chosen_instruction = particle_asm[chosen_index]
            if(chosen_instruction.find("ret") > -1 or
                    chosen_instruction.find("global") > -1 or
                    chosen_instruction.find("align") > -1 or
                    chosen_instruction.find("fuzz_instruction_extensions") > -1):
                continue
            break
        return chosen_instruction

class EquivalenceClass:
    def __init__(self):
        self.class_msr = None
        self.class_desc = None
        self.class_swarm = []

    def get_swarm(self):
        return self.class_swarm

    def set_class_msr(self, msr):
        self.class_msr = msr

    def set_class_desc(self, desc):
        self.class_desc = desc

    def get_class_msr(self):
        return self.class_msr

    def get_class_desc(self):
        return self.class_desc
    
    def is_in_swarm(self, test_particle):
        for index in range(len(self.class_swarm)):
            particle = self.class_swarm[index][0]
            if(particle == test_particle):
                return True
        return False

    def add_to_swarm(self, particle, count):
        self.class_swarm.append([particle, count])

    def update_event_count(self, test_particle, event_count):
        for index in range(len(self.class_swarm)):
            particle = self.class_swarm[index][0]
            if(particle == test_particle):
                self.class_swarm[index][1] = event_count

    def get_event_count(self, test_particle):
        for index in range(len(self.class_swarm)):
            particle = self.class_swarm[index][0]
            if(particle == test_particle):
                return self.class_swarm[index][1]

    def get_swarm_leader(self):
        if(len(self.class_swarm) == 0):
            return None
        max_fitness = self.class_swarm[0][1]
        max_fitness_index = 0
        for index in range(len(self.class_swarm)):
            if(self.class_swarm[index][1] > max_fitness):
                max_fitness_index = index
        return self.class_swarm[max_fitness_index]

class Optimizer:
    def __init__(self, optimizer_config_dict):
        self.root_xml = None
        self.num_instructions_to_fuzz = None
        self.enabled_extensions = []
        self.enabled_instructions = {}
        self.population = []
        self.position_map = {}
        self.position_map_index_counter = 0
        self.monitored_events = []
        self.equivalence_classes = {}
        self.optimizer_config_dict = optimizer_config_dict

    def parse_ise(self):
        self.root_xml = ET.parse("instructions.xml")
    
    def parse_enabled_extensions(self):
        if(args.avx):
            self.enabled_extensions.append("AVX")
        if(args.avx2):
            self.enabled_extensions.append("AVX2")
        if(args.sse):
            self.enabled_extensions.append("SSE")
        if(args.sse2):
            self.enabled_extensions.append("SSE2")
        if(args.ssse3):
            self.enabled_extensions.append("SSSE3")
        if(args.sse4):
            self.enabled_extensions.append("SSE4")
        if(args.aes):
            self.enabled_extensions.append("AES")
        if(args.avxaes):
            self.enabled_extensions.append("AVXAES")
        if(args.bmi1):
            self.enabled_extensions.append("BMI1")
        if(args.bmi2):
            self.enabled_extensions.append("BMI2")
        if(args.cet):
            self.enabled_extensions.append("CET")
        if(args.clflushopt):
            self.enabled_extensions.append("CLFLUSHOPT")
        if(args.clwb):
            self.enabled_extensions.append("CLWB")
        if(args.invpcid):
            self.enabled_extensions.append("INVPCID")
        if(args.sse3):
            self.enabled_extensions.append("SSE3")
        if(args.sse4a):
            self.enabled_extensions.append("SSE4a")
        if(args.wbnoinvd):
            self.enabled_extensions.append("WBNOINVD")
        if(args.x87):
            self.enabled_extensions.append("X87")
        if(args.xsave):
            self.enabled_extensions.append("XSAVE")
        if(args.xsavec):
            # TODO: Support non-register operations before adding XSAVEC
            self.enabled_extensions.append("XSAVEC")
        if(args.xsaveopt):
            self.enabled_extensions.append("XSAVEOPT")
        if(args.xsaves):
            #TODO: support non-register operations before adding XSAVES
            self.enabled_extensions.append("XSAVES")
        print("[*] Enabled extensions: ", self.enabled_extensions)

    def extract_ise_instructions(self): 
        for instrNode in self.root_xml.iter("instruction"):
            extension = instrNode.attrib['extension']
            if(extension not in self.enabled_extensions):
                continue
            if(extension not in self.enabled_instructions.keys()):
                self.enabled_instructions[extension] = []

            supported_instruction_type = True
            for operandNode in instrNode.iter('operand'):
                if(operandNode.attrib['type'] != 'reg'):
                    supported_instruction_type = False
                    break
            if(supported_instruction_type):
                self.enabled_instructions[extension].append(instrNode)
        print("[*] Instruction set gathered for extensions:", self.enabled_instructions.keys())
        count = 0
        for extension in self.enabled_instructions.keys():
            count = count + len(self.enabled_instructions[extension])
        print("[*] Total ISA search space: ", count, " instructions")

    def construct_position_vector_map(self, particle_asm):
        position_vector = []
        particle_asm_lines = particle_asm.split("\n")
        for line in particle_asm_lines:
            if(line.find("ret") > -1 or
                    line.find("global") > -1 or
                    line.find("align") > -1 or
                    line.find("fuzz_instruction_extensions") > -1):
                continue
            
            line = line.strip()
            line = line.replace(",", "")
            line = line.split()
            position_vector_element = 0
            for index in range(len(line)):
                word = line[index]
                if(index == 0): # Handle opcode here
                    if(word not in self.position_map.keys()):
                        self.position_map[word] = self.position_map_index_counter
                        self.position_map_index_counter = self.position_map_index_counter + 1
                    position_vector_element = self.position_map[word]

                else:           # Handle operands here
                    re_match = re.search(r'\d+', word)
                    try:
                        register_num = int(re_match.group())
                        position_vector_element = (position_vector_element << 4) | register_num
                    except:
                        pass
            position_vector.append(position_vector_element)
        return position_vector

    def initialize_population(self):
        self.population
        POPULATION_SIZE = self.optimizer_config_dict["POPULATION_SIZE"] 
        for _ in range(POPULATION_SIZE):
            particle = Particle()
            particle_asm = particle.initialize_particle(self.enabled_extensions, self.enabled_instructions, self.num_instructions_to_fuzz) 
            position_vector = self.construct_position_vector_map(particle_asm)
            particle.set_position_vector(position_vector)
            particle.set_asm(particle_asm)
            self.population.append(particle)

    def initialize_monitored_events(self):
        events = open("msr.config").readlines()
        for event in events:
            event = event.strip()
            event = event.split(":")
            self.monitored_events.append((event[0], event[1]))
            if(event[0] not in self.equivalence_classes.keys()):
                equivalence_class_object = EquivalenceClass()
                equivalence_class_object.set_class_msr(event[0])
                equivalence_class_object.set_class_desc(event[1])
                self.equivalence_classes[event[1]] = equivalence_class_object
                print("[*] Initialized Equivalence class {desc} with MSR address {addr}".format(
                        desc=equivalence_class_object.get_class_desc(), addr=equivalence_class_object.get_class_msr()))
   
    def evaluate_particle_fitness_on_event(self, particle, event, event_desc):
        try: 
            output = subprocess.check_output("make clean", shell=True).decode()
            output = subprocess.check_output("sudo make all MSR_ADDR={arg_1} MSR_NAME={arg_2}".format(
                arg_1=event, arg_2=event_desc), shell=True).decode()
            return output
        except:
            # Most probably a SEGFAULT, redo this particle
            particle_asm = particle.initialize_particle(self.enabled_extensions, self.enabled_instructions, self.num_instructions_to_fuzz)
            position_vector = self.construct_position_vector_map(particle_asm)
            particle.set_position_vector(position_vector)
            particle.set_asm(particle_asm)
            pass

    def evaluate_population_fitness(self):
        for particle in self.population:
            with open("fuzz.S", "w") as f:
                f.write(particle.get_asm())
            for event in self.monitored_events:
                output = self.evaluate_particle_fitness_on_event(particle, event[0], event[1])
                if(output is not None and len(output) > 0):
                    output = output.strip()
                    output = output.split(":") 
                    equivalence_class = self.equivalence_classes[output[0]]
                    if(not equivalence_class.is_in_swarm(particle)):
                        equivalence_class.add_to_swarm(particle, int(output[1]))
                    else:
                        equivalence_class.update_event_count(particle, int(output[1]))

    def cognitive_phase(self):
        COGNITIVE_BETA =  self.optimizer_config_dict["COGNITIVE_BETA"]
        COGNITIVE_GAMMA = self.optimizer_config_dict["COGNITIVE_GAMMA"]
        for particle in self.population:
            particle_asm = particle.get_asm()
            particle_asm = particle_asm.split("\n")
            if(random.random() < COGNITIVE_BETA):
                mutation_index = None
                while(1):
                    mutation_index = random.randint(0, len(particle_asm) - 1)
                    instruction = particle_asm[mutation_index]
                    if(instruction.find("ret") > -1 or
                        instruction.find("global") > -1 or
                        instruction.find("align") > -1 or
                        instruction.find("fuzz_instruction_extensions") > -1):
                        continue
                    break
                
                replacement_instruction = particle.choose_replacement_instruction(self.enabled_extensions, self.enabled_instructions)
                particle_asm[mutation_index] = replacement_instruction
                particle_asm = "\n".join(particle_asm)
                with open("fuzz.S", "w") as f:
                    f.write(particle_asm)
                for event in self.monitored_events:
                    output = self.evaluate_particle_fitness_on_event(particle, event[0], event[1])
                    if(output is not None and len(output) > 0):
                        output = output.strip()
                        output = output.split(":")
                        equivalence_class = self.equivalence_classes[output[0]]
                        if(not equivalence_class.is_in_swarm(particle)):
                            # discovered a new event
                            print("[*] (Cognitive Exploration Phase) Discovered new event {desc}".
                                    format(desc=equivalence_class.get_class_desc()))
                            equivalence_class.add_to_swarm(particle, int(output[1]))
                        else:
                            # did we improve an already known event?
                            old_event_count = equivalence_class.get_event_count(particle)
                            if(int(output[1]) > old_event_count):
                                equivalence_class.update_event_count(particle, int(output[1]))
                                particle.set_asm(particle_asm)
                                position_vector = self.construct_position_vector_map(particle_asm)
                                particle.set_position_vector(position_vector)
                                print("[*] (Cognitive Exploration Phase) Improved particle in class {desc} from {old_count} to {new_count}".
                                        format(desc=equivalence_class.get_class_desc(),
                                               old_count = old_event_count,
                                               new_count = int(output[1])))


    def mixed_phase(self):
        swarm_leaders = {}
        for equivalence_class in self.equivalence_classes.keys():
            class_object = self.equivalence_classes[equivalence_class]
            swarm_leaders[class_object.get_class_desc()] = class_object.get_swarm_leader()

        MIXED_BETA =  self.optimizer_config_dict["MIXED_BETA"]
        MIXED_GAMMA = self.optimizer_config_dict["MIXED_GAMMA"]

        ############## Exploration with rate MIXED_BETA ##############################
        for particle in self.population:
            particle_asm = particle.get_asm()
            particle_asm = particle_asm.split("\n")
            if(random.random() < MIXED_BETA):
                mutation_index = None
                while(1):
                    mutation_index = random.randint(0, len(particle_asm) - 1)
                    instruction = particle_asm[mutation_index]
                    if(instruction.find("ret") > -1 or
                        instruction.find("global") > -1 or
                        instruction.find("align") > -1 or
                        instruction.find("fuzz_instruction_extensions") > -1):
                        continue
                    break
                
                replacement_instruction = particle.choose_replacement_instruction(self.enabled_extensions, self.enabled_instructions)
                particle_asm[mutation_index] = replacement_instruction
                particle_asm = "\n".join(particle_asm)
                with open("fuzz.S", "w") as f:
                    f.write(particle_asm)
                for event in self.monitored_events:
                    output = self.evaluate_particle_fitness_on_event(particle, event[0], event[1])
                    if(output is not None and len(output) > 0):
                        output = output.strip()
                        output = output.split(":")
                        equivalence_class = self.equivalence_classes[output[0]]
                        if(not equivalence_class.is_in_swarm(particle)):
                            # discovered a new event
                            print("[*] (Mixed Exploration Phase) Discovered new event {desc}".format(
                                desc=equivalence_class.get_class_desc()))
                            equivalence_class.add_to_swarm(particle, int(output[1]))
                        else:
                            # did we improve an already known event?
                            old_event_count = equivalence_class.get_event_count(particle)
                            if(int(output[1]) > old_event_count):
                                equivalence_class.update_event_count(particle, int(output[1]))
                                particle.set_asm(particle_asm)
                                position_vector = self.construct_position_vector_map(particle_asm)
                                particle.set_position_vector(position_vector)
                                print("[*] (Mixed Exploration Phase) Improved particle in class {desc} from {old_count} to {new_count}".
                                        format(desc=equivalence_class.get_class_desc(),
                                               old_count = old_event_count,
                                               new_count = int(output[1])))


        ############## Exploitation with rate MIXED_GAMMA ##############################       
        for equivalence_class in self.equivalence_classes.keys():
            equivalence_class_swarm = self.equivalence_classes[equivalence_class].get_swarm()
            if(len(equivalence_class_swarm) == 0):
                continue
            for swarm_member in equivalence_class_swarm:
                particle = swarm_member[0]
                if(random.random() < MIXED_GAMMA):
                    mutation_index = None
                    particle_asm = particle.get_asm()
                    particle_asm = particle_asm.split("\n")
                    while(1):
                        mutation_index = random.randint(0, len(particle_asm) - 1)
                        instruction = particle_asm[mutation_index]
                        if(instruction.find("ret") > -1 or
                                instruction.find("global") > -1 or
                                instruction.find("align") > -1 or
                                instruction.find("fuzz_instruction_extensions") > -1):
                            continue
                        break
     
                    replacement_instruction = swarm_leaders[self.equivalence_classes[equivalence_class].get_class_desc()][0].return_single_instruction()
                    particle_asm[mutation_index] = replacement_instruction
                    particle_asm = "\n".join(particle_asm)
                    with open("fuzz.S", "w") as f:
                        f.write(particle_asm)
                    for event in self.monitored_events:
                        output = self.evaluate_particle_fitness_on_event(particle, event[0], event[1])
                        if(output is not None and len(output) > 0):
                            output = output.strip()
                            output = output.split(":")
                            swarm_class = self.equivalence_classes[output[0]]
                            if(not swarm_class.is_in_swarm(particle)):
                                # discovered a new event
                                swarm_class.add_to_swarm(particle, int(output[1]))
                                print("[*] (Mixed Exploitation Phase) Discovered new event {desc}".format(
                                   desc=swarm_class.get_class_desc()))
                            else:
                                # did we improve an already known event?
                                old_event_count = swarm_class.get_event_count(particle)
                                if(int(output[1]) > old_event_count):
                                    swarm_class.update_event_count(particle, int(output[1]))
                                    particle.set_asm(particle_asm)
                                    position_vector = self.construct_position_vector_map(particle_asm)
                                    particle.set_position_vector(position_vector)
                                    print("[*] (Mixed Exploitation Phase) Improved particle in class {desc} from {old_count} to {new_count}".
                                            format(desc=swarm_class.get_class_desc(),
                                                old_count = old_event_count,
                                                new_count = int(output[1])))
                            
                            if(int(output[1]) > swarm_member[1]):
                                # Found new swarm leader
                                swarm_leaders[self.equivalence_classes[equivalence_class].get_class_desc()] = [particle, int(output[1])]

        ############## Dimensionality Reduction with rate MIXED_BETA ##############################
        for particle in self.population:
            particle_asm = particle.get_asm()
            particle_asm = particle_asm.split("\n")
            if(random.random() < MIXED_BETA):
                mutation_index = None
                while(1):
                    mutation_index = random.randint(0, len(particle_asm) - 1)
                    instruction = particle_asm[mutation_index]
                    if(instruction.find("ret") > -1 or
                        instruction.find("global") > -1 or
                        instruction.find("align") > -1 or
                        instruction.find("fuzz_instruction_extensions") > -1):
                        continue
                    break
                 
                del particle_asm[mutation_index]
                dimensionality = len(particle_asm)
                particle_asm = "\n".join(particle_asm)
                with open("fuzz.S", "w") as f:
                    f.write(particle_asm)
                for event in self.monitored_events:
                    output = self.evaluate_particle_fitness_on_event(particle, event[0], event[1])
                    if(output is not None and len(output) > 0):
                        output = output.strip()
                        output = output.split(":")
                        equivalence_class = self.equivalence_classes[output[0]]
                        if(not equivalence_class.is_in_swarm(particle)):
                            # discovered a new event
                            equivalence_class.add_to_swarm(particle, int(output[1]))
                        else:
                            # did we improve an already known event?
                            old_event_count = equivalence_class.get_event_count(particle)
                            if(int(output[1]) >= old_event_count):
                                equivalence_class.update_event_count(particle, int(output[1]))
                                particle.set_asm(particle_asm)
                                position_vector = self.construct_position_vector_map(particle_asm)
                                particle.set_position_vector(position_vector)
                                print("[*] (Mixed Exploitation Phase) Reduced particle dimension in class {desc} from {old_count} to {new_count}".
                                        format(desc=equivalence_class.get_class_desc(),
                                               old_count = dimensionality + 1,
                                               new_count =  dimensionality))

    def dump_asm(self):
        filename_index = 0
        for particle in self.population:
            for equivalence_class in self.equivalence_classes.keys():
                if(self.equivalence_classes[equivalence_class].is_in_swarm(particle)):
                    class_desc = self.equivalence_classes[equivalence_class].get_class_desc()
                    event_count = self.equivalence_classes[equivalence_class].get_event_count(particle)
                    with open("asm/{index}.S".format(index=filename_index), "w") as f:
                        f.write(";{desc}:{count}\n".format(desc=class_desc, count=event_count))
                        f.write(particle.get_asm())
                    filename_index = filename_index + 1


    def main_loop(self):
        self.parse_ise()
        self.num_instructions_to_fuzz = int(args.num_instructions)
        print("[*] Fuzzing a group of ", self.num_instructions_to_fuzz, " instructions" )
        self.parse_enabled_extensions()
        self.extract_ise_instructions()
        self.initialize_population()
        self.initialize_monitored_events()

        GENERATION = 0
        THRESHOLD = self.optimizer_config_dict["THRESHOLD"]
        self.evaluate_population_fitness()
        DUMP_ASM =  self.optimizer_config_dict["DUMP_ASM"]
        print("[*] Beginning with cognitive phase...")
        while(1):
            GENERATION = GENERATION + 1
            if(GENERATION == THRESHOLD):
                print("[*] Moving to mixed phase...")

            if(GENERATION < THRESHOLD):
                self.cognitive_phase()
            else:
                self.mixed_phase()

            if(GENERATION % DUMP_ASM == 0):
                print("[*] Dumping particle ASMs")
                self.dump_asm()


optimizer_config = open("optimizer.config").readlines()
optimizer_config_dict = {}
for config in optimizer_config:
    config = config.strip()
    config = config.split(":")
    if(config[0] == "POPULATION_SIZE" or 
            config[0] == "THRESHOLD" or
            config[0] == "DUMP_ASM"):

        optimizer_config_dict[config[0]] = int(config[1])
    else:
        optimizer_config_dict[config[0]] = float(config[1])

pso = Optimizer(optimizer_config_dict)
pso.main_loop()
