import os
import lib

if __name__ == '__main__':
    client = lib.FileClient('localhost:8888')

    links = []
    links.append('./serverFiles/photos/1.png')
    links.append('./serverFiles/photos/2.png')
    links.append('./serverFiles/photos/3.png')
    links.append('./serverFiles/photos/un.rc')

    # demo for file uploading
    for link in links:
        in_file_name = link
        client.upload(in_file_name)

        # demo for file downloading:
        out_file_name = 'clientFiles' + link[20:] 
        if os.path.exists(out_file_name):
            os.remove(out_file_name)
        client.download('whatever_name', out_file_name)
        os.system(f'sha1sum {in_file_name}')
        os.system(f'sha1sum {out_file_name}')
