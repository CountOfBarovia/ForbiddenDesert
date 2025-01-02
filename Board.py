import random, pygame, Globals, Display, Controls
pygame.init()

# Class for the special items
class Treasure:
        def __init__(self, Name):
                self.type = Name
                self.row = None
                self.column = None
                self.set = False
                self.collected = False
                if Name == "Engine":
                        self.image = Globals.EnginePic
                        self.index = 0
                if Name == "Propeller":
                        self.image = Globals.PropellerPic
                        self.index = 1
                if Name == "Solar":
                        self.image = Globals.SolarPic
                        self.index = 2
                if Name == "Wheel":
                        self.image = Globals.WheelPic
                        self.index = 3
        
        # Subroutine to display the item
        def view(self, Surface, Shift):
                Pos = (self.pos[0] + 30, self.pos[1] + Shift)
                Surface.blit(self.image, Pos)

        # Subroutine to find the item's location
        def update(self):
                if self.column != None and self.row != None and not self.collected:
                        if Globals.Area.Layout[self.row][self.column].type != "S":
                                if Globals.Area.Layout[self.row][self.column].treasure == None:
                                        Globals.Area.Layout[self.row][self.column].treasure = self
                                        self.set = True
                                        Globals.Set += 1
                                        for i in Globals.Treasures:
                                                if i.index > self.index:
                                                        i.index -= 1
                if not self.set:
                        Globals.Screen.blit(self.image, (-20 + (Globals.ScreenW - 500) / 2 + (self.index + 0.5) * 500 / (4 - Globals.Set), 20))

# Class for the game tiles
class Tile:
        def __init__(self, Type):
                self.type = Type
                self.pos = (0, 0)
                # The default state is unexcavated and unburied
                self.revealed = False
                self.sand = 0
                # An if statement to assign a suitable image for the tile
                if self.type == "E" or self.type == "C":
                        self.image = Globals.TechSite
                elif self.type == "T":
                        self.image = Globals.Tunnel
                elif self.type == "W":
                        self.image = Globals.Well
                elif self.type == "M":
                        self.image = Globals.Mirage
                elif self.type == "P":
                        self.image = Globals.Pad
                elif self.type == "OH":
                        self.image = Globals.OH
                elif self.type == "OV":
                        self.image = Globals.OV
                elif self.type == "YH":
                        self.image = Globals.YH
                elif self.type == "YV":
                        self.image = Globals.YV
                elif self.type == "SH":
                        self.image = Globals.SH
                elif self.type == "SV":
                        self.image = Globals.SV
                elif self.type == "RH":
                        self.image = Globals.RH
                elif self.type == "RV":
                        self.image = Globals.RV
                elif self.type == "S":
                        self.image = Globals.Storm
                self.treasure = None
                self.player = []
                if self.type == "C":
                        for item in Globals.Adventurers:
                                self.player.append(item)

        # Subroutine to work out what image should be outputted for this tile
        def view(self, Glow):
                pic = pygame.Surface((100, 100), pygame.SRCALPHA)
                if not self.revealed:
                        if self.type == "W" or self.type == "M":
                                image = Globals.Oasis
                        elif self.type == "C":
                                image = Globals.Crash
                        else:
                                image = Globals.Dune
                else:
                        image = self.image
                if self.type == "S":
                        image = Globals.Storm
                        pic.fill((255, 255, 255))
                        pic.set_colorkey((255, 255, 255))
                        pic.blit(image, (0, 0))
                else:
                        if Glow:
                                pic.blit(Globals.Aura, (0, 0))
                        pic.blit(image, (5, 5))
                        pic.set_colorkey((0, 0, 0))
                if self.treasure != None:
                        self.treasure.pos = self.pos
                pic.set_colorkey((255, 255, 255))
                return pic

        # Subroutine to remove sand/excavate
        def Dig(self):
                if self.sand > 0:
                        self.sand -= 1
                elif not self.revealed:
                        self.revealed = True
                        pos = (self.pos[0] - (Globals.ScreenW - 500) / 2, self.pos[1] - Globals.ScreenH + 60)
                        if self.type == "SH":
                                Globals.Engine.row = int(pos[1] / 100)
                        elif self.type == "SV":
                                Globals.Engine.column = int(pos[0] / 100)
                        elif self.type == "OH":
                                Globals.Solar.row = int(pos[1] / 100)
                        elif self.type == "OV":
                                Globals.Solar.column = int(pos[0] / 100)
                        elif self.type == "YH":
                                Globals.Propeller.row = int(pos[1] / 100)
                        elif self.type == "YV":
                                Globals.Propeller.column = int(pos[0] / 100)
                        elif self.type == "RH":
                                Globals.Wheel.row = int(pos[1] / 100)
                        elif self.type == "RV":
                                Globals.Wheel.column = int(pos[0] / 100)
                        elif self.type == "E" or self.type == "T" or self.type == "C":
                                Globals.TechDeck.Draw(Globals.ActivePlayer.hand)
                        elif self.type == "W":
                                for player in self.player:
                                        player.water += 2

