# Paste your version of miner.py from the clinet_mining_p
# folder here
import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof 

def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """

    print("Start work on a new proof")
    proof = 4

    # for block 1, hash(1, p) = 000000x

    while not valid_proof(last_proof, proof) :
        proof += 1
    print("Attempting to mine")
    return proof

def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """
    # build string to hash
    guess = f'{last_proof}{proof}'.encode()
    # use hash function
    guess_hash = hashlib.sha256(guess).hexdigest()
    #check if 6 leading 0's in hash result
    solution = guess_hash[0:5] # [:6]
    if solution == "00000":
        return True
    else:
        return False

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        last_proof = requests.get(url = node+'/last_proof').json()['proof']
        print("Mining started!")

        new_proof = proof_of_work(last_proof)
        print(new_proof, last_proof)

        # TODO: When found, POST it to the server {"proof": new_proof}
        proof_data = {'proof': new_proof}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        #sending post request and saving response as response obj
        res = requests.post(url = node+'/mine', json = proof_data)

        # TODO: If the server responds with 'New Block Forged'
        if res.json()['message'] == "New Block Forged First":
            # add 1 to the number of coins mined and print it.  Otherwise,
            coins_mined += 1
            print("You have: " + str(coins_mined) + " coins", f'miner 2 won the block {proof_data}')

            res.json()['message'] = "New Block Was Forged Before You"


        elif res.json()['message'] == "New Block Was Forged Before You":
            last_proof = requests.get(url = node+'/last_proof').json()['proof']
            previous_hash = requests.get(url = node+'/last_proof').json()['previous_hash']

            if valid_proof(previous_hash, last_proof) == False:
                print('No Good, try again!')




        # print the message from the server.
        print(res.json()['message'])
