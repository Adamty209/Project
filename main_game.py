# main.py
import pygame
import sys
from entities import Player, NPC
from ai_module import get_npc_response

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width, screen_height = 1200, 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dialogues of Destiny")

# Load background image
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (screen_width, screen_height))

# Create a player instance
player_sprite = pygame.image.load('player.png').convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (75, 75))
player = Player(864, 819, screen_width, screen_height)
player.sprite = player_sprite

# Create an NPC instance
npc_sprite = pygame.image.load('npc.png').convert_alpha()
npc_sprite = pygame.transform.scale(npc_sprite, (75, 75))
npc = NPC(453, 835)
npc.sprite = npc_sprite  # Assuming the NPC is 50x50 in size

# Set up font for dialogue
font = pygame.font.Font(None, 20)

# Set up platform
platform_height = 50
platform_rect = pygame.Rect(0, screen_height - platform_height, screen_width, platform_height)

def display_dialogue(text, screen, npc, color=(255, 255, 255)):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if font.size(current_line + word)[0] < 250:  # 150 is the max width for each line
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    # Display dialogue text
    dialogue_y = npc.rect.top - (len(lines) * (font.get_height() + 2)) - 10
    for line in lines:
        dialogue_surface = font.render(line, True, color)
        dialogue_x = npc.rect.centerx - dialogue_surface.get_width() // 2
        screen.blit(dialogue_surface, (dialogue_x, dialogue_y))
        dialogue_y += font.get_height() + 2  # Add some spacing between lines

def display_player_input(text, screen, player, color=(255, 255, 255)):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if font.size(current_line + word)[0] < 250:  # 150 is the max width for each line
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    # Display player input text below the player
    dialogue_y = player.rect.bottom + 10
    for line in lines:
        dialogue_surface = font.render(line, True, color)
        dialogue_x = player.rect.centerx - dialogue_surface.get_width() // 2
        screen.blit(dialogue_surface, (dialogue_x, dialogue_y))
        dialogue_y += font.get_height() + 2

def player_npc_interaction(player_input):
    global running
    global npc_behavior
    global last_npc_dialogue

    # Append player input to a text file
    with open('conversation_log.txt', 'a') as file:
        file.write(f'Player: {player_input}\n')
    
    # Read entire conversation from the text file to use as prompt
    try:
        with open('conversation_log.txt', 'r') as file:
            conversation = file.read()
    except FileNotFoundError:
        conversation = ''
    
    # Generate NPC response
    full_prompt = f"{conversation}NPC replies to the player."
    last_npc_dialogue = get_npc_response(full_prompt)
    if not last_npc_dialogue:
        last_npc_dialogue = "I'm not sure how to respond to that."
    
    # Sentiment analysis to determine behavior
    sentiment_prompt = f"The player says: '{player_input}'. Is this behavior good, bad, or neutral? Respond with either 'good', 'bad', or 'neutral'."
    sentiment = get_npc_response(sentiment_prompt).strip().lower()
    if sentiment not in ['good', 'bad', 'neutral']:
        sentiment = 'neutral'

    # Update NPC behavior based on sentiment
    if sentiment == 'good':
        npc_behavior += 1
    elif sentiment == 'bad':
        npc_behavior -= 1

    # If behavior reaches -3, NPC shoots and displays a gun image
    if npc_behavior == -3:
        last_npc_dialogue = "Time to die!"
        display_dialogue(last_npc_dialogue, screen, npc, color=(255, 0, 0))
        pygame.display.flip()
        pygame.time.delay(1000)  # Pause for dramatic effect

        # Load and display gun image at specified position
        gun_image = pygame.image.load('gun.png').convert_alpha()
        gun_image = pygame.transform.scale(gun_image, (20, 20))
        gun_position = (513, 871)
        screen.blit(gun_image, gun_position)
        pygame.display.flip()

        # Shoot a small bullet to the right
        bullet_rect = pygame.Rect(gun_position[0] + 50, gun_position[1] + 25, 10, 5)
        bullet_color = (255, 0, 0)
        for _ in range(50):  # Move the bullet 50 times to the right
            bullet_rect.x += 10
            screen.blit(background, (0, 0))
            pygame.draw.rect(screen, (139, 69, 19), platform_rect)  # Draw the platform
            screen.blit(player.sprite, (player.rect.x, player.rect.y))
            screen.blit(npc.sprite, (npc.rect.x, npc.rect.y))
            screen.blit(gun_image, gun_position)
            pygame.draw.rect(screen, bullet_color, bullet_rect)  # Draw the bullet
            pygame.display.flip()
            pygame.time.delay(50)  # Delay for bullet animation

        # Wait for 5 seconds, then close the game
        pygame.time.delay(5000)
        running = False

    # If behavior reaches +3, NPC gives a gift and displays reward message and ring
    if npc_behavior == 3:
        last_npc_dialogue = "Here, take this ring as a gift."
        display_dialogue(last_npc_dialogue, screen, npc, color=(255, 0, 0))
        pygame.display.flip()
        pygame.time.delay(1000)  # Pause for dramatic effect

        reward_text = "YOU RECEIVED A RARE RING"
        reward_font = pygame.font.Font(None, 52)
        reward_surface = reward_font.render(reward_text, True, (128, 0, 128))
        reward_rect = reward_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(reward_surface, reward_rect)

        # Load and display ring image below the text
        ring_image = pygame.image.load('ring.png').convert_alpha()
        ring_image = pygame.transform.scale(ring_image, (100, 100))
        ring_rect = ring_image.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(ring_image, ring_rect)

        pygame.display.flip()
        pygame.time.delay(2000)  # Display reward for 2 seconds

        # Decrease behavior to 2 after giving the ring
        npc_behavior = 2

        
    # Neutral behavior does not change the value
    npc_behavior = max(-3, min(3, npc_behavior))  # Keep behavior value between -3 and 3

    # Write updated behavior to the file
    with open('npc_behavior.txt', 'w') as file:
        file.write(str(npc_behavior))

    # Append NPC response to the text file
    with open('conversation_log.txt', 'a') as file:
        file.write(f'NPC: {last_npc_dialogue}\n')