# Class for the game board
class Table:
        def __init__(self):
                # Creating the board - "S" = storm, "E" = blank tech space, "W" = well, "M" = mirage, "T" = tunnel, "P" = launch pad, "letter + V or H" = the vertical (V) or horizontal (H) indicator of a piece of a certain colour (the letter), "C" = crash site. The next line creates a board of blank tech spaces.
                Tiles = [[Tile("E") for x in range(5)] for i in range(5)]
                Specials = []
                NewTile = [2, 2]
                Specials.append([NewTile[0], NewTile[1]])
                # Working out which squares will be different from normal
                while len(Specials) < 17:
                        while NewTile in Specials:
                                NewTile[0] = random.randint(0, 4)
                                NewTile[1] = random.randint(0, 4)
                        Specials.append([NewTile[0], NewTile[1]])
                # Setting all the special tiles
                Tiles[2][2] = Tile("S")
                Tiles[Specials[1][0]][Specials[1][1]] = Tile("C")
                Tiles[Specials[2][0]][Specials[2][1]] = Tile("M")
                Tiles[Specials[3][0]][Specials[3][1]] = Tile("W")
                Tiles[Specials[4][0]][Specials[4][1]] = Tile("W")
                Tiles[Specials[5][0]][Specials[5][1]] = Tile("T")
                Tiles[Specials[6][0]][Specials[6][1]] = Tile("T")
                Tiles[Specials[7][0]][Specials[7][1]] = Tile("T")
                Tiles[Specials[8][0]][Specials[8][1]] = Tile("RH")
                Tiles[Specials[9][0]][Specials[9][1]] = Tile("RV")
                Tiles[Specials[10][0]][Specials[10][1]] = Tile("YH")
                Tiles[Specials[11][0]][Specials[11][1]] = Tile("YV")
                Tiles[Specials[12][0]][Specials[12][1]] = Tile("OH")
                Tiles[Specials[13][0]][Specials[13][1]] = Tile("OV")
                Tiles[Specials[14][0]][Specials[14][1]] = Tile("SH")
                Tiles[Specials[15][0]][Specials[15][1]] = Tile("SV")
                Tiles[Specials[16][0]][Specials[16][1]] = Tile("P")
                # Working out which squares will be buried
                Sanded = []
                while len(Sanded) < 8:
                        while NewTile in Sanded or NewTile == (2, 2):
                                NewTile[0] = random.randint(0, 4)
                                NewTile[1] = random.randint(0, 4)
                        Sanded.append([NewTile[0], NewTile[1]])
                        Tiles[NewTile[0]][NewTile[1]].sand = 1
                self.Layout = Tiles

        # Subroutine to set the board
        def Position(self):
                Pos = ((Globals.ScreenW - 500) / 2, Globals.ScreenH - 560)
                for Row in self.Layout:
                        for Space in Row:
                                Space.pos = Pos
                                Pos = (Pos[0] + 100, Pos[1])
                        Pos = ((Globals.ScreenW - 500) / 2, Pos[1] + 100)

        # Subroutine to draw the board
        def Draw(self, **Effects):
                R = 0
                C = 0
                for Row in self.Layout:
                        for Space in Row:
                                if Space.type == "S":
                                        Storm = (R, C)
                                        C += 1
                                else:
                                        pygame.event.get()
                                        Place = pygame.mouse.get_pos()
                                        Place = (Place[0] - (Globals.ScreenW - 500) / 2, Place[1] - (Globals.ScreenH - 560))
                                        if Globals.Glow == True:
                                                if Place[0] % 100 > 5 and Place[0] % 100 < 95 and Place[1] % 100 > 5 and Place[1] % 100 < 95 and Place[0] // 100 == C and Place[1] // 100 == R:
                                                        if Globals.Purpose == "Terrascope" and not Space.revealed:
                                                                Globals.Screen.blit(Space.view(True), Space.pos)
                                                        elif Globals.Purpose == "Jetpack" and Space.sand < 2 and Globals.Position != (R, C):
                                                                Globals.Screen.blit(Space.view(True), Space.pos)
                                                        else:
                                                                Globals.Screen.blit(Space.view(False), Space.pos)
                                                else:
                                                        Globals.Screen.blit(Space.view(False), Space.pos)
                                        elif Globals.Glow != False and Globals.Diagonal:
                                                if (Place[0] % 100 > 5 and Place[0] % 100 < 95 and Place[1] % 100 > 5 and Place[1] % 100 < 95 and Place[0] // 100 == C and Place[1] // 100 == R) and ((C <= Globals.Glow[1] + 1 and C >= Globals.Glow[1] - 1 and R <= Globals.Glow[0] + 1 and R >= Globals.Glow[0] - 1) or (Globals.Area.Layout[Globals.Glow[0]][Globals.Glow[1]].type == "T" and Space.type == "T" and Globals.Area.Layout[Globals.Glow[0]][Globals.Glow[1]].revealed and Space.revealed and Globals.Purpose == "Move")):
                                                        if Globals.Purpose == None:
                                                                Globals.Screen.blit(Space.view(True), Space.pos)
                                                        elif Globals.Purpose == "Dig0" and (Space.sand > 0 or (not Space.revealed and Globals.Glow == (R, C))):
                                                                Globals.Screen.blit(Space.view(True), Space.pos)
                                                        elif Globals.Purpose == "Dig1" and Space.sand > 0:
                                                                Globals.Screen.blit(Space.view(True), Space.pos)
                                                        elif Globals.Purpose == "Move" and Space.sand < 2 and not (R == Globals.Position[0] and C == Globals.Position[1]):
                                                                Globals.Screen.blit(Space.view(True), Space.pos)
                                                        elif Globals.Purpose == "DuneBlaster" and Space.sand > 0:
                                                                Globals.Screen.blit(Space.view(True), Space.pos)
                                                        else:
                                                                Globals.Screen.blit(Space.view(False), Space.pos)
                                                else:
                                                        Globals.Screen.blit(Space.view(False), Space.pos)
                                        elif Globals.Glow != False and not Globals.Diagonal:
                                                if (Place[0] % 100 > 5 and Place[0] % 100 < 95 and Place[1] % 100 > 5 and Place[1] % 100 < 95 and Place[0] // 100 == C and Place[1] // 100 == R) and ((((C <= Globals.Glow[1] + 1 and C >= Globals.Glow[1] - 1 and R == Globals.Glow[0]) or (R <= Globals.Glow[0] + 1 and R >= Globals.Glow[0] - 1 and C == Globals.Glow[1]))) or (Globals.Area.Layout[Globals.Glow[0]][Globals.Glow[1]].type == "T" and Space.type == "T" and Globals.Area.Layout[Globals.Glow[0]][Globals.Glow[1]].revealed and Space.revealed and Globals.Purpose == "Move")):
                                                        if Globals.Purpose == None:
                                                                Globals.Screen.blit(Space.view(True), Space.pos)
                                                        elif Globals.Purpose == "Dig0" and (Space.sand > 0 or (not Space.revealed and Globals.Glow == (R, C))):
                                                                Globals.Screen.blit(Space.view(True), Space.pos)
                                                        elif Globals.Purpose == "Dig1" and Space.sand > 0:
                                                                Globals.Screen.blit(Space.view(True), Space.pos)
                                                        elif Globals.Purpose == "Move" and (Space.sand < 2 or Globals.ActivePlayer.name == "Climber") and not (R == Globals.Glow[0] and C == Globals.Glow[1]):
                                                                Globals.Screen.blit(Space.view(True), Space.pos)
                                                        elif Globals.Purpose == "DuneBlaster" and Space.sand > 0:
                                                                Globals.Screen.blit(Space.view(True), Space.pos)
                                                        else:
                                                                Globals.Screen.blit(Space.view(False), Space.pos)
                                                else:
                                                        Globals.Screen.blit(Space.view(False), Space.pos)
                                        else:
                                                Globals.Screen.blit(Space.view(False), Space.pos)
                                        pic = pygame.Surface((100, 100))
                                        pic.fill((255, 255, 255))
                                        pic.set_colorkey((255, 255, 255))
                                        if Space.sand == 1:
                                                pic.blit(Globals.SandOpen, (5, 5))
                                                Globals.Screen.blit(pic, Space.pos )
                                        elif Space.sand > 1:
                                                pic.blit(Globals.SandBlocked, (5, 5))
                                                QuantRect = pygame.Rect(57, 40, 10, 20)
                                                Quant = Globals.Font_Small.render(str(Space.sand), False, (131, 71, 64))
                                                pic.blit(Quant, QuantRect)
                                                Globals.Screen.blit(pic, Space.pos )
                                        if Space.treasure != None:
                                                Space.treasure.row = R
                                                Space.treasure.column = C
                                                Space.treasure.view(Globals.Screen, Space.player != None)
                                                shift = 50
                                        else: shift = 25
                                        if len(Space.player) > 0:
                                                j = 0
                                                for pawn in Space.player:
                                                        pawnpos = (Space.pos[0] + 5 + (90 / len(Space.player)) * j + 90 / len(Space.player) / 2 - 11.25, Space.pos[1] + shift)
                                                        Globals.Screen.blit(pawn.pawn, pawnpos)
                                                        j += 1
                                        C += 1
                        R += 1
                        C = 0
                Globals.Screen.blit(self.Layout[Storm[0]][Storm[1]].view(False), self.Layout[Storm[0]][Storm[1]].pos)

        # Subroutine to move the storm up one
        def Up(self, Value):
                for i in range(Value):
                        R = 0
                        C = 0
                        for Row in self.Layout:
                                for Space in Row:
                                        if Space.type == "S":
                                                Storm_Pos = (R, C)
                                        C += 1
                                R += 1
                                C = 0
                        if Storm_Pos[0] != 0:
                                Moved_Pos = (Storm_Pos[0] - 1, Storm_Pos[1])
                                Storm = self.Layout[Storm_Pos[0]][Storm_Pos[1]]
                                Moved = self.Layout[Moved_Pos[0]][Moved_Pos[1]]
                                while Moved.pos[1] != Storm.pos[1]:
                                        Moved.pos = (Moved.pos[0], Moved.pos[1] + 2)
                                        Storm.pos = (Storm.pos[0], Storm.pos[1] - 2)
                                        Display.Update(Pos=False)
                                Moved.sand += 1
                                for x in range(0, 25):
                                        Moved.pos = (Moved.pos[0], Moved.pos[1] + 2)
                                        Storm.pos = (Storm.pos[0], Storm.pos[1] - 2)
                                        Display.Update(Pos=False)
                                self.Layout[Moved_Pos[0]][Moved_Pos[1]] = Storm
                                self.Layout[Storm_Pos[0]][Storm_Pos[1]] = Moved
                                Display.Update()
                for Item in Globals.Treasures:
                        Item.update()
                        
        # Subroutine to move the storm down one
        def Down(self, Value):
                for i in range(Value):
                        R = 0
                        C = 0
                        for Row in self.Layout:
                                for Space in Row:
                                        if Space.type == "S":
                                                Storm_Pos = (R, C)
                                        C += 1
                                R += 1
                                C = 0
                        if Storm_Pos[0] != 4:
                                Moved_Pos = (Storm_Pos[0] + 1, Storm_Pos[1])
                                Storm = self.Layout[Storm_Pos[0]][Storm_Pos[1]]
                                Moved = self.Layout[Moved_Pos[0]][Moved_Pos[1]]
                                while Moved.pos[1] != Storm.pos[1]:
                                        Moved.pos = (Moved.pos[0], Moved.pos[1] - 2)
                                        Storm.pos = (Storm.pos[0], Storm.pos[1] + 2)
                                        Display.Update(Pos=False)
                                Moved.sand += 1
                                for x in range(0, 25):
                                        Moved.pos = (Moved.pos[0], Moved.pos[1] - 2)
                                        Storm.pos = (Storm.pos[0], Storm.pos[1] + 2)
                                        Display.Update(Pos=False)
                                self.Layout[Moved_Pos[0]][Moved_Pos[1]] = Storm
                                self.Layout[Storm_Pos[0]][Storm_Pos[1]] = Moved
                                Display.Update()
                        
        # Subroutine to move the storm left one
        def Left(self, Value):
                for i in range(Value):
                        R = 0
                        C = 0
                        for Row in self.Layout:
                                for Space in Row:
                                        if Space.type == "S":
                                                Storm_Pos = (R, C)
                                        C += 1
                                R += 1
                                C = 0
                        if Storm_Pos[1] != 0:
                                Moved_Pos = (Storm_Pos[0], Storm_Pos[1] - 1)
                                Storm = self.Layout[Storm_Pos[0]][Storm_Pos[1]]
                                Moved = self.Layout[Moved_Pos[0]][Moved_Pos[1]]
                                while Moved.pos[0] != Storm.pos[0]:
                                        Moved.pos = (Moved.pos[0] + 2, Moved.pos[1])
                                        Storm.pos = (Storm.pos[0] - 2, Storm.pos[1])
                                        Display.Update(Pos=False)
                                Moved.sand += 1
                                for x in range(0, 25):
                                        Moved.pos = (Moved.pos[0] + 2, Moved.pos[1])
                                        Storm.pos = (Storm.pos[0] - 2, Storm.pos[1])
                                        Display.Update(Pos=False)
                                self.Layout[Moved_Pos[0]][Moved_Pos[1]] = Storm
                                self.Layout[Storm_Pos[0]][Storm_Pos[1]] = Moved
                                Display.Update()
                        
        # Subroutine to move the storm right one
        def Right(self, Value):
                for i in range(Value):
                        R = 0
                        C = 0
                        for Row in self.Layout:
                                for Space in Row:
                                        if Space.type == "S":
                                                Storm_Pos = (R, C)
                                        C += 1
                                R += 1
                                C = 0
                        if Storm_Pos[1] != 4:
                                Moved_Pos = (Storm_Pos[0], Storm_Pos[1] + 1)
                                Storm = self.Layout[Storm_Pos[0]][Storm_Pos[1]]
                                Moved = self.Layout[Moved_Pos[0]][Moved_Pos[1]]
                                while Moved.pos[0] != Storm.pos[0]:
                                        Moved.pos = (Moved.pos[0] - 2, Moved.pos[1])
                                        Storm.pos = (Storm.pos[0] + 2, Storm.pos[1])
                                        Display.Update(Pos=False)
                                Moved.sand += 1
                                for x in range(0, 25):
                                        Moved.pos = (Moved.pos[0] - 2, Moved.pos[1])
                                        Storm.pos = (Storm.pos[0] + 2, Storm.pos[1])
                                        Display.Update(Pos=False)
                                self.Layout[Moved_Pos[0]][Moved_Pos[1]] = Storm
                                self.Layout[Storm_Pos[0]][Storm_Pos[1]] = Moved
                                Display.Update()

# Class to store and manage the storm meter
class Meter:
        def __init__(self, players, level):
                if players < 4: self.image = Globals.Meter0
                else: self.image = Globals.Meter1
                self.level = level
                self.intensity = 3
                if players == 2:
                        self.level += Globals.Difficulty + 2
                        if self.level == 2: self.intensity = 2
                if players == 3 or players == 4:
                        self.level += Globals.Difficulty + 1
                        if self.level == 1: self.intensity = 2
                if players == 5:
                        self.level += Globals.Difficulty
                        if self.level == 0: self.intensity = 2
                if players >= 4:
                        self.scale = 15
                        self.start = 26
                else:
                        self.scale = 14.9
                        self.start = 24
                Globals.StormLevel = self.level
                self.pos = (Globals.ScreenW - 50 - self.image.get_size()[0], Globals.ScreenH / 2 - 10)

        # Subroutine to re-initialise the meter
        def reinit(self, players, level):
                if players < 4: self.image = Globals.Meter0
                else: self.image = Globals.Meter1
                self.level = level
                self.intensity = 3
                if players == 2:
                        self.level += Globals.Difficulty + 2
                        if self.level == 2: self.intensity = 2
                if players == 3 or players == 4:
                        self.level += Globals.Difficulty + 1
                        if self.level == 1: self.intensity = 2
                if players == 5:
                        self.level += Globals.Difficulty
                        if self.level == 0: self.intensity = 2
                if players >= 4:
                        self.scale = 15
                        self.start = 26
                else:
                        self.scale = 14.9
                        self.start = 24
                Globals.StormLevel = self.level
                self.pos = (Globals.ScreenW - 50 - self.image.get_size()[0], Globals.ScreenH / 2 - 10)

        # Subroutine to display the meter
        def update(self):
                self.level = Globals.StormLevel
                if self.level >= 13: self.intensity = 6
                elif self.level >= 10: self.intensity = 5
                elif self.level >= 6: self.intensity = 4
                elif self.level >= 3 and len(Globals.Adventurers) == 2: self.intensity = 3
                elif self.level >= 2 and len(Globals.Adventurers) < 5 and len(Globals.Adventurers) != 2: self.intensity = 3
                elif self.level >= 1 and len(Globals.Adventurers) == 5: self.intensity = 3
                else: self.intensity = 2
                Globals.StormIntensity = self.intensity
                Image = self.image.copy()
                Level = Globals.Level.copy()
                if len(Globals.Adventurers) == 2 or len(Globals.Adventurers) == 4:
                        x = 0
                else:
                        x = self.image.get_size()[0] - Globals.Level.get_size()[0]
                        Level = pygame.transform.flip(Level, True, False)
                Image.blit(Level, (x, (14 - self.level) * self.scale + self.start))
                Globals.Screen.blit(Image, self.pos)
                
