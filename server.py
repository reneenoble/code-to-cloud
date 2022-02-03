from flask import Flask, request, render_template

invite_app = Flask('app')

@invite_app.route("/view")
def view_invite():
    to = "Sarah"
    event = "Artermis' birthday party"
    date = "February 10th"
    time = "4am"
    sender = "Jack"

    template = "invite-kids.html"
    return render_template(template, to=to, event_name=event, date=date, time=time, sender=sender)

if __name__ == '__main__':
    invite_app.run(debug=True, use_reloader=True, host='0.0.0.0', port=8080)