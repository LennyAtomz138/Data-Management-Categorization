
from Source import FileHandle, CLIMenu
from openpyxl import Workbook, load_workbook

memoryFileName = 'DCMT_Results.xlsx'
entryCount = 0
workbook = Workbook()

def Main(text_dictionary = {}):
    ExcelInitialization()
    while True:
        print("=" * 8, "Excel Manager", "=" * 8)
        print("1 - Test Excel Tagging")
        print("2 - Print Excel Contents")
        print("3 - Reset Excel Sheet")
        print("0 - Quit to Main Menu\n")
        print("Current Dictionary Contents: \n", text_dictionary)
        ok_to_exit = int(input("Enter Number: "))
        if ok_to_exit < 0 or ok_to_exit > 3:
            print("Invalid input: Please try again.")
            continue
        elif ok_to_exit == 0:
            print("\n")
            return
        elif ok_to_exit == 1:
            TestExcelTagging(text_dictionary)
        elif ok_to_exit == 2:
            PrintContents()
        elif ok_to_exit == 3:
            ExcelReset()

def KeywordSelection(text_dictionary = {}):
    pass

def ExcelInitialization():
    global workbook
    try:
        #tries opening Excel memory file
        workbook = load_workbook(memoryFileName)
        activeWorkbook = workbook.active
        print(memoryFileName, " has been loaded\n")
    except:
        #if it doesn't work, it creates the workbook
        workbook = Workbook()
        activeWorkbook = workbook.active
        activeWorkbook['A1'] = "FILE_NAME"
        activeWorkbook['B1'] = "FILE_TYPE"
        activeWorkbook['C1'] = "BUCKET_LOCATION"
        activeWorkbook['D1'] = "FILE_TAG_1"
        activeWorkbook['E1'] = "FILE_TAG_2"
        activeWorkbook['F1'] = "FILE_TAG_3"
        activeWorkbook['G1'] = "FILE_TAG_4"
        activeWorkbook['H1'] = "FILE_TAG_5"
        workbook.save(memoryFileName)
        print(memoryFileName, " has been created\n")
    finally:
        global entryCount
        entryCount = activeWorkbook.max_row - 1
        print("Entry count is ", entryCount)

def ExcelReset():
    print("=" * 8, "Excel Reset", "=" * 8)
    while True:
        print("Would you like to reset the contents of the Excel sheet?")
        print("1 - Yes")
        print("0 - No\n")
        ok_to_exit = int(input("Enter Number: "))
        if ok_to_exit < 0 or ok_to_exit > 1:
            print("Invalid input: Please try again.")
            continue
        elif ok_to_exit == 0:
            print("\n")
            return
        elif ok_to_exit == 1:
            while True:
                print("Are you sure?")
                print("1 - Confirm")
                print("0 - Cancel\n")
                ok_to_confirm = int(input("Enter Number: "))
                if ok_to_confirm < 0 or ok_to_confirm > 1:
                    print("Invalid input: Please try again.")
                    continue
                elif ok_to_confirm == 0:
                    print("\n")
                    return
                elif ok_to_confirm == 1:
                    global workbook
                    workbook = Workbook()
                    activeWorkbook = workbook.active
                    activeWorkbook['A1'] = "FILE_NAME"
                    activeWorkbook['B1'] = "FILE_TYPE"
                    activeWorkbook['C1'] = "BUCKET_LOCATION"
                    activeWorkbook['D1'] = "FILE_TAG_1"
                    activeWorkbook['E1'] = "FILE_TAG_2"
                    activeWorkbook['F1'] = "FILE_TAG_3"
                    activeWorkbook['G1'] = "FILE_TAG_4"
                    activeWorkbook['H1'] = "FILE_TAG_5"
                    workbook.save(memoryFileName)
                    return
        elif ok_to_exit == 2:
            PrintContents()
            return

def AddEntry(text_dictionary = {}):
    pass



def TestExcelTagging(text_dictionary = {}):
    #does not work if the Excel file is opened
    """
    Proof of concept function for outputting tagged files into an Excel Document
    3 Test Documents (with pre-defined tags) used for testing
    Output document saved to the Source directory at the moment
    :return:
    """
    print("=" * 8, "Excel Tagging Test", "=" * 8)

    #file = FileHandle.FileHandle(CLIMenu.selected_filename)
    #print(file.file_name)
    #print(file.file_type)

    # Test files

    file1 = FileHandle.FileHandle("Planes.pdf")
    file2 = FileHandle.FileHandle("Trains.jpg")
    file3 = FileHandle.FileHandle("Automobiles.docx")

    file1.add_tag("aviation")
    file1.add_tag("documentation")

    file2.add_tag("locomotive")
    file2.add_tag("promotional")

    file3.add_tag("automotive")
    file3.add_tag("image")

    # List of all files to add to Excel doc

    files = [file1, file2, file3]

    # Set up Excel Doc

    outputbook = Workbook()
    worksheet = outputbook.active
    worksheet['A1'] = "File Name"
    worksheet['B1'] = "File Type"
    worksheet['C1'] = "Bucket Location"
    worksheet['D1'] = "File Tag 1"
    worksheet['E1'] = "File Tag 2"
    worksheet['F1'] = "File Tag 3"
    worksheet['G1'] = "File Tag 4"
    worksheet['H1'] = "File Tag 5"

    # Add the file names, types, and tags to the sheet

    fileCount = 2
    for file in files:
        worksheet.cell(row=fileCount, column=1, value=file.file_name)
        worksheet.cell(row=fileCount, column=2, value=file.file_type)
        tagCol = 3
        for tag in file.tags:
            worksheet.cell(row=fileCount, column=tagCol, value=tag)
            tagCol += 1
        fileCount += 1

    # Save the doc
    outputbook.save('DCMT_Results.xlsx')
    global entryCount
    entryCount = entryCount + 1


def PrintContents():
    print("=" * 8, "Excel Printed Contents", "=" * 8)
    activeWorkbook = workbook.active

    for i in range(1, activeWorkbook.max_row + 1):
        for j in range(1, 9):
            c = activeWorkbook.cell(row = i, column = j)

            # A check that only exists because not all the headers are labelled.
            if c.value is None:
                break

            print(c.value.center(15), end=" ")
        print('\n')
