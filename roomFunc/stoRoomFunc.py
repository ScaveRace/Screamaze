# # ---------- view transitions ----------
#     def _set_view(self, view, message=None):
#         self.view = view
#         self.current_image = {
#             View.ROOM: self.room_image,
#             View.DESK: self.desk_image,
#             View.QUIZ: self.quiz_paper,
#             View.DRAWER: self.desk_open,
#         }[view]
#
#         if view == View.QUIZ:
#             self.current_buttons = self.quiz_buttons_for_current_question()
#         elif view == View.DRAWER:
#             self.current_buttons = self.back_buttons if self.stone_collected else self.stone_buttons
#         else:
#             self.current_buttons = {View.ROOM: self.buttons, View.DESK: self.desk_buttons}[view]
#
#         if message:
#             self.chatbox.say(message)
#
#     def quiz_buttons_for_current_question(self):
#         _, answers, _ = self.quiz.current_question()
#         # i=i locks in the number for each button (avoids late-binding bug)
#         return [
#             u.Button(500, 300 + i * 60, 280, 50, text, lambda i=i: self.check_answer(i))
#             for i, text in enumerate(answers)
#         ] + self.back_buttons
#
#     # ---------- room ----------
#     def leave(self):
#         self.next_room = "corridor"
#
#     def goto_room(self):
#         self._set_view(View.ROOM)
#
#     def goto_desk(self):
#         msg = "You > The drawer is unlocked" if self.quiz.completed \
#             else "You > The drawer is locked, there is a quiz on the desk"
#         self._set_view(View.DESK, msg)
#
#     def open_drawer(self):
#         if not self.quiz.completed:
#             self._set_view(View.QUIZ, "Desk > " + self.quiz.current_question()[0])
#         elif self.stone_collected:
#             self._set_view(View.DRAWER, "You > The drawer is empty now")
#         else:
#             self._set_view(View.DRAWER, "You > The drawer is open, there is a green stone inside")
#
#     # ---------- quiz ----------
#     def check_answer(self, choice):
#         correct, just_completed = self.quiz.answer(choice)
#
#         if not correct:
#             self.chatbox.say("You > Wrong, try again :)")
#             return
#
#         if just_completed:
#             self._set_view(View.DRAWER, "You > 'click' the drawer unlocked")
#         else:
#             self._set_view(View.QUIZ, "Desk > " + self.quiz.current_question()[0])
#
#     # ---------- stone ----------
#     def collect_stone(self):
#         if self.stone_collected:
#             self.chatbox.say("You > I already have the green stone")
#             return
#         self.stone_collected = True
#         self.player.add_item("Stones", "Green", "assets/storrageRoom/storage_room_bigger.png")
#         self.chatbox.say("You > A green stone... one step closer")
#         self._set_view(View.DRAWER)