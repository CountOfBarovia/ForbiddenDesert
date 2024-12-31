import pygame, Board, Cards, Controls, Display
pygame.init()

# Initialising the tile images
Oasis = pygame.transform.scale(pygame.image.load("Tiles/Oasis.png"), (90, 90))
Dune = pygame.transform.scale(pygame.image.load("Tiles/Desert.png"), (90, 90))
TechSite = pygame.transform.scale(pygame.image.load("Tiles/Tower.png"), (90, 90))
Tunnel = pygame.transform.scale(pygame.image.load("Tiles/Tunnel.png"), (90, 90))
OH = pygame.transform.scale(pygame.image.load("Tiles/Orange_Horizontal.png"), (90, 90))
OV = pygame.transform.scale(pygame.image.load("Tiles/Orange_Vertical.png"), (90, 90))
SH = pygame.transform.scale(pygame.image.load("Tiles/Grey_Horizontal.png"), (90, 90))
SV = pygame.transform.scale(pygame.image.load("Tiles/Grey_Vertical.png"), (90, 90))
RH = pygame.transform.scale(pygame.image.load("Tiles/Red_Horizontal.png"), (90, 90))
RV = pygame.transform.scale(pygame.image.load("Tiles/Red_Vertical.png"), (90, 90))
YH = pygame.transform.scale(pygame.image.load("Tiles/Yellow_Horizontal.png"), (90, 90))
YV = pygame.transform.scale(pygame.image.load("Tiles/Yellow_Vertical.png"), (90, 90))
Pad = pygame.transform.scale(pygame.image.load("Tiles/Launch_Pad.png"), (90, 90))
Crash = pygame.transform.scale(pygame.image.load("Tiles/Crash.png"), (90, 90))
Mirage = pygame.transform.scale(pygame.image.load("Tiles/Mirage.png"), (90, 90))
Well = pygame.transform.scale(pygame.image.load("Tiles/Well.png"), (90, 90))
Storm = pygame.transform.scale(pygame.image.load("Tiles/Storm.png"), (100, 100))

# Anything that can stack onto a tile
SandBlocked = pygame.transform.scale(pygame.image.load("Misc images/Sand_Blocked.png"), (90, 90))
SandOpen = pygame.transform.scale(pygame.image.load("Misc images/Sand_Open.png"), (90, 90))
EnginePic = pygame.transform.scale(pygame.image.load("Misc images/Engine.png"), (40, 40))
EnginePic.set_colorkey((0, 0, 255))
SolarPic = pygame.transform.scale(pygame.image.load("Misc images/Solar.png"), (40, 40))
SolarPic.set_colorkey((0, 0, 255))
WheelPic = pygame.transform.scale(pygame.image.load("Misc images/Wheel.png"), (40, 40))
WheelPic.set_colorkey((0, 0, 255))
PropellerPic = pygame.transform.scale(pygame.image.load("Misc images/Propeller.png"), (40, 40))
PropellerPic.set_colorkey((0, 0, 255))
Aura = pygame.transform.scale(pygame.image.load("Misc images/Glow.png"), (100, 100))
Aura.set_colorkey((0, 0, 255))

# The text
Paper = pygame.image.load("Misc images/Scroll.png")
Font_Small = pygame.font.Font("Windlass.ttf", 21)
SmallScroll = Display.Scroll(Font_Small, [10, 5, 5, 10])
Font_Mid = pygame.font.Font("Windlass.ttf", 40)
MidScroll = Display.Scroll(Font_Mid, [20, 10, 10, 20])
Font_Large = pygame.font.Font("Windlass.ttf", 60)
LargeScroll = Display.Scroll(Font_Large, [30, 15, 15, 30])
Texts = []

# The treasures
Engine = Board.Treasure("Engine")
Propeller = Board.Treasure("Propeller")
Solar = Board.Treasure("Solar")
Wheel = Board.Treasure("Wheel")
Treasures = (Engine, Propeller, Solar, Wheel)
Set = 0
Collected = 0

# The screen and the time tracker
ScreenW = 1000
ScreenH = 625
Screen = pygame.display.set_mode((ScreenW, ScreenH))
Time = pygame.time.Clock()
pygame.display.set_caption("Forbidden Desert")

# Background
if ScreenH / 5 * 8 > ScreenW:
    Back = pygame.transform.scale(pygame.image.load("Misc images/Dunes.jpeg"), (ScreenH / 5 * 8, ScreenH))
else:
    Back = pygame.transform.scale(pygame.image.load("Misc images/Dunes.jpeg"), (ScreenW, ScreenW / 8 * 5))

