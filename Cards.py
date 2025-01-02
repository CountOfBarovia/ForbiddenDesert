import Globals, pygame, Controls, random, Display
pygame.init()

# Class for a generic card
class Card:
    def __init__(self, name):
        self.location = None
        self.name = name
        self.displayed = False
        self.image = Globals.CardList[name]
        self.image.set_colorkey((0, 0, 255))
        self.location = None
        self.big = False
        self.pos = (0, 0)
        self.collrect = Controls.CollRect(self.pos, (200, 277))
        self.hover = False

    # Subroutine to initialise the location
    def Place(self, loc):
        self.location = loc
    
    # Subroutine to put from one deck into another
    def Draw(self, dest):
        newcontents = []
        newcontents.append(self)
        newcontents.extend(dest.contents)
        dest.contents = newcontents
        self.location = dest
        self.big = True
        Globals.Priority.append(self)
        Controls.Wait()
        self.big = False
        Globals.Priority.remove(self)

    # Subroutine to display the card
    def Display(self):
        if self.big == True:
            Grey = pygame.Surface((Globals.ScreenW, Globals.ScreenH))
            Grey.fill((0, 0, 0))
            Grey.set_alpha(128)
            BigImage = pygame.transform.scale(self.image, (Globals.ScreenH / 1.5 * (self.image.get_size()[0]/self.image.get_size()[1]) - 5, Globals.ScreenH / 1.5 - 5))
            BigImage.set_colorkey((0, 0, 255))
            Globals.Screen.blit(Grey, (0, 0))
            Globals.Screen.blit(BigImage, (Globals.ScreenW / 2 - BigImage.get_size()[0] / 2, Globals.ScreenH / 2 - BigImage.get_size()[1] / 2))
        else:
            SmallImage = pygame.transform.scale(self.image, (100, 138.5))
            SmallImage.set_colorkey((0, 0, 255))
            Globals.Screen.blit(self.image, self.pos)

# Class for the technology cards
class TechCard(Card):
    def __init__(self, name):
        super().__init__(name)

    # Subroutine to use the card
    def Use(self, pos, user):
        if self.name == "DuneBlaster":
            Globals.Purpose = "DuneBlaster"
            Tile = Controls.Find(pos, "Dig")
            Globals.Purpose = None
            if Tile != None:
                Tile.sand = 0
                self.Draw(Globals.TechDiscard)
            else: user.hand.contents.append(self)
        elif self.name == "Jetpack":
            Globals.User = user
            Globals.Purpose = "Jetpack"
            Player = Controls.Find(True, "Player")
            Globals.Purpose = "Jetpack"
            NewTile = Controls.Find(True, "Move")
            while NewTile == Globals.Area.Layout[pos[0]][pos[1]]:
                NewTile = Controls.Find(True, "Move")
            Globals.User = None
            Globals.Purpose = None
            if NewTile != None:
                NewTile.player.append(user)
                Globals.Area.Layout[pos[0]][pos[1]].player.remove(user)
                if Player != None:
                    NewTile.player.append(Player)
                    Globals.Area.Layout[pos[0]][pos[1]].player.remove(user)
                self.Draw(Globals.TechDiscard)
            else: user.hand.contents.append(self)
        elif self.name == "Terrascope":
            Globals.Purpose = "Terrascope"
            Tile = Controls.Find(True, "Dig")
            Globals.Purpose = None
            if Tile != None:
                while Tile.revealed:
                    Tile = Controls.Find(True, "Dig")
                Globals.Priority.append(Tile)
                self.Draw(Globals.TechDiscard)
                Controls.Wait()
                Globals.Priority.remove(Tile)
            else: user.hand.contents.append(self)
        elif self.name == "SecretWaterReserve":
            for player in Globals.Area.Layout[pos[0]][pos[1]].player:
                player.water += 2
            self.Draw(Globals.TechDiscard)
        elif self.name == "TimeThrottle":
            if Globals.ActivePlayer != user:
                text = Display.Text("Can only be used#on your turn#", (Globals.ScreenW / 2, Globals.ScreenH / 2), True, (199, 9, 6), Globals.MidScroll)
                text.Output()
                Controls.Wait()
                text.Delete()
                user.hand.contents.append(self)
            else:
                Globals.Actions += 2
                self.Draw(Globals.TechDiscard)
        elif self.name == "SolarShield":
            text = Display.Text("Will be automatically#used when Sun Beats#Down#", (Globals.ScreenW / 2, Globals.ScreenH / 2), True, (199, 9, 6), Globals.MidScroll)
            text.Output()
            Controls.Wait()
            text.Delete()
            user.hand.contents.append(self)

