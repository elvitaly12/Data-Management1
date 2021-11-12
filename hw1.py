import socket
import os
import string
import hw1_utils

import matplotlib.pyplot as plt
import pdfminer
from pdfminer.high_level import extract_text
import glob

# import webbrowser
import urllib


# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8888
DATA_MAX_SIZE = 4096


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
    pic_name = pdf_file_path + ".png"
    result2 = hw1_utils.generate_wordcloud_to_file(result, pic_name)
    return result2


if __name__ == "__main__":

    # Get all files for buttons in Landing Page
    all_files_paths = get_all_files_rec("pdfs")
    all_files_buttons = [item[5:] for item in all_files_paths]
    print(all_files_paths)

    all_files_levels = [item.count('\\') for item in all_files_paths]
    pics_names = [item[item.rfind('\\')+1:] for item in all_files_paths]
    # print(pics_names)

    # Create Landing Page
    landing_page_html_string = "<!DOCTYPE html> <html> <body>\n"
    landing_page_html_string += "<h1>Landing Page</h1>\n"
    landing_page_html_string += "<h5>Welcome to the landing page!</h5>\n"
    landing_page_html_string += "<h5>Choose a .pdf file to generate a wordcloud from:</h5>\n"
    landing_page_html_string += "<table>\n"

    i = 0
    for item in all_files_buttons:
        # Create the photo
        picture = photo_from_pdf(all_files_paths[i], item)

        # Create the wordcloud html page
        wc_page_html_string = "<!DOCTYPE html> <html> <body>\n"
        wc_page_html_string += "<h1>" + item + "</h1>"
        wc_page_html_string += "<table><tr><td><img src = \"" + pics_names[i] + ".png\"></td></tr> \n"
        # wc_page_html_string += "<tr><td><button type=\"button\" onclick=\"location.href='../LandingPage.html'\">Go back</button></td></tr>\n"
        # wc_page_html_string += "<tr><td><a href=\"~\LandingPage.html\">Go back</a></td></tr>\n"

        # Create the Go Back button
        wc_page_html_string += "<tr><td><a href=\""
        for d in range(0, all_files_levels[i]):
            wc_page_html_string += "..\\"
        wc_page_html_string += "LandingPage.html\">Go back</a></td></tr>\n"
        wc_page_html_string += "</table></body> </html>\n"

        # Insert the html string to an html file
        item_name = "pdfs\\" + item + ".html"
        f = open(item_name, 'w')
        message = wc_page_html_string
        f.write(message)
        f.close()

        # landing_page_html_string += "<tr> <td> <button onclick = \"location.href='"
        # landing_page_html_string += "wordclouds_htmls/"
        # landing_page_html_string += item + ".html'\" " \
        # landing_page_html_string += item_name + "'\" "
        # landing_page_html_string += "type = \"button\">"
        # landing_page_html_string += item
        # landing_page_html_string += "</button> </td> </tr>\n"

        # Add a link in the landing page
        landing_page_html_string += "<tr><td><a href = \""
        landing_page_html_string += item_name + "\">"
        landing_page_html_string += item
        landing_page_html_string += "</a> </td> </tr>\n"

        i += 1
    landing_page_html_string += "</table>\n"
    landing_page_html_string += "</body> </html>"

    f = open('LandingPage.html', 'w')
    message1 = landing_page_html_string
    f.write(message1)
    f.close()

    # For showing a wordcloud
    # plt.figure(figsize=(10, 5))
    # plt.imshow(picture, interpolation="bilinear")
    # plt.axis('off')
    # # # plt.savefig(f'wordcloud.png', dpi=300)
    #
    # plt.show()

    # page = urllib.urlopen("wordcloud.html").read()
    # print(page)

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

