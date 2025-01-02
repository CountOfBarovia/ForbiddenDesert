import pygame, Globals, sys

class Scroll:
        def __init__(self, Font, buff):
                self.font = Font
                self.image = Globals.Paper
                self.buff = buff

        # Subroutine to display an onscreen message
        def Post(self, text, pos, back, col):
                lines = []
                for i in range(text.count("#")):
                        lines.append(text[0:text.find("#")])
                        text = text[text.find("#") + 1:len(text)]
                        w, h = self.font.size(lines[0])
                        for line in lines:
                                if self.font.size(line)[0] > w:
                                        w, h = self.font.size(line)     
                h += 2
                h *= len(lines)
                buff = self.buff
                if back:
                        pic = pygame.transform.scale(self.image, (w + self.buff[1] + self.buff[3], h + self.buff[0] + self.buff[2]))
                        push = 0
                        for line in lines:
                                textpic = self.font.render(line, True, col)
                                width = self.font.size(line)[0]
                                pic.blit(textpic, (buff[3] + (w - width) / 2, buff[0] + push))
                                push += h / len(lines) - 2
                else:
                        pic = pygame.Surface((w + self.buff[1] + self.buff[3], h + self.buff[0] + self.buff[2]), pygame.SRCALPHA)
                        push = 0
                        for line in lines:
                                textpic = self.font.render(line, True, col)
                                width = self.font.size(line)[0]
                                pic.blit(textpic, (buff[3] + (w - width) / 2, buff[0] + push))
                                push += h / len(lines) - 2                                
                pic.set_colorkey((0, 0, 255))
                Globals.Screen.blit(pic, (pos[0] - pic.get_size()[0] / 2, pos[1] - pic.get_size()[1] / 2))

class Text:
        def __init__(self, text, pos, back, col, font):
                self.text = text
                self.pos = pos
                self.back = back
                self.col = col
                self.font = font
                Globals.Texts.append(self)
        
        def Output(self):
                self.font.Post(self.text, self.pos, self.back, self.col)

        def Delete(self):
                Globals.Texts.remove(self)

