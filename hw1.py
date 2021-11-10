import socket
import os
import string
import hw1_utils
import matplotlib.pyplot as plt
#from pdfminer import high_level

# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8888
DATA_MAX_SIZE = 4096


if __name__ == "__main__":

    picture = hw1_utils.photoFromPDF('pdfs/test.pdf')
    # print(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(picture, interpolation="bilinear")
    plt.axis('off')

    plt.savefig(f'wordcloud.png',
                dpi=300)
    plt.show()

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', SERVER_PORT))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(DATA_MAX_SIZE)
                    print("data is ", data)
                    if not data:
                        # in any other error, return status 500
                        print('status 500')
                        break

                    data2 = "<!DOCTYPE html><html><body><h1>My First Heading</h1><p>My first paragraph.</p></body></html>"

                    # # with open ('test_server.txt', 'r') as f:
                    # #     file_str = f.read()
                    # #     my_str_as_bytes = str.encode(file_str)
                    #
                    # # http_data = hw1_utils.decode_http(my_str_as_bytes)
                    # http_data = hw1_utils.decode_http(data)
                    # request = http_data["Request"].split('\n')[0]
                    # URL = request[1]
                    #
                    # # check if the request is GET type
                    # # if not, return with status 501
                    # request_name =  URL.split(' ')[0]
                    # if request_name!='GET':
                    #     print('STATUS 501')
                    #
                    #
                    # # not need to check of it's localhost 8888 because it's defined already
                    #
                    # prefix_str = "GET localhost:"
                    # prefix_str += str(SERVER_PORT)
                    # pdfname_index = len(prefix_str)
                    # filename = request[pdfname_index+1:]
                    #
                    # # check if file exists, if not return 404
                    #
                    # # in case of success (valid) return status 200

                    conn.sendall(data2.encode())   ## NEED TO CHANGE ENCODE
                    #s.close()  MAYBE NEED TO ADD

