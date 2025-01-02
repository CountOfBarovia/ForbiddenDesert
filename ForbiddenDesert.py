# Forbidden Desert board game digitalisation

# Initialising pygame and the RNG
import pygame, random, sys
pygame.init()
pygame.display.init()

# Import the other files
import Globals, Display, Controls

# Initialising loop
Started = False
Title = Display.Text("Forbidden Desert#", (Globals.ScreenW / 2, Globals.ScreenH / 3), False, (255, 255, 255), Globals.LargeScroll)
Title.Output()
Prompt = Display.Text("Players:#", (Globals.ScreenW / 2, Globals.ScreenH / 2 + 50), False, (255, 255, 255), Globals.MidScroll)
Prompt.Output()
Players = 2
PlayerText = Display.Text(str(Players) + "#", (Globals.ScreenW / 2, Globals.ScreenH / 3 * 2), False, (255, 255, 255), Globals.MidScroll)
PlayerText.Output()
pygame.display.update()
while not Started and not Globals.QUIT:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                        if Globals.LeftArrow.hover:
                                Players -= 1
                                PlayerText.text = str(Players) + "#"
                        if Globals.RightArrow.hover:
                                Players += 1
                                PlayerText.text = str(Players) + "#"
                        if Globals.EnterButton.hover: Started = True
        # Update the position of the mouse
        Globals.MouseColl.rect.topleft = pygame.mouse.get_pos()
        # The background
        Globals.Screen.blit(Globals.WoodenBack, (0, 0))
        # The buttons
        if Players > 2:
                Globals.LeftArrow.update()
                Globals.Screen.blit(Globals.LeftArrow.image, Globals.LeftArrow.rect)
        else: Globals.LeftArrow.hover = False
        if Players < 4:
                Globals.RightArrow.update()
                Globals.Screen.blit(Globals.RightArrow.image, Globals.RightArrow.rect)
        else: Globals.RightArrow.hover = False
        Globals.EnterButton.update()
        Globals.Screen.blit(Globals.EnterButton.image, (Globals.EnterButton.rect.centerx - Globals.EnterButton.image.get_size()[0] / 2, Globals.EnterButton.rect.top))
        # Draw any text
        for item in Globals.Texts:
                item.Output()
        pygame.display.update()
        Globals.Time.tick(40)

# Clear the texts
Globals.Texts = []

# Randomly assign player cards
for i in range(0, Players):
        index = random.randint(0, len(Globals.AdventurerCards.contents) - 1)
        Globals.Adventurers.append(Globals.AdventurerCards.contents[index])
        Globals.AdventurerCards.contents.pop(index)
for row in Globals.Area.Layout:
        for tile in row:
                if tile.type == "C":
                        for player in Globals.Adventurers:
                                tile.player.append(player)
Globals.StormMeter.reinit(len(Globals.Adventurers), Globals.StormLevel)

# Main program
Display.Update()
while not Globals.Won and not Globals.Deaded and not Globals.QUIT:
        for player in range(len(Globals.Adventurers)):
                Globals.CardsToDraw = Globals.StormIntensity
                Globals.ActivePlayer = Globals.Adventurers[player]
                Globals.Actions = 4
                while Globals.Actions > 0 and not Globals.QUIT:
                        Prompt = Display.Text("Player " + str(player + 1) + "! Actions: " + str(Globals.Actions) + "#", (Globals.ScreenW / 2, Globals.ScreenH - 30), True, (0, 0, 0), Globals.MidScroll)
                        Prompt.Output()
                        Controls.Find(False, "Control")
                        Prompt.Delete()
                        Globals.Actions -= 1
                Controls.Wait()
                if not Globals.QUIT:
                        Globals.StormDeck.Draw(Globals.CardsToDraw)
        if not Display.Update():
                break

while Globals.Won:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP: Globals.Won = False
        # Create a scenic outro
        Congrats = Display.Text("YOU WIN!#", (Globals.ScreenW / 2, Globals.ScreenH / 4), False, (0, 0, 0), Globals.LargeScroll)
        Globals.Screen.blit(Globals.Sky, (0, 0))
        Globals.Screen.blit(Globals.Ship, Globals.ShipRect)
        for Text in Globals.Texts: Text.Output()
        pygame.display.update()
        Globals.Time.tick(40)

while Globals.Deaded:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP: Globals.Deaded = False
        # A friendly skull
        Death = Display.Text(Globals.Reason, (Globals.ScreenW / 2, Globals.ScreenH * 4/5), False, (163, 47, 39), Globals.LargeScroll)
        Globals.Screen.blit(Globals.HostileDesert, (Globals.ScreenW / 2 - Globals.HostileDesert.get_size()[0] / 2, 0))
        for Text in Globals.Texts: Text.Output()
        pygame.display.update()
        Globals.Time.tick(40)

Globals.Texts = []

Controls.Wait()
