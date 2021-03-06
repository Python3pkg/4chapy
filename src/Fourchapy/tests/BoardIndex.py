'''
Created on Dec 25, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import unittest
from .ConfigBase import ConfigBasedTests

class BoardIndexFetchSequence(ConfigBasedTests):
    
    def testBoardIndexHttpListFirst(self):
        from Fourchapy import BoardIndex
        i = BoardIndex(proto = 'http', proxies = self.proxy)
        self.assertFalse('Boards' in i.__dict__, "BoardIndex.Boards shouldn't exist")
        self.assertFalse('BoardsDict' in i.__dict__, "BoardIndex.BoardsDict shouldn't exist")
        boardsList = i.Boards
        self.assertTrue('Boards' in i.__dict__, "BoardIndex.Boards should have been auto created")
        self.assertFalse('BoardsDict' in i.__dict__, "BoardIndex.BoardsDict shouldn't exist")
        boardsDict = i.BoardsDict
        self.assertTrue('Boards' in i.__dict__, "BoardIndex.Boards should have been auto created")
        self.assertTrue('BoardsDict' in i.__dict__, "BoardIndex.BoardsDict should have been auto created")
        
    def testBoardIndexHttpDictFirst(self):
        from Fourchapy import BoardIndex
        i = BoardIndex(proto = 'http', proxies = self.proxy)
        self.assertFalse('Boards' in i.__dict__, "BoardIndex.Boards shouldn't exist")
        self.assertFalse('BoardsDict' in i.__dict__, "BoardIndex.BoardsDict shouldn't exist")
        boardsDict = i.BoardsDict
        self.assertTrue('Boards' in i.__dict__, "BoardIndex.Boards should have been auto created")
        self.assertTrue('BoardsDict' in i.__dict__, "BoardIndex.BoardsDict should have been auto created")
        
    def testBoardIndexHttpsListFirst(self):
        from Fourchapy import BoardIndex
        i = BoardIndex(proto = 'https', proxies = self.proxy)
        self.assertFalse('Boards' in i.__dict__, "BoardIndex.Boards shouldn't exist")
        self.assertFalse('BoardsDict' in i.__dict__, "BoardIndex.BoardsDict shouldn't exist")
        boardsList = i.Boards
        self.assertTrue('Boards' in i.__dict__, "BoardIndex.Boards should have been auto created")
        self.assertFalse('BoardsDict' in i.__dict__, "BoardIndex.BoardsDict shouldn't exist")
        boardsDict = i.BoardsDict
        self.assertTrue('Boards' in i.__dict__, "BoardIndex.Boards should have been auto created")
        self.assertTrue('BoardsDict' in i.__dict__, "BoardIndex.BoardsDict should have been auto created")
        
    def testBoardIndexHttpsDictFirst(self):
        from Fourchapy import BoardIndex
        i = BoardIndex(proto = 'https', proxies = self.proxy)
        self.assertFalse('Boards' in i.__dict__, "BoardIndex.Boards shouldn't exist")
        self.assertFalse('BoardsDict' in i.__dict__, "BoardIndex.BoardsDict shouldn't exist")
        boardsDict = i.BoardsDict
        self.assertTrue('Boards' in i.__dict__, "BoardIndex.Boards should have been auto created")
        self.assertTrue('BoardsDict' in i.__dict__, "BoardIndex.BoardsDict should have been auto created")

    def testBoardIndexAvailAttrs(self):
        from Fourchapy import BoardIndex
        bindex = BoardIndex(proto = 'http', proxies = self.proxy)
        self.assertTrue(hasattr(bindex, 'Boards'), "Expected a BoardIndex.Boards attr to exist")
        self.assertRaises(AttributeError, getattr, bindex, 'Posts')
        self.assertRaises(AttributeError, getattr, bindex, 'Threads')

class BoardConfigBasedTests(ConfigBasedTests):
    
    def setUp(self):
        ConfigBasedTests.setUp(self)
        # Get various options
        self.recursionMaxBoards = self._get_option(
                                                   section = 'RecursiveOptions',
                                                   option = 'MaxBoards',
                                                   default = 3,
                                                   vtype = 'int',
                                                   )
        self.recursionMaxPages = self._get_option(
                                                   section = 'RecursiveOptions',
                                                   option = 'MaxPages',
                                                   default = 2,
                                                   vtype = 'int',
                                                   )
        self.recursionMaxThreads = self._get_option(
                                                   section = 'RecursiveOptions',
                                                   option = 'MaxThreads',
                                                   default = 10,
                                                   vtype = 'int',
                                                   )
        self.recursionMaxPosts = self._get_option(
                                                   section = 'RecursiveOptions',
                                                   option = 'MaxPosts',
                                                   default = 10,
                                                   vtype = 'int',
                                                   )
        
        from Fourchapy import BoardIndex
        self.index = BoardIndex(proto = 'http', proxies = self.proxy)
        # Run the fetches now rather than wait
        boardList = self.index.Boards
        boardDict = self.index.BoardsDict
        self.log.debug("Setup %r with %d boards", self.index, len(self.index.Boards))
        

class BoardIndexTestSequence(BoardConfigBasedTests):

    def testBoardListVsDict(self):
        boardList = self.index.Boards
        boardDict = self.index.BoardsDict
        
        self.assertEqual(len(boardList), len(boardDict), "List and dict should have same items")
        self.assertTrue(len(boardDict) > 0, "There should be at least one board listed")
        for board in boardList[:self.recursionMaxBoards]:
            self.log.debug("Checking Boards vs BoardsDict for %r", board)
            self.assertTrue(board.Board in boardDict, "Board %r is in the list but not the dict" % board.Board)
            self.assertEqual(board, boardDict[board.Board], "Boards and BoardsDict should be the same object")
        
    def testBoardsItems(self):
        boardDict = self.index.BoardsDict
        
        # Check data values for all known boards
        for boardID, board in list(boardDict.items())[:self.recursionMaxBoards]:
            # Board ID tests
            self.assertEqual(boardID, board.Board, "Board ID str should match boardObj.Board")
            self.assertTrue(len(boardID) <= 5, "Board ID should be short")
            self.assertTrue(hasattr(board, 'Board'), 'Board should be defined')
            self.assertTrue(isinstance(board.Board, str) or board.Board is None, 'Board should be unicode based')
            
            # Other values
            self.assertTrue(hasattr(board, 'ThreadsPerPage'), 'ThreadsPerPage should be defined')
            self.assertTrue(isinstance(board.ThreadsPerPage, int) or board.ThreadsPerPage is None, 'ThreadsPerPage should be int based')
            
            self.assertTrue(hasattr(board, 'Pages'), 'Pages should be defined')
            self.assertTrue(isinstance(board.Pages, int) or board.Pages is None, 'Pages should be int based')
            
            self.assertTrue(hasattr(board, 'SafeForWork'), 'SafeForWork should be defined')
            self.assertTrue(isinstance(board.SafeForWork, bool) or board.SafeForWork is None, 'SafeForWork should be bool based')
            
            self.assertTrue(hasattr(board, 'BoardName'), 'BoardName should be defined')
            self.assertTrue(isinstance(board.BoardName, str) or board.BoardName is None, 'BoardName should be unicode based')
            
            self.assertEqual(board.getMinPage(), 0, 'Min page should always be zero')
            self.assertTrue(board.getMaxPage() >= 1, 'Max page should be at least 1')
            self.assertTrue(board.getMaxPage() <= 30, 'Max page should be less than 30')
            
            self.assertTrue(board.TotalThreads() > 0, "Total threads should be > 0")
            self.assertTrue(isinstance(board.TotalThreads(), int), "Total threads should be an int")

            self.assertTrue(
                            isinstance(board.getBoardAPIPageURL(), str),
                            "URL should be a string. Got %r" % board.getBoardAPIPageURL(),
                            )
            self.assertTrue(board.getBoardAPIPageURL().startswith(board.Proto), "Protocol should match the API URL")
    
    def testBoardPages(self):
        boardDict = self.index.BoardsDict
        
        # Check data values for all known boards
        for boardID, board in list(boardDict.items())[:self.recursionMaxBoards]:
            boardPages = board.getPages()
            self.assertTrue(len(boardPages) > 0, "Should have at least one page")
            totalItems = 0
#            Disabling this as it'll generate a lot of requests
#            for page in boardPages:
#                totalItems += len(page.Threads)
#            self.assertTrue(totalItems <= board.TotalThreads(), "There are more threads listed than boardObj.TotalThreads() says should exist")
#            self.assertTrue(totalItems >= (board.getMaxPage() - 1) * board.ThreadsPerPage)
            
            
            
