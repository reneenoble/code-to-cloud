from sqlite3 import connect
from flask import Flask, request, render_template
import json, os

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

app = Flask('app')

local_path = "./data"

############################################################################################################
# Use dotenv when you want to run this locally and get your environement variables out of the .env file
############################################################################################################

# import dotenv
# from dotenv import load_dotenv
# load_dotenv(".env")
############################################################################################################


# Make Containter 
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
print(connect_str)
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Create a unique name for the container
container_name = "rsvps-live"

try:
    container_client = blob_service_client.create_container(container_name)
except ResourceExistsError:
    container_client = blob_service_client.get_container_client(container_name)



@app.route("/")
def form():
    return render_template("form.html")


@app.route("/view")
def view_invite():
    # to = "Sarah"
    # event = "Artemis' birthday party"
    # date = "February 10th"
    # time = "4am"
    # sender = "Jack"

    to = request.args.get("to")
    event = request.args.get("event")
    date = request.args.get("date")
    time = request.args.get("time")
    sender = request.args.get("sender")
    style = request.args.get('style')
    eventId = sender + "|" + event
  
    template = "invite-" + style + ".html"
    

    return render_template(template, to=to, event_name=event, date=date, time=time, sender=sender, eventId=eventId)

@app.route("/events")
def events():
    blob_list = container_client.list_blobs()

    blob_list = [b.name for b in blob_list]

    return render_template("events.html", event_list=blob_list)

@app.route("/event-rsvps/<event_file>")
def event_rsvps(event_file):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=event_file)
    attendees = str(blob_client.download_blob().readall(), "utf-8")
    attendees = attendees.split("\n")
    print(attendees)
    return render_template("event-rsvps.html", attendees=attendees)


@app.route("/rsvp", methods=('GET', 'POST'))
def rsvp():
    data = request.json
    event_data = data["ID"].split(",")
    attendee = event_data[0]
    event_ID = event_data[1]
    
    try:
        sync_blob(event_ID, attendee)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    except:
        return json.dumps({'success':True}), 400, {'ContentType':'application/json'}


def sync_blob(event_ID, attendee):
    filename = event_ID + ".txt"
    local_file = os.path.join(local_path, filename)
    print(local_file)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

    try:
        print("\nDownloading blob to \n\t" + local_file)

        # Get the data out of the file, split it into a list of people who have already RSVPed
        attendees = str(blob_client.download_blob().readall(), "utf-8")
        attendees = attendees.split("\n")

        if attendee not in attendees:
            attendees.append(attendee)
        
            # Make the local file
            with open(local_file, "w") as download_file:
                download_file.writelines("\n".join(attendees))

            # Push the local file to Azure blob
            with open(local_file, "rb") as data:
                blob_client.delete_blob()
                blob_client.upload_blob(data)
            print(f"File ({filename}) updated on blob.")

    # The blob wasn't there, oh no!
    except ResourceNotFoundError:
        # If the file doesn't exist, make a local file, conatining the single attendee from the request
        with open(local_file, "w") as f:
            f.write(attendee)

        # Write the file to Azure blob
        with open(local_file, "rb") as data:
            blob_client.upload_blob(data)
            print("New file uploaded to blob.")

    

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=8000)