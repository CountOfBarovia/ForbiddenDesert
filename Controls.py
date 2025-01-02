import pygame, Globals, Display
pygame.init()

# Subroutine to allow the player to select something
def Find(Adjacent, Purpose):
        Complete = False
        while not Complete and Purpose == "Dig":
                Globals.Glow = Adjacent
                Wait()
                if Globals.CancelButton.hover:
                        Complete = True
                Globals.Glow = False
                Place = pygame.mouse.get_pos()
                if Place[1] > 0 and Place[0] > 0:
                        Place = (Place[0] - (Globals.ScreenW - 500) / 2, Place[1] - (Globals.ScreenH - 560))
                        if Place[0] > 0:
                                Row = int(Place[0] // 100)
                        else:
                                Row = -1
                        Column = Place[1] // 100
                        if Place[0] > 0 or Place[1] > 0:
                                if Place[0] % 100 > 5 and Place[0] % 100 < 95 and Place[1] % 100 > 5 and Place[1] % 100 < 95 and Row < 5 and Column < 5:
                                        if (Globals.Area.Layout[Column][Row].sand > 0 or Globals.Area.Layout[Column][Row].revealed == False) and Globals.Area.Layout[Column][Row].type != "S":
                                                if Adjacent == True:
                                                        tile = Globals.Area.Layout[Column][Row]
                                                        if tile.sand > 0:
                                                                return tile
                                                elif Globals.Diagonal:
                                                        if Adjacent[0] <= Column + 1 and Adjacent[0] >= Column - 1 and Adjacent[1] <= Row + 1 and Adjacent[1] >= Row - 1:
                                                                tile = Globals.Area.Layout[Column][Row]
                                                                if tile.sand > 0 or Globals.ActivePlayer.Locate() == (Column, Row):
                                                                        return tile
                                                else:
                                                        if (Adjacent[0] <= Column + 1 and Adjacent[0] >= Column - 1 and Adjacent[1] == Row) or (Adjacent[1] <= Row + 1 and Adjacent[1] >= Row - 1 and Adjacent[0] == Column):
                                                                tile = Globals.Area.Layout[Column][Row]
                                                                if tile.sand > 0 or Globals.ActivePlayer.Locate() == (Column, Row):
                                                                        return tile
        while not Complete and Purpose == "Move":
                Globals.Glow = Adjacent
                Wait()
                if Globals.CancelButton.hover:
                        Complete = True
                Globals.Glow = False
                Place = pygame.mouse.get_pos()
                if Place[1] > 0 and Place[0] > 0:
                        Place = (Place[0] - (Globals.ScreenW - 500) / 2, Place[1] - (Globals.ScreenH - 560))
                        if Place[0] > 0:
                                Row = int(Place[0] // 100)
                        else:
                                Row = -1
                        Column = Place[1] // 100
                        if Place[0] > 0 or Place[1] > 0:
                                if Place[0] % 100 > 5 and Place[0] % 100 < 95 and Place[1] % 100 > 5 and Place[1] % 100 < 95 and Row < 5 and Column < 5:
                                        if (Globals.Area.Layout[Column][Row].sand < 2 or Globals.ActivePlayer.name == "Climber") and Globals.Area.Layout[Column][Row].type != "S":
                                                if Adjacent == True:
                                                        return Globals.Area.Layout[Column][Row]
                                                elif Globals.Diagonal and not (Column == Adjacent[0] and Row == Adjacent[1]):
                                                        if (Adjacent[0] <= Column + 1 and Adjacent[0] >= Column - 1 and Adjacent[1] <= Row + 1 and Adjacent[1] >= Row - 1) or (Globals.Area.Layout[Column][Row].type == "T" and Globals.Area.Layout[Adjacent[0]][Adjacent[1]].type == "T"):
                                                                return Globals.Area.Layout[Column][Row]
                                                elif not (Column == Adjacent[0] and Row == Adjacent[1]):
                                                        if ((Adjacent[0] <= Column + 1 and Adjacent[0] >= Column - 1 and Adjacent[1] == Row) or (Adjacent[1] <= Row + 1 and Adjacent[1] >= Row - 1 and Adjacent[0] == Column)) or (Globals.Area.Layout[Column][Row].type == "T" and Globals.Area.Layout[Adjacent[0]][Adjacent[1]].type == "T"):
                                                                return Globals.Area.Layout[Column][Row]
        while not Complete and Purpose == "Control":
                Globals.Grow = True
                Globals.Texts[0].text = Globals.Texts[0].text[0:19] + str(Globals.Actions) + "#"
                Wait()
                Globals.Grow = False
                Globals.Position = Globals.ActivePlayer.Locate()
                if Globals.MoveButton.hover and Globals.Buttons.has(Globals.MoveButton):
                        Complete = Globals.ActivePlayer.Move()
                elif Globals.DigButton.hover:
                        if Globals.ActivePlayer.name == "Explorer": Globals.Diagonal = True
                        else: Globals.Diagonal = False
                        if Globals.ActivePlayer.name == "Archeologist":
                                reps = 2
                        else: reps = 1
                        rep = 0
                        while rep < reps:
                                Globals.Purpose = "Dig" + str(rep)
                                tile = Find(Globals.Position, "Dig")
                                Globals.Purpose = None
                                if tile != None:
                                        if tile.sand > 0:
                                                rep += 1
                                                tile.Dig()
                                                Complete = True
                                        else:
                                                if Globals.ActivePlayer.name != "Archeologist" or rep == 0:
                                                        tile.Dig()
                                                        rep = 2
                                                        Complete = True
                                else: rep = 2
                elif Globals.SuccessButton.hover and Globals.Buttons.has(Globals.SuccessButton):
                        Pos = Globals.ActivePlayer.Locate()
                        tile = Globals.Area.Layout[Pos[0]][Pos[1]]
                        if tile.treasure != None:
                                Globals.ActivePlayer.treasures.append(tile.treasure)
                                tile.treasure.collected = True
                                tile.treasure = None
                        else: Globals.Won = True
                elif Globals.SpecialButton.hover and Globals.Buttons.has(Globals.SpecialButton):
                        Complete = Globals.ActivePlayer.Power()
                for player in Globals.Adventurers:
                        if player.handhover:
                                player.hand_displayed = True
                                Globals.Priority.append(player)
                                Find(False, "Card")
                        elif player.hover:
                                player.big = True
                                Globals.Priority.append(player)
                                Wait()
                                Globals.Priority.remove(player)
                                player.big = False
        if Purpose == "Card":
                Wait()
                User = Globals.Priority[0]
                Globals.Priority.remove(User)
                User.hand_displayed = False
                for card in User.hand.contents:
                        if card.hover:
                                Globals.Position = User.Locate()
                                User.hand.contents.remove(card)
                                if User.name == "Explorer": Globals.Diagonal = True
                                else: Globals.Diagonal = False
                                card.Use(Globals.Position, User)

        while Purpose == "Player" and not Complete:
                Globals.PlayerSelect = True
                Text = Display.Text("Choose a player#", (Globals.ScreenW / 2, Globals.ScreenH / 2), True, (0, 0, 0), Globals.MidScroll)
                Text.Output()
                Wait()
                Text.Delete()
                Globals.PlayerSelect = False
                for player in Globals.Adventurers:
                    if player.hover:
                        return player
                if Globals.CancelButton.hover:
                    return None

# Subroutine to wait for a click
def Wait():
        clicked = False
        while not clicked and not Globals.QUIT:
                Display.Update()
                for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYDOWN:
                                clicked = True

# Class for the buttons
class Button(pygame.sprite.Sprite):
        def __init__(self, image, pos):
                super().__init__()
                self.srcimage = image
                self.image = pygame.transform.scale(self.srcimage, (50, 50))
                self.rect = self.image.get_rect()
                self.rect.center = pos
                self.collrect = CollRect(pos, (50, 50))
                self.radius = 25
                self.pos = pos
                self.hover = False
                # Is the button a different shape to the others?
                self.different = False

        def update(self):
                if pygame.sprite.collide_circle(Globals.MouseColl, self) and not self.different:
                        self.hover = True
                        self.radius = 30
                        self.rect.center = (self.pos[0] - 5, self.pos[1] - 5)
                        self.image = pygame.transform.scale(self.srcimage, (60, 60))
                elif pygame.sprite.collide_rect(Globals.MouseColl, self.collrect) and self.different:
                        self.hover = True
                        self.image = pygame.transform.scale(self.srcimage, (170, 47 * 17/16))
                        self.rect = self.srcimage.get_rect()
                        self.rect.center = self.pos
                elif not self.different:
                        self.hover = False
                        self.radius = 25
                        self.rect.center = self.pos
                        self.image = pygame.transform.scale(self.srcimage, (50, 50))
                elif self.different:
                        self.hover = False
                        self.image = pygame.transform.scale(self.srcimage, (160, 47))
                        self.rect = self.srcimage.get_rect()
                        self.rect.center = self.pos
                self.collrect = CollRect((self.pos[0] - self.image.get_size()[0] / 2, self.pos[1] - self.image.get_size()[1] / 2), (self.rect.w, self.rect.h))
                self.image.set_colorkey((0, 0, 255))

# Class for collision checker rectangles
class CollRect(pygame.sprite.Sprite):
        def __init__(self, pos, dim):
                super().__init__()
                self.rect = pygame.Rect(pos, dim)
                self.radius = dim[1] / 2