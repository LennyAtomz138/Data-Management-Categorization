import textract, re, os

def extractDOCX(local_filepath):
    text = textract.process(local_filepath)
    text = text.decode('utf-8')
    text_array = re.split('\t|\n|\s',text)
    text_array = list(filter(None, text_array))
    os.remove(local_filepath)
    return text_array
