# final project 1 sem
Creating a game "MIPTario"


Documentation for main.py

class Profile(object, DataBase)
    # init features before the game started

  def __init__(self)
      # init started profile`s value

  def alert(self)
      # create greeting title

  def basicMenu(self)
      # create main game menu    

  def get_users(self)
      # init data base with all players

  def play(self)
      # record name, time the game played ang rating achieved for player


class MarioGame(object)
    # init main options of the game

  def __init__(self, Profile)
      # init started profile`s value

  def init(self)
      # init screen features

  def init_map(self, map_file, new_pos, first_time)
      """ init map features: set coinboxs, bricks, coins, enemies on the map,  

      define layer order: background, midground + sprites, foreground

      map_file - tmx file creating map
      first_time - condition for first attempt """
     
  def run(self)
      # main game loop; features: time counter, game exit, screen update

  def draw(self, screen)
      """ draw objects on the screen; represent name, score of the player;
      create screen for 'dead' condition

      screen - surface"""

  def draw_debug(self, screen)
      # create screen (surface) for condition 'dead'

  def handle(self, event) 
      # event handling

  def draw_profile_username(self, screen)
      # dislay player name on screen (surface)

  def draw_score_texts(self, screen)
      # draw score of the current and previous players

  def draw_gameover_screen(self, screen)
      # draw gameover screen on screen (surface)

  def draw_dying_screen(self, screen)
      # draw surface on screen (surface) when condition is 'dead'

  def __del__(self)
      """ uploaded collected coins into base data; 
      choosing max of these current rating and old rating """
      