# Class for the storm cards
class StormCard(Card):

    # Subroutine to draw this card
    def Draw(self):
        super().Draw(Globals.StormDiscard)
        self.Display()
        # And the effects of the cards
        if self.name == "SunBeatsDown":
            # All players lose one water unless they use a solar shield or are in a tunnel
            for item in Globals.Adventurers:
                item.protected = False
                pos = item.Locate()
                tile = Globals.Area.Layout[pos[0]][pos[1]]
                if tile.type == "T" and tile.revealed: item.protected = True
                for other in tile.player:
                    if other.protected: item.protected
                for card in item.hand.contents:
                    if card.name == "SolarShield" and not item.protected:
                        item.protected = True
                        card.Draw(Globals.TechDiscard)
                        item.hand.contents.remove(card)
                if not item.protected:
                    item.water -= 1
                    if item.water == 0:
                        Globals.Deaded = True
        elif self.name == "StormPicksUp":
            Globals.StormLevel += 1
            if Globals.StormLevel == 15:
                Globals.Deaded = True
        elif "Up" in self.name:
            Globals.Area.Up(int(self.name[2]))
        elif "Down" in self.name:
            Globals.Area.Down(int(self.name[4]))
        elif "Right" in self.name:
            Globals.Area.Right(int(self.name[5]))
        elif "Left" in self.name:
            Globals.Area.Left(int(self.name[4]))

# Class for the identity cards
class Player(Card):
    def __init__(self, name):
        super().__init__(name)
        if name == "WaterCarrier":
            self.watercap = 5
        elif name == "Climber" or name == "Archeologist":
            self.watercap = 3
        else:
            self.watercap = 4
        self.water = self.watercap
        self.hand = Deck(None, [])
        self.hand.back = Globals.CardList["TechBack"]
        self.hand_displayed = False
        self.collrect = Controls.CollRect(self.pos, (100, 138.5))
        self.handcollrect = Controls.CollRect(self.pos, (100, 138.5))
        self.hover = False
        self.handhover = False
        self.pawn = Globals.Pawns[name]
        self.pawn = pygame.transform.scale(self.pawn, (22.5, 50))
        self.pawn.set_colorkey((0, 0, 255))
        self.treasures = []
        self.protected = False

    # Subroutine to output the card (with the water ticker)
    def Display(self):
        if self.big == True:
            self.big = False
            self.Display()
            self.big = True
            Grey = pygame.Surface((Globals.ScreenW, Globals.ScreenH))
            Grey.fill((0, 0, 0))
            Grey.set_alpha(128)
            BigImage = pygame.transform.scale(self.image, (Globals.ScreenH / 1.5 * (self.image.get_size()[0]/self.image.get_size()[1]) - 5, Globals.ScreenH / 1.5 - 5))
            BigImage.set_colorkey((0, 0, 255))
            Globals.Screen.blit(Grey, (0, 0))
            Globals.Screen.blit(BigImage, (Globals.ScreenW / 2 - BigImage.get_size()[0] / 2, Globals.ScreenH / 2 - BigImage.get_size()[1] / 2))
        else:
            if self.name == "WaterCarrier":
                mod =  15
                max = 5
                start = 25
            elif self.name == "Climber" or self.name == "Archeologist":
                mod = 18
                max = 3
                start = 45
            else:
                mod = 18
                max = 4
                start = 27
            meterpos = mod * (max - self.water) + start
            if self.hover: Image = pygame.transform.scale(self.image, (110, 148.5))
            else:
                Image = pygame.transform.scale(self.image, (100, 138.5))
                level = pygame.transform.scale(Globals.Level, (30, 30 / 1.569))
                level.set_colorkey((0, 0, 255))
                Image.blit(level, (0, meterpos))
            Image.set_colorkey((0, 0, 255))
            j = 0
            for treasure in self.treasures:
                Image.blit(treasure.image, (35, 138.5 / len(self.treasures) * j + 138.5 / len(self.treasures) / 2 - 15))
                j += 1
            Globals.Screen.blit(Image, self.pos)
        if self.hand_displayed:
            Grey = pygame.Surface((Globals.ScreenW, Globals.ScreenH))
            Grey.fill((0, 0, 0))
            Grey.set_alpha(128)
            Globals.Screen.blit(Grey, (0, 0))
            Image = pygame.transform.scale(self.image, (200, 138.5 * 2))
            Image.set_colorkey((0, 0, 255))
            self.pos = (Globals.ScreenW / 2 - 100, 20)
            Globals.Screen.blit(Image, self.pos)
            i = 0
            for card in self.hand.contents:
                NewImage = pygame.transform.scale(card.image, (200, 138.5 * 2))
                card.pos = (Globals.ScreenW / len(self.hand.contents) * i + Globals.ScreenW / len(self.hand.contents) / 2 - NewImage.get_size()[0] / 2, Globals.ScreenH / 2)
                if pygame.sprite.collide_rect(card.collrect, Globals.MouseColl):
                    card.pos = (card.pos[0] - 5, card.pos[1] - 5)
                    card.hover = True
                    NewImage = pygame.transform.scale(card.image, (210, 138.5 * 2 + 10))
                else: card.hover = False
                card.collrect.rect.update(card.pos, (200, 277))
                NewImage.set_colorkey((0, 0, 255))
                Globals.Screen.blit(NewImage, card.pos)
                i += 1
        
    # Subroutine to work out where the player is
    def Locate(self):
        R = 0
        for Row in Globals.Area.Layout:
            C = 0
            for Tile in Row:
                if self in Tile.player:
                    return (R, C)
                C += 1
            R += 1

    # Subroutine to move the player
    def Move(self):
        OldPos = self.Locate()
        if self.name == "Explorer": Globals.Diagonal = True
        else: Globals.Diagonal = False
        if Globals.ActivePlayer.name == "Climber":
            Globals.Purpose = "ClimberMove"
            Player = Controls.Find(None, "Player")
            Globals.Purpose = None
        else: Player = None
        Globals.Purpose = "Move"
        NewTile = Controls.Find(OldPos, "Move")
        Globals.Purpose = None
        if NewTile != None:
            NewTile.player.append(self)
            Globals.Area.Layout[OldPos[0]][OldPos[1]].player.remove(self)
            if Player != None:
                Pos = Globals.ActivePlayer.Locate()
                Globals.Area.Layout[Pos[0]][Pos[1]].player.append(Player)
                Globals.Area.Layout[Globals.Position[0]][Globals.Position[1]].player.remove(Player)
            return True
        else:
            return False

    # Subroutine to use the special ability
    def Power(self):
        if self.name == "Meteorologist":
            Globals.CardsToDraw -= 1
            return True
        elif self.name == "WaterCarrier":
            self.water += 2
            return True
        elif self.name == "Navigator":
            player = Controls.Find(None, "Player")
            for i in range(0, 3):
                player.Move()