# Initialising the cards and the decks
CardList = {
    "DuneBlaster" : pygame.image.load("Cards/Tech cards/Dune Blaster.png"),
    "Jetpack" : pygame.image.load("Cards/Tech cards/Jetpack.png"),
    "SecretWaterReserve" : pygame.image.load("Cards/Tech cards/Secret Water Reserve.png"),
    "SolarShield" : pygame.image.load("Cards/Tech cards/Solar Shield.png"),
    "Terrascope" : pygame.image.load("Cards/Tech cards/Terrascope.png"),
    "TimeThrottle" : pygame.image.load("Cards/Tech cards/Time Throttle.png"),
    "TechBack" : pygame.image.load("Cards/Tech cards/TechBack.png"),
    "Up1" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/Up1.png"), (300, 415.5)),
    "Up2" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/Up2.png"), (300, 415.5)),
    "Up3" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/Up3.png"), (300, 415.5)),
    "Left1" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/Left1.png"), (300, 415.5)),
    "Left2" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/Left2.png"), (300, 415.5)),
    "Left3" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/Left3.png"), (300, 415.5)),
    "Down1" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/Down1.png"), (300, 415.5)),
    "Down2" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/Down2.png"), (300, 415.5)),
    "Down3" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/Down3.png"), (300, 415.5)),
    "Right1" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/Right1.png"), (300, 415.5)),
    "Right2" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/Right2.png"), (300, 415.5)),
    "Right3" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/Right3.png"), (300, 415.5)),
    "SunBeatsDown" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/SunBeatsDown.png"), (300, 415.5)),
    "StormPicksUp" : pygame.transform.scale(pygame.image.load("Cards/Storm cards/StormPicksUp.png"), (300, 415.5)),
    "StormBack" : pygame.image.load("Cards/Storm cards/StormBack.png"),
    "Archeologist" : pygame.transform.scale(pygame.image.load("Cards/Player cards/Archeologist.png"), (ScreenH / 1.5 * (2045/2778), ScreenH / 1.5)),
    "Climber" : pygame.transform.scale(pygame.image.load("Cards/Player cards/Climber.png"), (ScreenH / 1.5 * (2034/2778), ScreenH / 1.5)),
    "Explorer" : pygame.transform.scale(pygame.image.load("Cards/Player cards/Explorer.png"), (ScreenH / 1.5 * (2048/2778), ScreenH / 1.5)),
    "Meteorologist" : pygame.transform.scale(pygame.image.load("Cards/Player cards/Meteorologist.png"), (ScreenH / 1.5 * (2009/2778), ScreenH / 1.5)),
    "Navigator" : pygame.transform.scale(pygame.image.load("Cards/Player cards/Navigator.png"), (ScreenH / 1.5 * (2028/2778), ScreenH / 1.5)),
    "WaterCarrier" : pygame.transform.scale(pygame.image.load("Cards/Player cards/Water Carrier.png"), (ScreenH / 1.5 * (2045/2778), ScreenH / 1.5))}
Pawns = {
    "Archeologist" : pygame.image.load("Misc images/RedPawn.png"),
    "Climber" : pygame.image.load("Misc images/BlackPawn.png"),
    "Explorer" : pygame.image.load("Misc images/GreenPawn.png"),
    "Meteorologist" : pygame.image.load("Misc images/WhitePawn.png"),
    "Navigator" : pygame.image.load("Misc images/YellowPawn.png"),
    "WaterCarrier" : pygame.image.load("Misc images/BluePawn.png") }
TechDeck = Cards.Deck_Tech((ScreenW - 240, 10))
TechDeck.Place()
StormDeck = Cards.Deck_Storm((ScreenW - 120, 10))
StormDeck.Place()
TechDiscard = Cards.Deck((ScreenW - 240, 158.5), [])
StormDiscard = Cards.Deck((ScreenW - 120, 158.5), [])
Decks = [TechDeck, StormDeck, TechDiscard, StormDiscard]
Archeologist = Cards.Player("Archeologist")
Climber = Cards.Player("Climber")
Explorer = Cards.Player("Explorer")
Meteorologist = Cards.Player("Meteorologist")
Navigator = Cards.Player("Navigator")
WaterCarrier = Cards.Player("WaterCarrier")
AdventurerCards = Cards.Deck(None, [Archeologist, Climber, Explorer, Meteorologist, Navigator, WaterCarrier])
AdventurerCards.Shuffle()
Adventurers = [Navigator, Explorer, Climber, Archeologist]
ActivePlayer = Adventurers[0]
Actions = 4

# The board
Area = Board.Table()
# Any variables for changing items as the mouse hovers over them
Glow = False
Grow = False
Diagonal = False
Purpose = None
Position = None
PlayerSelect = False

# The Storm Meter
Meter0 = pygame.transform.scale(pygame.image.load("Misc images/Meter0.png"), (ScreenH * 0.5 * 0.37, ScreenH * 0.5))
Meter0.set_colorkey((0, 0, 255))
Meter1 = pygame.transform.scale(pygame.image.load("Misc images/Meter1.png"), (ScreenH * 0.5 * 0.356, ScreenH * 0.5))
Meter1.set_colorkey((0, 0, 255))
StormLevel = 0
Difficulty = 0
StormIntensity = 2
Level = pygame.transform.scale(pygame.image.load("Misc images/Level.png"), (27 * 1.569, 27))
Level.set_colorkey((0, 0, 255))
StormMeter = Board.Meter(len(Adventurers), StormLevel)
CardsToDraw = StormIntensity

# The front-and-centre items
Priority = []

# The action buttons and mouse
MouseImage = pygame.transform.scale(pygame.image.load("Misc images/Cursor.png"), (40, 40))
MouseImage.set_colorkey((0, 0, 255))
pygame.mouse.set_cursor((20, 20), MouseImage)
MouseColl = Controls.CollRect(pygame.mouse.get_pos(), (1, 1))
SpecialButtonImg = pygame.image.load("Misc images/SpecialButton.png")
SpecialButton = Controls.Button(SpecialButtonImg, (800, 320))
MoveButtonImg = pygame.image.load("Misc images/MoveButton.png")
MoveButton = Controls.Button(MoveButtonImg, (800, 385))
DigButtonImg = pygame.image.load("Misc images/DigButton.png")
DigButton = Controls.Button(DigButtonImg, (800, 450))
CancelButtonImg = pygame.image.load("Misc images/CancelButton.png")
CancelButton = Controls.Button(CancelButtonImg, (800, 320))
SuccessButtonImg = pygame.image.load("Misc images/SuccessButton.png")
SuccessButton = Controls.Button(SuccessButtonImg, (800, 515))
Buttons = pygame.sprite.Group(MoveButton, DigButton, SpecialButton)

Won = False
Deaded = False
