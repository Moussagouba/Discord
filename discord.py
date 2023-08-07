import discord
import smtplib
import random
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
verification_tokens = {}

def generate_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))

async def send_verification_email(user):
    email = "your@email.com"
    password = "your_email_password"
    token = generate_token()
    verification_tokens[user.id] = token

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = user.email
    msg['Subject'] = "Verify Your Email"
    body = f"Click the following link to verify your email: http://yourbotdomain.com/verify?user_id={user.id}&token={token}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, user.email, msg.as_string())
        server.quit()
    except:
        print("Error sending email")

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_member_join(member):
    await send_verification_email(member)

client.run("YOUR_DISCORD_TOKEN")
