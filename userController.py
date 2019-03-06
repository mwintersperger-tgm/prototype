
import json
import os


class UserController:

    def addUser(self,name,passwd,type,CC):
        """
        This method adds a new user to the System as long as its userame is unique
        :param name: the name of the new user
        :type String
        :param passwd: the hashed password of the user
        :type String
        :param type: the type of the user
        :type String
        :param CC: the country code of the new user
        :type String
        :return: A message depending on success or failure
        """
        filelen = self.fileLength()
        # Check if the list of CCs doesn't contain multiples of the same and that the name of the user is unique.
        if self.uniqueCC(filelen, CC) == False or self.uniqueUsernames(filelen, name) == False:
            return "failure"
        curline = 0
        with open("user.json", "r") as of:
            line = of.readline()
            curline += 1
            with open("newuser.json", "w") as nf:
                # Write the header
                nf.write("%s" % line)
                for i in range(0, filelen-2):
                    # Write the existing users, this setup is to add a ',' to the formerly newest user
                    line = of.readline().rstrip(",\n")
                    curline += 1
                    nf.write("%s,\n" % line)
                # Write the new user and the end if file
                nf.write('{"name":"%s", "pswd":"%s", "type":"%s", "cc":"%s"}\n' % (name,passwd,type,CC))
                nf.write(']}')
        # remove the old file and rename the new file to the old one
        os.remove("user.json")
        os.rename("newuser.json", "user.json")
        # Return a success message if everything worked
        return "success"

    def uniqueUsernames(self,filelen, nname):
        """
        This method returns a list of usernames
        :param filelen:
        :type int
        :return: list of usernames
        """
        names = []
        with open("user.json", "r") as of:
            line = of.readline()
            for i in range(0, filelen-2):
                line = of.readline()
                name = line[line.find(':')+2:line.find(',')-1]
                names.append(name)
        return nname in names

    def uniqueCC(self,filelen, ccs):
        seen = set()
        return not any(i in seen or seen.add(i) for i in ccs)

    def removeUser(self,name):
        """
        This method removes the user with the gives username
        :param name: the name of the user to be removed
        :type String
        :return: void
        """
        filelen = self.fileLength()
        curline = 0
        with open("user.json", "r") as of:
            line = of.readline()
            curline += 1
            with open("newuser.json", "w") as nf:
                nf.write("%s" % line)
                for i in range(0, filelen-2):
                    line = of.readline()
                    curline += 1
                    temp = line[9:line.find(",")-1]
                    if temp != name:
                        if curline < filelen-2:
                            nf.write(line)
                        else:
                            nf.write("%s\n" % line.rstrip(",\n"))
                nf.write(']}')
        os.remove("user.json")
        os.rename("newuser.json", "user.json")

    def checkUser(self,username,password):
        """
        This method checks of the given username and password is proper and returns the information of the user if yes and a small message of no
        :param username: the given username to be checked
        :type String
        :param password: the given hashed password to be checked
        :return: A list of the user information if successful
        :return: A failure message if not successful
        """
        filelen = self.fileLength()
        curline = 0
        names = []
        passwords = []
        types = []
        CCs = []
        with open("user.json", "r") as of:
            line = of.readline()
            for i in range(0,filelen-2):
                line = of.readline().rstrip("\n")
                list = line.split(":")
                name,scrap = list[1].split(",")
                pwd, scrap = list[2].split(",")
                type, scrap = list[3].split(",")
                CC = list[4].rstrip("}")
                names.append(name.strip('"'))
                passwords.append(pwd.strip('"'))
                types.append(type.strip('"'))
                CCs.append(CC.strip('"'))
        for i in range(0,len(passwords)):
            if names[i] == username and passwords[i] == password:
                return '{"name":"%s", "type":"%s", "cc":"%s"}' % (names[i], types[i], CCs[i])
        return "failure"

    def filesOfUser(self,directory,CC):
        """
        This Method returns a list of files the user can access with his CC
        :param directory: the directory to be looked through
        :param CC: the country code to be checked with
        :return: a list of files
        """
        file_names = [fn for fn in os.listdir(directory)
                      if "data"+CC in fn]
        return file_names

    def fileLength(self):
        """
        This function returns the number of lines in a file
        :param filename: the name/path of the data file
        :type: string
        :return: the number of lines in the file
        :rtype: integer
        """
        num_lines = sum(1 for line in open("user.json"))
        return num_lines
