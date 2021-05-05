import os
import lib

if __name__ == '__main__':
    client = lib.FileClient('localhost:8888')

    links = []
    links.append('./serverFiles/1.png')
    # links.append('./serverFiles/2.png')
    links.append('./serverFiles/input1.txt')
    links.append('./serverFiles/run.c')

    # demo for file uploading
    for link in links:
        in_file_name = link
        client.upload(in_file_name)

        # demo for file downloading:
        out_file_name = 'clientFiles/' + link[14:] 
        if os.path.exists(out_file_name):
            os.remove(out_file_name)
        client.download('whatever_name', out_file_name)
        os.system(f'sha1sum {in_file_name}')
        os.system(f'sha1sum {out_file_name}')
