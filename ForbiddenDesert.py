# Forbidden Desert board game digitalisation

# Initialising pygame and the RNG
import pygame, random
pygame.init()
pygame.display.init()

# Import the other files
import Globals, Display, Controls

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
