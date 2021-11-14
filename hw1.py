import socket
import string
import hw1_utils
import os
import datetime
# import matplotlib.pyplot as plt
# import pdfminer
from pdfminer.high_level import extract_text
import glob


# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8888
DATA_MAX_SIZE = 4096


def check_if_photo_exists(path_photo):
    print("check_if_photo_exists for path: ", path_photo, "\n")
    return os.path.exists(path_photo)


# assume we got something like: ..../pdfs/
def get_all_files_rec(path):
    return glob.glob(path + '/**/*.pdf', recursive=True)


# gets a pdf file, filters the stopwords and returns a wordcloud photo
def photo_from_pdf(pdf_file_path, pdf_file_name):
    # convert pdf to string
    text = extract_text(pdf_file_path)
    text = text.split()
    file = open('stopwords.txt', 'r')

    stop_words_txt = [line.split('\n') for line in file.readlines()]
    stop_words = [item[0] for item in stop_words_txt]

    # filter the stopwords
    filtered_words = [word for word in text if word not in stop_words]
    result = ' '.join(filtered_words)

    # pic_name = "wordclouds_pics/" + pdf_file_path + ".png"
    pic_name = pdf_file_path[0:len(pdf_file_path) - 4] + ".png"
    print("pic_name: ", pic_name, "\n")
    result2 = hw1_utils.generate_wordcloud_to_file(result, pic_name)
    return result2

    # For showing a wordcloud
    # plt.figure(figsize=(10, 5))
    # plt.imshow(picture, interpolation="bilinear")
    # plt.axis('off')
    # # # plt.savefig(f'wordcloud.png', dpi=300)
    # plt.show()

