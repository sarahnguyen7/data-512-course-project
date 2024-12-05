#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 
#   FILE: Reader.py
#   REVISION: August, 2023
#   CREATION DATE: August, 2023
#   Author: David W. McDonald
#
#   A simple streaming reader/loader that is designed to load GeoJSON files. This class is part of
#   the wildfire user module. This module is distributed for student use in solving the DATA 512
#   class project.
#
#   Copyright by Author. All rights reserved. Not for reuse without express permissions.
#

import os, json


class Reader(object):
    '''
    
    This class implements a simple streaming reader that is compatible with the GeoJSON data formats for the
    wildfire datasets provided by the USGS. One example of that data can be found at:
    
    https://www.sciencebase.gov/catalog/item/61aa537dd34eb622f699df81
    
    The Reader class provides the public methods:
        open()    - to open the named GeoJson file
        header()  - to return the descriptive information for the dataset
        next()    - to get, one at a time, each GeoJSON feature from the file
        rewind()  - to return the file to the start of the GeoJSON features
        close()   - to close the file
        
    The class will attempt to maintain consistency of the Reader and will throw exceptions to attempt to prevent
    some inconsistent operations.
    
    A new object can be created and initialized, and have the file opened in one shot
    
        reader = Reader("file_to_read.json")
    
    This would initialize the reader and open the file, making the file read to read each of the GeoJSON features
    using something like 'reader.next()'. An alternate idiom would be two lines
    
        reader = Reader()
        reader.open("file_to_read.json")
    
    
    '''
    def __init__(self, filename=None):
        super().__init__()
        self.filename = ""
        self.filehandle = None
        self.is_open = False
        self.header_dict = None
        self.feature_start_offset = 0
        
        if filename:
            self.open(filename)
        
        return


    #####
    #   
    #   PUBLIC METHODS
    #   
    #####
    
    def open(self, filename=None):
        '''
        This opens the named file, reading the file header information and setting up the file to
        start reading features uing the next() method.
        
        The method takes one parameter a filename or the full path to a file that will be read by the Reader
        
        '''
        # if there's no filename, then there's nothing to open
        if not filename:
            raise Exception("Must supply a filename to 'open()' a file for reading")
        
        # if we're already managing an open file - throw an exception
        if self.is_open:
            raise Exception(f"Reader is already open, using file '{self.filename}'")

        # save that filename incase we need it later
        self.filename = filename
        
        # try to open that file
        try:
            f = open(filename,"r")
            self.filehandle = f
            self.is_open = True
            self.header_dict = self.__read_geojson_header__(f)
        except:
            path = os.getcwd()
            raise Exception(f"Could not find '{filename}' in directory '{path}'")
            #raise Exception(f"Could not open file '{filename}'")
            self.filename = ""
        return
        
    
    #   
    #   Returns the file header, read and saved when the file is opened
    #    
    def header(self):
        '''
        This method returns a python dictionary containing the header information that was read from the 
        GeoJSON file when it was opened.
        
        This method takes no parameters.
        
        '''
        if not self.is_open:
            raise Exception(f"Must 'open()' a file before getting the file header")
        return self.header_dict
    
    
    #   
    #   Read and return the next GeoJSON feature
    #    
    def next(self):
        '''
        This method reads the next complete geographic 'feature' from the GeoJSON file and returns that
        as a python dictionary. It reads and returns one complete feature with each call, until there are
        no more features. When there are no remaining features the method returns an empty value.
        
        This method takes no parameters.
        
        '''
        if not self.is_open:
            raise Exception(f"Must 'open()' a file before reading GeoJSON features")
        feature = self.__next_geojson_feature__(self.filehandle)
        return feature
    
    
    #   
    #   Reset the file pointer to the start of the features
    #    
    def rewind(self):
        '''
        This method resets the file handle to the start of the 'feature' list. This method allows
        the next() method to restart reading features one at a time. 
                
        This method takes no parameters.
        
        '''
        if self.is_open:
            try:
                # move to the absolute position in the file
                self.filehandle.seek(self.feature_start_offset,0)
            except:
                print("When attempting to rewind() it looks like the file handle is empty. Attempting to close() the file.")
                self.close()
                raise
        return 
    
    
    #   
    #   Close the file, reset the object to initial conditions
    #    
    def close(self):
        '''
        This method will close the open file handle and reset the object to initial conditions.
        
        This method takes no parameters.
        
        '''
        if self.is_open:
            self.filehandle.close()
            self.filehandle = None
            self.filename = ""
            self.is_open = False
            self.header_dict = None
            self.feature_start_offset = 0
        return 
    
    
    #####
    #   
    #   NON-PUBLIC (PRIVATE) METHODS
    #   
    #####
    
    ####
    #
    #   This method is called as part of an 'open()' operation. Generally, header fields/keys are the
    #   first things in the GeoJSON file. This method makes the assumption that all of these header
    #   fields occur *before* the list of features. This works for the USGS wildfire dataset.
    #
    #   However, this may need to be generalized for compatibility with other GeoJSON files. For example, what
    #   if fields/keys were in sorted order?
    #
    def __read_geojson_header__(self, f=None):
        if not f:
            return dict()
        
        header_dict = None
        header = None
        buf = ""

        #print(f"Openend file '{fname}'")
        i = 0
        #
        #   Read small chunks of the file building a buffer, we're looking to find
        #   a specific part of the GeoJSON file - the list of "features"
        c = f.read(100)
        while c and i<1200:
            #   Add the chunk to the buffer
            buf = buf+c
            #   Look to see if what we want is in the current buffer
            if ('"features":' in buf) or ("'features':" in buf):
                #print("Buffer is:")
                #print(buf)
                #
                # We need to find the offset of the key in the buffer
                index = buf.find("'features'")      # find with the single quote
                if index < 0:     # maybe it's the double quote version
                    index = buf.find('"features"')  # find with the double quote
                #
                # Seek to the start of the file, to read the header as one chunk
                f.seek(0,0)
                #print(f"Reading up to: {index}")
                #
                # Now, read the header, except the 'features' key that we were looking for
                header = f.read(index)
                #print("header is:")
                #print(header)
                #
                # Read the specific 'features' key, we're skipping that, to set the file
                # pointer to point to the first feature, this sets up for a next() operation
                c = f.read(len("'features'"))
                #print(f"Found key: {c}")
                #
                # Save the file offset where the features start to support the reset() operation
                self.feature_start_offset = f.tell()
                break
            #
            #   If we did not find the key in the buffer, read another chunk
            c = f.read(100)
            i += 1
        if header:
            # remove any whitespace - JSON encoders sometimes add whitespace
            header = header.strip(" \t\n\r")
            # remove the trailing comma - to maintain proper JSON formatting
            if header.endswith(','):
                header = header[0:-1]
            # close the open dictionary of the header
            header = header + "}"
            # convert the header to a usable python dictionary
            header_dict = json.loads(header)
        return header_dict
    
    
    
    ####
    #
    #   This procedure takes a file handle and attempts to read one dictionary 'feature' item from the file. 
    #   When successful it returns the python dictionary based on the JSON that was read.
    #
    #   In GeoJSON the 'features' list is a list of geographic features, which is just a list of dictionary items.
    #   The list is of arbitrary length, and is supposed to be composed of a set of 'attributes' and set of
    #   'geometry' items. The 'attributes' are descriptions of the 'geometry' items. The 'geometry' is a set of
    #   geographic primitives that can be composed to create a geographic entity of some kind.
    #
    #   This code assumes that the feature list is well formed JSON and compliant with the GeoJSON standard.
    #
    def __next_geojson_feature__(self, f=None):
        feat_str = None     # the feature as a JSON dictionary string
        feat_dict = None    # the feature converted to a dictionary
        if f:
            c = f.read(1)
            while c:
                if c[0] == '{':
                    feat_str = self.__recurse_geojson_feature_dict__(f,c)
                    break
                c = f.read(1)
            if feat_str:
                try:
                    feat_dict = json.loads(feat_str)
                except Exception as e:
                    print("Looks like the feature string has a problem!")
                    print(feat_str)
                    raise e
        return feat_dict
    
    
    ####
    #
    #   We use recursion to manage the composition of each JSON feature dictionary. The recursion
    #   tracks any nested dictionaries. When we exit the recursion we will have read one complete
    #   JSON dictionary item. This should also correspond to one GeoJSON feature.
    #
    def __recurse_geojson_feature_dict__(self, f=None, buf="", depth=0):
        # there is no way these nested features should have more than a few nested
        # dictionary levels, if we get this deep in a recursion, there is a problem
        if depth > 10:
            raise Exception("Suspect corrupted GeoJSON 'features' list.")
        #
        #
        obj = buf
        c = f.read(1)
        #
        while c:
            # the start of a new nested dictionary, recurse
            if c[0] == '{':
                obj = obj + self.__recurse_geojson_feature_dict__(f,c,(depth+1))
            else:
                # its not a nested dictionary, no new recursion just add the character
                obj = obj + c
            # closed a dictionary, then return from the recursion
            if c[0] == '}':
                return obj
            c = f.read(1)
        return obj
    
    
if __name__ == '__main__':
    print("Reader.py is a class with no main()")

    
    
    
