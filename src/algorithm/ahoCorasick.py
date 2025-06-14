def buildAhoCorasickMachine(keywords: list[str]) -> list:
    machine = [{'children': {}, 'output': [], 'fail': 0}]
    
    for keyword in keywords:
        nodeIndex = 0
        for char in keyword:
            currentNode = machine[nodeIndex]
            if char not in currentNode['children']:
                newNodeIndex = len(machine)
                currentNode['children'][char] = newNodeIndex
                machine.append({'children': {}, 'output': [], 'fail': 0})
                nodeIndex = newNodeIndex
            else:
                nodeIndex = currentNode['children'][char]
        machine[nodeIndex]['output'].append(keyword)

    queue = []
    for char, nodeIndex in machine[0]['children'].items():
        queue.append(nodeIndex)
        machine[nodeIndex]['fail'] = 0

    head = 0
    while head < len(queue):
        nodeIndex = queue[head]
        head += 1
        
        currentNode = machine[nodeIndex]
        for char, nextNodeIndex in currentNode['children'].items():
            queue.append(nextNodeIndex)
            
            failIndex = machine[nodeIndex]['fail']
            
            while char not in machine[failIndex]['children'] and failIndex != 0:
                failIndex = machine[failIndex]['fail']
            
            if char in machine[failIndex]['children']:
                newFailIndex = machine[failIndex]['children'][char]
                machine[nextNodeIndex]['fail'] = newFailIndex
            else:
                machine[nextNodeIndex]['fail'] = 0
            
            finalFailIndex = machine[nextNodeIndex]['fail']
            if machine[finalFailIndex]['output']:
                machine[nextNodeIndex]['output'].extend(machine[finalFailIndex]['output'])
            
    return machine

def ahoCorasickMatch(text: str, keywords: list[str]) -> dict:
    machine = buildAhoCorasickMachine(keywords)
    
    result = {}
    nodeIndex = 0

    for i, char in enumerate(text.lower()):
        while char not in machine[nodeIndex]['children'] and nodeIndex != 0:
            nodeIndex = machine[nodeIndex]['fail']
        
        if char in machine[nodeIndex]['children']:
            nodeIndex = machine[nodeIndex]['children'][char]
        
        if machine[nodeIndex]['output']:
            for keyword in machine[nodeIndex]['output']:
                if keyword not in result:
                    result[keyword] = []
                result[keyword].append(i)
                
    return result


# contohTeks = "ushers measured his shekels"
# daftarKataKunci = ["he", "she", "his", "hers"]

# hasilPencarian = ahoCorasickMatch(contohTeks, daftarKataKunci)

# print(f"Teks: '{contohTeks}'")
# print("Hasil Pencarian Aho-Corasick:")
# import json
# print(json.dumps(hasilPencarian, indent=2))