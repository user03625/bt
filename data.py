import os
from blockchain_parser.blockchain import Blockchain
import pandas as pd
import struct

col = ["version","prev","merkle","timestamp","utc","bits","nonce","difficulty","hash"]
df = pd.DataFrame(columns = col)

#df = pd.read_csv("data.csv")

blockchain =  Blockchain(os.path.expanduser('~/.bitcoin/blocks'))

index = 0

def decode_uint32(data):
    assert(len(data) == 4)
    return struct.unpack("<I", data)[0]



for block in blockchain.get_unordered_blocks():
    if index<480000:
        print("Skipping block number:{}".format(index))
        index+=1
        continue
    header = block.header
    df.loc[index] = [
            header.version,
            header.previous_block_hash,
            header.merkle_root,
            decode_uint32(header.hex[68:72]),
            header.timestamp,
            header.bits,
            header.nonce,
            header.difficulty,
            block.hash
        ]
    index+=1
    if index%10000==0:
        df.to_csv("data3.csv")
    print("Parsing block number:{}".format(index))

df.to_csv("data3.csv")
