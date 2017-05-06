from bot_email_parser import BotEmailParser

parser = BotEmailParser('templates/email_template.html')
parser.parse('Cardiff', 'GBP', None)
