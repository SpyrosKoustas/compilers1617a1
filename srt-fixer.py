import sys
import re
import argparse

#Semester Project
#Spyridon Georg Koustas (Π2014027)
#09/05/2017

parser = argparse.ArgumentParser()
# add mandatory (positional) arguments
parser.add_argument("fname",help="input srt file name")
parser.add_argument("offset",type=float,help="subtitle offset in seconds to apply (can be fractional)")

# parse arguments
args = parser.parse_args()

# Defining the regular expression that we are going to use inside a string
regex = r'([0-9][0-9]):([0-9][0-9]):([0-9][0-9]),([0-9][0-9][0-9]) --> ([0-9][0-9]):([0-9][0-9]):([0-9][0-9]),([0-9][0-9][0-9])'
# Creating the regular expression object
rexp = re.compile(regex)

# The following boolean is an error checking in case we don't find any time intput
isTime = False

with open(args.fname,newline='') as ifp:	
	for line in ifp:

		# Starting the searching process which will return the matching objects
		m = rexp.search(line)
		# Now we will check if the matching objects are other than empty, so that we can continue with our code
		# and store in variables the matching objects
		if m != None:
			# We activate out boolean for the error checking, because we found a time input
			isTime = true

			# We are storing the matching objects into new variables, so that we can later add the time amount me want
			# the numbers 0 and 1 define whether the time stamp is the start timestamp or the end timestamp
			hours0 = int(m.group(1))
			hours1 = int(m.group(5))

			minutes0 = int(m.group(2))
			minutes1 = int(m.group(6))

			seconds0 = int(m.group(3))
			seconds1 = int(m.group(7))

			milliseconds0 = int(m.group(4))
			milliseconds1 = int(m.group(8))

			# Now we will create some variables that are going to be the output of the code,
			# which we will then also check if some of them are greater than they should be.

			# Declaring the new output variables
			newMilliseconds0 = 0
			newMilliseconds1 = 0
			newSeconds0 = 0
			newSeconds1 = 0
			newMinutes0 = 0
			newMinutes1 = 0
			newHours0 = 0
			newHours1 = 0

			# First we get the milliseconds and check the tolat amount
			newMilliseconds0 = milliseconds0 + (args.offset - int(args.offset))
			newMilliseconds1 = milliseconds1 + (args.offset - int(args.offset))
			if newMilliseconds0 > 999:
				newMilliseconds0 = newMilliseconds0 - 1000
				newSeconds0 = newSeconds0 + 1

			if newMilliseconds1 > 999:
				newMilliseconds1 = newMilliseconds1 -1000
				newSeconds1 = newSeconds1 + 1

			# Now we get the seconds and check the total amount
			newSeconds0 = newSeconds0 + seconds0 + int(args.offset)
			newSeconds1 = newSeconds1 + seconds1 + int(args.offset)
			if newSeconds0 > 59:
				newSeconds0 = newSeconds0 - 60
				newMinutes0 = newMinutes0 + 1

			if newSeconds1 > 59:
				newSeconds1 = newSeconds1 - 60
				newMinutes1 = newMinutes1 + 1

			# Now we get the minutes and chech the total amount
			newMinutes0 = newMinutes0 + minutes0
			newMinutes1 = newMinutes1 + minutes1
			if newMinutes0 > 59:
				newMinutes0 = newMinutes0 - 60
				newHours0 = newHours0 + 1

			if newMinutes1 > 59:
				newMinutes1 = newMinutes1 - 60
				newHours1 = newHours1 + 1

			# Last but not least we get the hour, this time we don't have to check the total amount
			newHours0 = newHours0 + hours0
			newHours1 = newHours1 + hours1

			# Now we will transform our variables to string and also add zeros (00) where they are needed, so that we can save them to a file
			# to do so we will use the pytnon funtion str() and str.zfill()
			newMilliseconds0 = str(newMilliseconds0).zfill(3)
			newMilliseconds1 = str(newMilliseconds1).zfill(3)

			newSeconds0 = str(newSeconds0).zfill(2)
			newSeconds1 = str(newSeconds1).zfill(2)

			newMinutes0 = str(newMinutes0).zfill(2)
			newMinutes1 = str(newMinutes1).zfill(2)

			newHours0 = str(newHours0).zfill(2)
			newHours1 = str(newHours1).zfill(2)

			# Now the only thing we have to do is put together our new string, which will be the output
			newTime = "%s:%s:%s,%s --> %s:%s:%s,%s \n" % (newHours0, newMinutes0, newSeconds0, newMilliseconds0, newHours1, newMinutes1, newSeconds1, newMilliseconds1)
			# Now let's write
			sys.stdout.write(newTime)

		# In the else tab we print anything that has not to do with the time that we want to edit
		# and also writing an error message if an error should appear
		else:
			if isTime:
				sys.stdout.write(line)
			else:
				sys.stdout.write('There was some kind of error!')

# Closing the file
ifp.close()
