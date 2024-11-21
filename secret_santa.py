import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

participants = {
    "Will": {
        "email": "test@gmail.com",
        "previous_secret_santa": ["Wesley", "Whitt", "Winona", "Navy"] 
    },
    "Wesley": {
        "email": "test@gmail.com",
        "previous_secret_santa": ["Will",  "Whitt", "Winona"]
    },
    "Whitt": {
        "email": "test@gmail.com",
        "previous_secret_santa": ["Wesley", "Will", "Winona", "Beau"]
    },
    "Winona": {
        "email": "test@gmail.com",
        "previous_secret_santa": ["Will",  "Whitt", "Wesley", "Lucy"]
    },
    "Gabrieller": {
        "email": "test@gmail.com",
        "previous_secret_santa": ["Brody", "Beau", "Whitt"]
    },
    "Brody": {
        "email": "test@gmail.com",
        "previous_secret_santa": ["Gabrieller", "Beau", "Nancy"]
    },
    "Beau": {
        "email": "test@gmail.com",
        "previous_secret_santa": ["Gabrieller", "Brody", "Connor"]
    },
    "Amanda": {
        "email": "test@yahoo.com",
        "previous_secret_santa": ["Lucy", "Novena", "Will"]
    },
    "Lucy": {
        "email": "test@yahoo.com",
        "previous_secret_santa": ["Amanda", "Novena", "Cash"]
    },
    "Novena": {
        "email": "test@yahoo.com",
        "previous_secret_santa": ["Amanda", "Lucy", "Gabrieller"]
    },
    "Connor": {
        "email": "test@gmail.com",
        "previous_secret_santa": ["Nancy", "Navy", "Cash", "Wesley"]
    },
    "Nancy": {
        "email": "test@gmail.com",
        "previous_secret_santa": ["Connor", "Navy", "Cash", "Novena"]
    },
    "Navy": {
        "email": "test@gmail.com",
        "previous_secret_santa": ["Connor", "Nancy", "Cash", "Amanda"]
    },
    "Cash": {
        "email": "test@gmail.com",
        "previous_secret_santa": ["Connor", "Nancy", "Navy", "Brody"]
    }
}
def assign_secret_santa(participants):
    names = list(participants.keys())
    assignments = {}
    # keep looping and shuffling until we get a valid assignment
    while True:
        random.shuffle(names)
        can_assign = True
        for i, name in enumerate(participants):
            assignee = names[i]
            
            print(f"Checking if {name} can be assigned to {assignee}...")

            # check if the assignee has been a previous secret santa or is the same as the name
            if assignee in participants[name]["previous_secret_santa"] or assignee == name:
                print(f"{name} cannot be assigned to {assignee} because {assignee} is in {name}'s previous_secret_santa list or is the same as {name}...")
                can_assign = False
                break
        if can_assign:
            print("Went through shuffle and all names can be assigned!!! Let's go ho ho!!")
            break

    # now that we have a good assignment set, build it
    for i, name in enumerate(participants):
        assignments[name] = names[i]
    return assignments

def send_email(to_email, secret_santa_name, giver_name, email, password):
    subject = "Your Secret Santa!"
    body = f"Oh hey {giver_name},\n\nYour Secret Santa assignment is: {secret_santa_name}.\n\nMerry Christmas ya filthy animal!"
    
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email, password)
            server.sendmail(email, to_email, msg.as_string())
        print(f"Email sent to {to_email} for {giver_name}'s Secret Santa assignment.")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")

def main():
    # first assign everybody by passing in the dict of participants
    assignments = assign_secret_santa(participants)
    
    # print assignments to make sure no errors
    for giver, receiver in assignments.items():
        print(f"{giver} has {receiver}")
    # your email info and gmail app password to void 2FA and be able to send emails
    email = "email@gmail.com"
    password = ""
    
    # send the emails
    for giver, receiver in assignments.items():
        giver_email = participants[giver]["email"]
        send_email(giver_email, receiver, giver, email, password)

    # email master list to yourslef
    organizer_email = "email@gmail.com"
    organizer_subject = "Secret Santa MASTER LIST"
    organizer_body = "Here are the Secret Santa assignments:\n\n" + \
                     "\n".join([f"{giver} -> {receiver}" for giver, receiver in assignments.items()]) + \
                     "\n\nPeace in the Middle East"
    send_email(organizer_email, organizer_subject, organizer_body, email, password)


if __name__ == "__main__":
    main()
