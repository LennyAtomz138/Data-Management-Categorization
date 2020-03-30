import textract

def extractDOCX(local_filepath):
    text = textract.process(local_filepath)
    #TODO perform text manips here to format the raw string into an array of words
    text_array = []
    print(text)
    return text_array
