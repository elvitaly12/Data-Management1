
import glob

# from pdfminer.high_level import extract_text
from pdfminer.high_level import extract_text
from wordcloud import WordCloud

'''
This function generates a word cloud from a string, and saves it as a .png file.

input: text - a string to generate a word cloud from, filename - a string with the file's path. The string must end with ".png".
'''


def generate_wordcloud_to_file(text, filename):
    if not filename.endswith('.png'):
        raise Exception('Invalid filename parameter: '
                        'This function should only be used to create .png files. '
                        'Please use a filename that ends with ".png"')
    wc = WordCloud().generate(text)
    wc.to_file(filename)

    return wc

'''
This function parses a raw (bytes) HTTP request.
Each header as a corresponding key with the same name.
The first request line (e.g. "GET www.google.com ....") key is 'Request'

input: HTTP raw request, in bytes.
output: A dictionary of the parsed request 
'''


def decode_http(http_data):
    http_dict = {}
    fields = http_data.decode('utf-8').split("\r\n")  # convert to string from bytes
    http_dict['Request'] = fields[0]
    fields = fields[1:]
    for field in fields:  # go over the fields
        if not field:
            continue
        key, value = field.split(':', 1)  # split each line by http field name and value
        http_dict[key] = value
    return http_dict


# assume we got something like: ..../pdfs/
def get_all_files_rec(path):
    return glob.glob(path + '/**/*.pdf', recursive=True)

# gets a pdf file, filters the stopwords and returns a wordcloud photo
def photoFromPDF(pdf_file_path):
    # convert pdf to string
    text = extract_text(pdf_file_path)
    text = text.split()
    # print(text)
    file = open('stopwords.txt', 'r')
    stop_words_txt = [line.split('\n') for line in file.readlines()]
    # print(stop_words.dtype)
    stop_words = [item[0] for item in stop_words_txt]
    # print(stop_words)
    # filter the stopwords
    filtered_words = [word for word in text if word not in stop_words]
    # print(filtered_words)
    result = ' '.join(filtered_words)
    result2 = generate_wordcloud_to_file(result, 'ofir_image.png')

    return result2