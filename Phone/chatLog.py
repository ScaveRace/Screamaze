import functions.language as lang


# one line in the chat
# a game message is kept as (table, id) and looked up again every time it is shown, so when the player changes the language, the old messages change too
# a message the player typed has no id, it is kept as it was typed
class Message:
    def __init__(self, who="", table=None, messageID=None, values=None, text=""):
        self.who = who.strip().rstrip(":").strip()     # "Thuas: " and "Thuas" are the same speaker
        self.table = table
        self.messageID = messageID
        self.values = values
        self.text = text

    def body(self):
        if self.table is None:
            return self.text
        text = lang.chatMessage(self.table, self.messageID) or ""
        if self.values is not None:
            text = text.format(**self.values)
        return text


# every message of the game, the rooms put theirs here through fui.chat, the ChatPage of the phone shows them
class ChatLog:
    def __init__(self):
        self.messages = []
        self.unread = False      # something new came, the chat app gets a red dot until the chat is open

    # a message from the language files: log.sayKey("You", "TeacherRoom", 3), values fill the {} in the text
    def sayKey(self, who, table, messageID, **values):
        self.add(Message(who, table, messageID, values if values else None))

    # a message that is not in the language files, "Name > text" or just text
    def say(self, text):
        who, sep, rest = text.partition(" > ")
        if not sep:
            who, rest = "", text
        self.add(Message(who, text=rest))

    def add(self, message):
        message.body()       # a wrong table or id shows up here, where the room said it, and not later in the drawing
        self.messages.append(message)
        self.unread = True