if __name__ == "__main__":

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', SERVER_PORT))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(DATA_MAX_SIZE)
                    response_proto = 'HTTP/1.1'
                    landing_page_requested = False
                    specific_page_requested = False
                    photo_requested = False
                    # print("data is ", data)
                    if not data:
                        # in any other error, return status 500
                        response_status = '500'
                        response = str.encode(response_proto)
                        response += b' '
                        response += str.encode(response_status)
                        response += b' '
                        response += str.encode("EMPTY DATA\r\n")
                        conn.sendall(response)
                        break

                    # data2 = "<!DOCTYPE html><html><body><h1>My First Heading</h1><p>My first paragraph.</p></body></html>"
                    # with open ('test_server.txt', 'r') as f:
                    #     file_str = f.read()
                    #     my_str_as_bytes = str.encode(file_str)

                    # http_data = hw1_utils.decode_http(my_str_as_bytes)
                    http_data = hw1_utils.decode_http(data)

                    print("http_data: ", http_data, "\n")

                    host = http_data["Host"][1:]
                    # print("host: ", host, "\n")

                    request = http_data["Request"].split('\n')[0]
                    print("request: ", request, "\n")
                    URL = request.split(' ')[1]
                    # print("URL: ", URL, "\n")

                    # check if the request is GET type
                    # if not, return with status 501
                    request_name = request.split(' ')[0]
                    # print("request_name: ", request_name, "\n")

                    if request_name != 'GET':
                        response_status = '501'
                        response = str.encode(response_proto)
                        response += b' '
                        response += str.encode(response_status)
                        response += b' '
                        response += str.encode("INVALID REQUEST TYPE")
                        response += str.encode("\r\n")
                        conn.sendall(response)
                        break

                    str_local_host = "localhost:8888"
                    # str_local_host_postman = "localhost:8888"
                    # sub_url = URL
                    # print("URL[0:15]: ", URL[0:15], "\n")
                    # print("host: ", host, ";\n")
                    # print("str_local_host: ", str_local_host, "\n")

                    # if str_local_host != host:
                    if host != str_local_host:
                        # print("here")
                        response_status = '500'
                        response = str.encode(response_proto)
                        response += b' '
                        response += str.encode(response_status)
                        response += b' '
                        response += str.encode("INVALID URL\r\n")
                        conn.sendall(response)
                        # print("here")
                        break

                    # print("sub_url: ", URL, "\n")
                    print("str_local_host: ", str_local_host, "\n")

                    filename_path = request.split(' ')[1][1:]
                    # We have a valid url here:
                    # if sub_url == str_local_host:
                    if URL == "/":
                        # print("david")
                        landing_page_requested = True
                    elif URL.split('.')[-1] == "png":
                        print("photo_requested\n")
                        photo_requested = True
                        # search for photo
                        print("filename_path: ", filename_path, "\n")
                        exists = check_if_photo_exists(filename_path)
                        print("exists: ", exists, "\n")

                        if not exists:
                            # print("4044444444")
                            response_status = '404'
                            response = str.encode(response_proto)
                            response += b' '
                            response += str.encode(response_status)
                            response += b' '
                            response += str.encode("PHOTO NOT FOUND\r\n")
                            conn.sendall(response)
                            break

                    #     if exists return the photo:
                        # Build the response message:
                        response_status = '200'  # in case of success (valid) return status 200
                        response = str.encode(response_proto)
                        response += b' '
                        response += str.encode(response_status)
                        response += b' '
                        response += str.encode("OK\r\n")

                        # current_date = datetime.datetime.now()
                        # response_headers_date = current_date.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                        # response_headers_content_type = "image/png"
                        # # response_headers_content_len = ""
                        # response_headers = response_headers_date + " " + response_headers_content_type + "\n"
                        # response += str.encode(response_headers)
                        # response += b'\n '  # to separate headers from body

                        filename_path_updated_slash = filename_path.replace("/", "\\")
                        output = open(filename_path_updated_slash, 'rb')
                        response += output.read()

                        # response += str.encode(filename_path_updated_slash)
                        conn.sendall(response)
                        # output.close()
                        break
                    else:
                        specific_page_requested = True
                    print("here8")

                    # not need to check of it's localhost 8888 because it's defined already
                    # prefix_str = "GET localhost:"
                    # prefix_str += str(SERVER_PORT)
                    # pdfname_index = len(prefix_str)
                    # filename = request[pdfname_index+1:].split(' ')[0]

                    # print("filename: ", filename, "\n")
                    filepath = filename_path + ".pdf"
                    # print("filepath: ", filepath, "\n")
                    print("before if")
                    # if the request if for a wordcloud, check if file exists. if not return 404
                    if not landing_page_requested \
                            and not check_if_photo_exists(filepath):
                        # print("4044444444")
                        print("inside 404")
                        response_status = '404'
                        response = str.encode(response_proto)
                        response += b' '
                        response += str.encode(response_status)
                        response += b' '
                        response += str.encode("FILE NOT FOUND\r\n")
                        conn.sendall(response)
                        break

                    print("here0")

                    if specific_page_requested:
                        # Create the photo

                        print("here1")

                        print("specific_page_requested!")
                        print("filepath: ", filepath, "\n")
                        item = filepath[5:]
                        print("item/filepath[5:]: ", item, "\n")
                        picture = photo_from_pdf(filepath, item)
                        print("photo_from_pdf: ", picture, "\n")

                        print("here2")

                        # Create the wordcloud html page
                        wc_page_html_string = "<!DOCTYPE html> <html> <body>\n"
                        wc_page_html_string += "<h1>" + item + "</h1>"
                        # print("pics_names[i]: ", pics_names[i], "\n")
                        # pic_name = pics_names[i][0:len(pics_names[i]) - 4]
                        pic_name = filename_path
                        print("pic_name: ", pic_name, "\n")

                        wc_page_html_string += "<table><tr><td><img src = \"" + pic_name + ".png\"></td></tr> \n"

                        # Create the Go Back button
                        wc_page_html_string += "<tr><td><a href=\""
                        # for d in range(0, all_files_levels[i]):
                        #     wc_page_html_string += "..\\"
                        for d in range(0, filepath.count('\\')):
                            wc_page_html_string += "..\\"
                        print("here3")
                        # wc_page_html_string += "LandingPage.html\">Go back</a></td></tr>\n"
                        wc_page_html_string += "\">Go back</a></td></tr>\n"
                        wc_page_html_string += "</table></body> </html>\n"

                        # Insert the html string to an html file
                        item_name = "pdfs\\" + item + ".html"
                        desired_wc_page_html_file = item_name
                        f = open(item_name, 'w')
                        message = wc_page_html_string
                        f.write(message)
                        f.close()


                    # here comes the logic:
                    if landing_page_requested:
                        # Get all files for buttons in Landing Page
                        all_files_paths = get_all_files_rec("pdfs")
                        all_files_buttons = [item[5:] for item in all_files_paths]
                        all_files_levels = [item.count('\\') for item in all_files_paths]
                        pics_names = [item[item.rfind('\\') + 1:] for item in all_files_paths]

                        # Create Landing Page
                        landing_page_html_string = "<!DOCTYPE html> <html> <body>\n"
                        landing_page_html_string += "<h1>Landing Page</h1>\n"
                        landing_page_html_string += "<h5>Welcome to the landing page!</h5>\n"
                        landing_page_html_string += "<h5>Choose a .pdf file to generate a wordcloud from:</h5>\n"
                        landing_page_html_string += "<table>\n"

                        desired_wc_page_html_string = ""
                        i = 0
                        for item in all_files_buttons:
                            # # Create the photo
                            # picture = photo_from_pdf(all_files_paths[i], item)
                            #
                            # # Create the wordcloud html page
                            # wc_page_html_string = "<!DOCTYPE html> <html> <body>\n"
                            # wc_page_html_string += "<h1>" + item + "</h1>"
                            # # print("pics_names[i]: ", pics_names[i], "\n")
                            # pic_name = pics_names[i][0:len(pics_names[i]) - 4]
                            # wc_page_html_string += "<table><tr><td><img src = \"" + pic_name + ".png\"></td></tr> \n"
                            #
                            # # Create the Go Back button
                            # wc_page_html_string += "<tr><td><a href=\""
                            # for d in range(0, all_files_levels[i]):
                            #     wc_page_html_string += "..\\"
                            # # wc_page_html_string += "LandingPage.html\">Go back</a></td></tr>\n"
                            # wc_page_html_string += "\">Go back</a></td></tr>\n"
                            # wc_page_html_string += "</table></body> </html>\n"
                            #
                            # # Insert the html string to an html file
                            item_name = "pdfs\\" + item + ".html"
                            # f = open(item_name, 'w')
                            # message = wc_page_html_string
                            # f.write(message)
                            # f.close()

                            # print("filename: ", filename, "\n")
                            # print("all_files_paths[i]: ", all_files_paths[i], "\n")
                            filename_updated_slash = filename_path.replace("/", "\\")
                            # print("filename_updated_slash: ", filename_updated_slash, "\n")

                            # if not landing_page_requested \
                            #         and filename_updated_slash+".pdf" == "\\"+all_files_paths[i]:
                            #     # desired_wc_page_html_string = wc_page_html_string
                            #     desired_wc_page_html_file = item_name
                                # print("item_name: ", item_name, "\n")

                            # Add a link in the landing page
                            landing_page_html_string += "<tr><td><a href = \""
                            landing_page_html_string += item_name[0:len(item_name)-9] + "\">"
                            landing_page_html_string += item
                            landing_page_html_string += "</a> </td> </tr>\n"

                            i += 1
                        landing_page_html_string += "</table>\n"
                        landing_page_html_string += "</body> </html>"

                        f = open('LandingPage.html', 'w')
                        message1 = landing_page_html_string
                        f.write(message1)
                        f.close()

                    # Build the response message:
                    response_status = '200'  # in case of success (valid) return status 200
                    response = str.encode(response_proto)
                    response += b' '
                    response += str.encode(response_status)
                    response += b' '
                    response += str.encode("OK\r\n")

                    current_date = datetime.datetime.now()
                    response_headers_date = current_date.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                    response_headers_content_type = "text/html"
                    # response_headers_content_len = ""
                    response_headers = response_headers_date + " " + response_headers_content_type + "\n"
                    response += str.encode(response_headers)
                    response += b'\n '  # to separate headers from body

                    if landing_page_requested:
                        print("if")
                        output = open('LandingPage.html', 'rb')
                        # we can input the string right away
                        response += output.read()  # sending landing page
                        conn.sendall(response)
                        output.close()
                    else:
                        print("else")
                        output = open(desired_wc_page_html_file, 'rb')
                        response += output.read()  # sending landing page
                        conn.sendall(response)
                        output.close()

