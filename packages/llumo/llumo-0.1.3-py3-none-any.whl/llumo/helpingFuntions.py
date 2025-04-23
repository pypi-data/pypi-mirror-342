import time
import uuid

def getProcessID():
    return f"{int(time.time() * 1000)}{uuid.uuid4()}"


def getInputPopulatedPrompt(promptTemplate, tempObj):
    for key, value in tempObj.items():
        promptTemplate = promptTemplate.replace(f"{{{{{key}}}}}", value)
    return promptTemplate



import time
import uuid

def getProcessID():
    return f"{int(time.time() * 1000)}{uuid.uuid4()}"


def getInputPopulatedPrompt(promptTemplate, tempObj):
    for key, value in tempObj.items():
        promptTemplate = promptTemplate.replace(f"{{{{{key}}}}}", value)
    return promptTemplate

def costColumnMapping(costResults,allProcess):
    # this dict will store cost column data for each row
    cost_cols = {}
    compressed_prompt = []
    compressed_prompt_output = []
    cost = []
    cost_saving = []
    print("BATCHES: ",allProcess)
    print("COST RESULTS :", costResults)
    # iterate through each batch
    for record in allProcess:
        cost_cols[record] = []
        # iterate through each record of cost saving results received from the api
        for item in costResults:
            # fetching all cost column data for a specific row. i.e each row will have 4 columns
            if list(item.keys())[0].split("-")[0] == record.split("-")[0]:
                cost_cols[record].append(list(item.values())[0])

    for ky, val in cost_cols.items():
        # compressed prompt column
        compressed_prompt.append(val[0])
        # compressed output
        compressed_prompt_output.append(val[1])
        # cost
        cost.append(val[2])
        # cost saved
        cost_saving.append(val[3])

    return compressed_prompt , compressed_prompt_output  , cost , cost_saving





