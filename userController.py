
import json
import os


class UserController:

    def addUser(self,name,passwd,type,CC):
        filelen = self.fileLength()
        curline = 0
        with open("user.json", "r") as of:
            line = of.readline()
            curline += 1
            with open("newuser.json", "w") as nf:
                nf.write("%s" % line)
                for i in range(0, filelen-3):
                    line = of.readline()
                    curline += 1
                    nf.write(line)
                line = of.readline()
                nf.write("%s,\n" % line.rstrip("\n"))
                nf.write('{"name":"%s", "pswd":"%s", "type":"%s", "cc":"%s"}\n' % (name,passwd,type,CC))
                nf.write(']}')
        os.remove("user.json")
        os.rename("newuser.json", "user.json")

    def removeUser(self,name):
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
        filelen = self.fileLength()
        curline = 0
        names = []
        passwords = []
        with open("user.json", "r") as of:
            line = of.readline()
            for i in range(0,filelen-2):
                line = of.readline().rstrip("\n")
                list = line.split(":")
                name,scrap = list[1].split(",")
                pwd, scrap = list[2].split(",")
                names.append(name.strip('"'))
                passwords.append(pwd.strip('"'))
        for i in range(0,len(passwords)):
            if names[i] == username and passwords[i] == password:
                return True
            else:
                return False


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
