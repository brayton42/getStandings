from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import csv
import smtplib, ssl
import sys
from Team import Team
#run with python3
client.standings(
    season_end_year=2021,
    output_type=OutputType.JSON,
    output_file_path="./curStand.csv"
)

# create Paul Roster, Brayton Roster, Lucas Roster
paulsRoster = []
with open("PaulsRoster.csv") as file:
    reader = csv.reader(file)
    i = 0
    for teamName, draftPos, round, exp in reader:
        paulsRoster.append(Team(teamName, draftPos, round, 0, exp))
        i+=1

lucassRoster = []
with open("LucassRoster.csv") as file:
    reader = csv.reader(file)
    i = 0
    for teamName, draftPos, round, exp in reader:
        lucassRoster.append(Team(teamName, draftPos, round, 0, exp))
        i+=1

braytonsRoster = []
with open("BraytonsRoster.csv") as file:
    reader = csv.reader(file)
    for teamName, draftPos, round, exp in reader:
        braytonsRoster.append(Team(teamName, draftPos, round, 0, exp))

pSum = 0
lSum = 0
bSum = 0
#for each team in standings
with open("curStand.csv") as file:
    reader = csv.reader(file)
    i = 0
    for docText in reader:
        if i%7 == 5:
            temName = docText[0]
            teamName = temName[17:-1]
        if i%7 == 6:
            win = docText[0]
            wins = win[16:]
            for match in paulsRoster:
                if teamName == match.name:
                    match.setWins(int(wins))
                    pSum+= int(wins)
            for match in lucassRoster:
                if teamName == match.name:
                    match.setWins(int(wins))
                    lSum+= int(wins)
            for match in braytonsRoster:
                if teamName == match.name:
                    match.setWins(int(wins))
                    bSum += int(wins)
        i+=1

#check who owns it
#add that to owner total
#show owner standings, there best team, there worst team, most over performing team, under performing team (SORTED-draft pick

paulsRoster.sort(key=lambda x: x.wins, reverse = True)
lucassRoster.sort(key=lambda x: x.wins, reverse = True)
braytonsRoster.sort(key=lambda x: x.wins, reverse = True)

paulsUpdate = f'Paul has {pSum} wins\nHis best team is the {paulsRoster[0].name} with {paulsRoster[0].wins} wins\nHis worst team is the {paulsRoster[-1].name} with {paulsRoster[-1].wins} wins.'
lucassUpdate = f'Lucas has {lSum} wins\nHis best team is the {lucassRoster[0].name} with {lucassRoster[0].wins} wins\nHis worst team is the {lucassRoster[-1].name} with {lucassRoster[-1].wins} wins.'
braytonsUpdate = f'Brayton has {bSum} wins\nHis best team is the {braytonsRoster[0].name} with {braytonsRoster[0].wins} wins\nHis worst team is the {braytonsRoster[-1].name} with {braytonsRoster[-1].wins} wins.'


smtp_server = 'smtp.gmail.com'
sender_email = sys.argv[1]
password = sys.argv[2] #input("Type your password and press enter: ")
update = f'{paulsUpdate}\n\n{lucassUpdate}\n\n{braytonsUpdate}\n'
#write email

server = smtplib.SMTP_SSL(smtp_server, 465)
server.login(sender_email, password)
#server.sendmail(sender_email, 'braytonsmith42@gmail.com', f'')
with open("emailList.csv") as file:
    reader = csv.reader(file)
    for name, email in reader:
        print(f"Sending email to {name} at {email}")
        server.sendmail(sender_email, email, f'Hello {name}, here is your weekly bet update:\n\n{update}')
