import sys
import os
# sys.path.append('..')
from Files import lib
import json

CLIENT_DIR = "TransferredFiles/"

if __name__ == '__main__':
    client = lib.FileClient('localhost:8888')

    print("File receiving initiated")


    # in_file_name = "transfer1.json"
    # client.upload(in_file_name)

    # # demo for file downloading:
    # out_file_name = "transfer1.json"
    # if os.path.exists(out_file_name):
    #     os.remove(out_file_name)
    # client.download('whatever_name', out_file_name)

    links = []

    with open("transfer1.json", "r") as f:
        content = json.load(f)

    for index1 in content :
        tempString = content[index1]['file']
        # print(tempString)
        links.append(tempString)

        tempTokens = tempString.split('/')
        tempToken = tempTokens[len(tempTokens)-1]
        content[index1]['file'] =  CLIENT_DIR + tempToken

    with open("transfer2.json", "w") as f :
        json.dump(content, f, indent = 4)


    # demo for file uploading
    for link in links:
        print (link)
        filename = link.split('/')
        filename = filename[len(filename)-1]
        print(f"Receiving file {filename}")

        print(filename)

        in_file_name = link
        client.upload(in_file_name)

        # demo for file downloading:
        out_file_name = CLIENT_DIR + filename 
        if os.path.exists(out_file_name):
            os.remove(out_file_name)
        client.download('whatever_name', out_file_name)
        print(f"Received file saved as {filename}")

    print ('All files received successfully')
