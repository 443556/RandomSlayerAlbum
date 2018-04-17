import base64
import datetime
import os
import random
import shutil
import sys
import time
import urllib2

from bs4 import BeautifulSoup
import requests

class RandomSlayerAlbum:

      def __init__(self):
          self.intro()


      def intro(self):
	  
	  self.data_url = "http://www.releaselyrics.com/1807/slayer-evil-has-no-boundaries/"

	  try:
    		req = requests.get(self.data_url)
		assert(req.status_code == 200)
	  except Exception as e: 
		print "ERROR"
		print "If you are seeing this, there has likely been one of the following:" 
		print "404"
		print "'ERR_NAME_NOT_RESOLVED',"
		print "'Server not found' or" 
		print "'Network Error'"
		print "...with the URL from which this script obtains data."
		print "Therefore the webscrape cannot execute."
		print "NIL DESPERANDUM!"
		print "The data has been preserved when the scrape URL was extant."
		print "It lives in the /data/ folder of this repo."
		print "The webscrape code remains in-situ for posterity; refer to the 'get_data()' function. It is not called in this version of the script."
		print "Refer to previous version of this script for orig version of this here 'intro' function."

          self.data_dir = "data"
	  self.albums_dir = "albums/"

          if not os.path.exists(self.albums_dir):
             os.makedirs(self.albums_dir)
          
	  self.generate_randomised_album()


      def get_data(self):
          data_start = time.time()
		
          base_URL = urllib2.Request(self.data_url)
          target = urllib2.urlopen(base_URL)
          base_soup = BeautifulSoup(target)
          release_URLs = base_soup.find_all("a", class_="release-plain")
          album_names = [
                         "SHOW NO MERCY",
                         "HELL AWAITS",
                         "REIGN IN BLOOD",
                         "SOUTH OF HEAVEN",
                         "SEASONS IN THE ABYSS",
                         "DIVINE INTERVENTION",
                         "DIABOLUS IN MUSICA",
                         "GOD HATES US ALL",
                         "CHRIST ILLUSION",
                         "WORLD PAINTED BLOOD"
                         ]

          album_URL_list = []
          album_track_counts = []
          song_URL_list= []

          for item in release_URLs:
              if not "undisputed" in item['href']:
                 album_URL_list.append(item['href'])

          for A in album_URL_list:
              album_URL = urllib2.Request(A)
              target_album = urllib2.urlopen(album_URL)
              album_soup = BeautifulSoup(target_album)
              album_track_links = album_soup.find("div", class_="content-lyrics")
              album_track_hrefs = album_track_links.find_all("a")
              album_track_count = 0
              for ATH in album_track_hrefs:
                  album_track_count += 1
                  if not "explicit-live-version" in ATH['href']:
                     song_URL_list.append(ATH['href'])
              album_track_counts.append(album_track_count)

          all_track_titles = []
          all_track_words = []
          unique_track_words = []
          no_words_in_tracks = []

          for SUL in song_URL_list:
              R = urllib2.Request(SUL)
              T = urllib2.urlopen(R)
              BS = BeautifulSoup(T)
              title = BS.find("h1")
              title = title.text.replace("Lyrics", "")
              title = title.upper()
              all_track_titles.append(title)
              words = BS.find("div", class_="content-lyrics")
              words = words.text.upper()

              no_words_in_track = 0
              illegal_tokens = ["MOC", "DOM", "LIC", "SPEA", "AWA", "LEAD:", "HANNEMAN", "KANNEMAN", "KING", "ARAYA", "/", " / "]

              for W in words.split():
                  W = W.replace("\n", " ")
                  W = W.replace(",", "")
                  W = W.replace(".", "")
                  W = W.replace("!", "")
                  W = W.replace("?", "")
                  W = W.replace(";", "")
                  W = W.replace('"', '')
                  W = W.replace("-", "")
                  W = W.replace("/", "")
                  W = W.replace(" / ", "")
                  W = W.replace(".", "")

                  if not "[" in W and not "]" in W and not "(" in W and not ")" in W and not W in illegal_tokens and W != "":
                     all_track_words.append(W)
                     no_words_in_track += 1
              no_words_in_tracks.append(no_words_in_track)

          ATW_count = 0
          for ATW in all_track_words:
              ATW_count  += 1
              if not ATW in unique_track_words:
                 unique_track_words.append(ATW)

          unique_track_words.sort()

          UTW_count = len(unique_track_words)

          unique = open("unique.txt", "w+")
          all =    open("all.txt", "w+")
          stats =  open("stats.txt", "w+")
          required_data = open("required_data.txt", "w+")

          split_album_names = []
          split_track_titles = []

          for AN in album_names:
              AN = AN.split()
              for item in AN:
                  if not item == "\n" and not item in split_album_names:
                     split_album_names.append(item)

          for ATT in all_track_titles:
              ATT = ATT.split()
              for item in ATT:
                  if not item == "\n" and not item in split_track_titles:
                     split_track_titles.append(item)

          ALBUM_NAMES_TRACK_TITLES_PLUS_UNIQUE_WORDS = split_album_names + split_track_titles + unique_track_words
          ALL_WORDS = split_album_names + split_track_titles + all_track_words

          unique.write("\n".join(ALBUM_NAMES_TRACK_TITLES_PLUS_UNIQUE_WORDS))
          all.write("\n".join(ALL_WORDS))

          fewest_no_tracks = min(album_track_counts)
          greatest_no_tracks = max(album_track_counts)

          stats_list = []

          stats_list.append("Assessed "+str(len(album_URL_list))+" full-length Slayer releases\n")
          stats_list.append("Least no. of words in a Slayer album title: 2\n")
          stats_list.append("Greatest no. of words in a Slayer album title: 4\n")
          stats_list.append("Average no. of words in a Slayer album title: 3\n")

          stats_list.append("Least no of tracks on a Slayer album: "+str(fewest_no_tracks)+"\n")
          stats_list.append("Greatest no of tracks on a Slayer album: "+str(greatest_no_tracks)+"\n")
          stats_list.append("Average no of tracks on a Slayer album: "+str(sum(album_track_counts)/len(album_track_counts))+"\n")

          stats_list.append("Assessed "+str(len(all_track_titles))+" tracks from "+str(len(album_URL_list))+" full-length Slayer releases\n")
          stats_list.append("No. of unique words (including some plural and possesive forms) in all tracks: "+str(UTW_count)+"\n")
          stats_list.append("No. of all words (including repeats, choruses etc) in all tracks, track titles and album titles: "+str(len(ALL_WORDS))+"\n")
          stats_list.append("Least no. of words in a Slayer track: "+str(min(no_words_in_tracks))+"\n")
          stats_list.append("Greatest no. of words in a Slayer track: "+str(max(no_words_in_tracks))+"\n")
          stats_list.append("Average no. of words in a Slayer track is: "+str(sum(no_words_in_tracks)/len(no_words_in_tracks))+"\n\n")

          most_common_words = []
          most_common_words = self.lexical_analysis(ALBUM_NAMES_TRACK_TITLES_PLUS_UNIQUE_WORDS, ALL_WORDS)

          stats_list.append("\nThe 100 most frequently occuring words are: \n")
          for index, MCW in enumerate(most_common_words):
              item = str((index + 1))+". " + MCW
              stats_list.append(item + "\n")

          for SL in stats_list:
              stats.write(SL)

          required_data.write("FEWEST_NO_TRACKS " + str(fewest_no_tracks) + "\n")
          required_data.write("GREATEST_NO_TRACKS " + str(greatest_no_tracks) + "\n")
          required_data.write("FEWEST_TRACK_WORDS " + str(min(no_words_in_tracks)) + "\n")
          required_data.write("GREATEST_TRACK_WORDS " + str(max(no_words_in_tracks)) + "\n")
          required_data.write("NO_UNIQUE_WORDS " + str(len(ALBUM_NAMES_TRACK_TITLES_PLUS_UNIQUE_WORDS)) + "\n")
          required_data.write("NO_ALL_WORDS " + str(len(ALL_WORDS)) + "\n")

          unique.close()
          all.close()
          stats.close()
          required_data.close()

          data_end = time.time()
          data_time = data_end - data_start
          data_time = int(data_time)
          print "It took",data_time,"seconds to collect the required data.\nThanks for your patience.\n"

          orig_dir = "../"
          os.chdir(orig_dir)

          self.generate_randomised_album()


      def generate_randomised_album(self):

          required_data_file = self.data_dir+"/required_data.txt"
          open_required_data = open(required_data_file, "r")
          unique_data_file = self.data_dir+"/unique.txt"
          open_unique_data = open(unique_data_file, "r")
          all_data_file = self.data_dir+"/all.txt"
          open_all_data = open(all_data_file, "r")

          reqd_data = {}

          for ORD in open_required_data:
              split_value = ORD.split(" ")
              reqd_data[split_value[0]] = split_value[1]

          small_tracks =    int(reqd_data['FEWEST_NO_TRACKS'])
          large_tracks =    int(reqd_data['GREATEST_NO_TRACKS'])
          small_lyrics    = int(reqd_data['FEWEST_TRACK_WORDS'])
          large_lyrics    = int(reqd_data['GREATEST_TRACK_WORDS'])
          no_unique_words = int(reqd_data['NO_UNIQUE_WORDS'])
          no_all_words    = int(reqd_data['NO_ALL_WORDS'])

          track_titles = []
          unique_words = []
          all_words = []

          for OUD in open_unique_data:
              unique_words.append(OUD)

          for OAD in open_all_data:
              all_words.append(OAD)

          album_title_tokens = random.randint(2, 4)
          no_tracks_on_album = random.randint(small_tracks, large_tracks)
          album_title_token = ""
          album_title = ""
          tokens_in_track_titles = []
          tokens_in_tracks = ""

          for k in range(album_title_tokens):
              album_title_token = unique_words[random.randint(0, (len(unique_words) - 1))]
              if not album_title_token in album_title:
                 album_title += album_title_token + " "
              album_title = "".join(album_title.split("\n"))

          for x in range(no_tracks_on_album):
              tokens_in_track_titles.append(random.randint(1, 5))

          album_lyrics = []
          track_title_token = ""

          for TITT in tokens_in_track_titles:
              track_title = ""
              for x in range(TITT):
                  track_title_token = unique_words[random.randint(0, (len(unique_words) - 1))]
                  if not track_title_token in track_title:
                     track_title += track_title_token
              track_title = " ".join(track_title.split())
              track_titles.append(track_title)

          os.chdir(self.albums_dir)
          album_file_name = album_title
	  test = album_file_name
          album_file_name = album_file_name.replace(" ", "_")
          album_file_name = album_file_name[:-1]
	  

          random_slayer_album =  open(album_file_name+".txt", "w+")

          for index, TT in enumerate(track_titles):
              track_lyrics = ""
              print_title = str((index + 1))+". "+TT
              if index == 0:
                 random_slayer_album.write(print_title)
              else:
                 random_slayer_album.write("\n\n\n" + print_title)

              divider = "\n"
              for z in range(len(print_title)):
                  divider += "-"
              divider += "\n"
              random_slayer_album.write(divider)

              for x in random.randrange(small_lyrics, large_lyrics), 1:
                  for y in range(x):
                      track_lyrics += all_words[random.randint(0, (len(all_words) - 1))]
              track_lyrics = " ".join(track_lyrics.split())

              count = 0
              word_count = 0
              line_count = 0
              string = ""

              for item in track_lyrics.split():

                  if word_count > 0 and word_count % 5 == 0:
                     line_count += 1
                     string += "\n"

                     if line_count % 4 == 0:
                        string += "\n"

                  string += item + " "
                  word_count += 1

              random_slayer_album.write(string)

          orig_dir = "../"
          os.chdir(orig_dir)
          
	  #Sorry folks, this was necessary until the data files were converted from DOS to UNIX. 
	  #Leaving it in anyway.
          album_name_for_terminal = ""
	  album_filename_for_terminal = ""
	  album_filename_for_terminal = str(random_slayer_album).split(".txt")[0][12:]
          album_filename_for_terminal = album_filename_for_terminal.replace("\\r", "")+".txt"
	  album_name_for_terminal = album_filename_for_terminal.replace("_", " ")[:-4] 
	
	  print	
          print "Your new randomly-generated Slayer album is called: "+album_name_for_terminal
          print "You will find a text file ["+album_filename_for_terminal+"] in the '/"+self.albums_dir+"' folder of the current directory."

          print "There are " + str(no_tracks_on_album) + " tracks on this album\n"
          print "The tracks are: \n"
          for index, TT in enumerate(track_titles):
              print_title = str((index + 1))+". "+TT
              print print_title

	  lex_list = self.lexical_analysis(unique_words, all_words)	  
	  self.print_stats()
	  
	  print "The 100 most frequent words in SLAYER's lyrics are:"
	  for index, item in enumerate(lex_list):	
		print item	

          open_required_data.close()
          open_unique_data.close()
          open_all_data.close()
	  random_slayer_album.close()


      def print_stats(self):

          print

          stats_data_file = self.data_dir+"/stats.txt"
          open_stats_data = open(stats_data_file, "r")

          for OSD in open_stats_data:
              OSD = OSD.rstrip('\n')
              print OSD

          open_stats_data.close()

          print


      def lexical_analysis(self, unique_list, all_list):

          UL = unique_list
          UL.sort()
          AL = all_list
          AL.sort()
          count = 0

          instances = []
          intance_count = []

          for UL in unique_list:
              count = 0
              for AL in all_list:
                  if UL == AL:
                     count += 1
              if count > 1:
                 instances.append([UL, count])

          instance_count = sorted(instances, key=lambda instance: instance[1])

          top_100 = []
          word = ""
	  occurrences = ""
	  string = ""

          for IC in instance_count:	
                    string = ""	
		    word = IC[0].replace("\n", "")
		    occurrences = str(IC[1])
		    string = "'" + word + "' occurs " + occurrences + " times"
                    if not string in top_100:
                       top_100.append(string)

          top_100 = top_100[-100:]

          return top_100


if __name__ == '__main__':
   RandomSlayerAlbum()
