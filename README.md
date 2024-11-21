
## **Memory Game 🎮 **

This is a memory game implemented using Python's `turtle` graphics library. The player flips cards to find matching pairs, and the game supports dynamic card sets, customizable configurations, and a leaderboard to track the best scores. You can even add personalized cards for family or fandom!

---

### **Features**
1. **Dynamic Card Decks**:
   - Supports multiple card themes, such as `default`, `dog`, and `programming_languages`.
   - Allows users to easily add new card sets by modifying a configuration file (`config.txt`).

2. **Customizable Gameplay**:
   - Choose the number of cards to play with: 8, 10, or 12.
   - Dynamically loads user-specified card sets.

3. **Interactive UI**:
   - Buttons for `Quit` and `New Game`.
   - Displays a leaderboard with the top 5 players and their scores.

4. **Personalization**:
   - Add your own custom card sets with your favorite images! Create family sets or fan sets—anything goes.

---

### **Libraries Used**
1. **`turtle`**:
   - For drawing the game interface and handling user interactions.
2. **`random`**:
   - For shuffling the card deck.
3. **`os`**:
   - For handling file and directory operations.
4. **`configparser`**:
   - For managing dynamic card set configurations.

---

### **Adding a Custom Card Set 🌈**
Want to add your own cards to the game? It's simple! 😁

1. **Prepare Your Card Images**:
   - Create **6 card images** in `.gif` format for the front of the cards.
   - Create **1 back image** named `card_back.gif`.
   - Each image should be resized to **75x120 pixels** for optimal display.(The card is set to 70, 100 on the screen, but if it is strict, it will appear smaller on the screen...)

2. **Organize Your Files**:
   - Create a folder under `assets/cards` for your new card set.
   - Add all 7 images (6 front + 1 back) into this folder.(**The back card must be named `card_back.gif`**)

3. **Update `config.txt`**:
   - Open the `config.txt` file in the project root.
   - Add a new section with the name of your card set and the path to your folder. For example:
     ```ini
     [my_custom_set]
     path = assets/cards/my_custom_set
     description = A personalized card set for my family and friends
     ```

4. **Test Your New Set**:
   - Launch the game.
   - Select your new card set by its number during the card set selection step.
   - Enjoy your personalized card game!

---

### **Configuration File Example**
Here’s how the `config.txt` file looks after adding a custom card set:

```ini
[default]
path = assets/cards/default
description = The default card set

[dog]
path = assets/cards/dog
description = Dog-themed card set

[programming_languages]
path = assets/cards/programming_languages
description = Programming languages card set

[my_custom_set]
path = assets/cards/my_custom_set
description = A personalized card set for my family and friends
```

---

### **Instructions for Adding Cards**
1. **Pick a Theme**:
   - Whether it's family, fandom, or something fun, choose 6 images to represent the theme.

2. **Resize Images**:
   - Resize the images to **75x120 pixels**. This ensures that the cards fit nicely in the game grid.

3. **Organize Files**:
   - Place the 6 front card images and the `card_back.gif` in a folder under `assets/cards`.

4. **Modify Configurations**:
   - Add a new section to the `config.txt` file for your card set.

5. **Dynamic Loading**:
   - The game automatically detects and dynamically loads your new card set based on the configuration.

---

### **Example Use Cases**
- **Family-Themed Set**:
  - Create a card set with pictures of your family members.
- **Fan Card Set**:
  - Add your favorite K-pop idols or celebrities.
- **Pet Set**:
  - Use adorable pictures of your pets.

---

### **Gameplay**
1. **Start the Game**:
   - Run the `memory_game.py` script.
   - Enter your name and choose a card set and card count.

2. **Flip Cards**:
   - Click on the cards to reveal their faces.
   - Match pairs to win!

3. **New Game**:
   - Click the `New Game` button to restart with a new configuration.

4. **Quit**:
   - Click the `Quit` button to exit.

---

Enjoy playing and customizing your Memory Game! 🎉
