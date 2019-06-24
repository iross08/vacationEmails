# coding: utf-8
from autoreplyer import AutoReplyer

class YourAutoReplyer(AutoReplyer):
        imap_server = 'imap.gmail.com'
        imap_port = 993  # Custom port, only use if the default one doesn’t work.
        imap_user = 'username@gmail.com'
        imap_password = 'passphrases'

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # Custom port, only use if the default one doesn’t work.
        smtp_user = 'username@gmail.com'
        smtp_password = 'passphrases'
        
        ##https://support.google.com/mail/answer/7126229?hl=en
        
        from_address = 'Name <username@gmail.com>'
        body = '''
        
            Vacation-ain't you love this? I'm into this until upcoming monsoon.<br />
            Quesries ( yours) are under reciew & you'll have an answer ready when I’m back.<br />
            Please ring at my <a href="tel:+012345678">residence</a> in case of and with gorgeous urgency.
        
        Have a nice day sir, thank you for having me:
        you
        '''
        body_html = '''
        
        <p>
            Vacation-ain't you love this? I'm into this until upcoming monsoon.<br />
            Quesries ( yours) are under reciew & you'll have an answer ready when I’m back.<br />
            Please ring at my <a href="tel:+012345678">residence</a> in case of and with gorgeous urgency.        </p>

        <p>
            Have a nice day sir, thank you for having me:<br />
            you
        </p>
        '''

YourAutoReplyer().run()
