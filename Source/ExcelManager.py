
from Source import FileHandle, CLIMenu
from openpyxl import Workbook, load_workbook

def ExcelMenu(text_dictionary = {}):
    print("=" * 8, "Excel Manager", "=" * 8)
    while True:
        print("1 - Test Excel Tagging")
        print("2 - Test Excel Loading")
        print("0 - Quit to Main Menu\n")
        print("Current Dictionary Contents: ", text_dictionary)
        ok_to_exit = int(input("Enter Number: "))
        if ok_to_exit < 0 or ok_to_exit > 2:
            print("Invalid input: Please try again.")
            raise ValueError
        elif ok_to_exit == 0:
            print("\n")
            CLIMenu.MainMenu()
        elif ok_to_exit == 1:
            TestExcelTagging(text_dictionary)
        elif ok_to_exit == 2:
            TestExcelLoading()

def ExcelFileSelection():
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

#    file = FileHandle.FileHandle(CLIMenu.selected_filename)
#    print(file.fileName)
#    print(file.fileType)

    # Test files

    file1 = FileHandle.FileHandle("Planes.pdf")
    file2 = FileHandle.FileHandle("Trains.jpg")
    file3 = FileHandle.FileHandle("Automobiles.docx")

    file1.addtag("aviation")
    file1.addtag("documentation")

    file2.addtag("locomotive")
    file2.addtag("promotional")

    file3.addtag("automotive")
    file3.addtag("image")

    # List of all files to add to Excel doc

    files = [file1, file2, file3]

    # Set up Excel Doc

    outputbook = Workbook()
    worksheet = outputbook.active
    worksheet['A1'] = "File Name"
    worksheet['B1'] = "File Type"
    worksheet['C1'] = "File Tag 1"
    worksheet['D1'] = "File Tag 2"

    # Add the file names, types, and tags to the sheet

    fileCount = 2
    for file in files:
        worksheet.cell(row=fileCount, column=1, value=file.fileName)
        worksheet.cell(row=fileCount, column=2, value=file.fileType)
        tagCol = 3
        for tag in file.tags:
            worksheet.cell(row=fileCount, column=tagCol, value=tag)
            tagCol += 1
        fileCount += 1

    # Save the doc
    outputbook.save('DCMT_Results.xlsx')


def TestExcelLoading():
    print("=" * 8, "Excel Loading Test", "=" * 8)

    # Path can also be a path to a excel file location.
    path = 'DCMT_Results.xlsx'

    wb = load_workbook(path)
    ws = wb.active

    for i in range(1, ws.max_row + 1):
        for j in range(1, ws.max_column + 1):
            c = ws.cell(row = i, column = j)

            # A check that only exists because not all the headers are labelled.
            if c.value is None:
                break

            print(c.value.center(15), end=" ")
        print('\n')
