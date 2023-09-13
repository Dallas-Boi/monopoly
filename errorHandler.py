# Made December 15th, 2022
# This handles the errors
import requests
import time

send_data = False

# This is the logging system for handling errors
def write_to_log(log, error = False, line = None):
    logs = open('logs.txt', 'wx')
    if error == False:
        logs.write('Playing: '+log)
    else:
        logs.write('[ERROR]: '+log+' | On Line: '+str(line))
    logs.close()
        
# Sends the data to a google form to submit to a google sheet
def send_monopoly_error(error, file, line, detail_error):
    """It takes google form url which is to be submitted and also 
    data which is a list of data to be submitted in the form iteratively.
    """
    # URL and Data that needs to be sent
    url = f'https://docs.google.com/forms/d/e/1FAIpQLSfLojHkqp79lK23U9wNj8QJMnDshbjvTOmeTJseMAMl8AintA/formResponse'
    form_data = {
        "entry.1582206937": "Bug",
        "entry.2140253851": "Monopoly",
        "entry.1775379057": "SERIOUS (IT BROKE THE GAME)",
        "entry.1129911072": f'(Error System) {file} on {line}',
        "entry.2009660152": f'{error}: {detail_error}',
        "draftResponse":'[]',
        "fvv": 1,
        "pageHistory":'0,1',
        "fbzx": 7179439377727532186
    }
    print(form_data)
    # User Agent so that it doesn't think its a bot
    if send_data == True:
        try:
            sent_form = requests.post(url, data=form_data)
            print("Error Reported, Please Continue")
            time.sleep(2)
        except Exception as e:
            print("Error Occured! With sending a Report!\nPLEASE REPORT ASAP TO Developer!!!")
    else:
        print(f'In {file} on {line} occured {error}: {detail_error}')