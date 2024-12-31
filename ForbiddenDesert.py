# Forbidden Desert board game digitalisation

# Initialising pygame and the RNG
import pygame, random
pygame.init()
pygame.display.init()

# Import the other files
import Globals, Display, Controls

# Initialising loop
Started = False
Title = Display.Text("Forbidden Desert#", (Globals.ScreenW / 2, Globals.ScreenH / 3), True, (0, 0, 0), Globals.LargeScroll)
Title.Output()
Players = 2
PlayerText = Display.Text(str(Players) + "#", (Globals.ScreenW / 2, Globals.ScreenH / 3 * 2), True, (0, 0, 0), Globals.MidScroll)
PlayerText.Output()
while not Started:
        # Update the position of the mouse
        Globals.MouseColl.rect.topleft = pygame.mouse.get_pos()
        # The background
        Globals.Screen.blit(Globals.Back, (0, 0))
        # Draw any text
        for item in Globals.Texts:
                item.Output()      
        pygame.display.update()
        Globals.Time.tick(40)

# Main program
Display.Update()
while not Globals.Won and not Globals.Deaded:
        for player in range(len(Globals.Adventurers)):
                Globals.CardsToDraw = Globals.StormIntensity
                Globals.ActivePlayer = Globals.Adventurers[player]
                Globals.Actions = 4
                while Globals.Actions > 0:
                        Prompt = Display.Text("Player " + str(player + 1) + "! Actions: " + str(Globals.Actions) + "#", (Globals.ScreenW / 2, Globals.ScreenH - 30), True, (0, 0, 0), Globals.MidScroll)
                        Prompt.Output()
                        Controls.Find(False, "Control")
                        Prompt.Delete()
                        Globals.Actions -= 1
                Controls.Wait()
                Globals.StormDeck.Draw(Globals.CardsToDraw)
        Display.Update()

Controls.Wait()
