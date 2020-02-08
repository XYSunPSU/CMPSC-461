# Project 1
# CMPSC 461
# Xunyuan Sun
# xzs5138
# Purpose: This is the file for CMPSC461 Project 1, it includes three classes: Token stores the value and 
#          and category of any token, a lexical analyzer, and a syntatic analyzer which parses the tokens 
#          given by Lexer using the recursive descent technique

INT, FLOAT, ID, KEYWORD, OPERATOR, COMMA, EOI, INVALID = 1, 2, 3, 4, 5, 6, 7, 8

def typeToString(tp):
    if (tp == INT): return "Int"
    elif (tp == FLOAT): return "Float"
    elif (tp == ID): return "ID"
    elif (tp == KEYWORD): return "Keyword"
    elif (tp == OPERATOR): return "Operator"
    elif (tp == COMMA): return "Comma"
    elif (tp == EOI): return "EOI"
    return "Invalid"

class Token:
    "A class for representign Tokens"

    def __init__ (self, tokenType, tokenVal):
        self.type = tokenType
        self.val = tokenVal

    def getTokenType(self):
        return self.type

    def getTokenValue(self):
        return self.val

    def __repr__(self):
        if (self.type in [INT, FLOAT, ID]):
            return self.val
        elif (self.type == KEYWORD):
            return "SELECT" or "FROM" or "WHERE" or "AND"
        elif (self.type == OPERATOR):
            return "=" or "<" or ">"
        elif (self.type == COMMA):
            return ","
        elif (self.type == EOI):
            return ""
        else:
            return "invalid"


LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"

class Lexer:

    # stmt is the current statement to perform the lexing;
    # index is the index of the next char in the statement
    def __init__ (self, s):
        self.stmt = s
        self.index = 0
        self.nextChar()

    def nextToken(self):
        while True:
            if self.ch.isalpha(): # is a letter
                id = self.consumeChars(LETTERS+DIGITS)
                return Token(ID, id)
            elif self.ch.isdigit():
                num = self.consumeChars(DIGITS)
                if self.ch != ".":
                    return Token(INT, num)
                num += self.ch
                self.nextChar()
                if self.ch.isdigit(): 
                    num += self.consumeChars(DIGITS)
                    return Token(FLOAT, num)
                else: return Token(INVALID, num)
            elif self.ch==' ': self.nextChar()
            elif self.ch==',': 
                self.nextChar()
                return Token(COMMA, "")
            elif self.ch=='=' or '<' or '>':
                self.nextChar()
                return Token(OPERATOR, "")
            elif self.ch=='SELECT' or 'FROM' or 'WHERE' or 'AND':
                self.nextChar()
                return Token(KEYWORD, "")
            elif self.ch=='$':
                return Token(EOI,"")
            else:
                self.nextChar()
                return Token(INVALID, self.ch)

    def nextChar(self):
        self.ch = self.stmt[self.index] 
        self.index = self.index + 1

    def consumeChars (self, charSet):
        r = self.ch 
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r

    def checkChar(self, c):
        self.nextChar()
        if (self.ch==c):
            self.nextChar()
            return True
        else: return False

import sys

class Parser:
    def __init__(self, s):
        self.lexer = Lexer(s+"$")
        self.token = self.lexer.nextToken()
    
    def run(self):
        self.Query()

    def next(self):
        self.token = self.lexer.nextToken()

    def Query(self):
        print "<Query>"
        if self.token.getTokenValue() == "SELECT":
            print ("\t<Keyword>" + self.token.getTokenValue() + "</Keyword>")
            self.next()
            self.Idlist()
        else:
            self.error(KEYWORD)
        
        if self.token.getTokenValue() == 'FROM':
            print ("\t<Keyword>" + self.token.getTokenValue() + "</Keyword>")
            self.next()
            self.Idlist()
        else: 
            self.error(KEYWORD)

        if self.token.getTokenValue() == 'WHERE':
            print ("\t<Keyword>" + self.token.getTokenValue() + "</Keyword>")
            self.next()
            self.Condlist()
            self.match(EOI)
            print ("</Query>")
            self.token = self.lexer.nextToken()
        else:
            self.error(KEYWORD)
            
        
    def Idlist(self):
        print ("\t<Idlist>")
        if self.token.getTokenType() == ID:
            print ("\t\t<Id>" + self.token.getTokenValue() + "</Id>")
            self.next()

        while self.token.getTokenType() == COMMA:
            print ("\t\t<Comma>,</Comma>")
            self.next()
            if self.token.getTokenType() == ID:
                print ("\t\t<Id>" + self.token.getTokenValue() + "</Id>")
                self.next()
            else:
                self.error(ID)
        print ("\t</Idlist>")

    def Condlist(self):
        print ("\t<Condlist>")
        if self.token.getTokenType() == ID:
            self.Cond()
        else:
            self.error(self.token.getTokenType())
        
        while self.token.getTokenValue == 'AND':
            print ("\t<Keyword>" + self.token.getTokenValue() + "</Keyword>")
            self.next()

            if self.token.getTokenType() == ID:
                self.Cond()
            else:
                self.error(self.token.getTokenType())
        print ("\t</Condlist>")

    def Cond(self):
        print ("\t\t<Cond>")
        if not (self.token.getTokenType() == ID):
            self.error(self.token.getTokenType())
        else:
            print ("\t\t\t<Id>" + self.token.getTokenValue() + "</Id>")
            self.next()
            if not (self.token.getTokenType() == OPERATOR):
                self.error(self.token.getTokenType())
            else:
                print ("\t\t\t<Operator>=</Operator>")
                self.next()
                self.term() 
        print ("\t\t</Cond>")

    def term(self):
        print ("\t\t\t<term>")
        if self.token.getTokenType() == ID:
            print ("\t\t\t\t<Identifier>" + self.token.getTokenValue() \
                + "</Identifier>")
        elif self.token.getTokenType() == INT:
            print ("\t\t\t\t<Int>" + self.token.getTokenValue() + "</Int>")
        elif self.token.getTokenType() == FLOAT:
            print ("\t\t\t\t<Float>" + self.token.getTokenValue() + "</Float>")
        else:
            print ("Syntax error: expecting an ID, an int, or a float" \
                + "; saw:" \
                + typeToString(self.token.getTokenType()))
            sys.exit(1)
        print ("\t\t\t</term>")

    def match(self, tp):
        val = self.token.getTokenValue()
        if (self.token.getTokenType() == tp):
            self.token = self.lexer.nextToken()
        else: self.error(tp)
        return val

    def error(self, tp):
        print ("Syntax error: expecting: " + typeToString(tp) \
              + "; saw: " + typeToString(self.token.getTokenType()))
        sys.exit(1)

print "Testing the parser: test 1"
parser = Parser ("SELECT C1,C2 FROM T1 WHERE C1=5.23") 
parser.run()