def Update(**Effects):
        # Check whether the game is over
        if Globals.Won or Globals.Deaded:
                return False
        # Update the position of the mouse
        Globals.MouseColl.rect.topleft = pygame.mouse.get_pos()
        # The background
        Globals.Screen.blit(Globals.Back, (0, 0))
        # Can items be selected?
        if Globals.Grow:
                Globals.Buttons.update()
                Globals.Buttons.draw(Globals.Screen)
                pos = Globals.ActivePlayer.Locate()
                ActiveTile = Globals.Area.Layout[pos[0]][pos[1]]
                Winning = 0
                if ActiveTile.sand >= 2 and not Globals.Climber in ActiveTile.player:
                        Globals.Buttons.empty()
                        Globals.Buttons.add(Globals.DigButton)
                else: Globals.Buttons = pygame.sprite.Group(Globals.MoveButton, Globals.DigButton)
                if (Globals.ActivePlayer.name == "Meteorologist" and Globals.CardsToDraw > 0) or (Globals.ActivePlayer.name == "Water Carrier" and ActiveTile.type == "W" and ActiveTile.revealed) or Globals.ActivePlayer.name == "Navigator":
                        Globals.Buttons.add(Globals.SpecialButton)
                for i in Globals.Treasures:
                        if i.collected:
                                Winning += 1
                if not Globals.Buttons.has(Globals.SuccessButton) and ((ActiveTile.treasure != None and ActiveTile.sand == 0) or (ActiveTile.type == "P" and ActiveTile.sand == 0 and Winning == 4 and len(ActiveTile.player) == len(Globals.Adventurers))):
                        Globals.Buttons.add(Globals.SuccessButton)
                elif Globals.Buttons.has(Globals.SuccessButton) and not ((ActiveTile.treasure != None and ActiveTile.sand == 0) or (ActiveTile.type == "P" and ActiveTile.sand == 0 and Winning == 4 and len(ActiveTile.player) == len(Globals.Adventurers))):
                        Globals.Buttons.remove(Globals.SuccessButton)
                for player in Globals.Adventurers:
                        if pygame.sprite.collide_rect(player.collrect, Globals.MouseColl): player.hover = True
                        else: player.hover = False
                        if pygame.sprite.collide_rect(player.handcollrect, Globals.MouseColl) and len(player.hand.contents) > 0: player.handhover = True
                        else: player.handhover = False
        else:
                for player in Globals.Adventurers:
                       if player in Globals.Priority:
                                player.hover = False
                                player.handhover = False
        if Globals.PlayerSelect:
                for player in Globals.Adventurers:
                        if pygame.sprite.collide_rect(player.collrect, Globals.MouseColl) and not (Globals.ActivePlayer.name == "Navigator" and player.name == "Navigator"):
                                if Globals.Purpose == "Jetpack":
                                        Position = Globals.User.Locate()
                                        if Globals.User != player and player in Globals.Area.Layout[Position[0]][Position[1]].player: player.hover = True
                                else: player.hover = True
                        else: player.hover = False
        elif not Globals.Grow:
            for player in Globals.Adventurers:
                player.hover = False
        if Globals.Glow or Globals.PlayerSelect:
                Globals.CancelButton.update()
                Globals.Screen.blit(Globals.CancelButton.image, Globals.CancelButton.rect.topleft)
        # Locate the treasure items
        for item in Globals.Treasures:
                item.update()
        try:
                if Effects["Pos"]:
                        Globals.Area.Position()
        except:
                Globals.Area.Position()
        # Draw the board
        Globals.Area.Draw()
        # Draw the meter
        Globals.StormMeter.update()
        # Display the players
        i = 0
        for item in Globals.Adventurers:
                # Cap their water supplies
                if item.water > item.watercap:
                        item.water = item.watercap
                item.pos = (25, i * (Globals.ScreenH / 5 + 20) + 10)
                item.collrect.rect.update(item.pos, (100, 138.5))
                if Globals.Purpose == "ClimberMove" and (item.Locate() != Globals.ActivePlayer.Locate() or item.name == "Climber"): item.hover = False
                if item.hover and (Globals.PlayerSelect or Globals.Grow):
                        item.pos = (item.pos[0] - 5, item.pos[1] - 5)
                if item.hand_displayed:
                        item.hand_displayed = False
                        item.Display()
                        item.hand_displayed = True
                elif not item in Globals.Priority: item.Display()
                # Display the hands
                item.hand.pos = (133, i * (Globals.ScreenH / 5 + 20) + 10)
                item.handcollrect.rect.update(item.hand.pos, (100, 138.5))
                if item.handhover and Globals.Grow:
                        item.hand.pos = (item.hand.pos[0] - 5, item.hand.pos[1] - 5)
                        item.hand.back = pygame.transform.scale(Globals.CardList["TechBack"], (110, 148.5))
                else: item.hand.back = pygame.transform.scale(Globals.CardList["TechBack"], (100, 138.5))
                if len(item.hand.contents) > 0:
                        item.handcollrect.rect.update(item.hand.pos, item.hand.back.get_size())
                        item.hand.Display(False)
                i += 1
        # Display the decks
        for deck in Globals.Decks:
                deck.Display(False)
        # Draw any text
        for item in Globals.Texts:
                item.Output()       
        # Draw any highlighted items
        for item in Globals.Priority:
                try:
                        item.Display()
                except:
                        try:
                                Grey = pygame.Surface((Globals.ScreenW, Globals.ScreenH))
                                Grey.fill((0, 0, 0))
                                Grey.set_alpha(128)
                                Globals.Screen.blit(Grey, (0, 0))
                                item.Output()
                        except:
                                Grey = pygame.Surface((Globals.ScreenW, Globals.ScreenH))
                                Grey.fill((0, 0, 0))
                                Grey.set_alpha(128)
                                BigImage = pygame.transform.scale(item.image, (200, 200))
                                BigImage.set_colorkey((0, 0, 255))
                                Globals.Screen.blit(Grey, (0, 0))
                                Globals.Screen.blit(BigImage, (Globals.ScreenW / 2 - BigImage.get_size()[0] / 2, Globals.ScreenH / 2 - BigImage.get_size()[1] / 2))
        pygame.display.update()
        Globals.Time.tick(40)
        return True