# Generic class for a store of cards
class Deck:
    def __init__(self, pos, contents):
        self.contents = contents
        self.pos = pos
        self.back = None

    # Subroutine to shuffle the deck
    def Shuffle(self):
        newindexes = []
        for i in range(0, len(self.contents)):
            valid = False
            while not valid:
                new = random.randint(0, len(self.contents) - 1)
                if not new in newindexes:
                    newindexes.append(new)
                    valid = True
        newlist = []
        for i in newindexes:
            newlist.append(self.contents[i])
        self.contents = newlist

    # Subroutine to shuffle one deck into another
    def ShuffleInto(self, dest):
        dest.contents.extend(self.contents)
        dest.Shuffle()

    # Subroutine to draw a card
    def Draw(self, dest):
        card = self.contents[0]
        card.Draw(dest)
        self.contents.pop(0)

    # Subroutine to display the deck - True for face up, False for face down
    def Display(self, Face):
        image = None
        if Face or self.back == None:
            if self.contents != None:
                if len(self.contents) > 0:
                    image = pygame.transform.scale(self.contents[0].image, (100, 138.5))
        else:
            image = self.back
        if image != None:
            image.set_colorkey((0, 0, 255))
            Globals.Screen.blit(image, self.pos)

    # Subroutine to initialise the card locations
    def Place(self):
        for card in self.contents:
            card.Place(self)

# Class for the storm deck
class Deck_Storm(Deck):
    def __init__(self, pos):
        super().__init__(pos, [])
        for i in range(3):
            for x in range(3 - i):
                self.contents.append(StormCard("Up" + str(i + 1)))
                self.contents.append(StormCard("Down" + str(i + 1)))
                self.contents.append(StormCard("Left" + str(i + 1)))
                self.contents.append(StormCard("Right" + str(i + 1)))
                self.contents.append(StormCard("StormPicksUp"))
            if i < 2:
                self.contents.append(StormCard("SunBeatsDown"))
                self.contents.append(StormCard("SunBeatsDown"))
        self.back = pygame.transform.scale(Globals.CardList["StormBack"], (100, 138.5))
        self.Shuffle()

    def Draw(self, quant):
        for i in range(quant):
            if len(self.contents) > 0:
                card = self.contents[0]
                card.Draw()
                self.contents.pop(0)
            else:
                Globals.StormDiscard.ShuffleInto(self)
                card = self.contents[0]
                card.Draw()
                self.contents.pop(0)

# Class for the tech deck
class Deck_Tech(Deck):
    def __init__(self, pos):
        super().__init__(pos, [])
        for i in range(3):
            self.contents.append(TechCard("DuneBlaster"))
            self.contents.append(TechCard("Jetpack"))
            if i < 2:
                self.contents.append(TechCard("SolarShield"))
                self.contents.append(TechCard("Terrascope"))
            if i < 1:
                self.contents.append(TechCard("SecretWaterReserve"))
                self.contents.append(TechCard("TimeThrottle"))
        self.back = pygame.transform.scale(Globals.CardList["TechBack"], (100, 138.5))
        self.Shuffle()
