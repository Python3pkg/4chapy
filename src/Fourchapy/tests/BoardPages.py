'''
Created on Dec 25, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import unittest
from Fourchapy.tests.BoardIndex import BoardConfigBasedTests


class BoardPageConfigBasedTests(BoardConfigBasedTests):
    
    def setUp(self):
        BoardConfigBasedTests.setUp(self)
        self.log.debug("Setting up %r", self)
        self.boardPages = {}
        
        # Run the fetches now rather than wait
        for boardID, board in list(self.index.BoardsDict.items())[:self.recursionMaxBoards]:
            self.log.debug("Adding board %r to test list", board)
            self.boardPages[boardID] = dict(
                                          board = board,
                                          pages = {},
                                          )
            for page in board.getPages()[:self.recursionMaxPages]:
                self.log.debug("Adding page %r to test list", page)
                self.boardPages[boardID]['pages'][page.Page] = page
                
        self.log.debug("Done listing boards+pages to use")

class PageInitialTestSequence(BoardPageConfigBasedTests):
    
    def testPageThreadFetching(self):
        for boardID, info in list(self.boardPages.items()):
            for pageNumber, page in list(info['pages'].items()):
                self.log.log(5, "Looking at page %r", page)
                # Thread list for page fetching test
                self.assertFalse('Threads' in page.__dict__, "Threads shouldn't exist yet in page %r" % page)
                threads = page.Threads
                self.assertTrue('Threads' in page.__dict__, "Threads should have been auto created in %r" % page)
    
    def testPageInfo(self):
        for boardID, info in list(self.boardPages.items()):
            for pageNumber, page in list(info['pages'].items()):
                self.log.log(5, "Looking at page %r", page)
                # Attributes tests
                self.assertTrue(isinstance(page.Page, int) or page.Page is None, "The page number should be an int")
                self.assertTrue(isinstance(page.Board, str), "The board ID string should be a str")
                self.assertTrue(isinstance(page.Proto, str), "The protocol should be a str")
                self.assertTrue(page.Proto.lower() in ['http', 'https'], "Proto %r isn't http or https" % page.Proto)


class ThreadTestSequence(BoardPageConfigBasedTests):
    
    def testThreadFetch(self):
        for boardID, info in list(self.boardPages.items()):
            for pageNumber, page in list(info['pages'].items()):
                self.log.log(5, "Looking at page %r", page)
                for threadID, thread in list(page.ThreadsDict.items())[:self.recursionMaxThreads]:
                    self.log.log(4, "Looking at thread %r", thread)
                    # Thread list for page fetching test
                    self.assertFalse('Posts' in thread.__dict__, "Posts shouldn't exist yet in thread %r" % thread)
                    posts = thread.Posts
                    self.assertTrue('Posts' in thread.__dict__, "Posts should have been auto created in %r" % thread)

    def testThreadFetchDict(self):
        for boardID, info in list(self.boardPages.items()):
            for pageNumber, page in list(info['pages'].items()):
                self.log.log(5, "Looking at page %r", page)
                for threadID, thread in list(page.ThreadsDict.items())[:self.recursionMaxThreads]:
                    self.log.log(4, "Looking at thread %r", thread)
                    # Thread list for page fetching test
                    self.assertFalse('PostsDict' in thread.__dict__, "PostsDict shouldn't exist yet in thread %r" % thread)
                    posts = thread.PostsDict
                    self.assertTrue('PostsDict' in thread.__dict__, "PostsDict should have been auto created in %r" % thread)

    def testThreadObj(self):
        for boardID, info in list(self.boardPages.items()):
            for pageNumber, page in list(info['pages'].items()):
                self.log.log(5, "Looking at page %r", page)
                for threadID, thread in list(page.ThreadsDict.items())[:self.recursionMaxThreads]:
                    self.log.log(4, "Looking at thread %r", thread)
                    self.assertTrue(isinstance(threadID, int) or threadID is None, "The thread ID number should be an int")
                    self.assertTrue(isinstance(thread.Thread, int) or thread.Thread is None, "The thread ID number should be a int")
                    self.assertTrue(isinstance(thread.Board, str), "The board ID string should be a str")
                    self.assertTrue(isinstance(thread.Proto, str), "The protocol should be a str")
                    self.assertTrue(thread.Proto.lower() in ['http', 'https'], "Proto %r isn't http or https" % thread.Proto)