# Add initial NPC dialogue to the conversation log
with open('conversation_log.txt', 'w') as file:
    file.write("NPC: You meet an NPC by the name of Erwin who congratulates you on playing DIALOGUES OF DESTINY who says: What do they say next?\n")

# Initialize NPC behavior
with open('npc_behavior.txt', 'w') as file:
    file.write('0')

# Main game loop
running = True
last_npc_dialogue = ""
input_active = False
player_input = ""

while running:
    # Read NPC behavior value
    try:
        with open('npc_behavior.txt', 'r') as file:
            npc_behavior = int(file.read().strip())
    except FileNotFoundError:
        npc_behavior = 0
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Clear the conversation log when exiting the game
            try:
                with open('conversation_log.txt', 'w') as file:
                    file.truncate()
            except FileNotFoundError:
                pass
            try:
                with open('npc_behavior.txt', 'w') as file:
                    file.truncate()
            except FileNotFoundError:
                pass
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and player.rect.colliderect(npc.rect.inflate(100, 100)):
            player_input = ''
            input_active = True

        while input_active and running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    input_active = False
                    running = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RETURN:
                        player_npc_interaction(player_input)
                        input_active = False
                    elif ev.key == pygame.K_BACKSPACE:
                        player_input = player_input[:-1]
                    else:
                        player_input += ev.unicode

            screen.blit(background, (0, 0))
            pygame.draw.rect(screen, (139, 69, 19), platform_rect)  # Draw the platform
            screen.blit(player.sprite, (player.rect.x, player.rect.y))
            screen.blit(npc.sprite, (npc.rect.x, npc.rect.y))

            # Display player input below the player while typing
            if input_active:
                display_player_input(player_input, screen, player, color=(0, 0, 255))

            # Display player and NPC coordinates
            player_position_text = f"Player Position: ({player.rect.x}, {player.rect.y})"
            npc_position_text = f"NPC Position: ({npc.rect.x}, {npc.rect.y})"

            player_position_surface = font.render(player_position_text, True, (255, 255, 255))
            npc_position_surface = font.render(npc_position_text, True, (255, 255, 255))

            screen.blit(player_position_surface, (10, 10))  # Display player coordinates at the top-left
            screen.blit(npc_position_surface, (10, 30))  # Display NPC coordinates below player coordinates

            pygame.display.flip()
    
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player.rect.colliderect(npc.rect.inflate(100, 100)):
            prompt = "You meet an NPC by the name of Erwin who congratulates you on playing DIALOGUES OF DESTINY who says: {} What do they say next?".format(npc.dialogue)
            last_npc_dialogue = get_npc_response(prompt)
            if not last_npc_dialogue:
                last_npc_dialogue = "I don't have a response right now."

    # Move and draw the player and NPC
    player.move(keys)
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (139, 69, 19), platform_rect)  # Draw the platform
    player.draw(screen)
    npc.draw(screen)
    # Check if player is near the NPC
    if player.rect.colliderect(npc.rect.inflate(100, 100)):
        if last_npc_dialogue:
            display_dialogue(last_npc_dialogue, screen, npc, color=(255, 0, 0))
        else:
            display_dialogue(npc.dialogue, screen, npc, color=(255, 0, 0))

    # Display NPC behavior below the NPC
    behavior_text = f"Behavior: {npc_behavior}"
    behavior_surface = font.render(behavior_text, True, (255, 255, 255))
    screen.blit(behavior_surface, (npc.rect.centerx - behavior_surface.get_width() // 2, npc.rect.bottom + 10))

    # Display player and NPC coordinates
    player_position_text = f"Player Position: ({player.rect.x}, {player.rect.y})"
    npc_position_text = f"NPC Position: ({npc.rect.x}, {npc.rect.y})"

    player_position_surface = font.render(player_position_text, True, (255, 255, 255))
    npc_position_surface = font.render(npc_position_text, True, (255, 255, 255))

    screen.blit(player_position_surface, (10, 10))  # Display player coordinates at the top-left
    screen.blit(npc_position_surface, (10, 30))  # Display NPC coordinates below player coordinates

    pygame.display.flip()

pygame.quit()
sys.exit()



