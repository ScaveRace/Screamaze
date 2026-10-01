import pygame
import sqlite3

conn = sqlite3.connect("data/database/storyDB.db")
cur = conn.cursor()

def chatMessage(room,messageID):
    cur.execute("SELECT text_en FROM ? WHERE id = ?",(room,messageID))
    cur.close()