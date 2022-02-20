from flask import Flask, request, render_template
import json, os
# import dotenv
# from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

app = Flask('app')

local_path = "./data"

# from dotenv import load_dotenv
# load_dotenv(".env")


# # Make Containter 
# connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
# blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# # Create a unique name for the container
# container_name = "rsvps"
# container_client = blob_service_client.create_container(container_name)


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


    # http://192.168.1.122:8080/view?style=kids
    # http://192.168.1.122:8080/view?event=Bibi's+Bday&to=Clair&date=Monday+32nd+of+Mocktober&time=4pm&sender=Renee&style=cat
    

    template = "invite-" + style + ".html"
    

    return render_template(template, to=to, event_name=event, date=date, time=time, sender=sender, eventId=eventId)


@app.route("/rsvp", methods=('GET', 'POST'))
def rsvp():
    data = request.json
    event_data = data["ID"].split(",")
    attendee = event_data[0]
    event_ID = event_data[1]
    filename = event_ID + ".txt"

    filepath = os.path.join(local_path, filename)

    with open(filepath ,"w") as f:
        f.write(attendee)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=8080)