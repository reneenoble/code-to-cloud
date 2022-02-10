from flask import Flask, request, render_template

app = Flask('app')

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

    # http://192.168.1.122:8080/view?style=kids
    # http://192.168.1.122:8080/view?event=Bibi's+Bday&to=Clair&date=Monday+32nd+of+Mocktober&time=4pm&sender=Renee&style=cat
    

    template = "invite-" + style + ".html"
    

    return render_template(template, to=to, event_name=event, date=date, time=time, sender=sender)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=8080)