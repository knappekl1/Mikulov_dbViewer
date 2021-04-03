import PySimpleGUI as sg
import ViewDb

dataDict = ViewDb.getDbData()
lastDbDate = dataDict["maxDate"][0][0].strftime("%d.%m.%Y")
# Start up screen
# Define the window's contents
layout = [[sg.Text("Spotřeba Mikulov", font=1, size=(100,1), border_width=15)],
            [sg.Text("Poslední měřené datum: " + lastDbDate,size=(100,1), border_width=15)],
          [sg.Button('Update', auto_size_button=False, size=(15,2)), sg.Button('Show Data', auto_size_button=False, size=(15,2)), sg.Button('Quit', auto_size_button=False, size=(15,2))]]


# Create the window
window = sg.Window('Window Title', layout, finalize=True)
window.Size = (400,230)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    elif event == "Show Data":
        myData = ViewDb.ProcessData(dataDict["result"])
        ViewDb.PlotDbData(myData[0], myData[1], myData[2])
        continue
    else:
        continue
    # Finish up by removing from the screen
    window.close()