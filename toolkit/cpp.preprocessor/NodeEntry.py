import math
import datetime, time

########################################################################
class MathToolkit:
    """"""
    #----------------------------------------------------------------------
    @staticmethod
    def IsMultipleOf(number, base):
        """"""
        return number % base  == 0
    #----------------------------------------------------------------------
    @staticmethod
    def Even(number):
        """"""
        return  MathToolkit.IsMultipleOf (number, 2)
    #----------------------------------------------------------------------
    @staticmethod
    def MultipleOf4(number):
        """"""
        return  MathToolkit.IsMultipleOf (number, 4)
    #----------------------------------------------------------------------
    @staticmethod
    def MultipleOf8(number):
        """"""
        return  MathToolkit.IsMultipleOf (number, 8)
    #----------------------------------------------------------------------
    @staticmethod
    def IsPowerOf(number, base):
        """"""
        return math.pow (base, math.log (number, base)) == number
    pass

########################################################################
class TextToolkit:
    """"""
    @staticmethod
    def Space(number = 2):
        """"""
        return ' ' * number
    
########################################################################
class Engine:
    """"""
    #----------------------------------------------------------------------
    def __init__(self, patternGenerator, outputFile):
        """Constructor"""
        self.patternGenerator = patternGenerator
        self.outputFileName = outputFile
        pass
    #----------------------------------------------------------------------
    def Run(self):
        """"""
        import sys
        try:
            outfile = open (self.outputFileName, mode = 'w') 
        except Exception as ex:
            print 'Failed to open output file %s' % self.outputFileName
            return
        try:
            outfile.writelines (('%s\n' % line for line in self.patternGenerator.Output ()))
        except:
            print 'An exception occurred while generating the output file lines'
            raise
            pass
        finally:
            outfile.close ()
        pass 
    pass

########################################################################
class PatternGenerator:
    """"""
    #----------------------------------------------------------------------
    def Output(self):
        """"""
        raise StopIteration
    pass
########################################################################
class DummyGenerator (PatternGenerator):
    """"""
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
    #----------------------------------------------------------------------
    def Output(self):
        """"""
        mCount = 0
        while mCount < 10:
            mCount = mCount + 1
            yield 'Dummy [%d]' % mCount
            pass
        return
    pass
########################################################################
class IfndefDefGuardGenerator (PatternGenerator):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, guard):
        """Constructor"""
        self.mLines = '#ifndef %s\n#define %s' % (guard, guard) 
        pass
    #----------------------------------------------------------------------
    def Output(self):
        """"""
        yield self.mLines
        pass
    pass
########################################################################
class EndifGuardGenerator (PatternGenerator):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, guard):
        """Constructor"""
        self.mLine = '#endif /* %s */' % guard
        pass
    #----------------------------------------------------------------------
    def Output(self):
        """"""
        yield self.mLine
        pass
    pass    
########################################################################
class FileHeaderCommentGenerator (PatternGenerator):
    """"""
    PATTERN = """
/*
 * Copyright (C) 2011 Providence M. Salumu
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED AS IS AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 * 
 *  %s 
 *  Created on: %s
 */
 """
    #----------------------------------------------------------------------
    def __init__(self, filename):
        """Constructor"""
        self.mFilename = filename
        self.mDate = time.asctime ()
        pass
    #----------------------------------------------------------------------
    def Output(self):
        """"""
        yield FileHeaderCommentGenerator.PATTERN  % (self.mFilename, self.mDate)
        pass
    pass    

########################################################################
class CharGenerator (PatternGenerator):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, character = '#', lines = 2):
        """Constructor"""
        self.mLines = lines
        self.mChar = character
        pass
    #----------------------------------------------------------------------
    def Output(self):
        """"""
        while self.mLines > 0:
            yield str (self.mChar)
            self.mLines -= 1
            
########################################################################
class NodeEntryGenerator (PatternGenerator):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, higher2Power = 256):
        """Constructor"""
        self.higherPowOf2 = higher2Power
        self.mPattern = '#%sdefine SMUNIX_PP_NODE_ENTRY_%s(p) SMUNIX_PP_NODE_%s%s' 
        pass
    #----------------------------------------------------------------------
    def Output(self):
        """"""
        import math
        lCount = int (math.log (self.higherPowOf2, 2))
        lHightPowOf2 = int (math.pow (2, lCount)) 
        while lCount >= 1:
            res = self.mPattern % (TextToolkit.Space (), lHightPowOf2, 
                                   lHightPowOf2 / 2,
                                   '(p)' * int (lCount))
            lCount -= 1
            lHightPowOf2 /= 2
            yield res 
    pass

########################################################################
class Node_XXX(PatternGenerator):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, higher = 255):
        """Constructor"""
        self.mHigher = higher
        self.mPattern = '#%sdefine SMUNIX_PP_NODE_%d(p) SMUNIX_PP_IIF(p(%d), %s, %s)'
        pass
    #----------------------------------------------------------------------
    def ParametersToFill(self, count):
        """"""
        thirdAndFourthRes = self.ThirdAndFourthParameters (count)
        return (TextToolkit.Space (2), count, count, thirdAndFourthRes[0], thirdAndFourthRes[1])
    #----------------------------------------------------------------------
    def ThirdParameter(self, count):
        """"""
        if not MathToolkit.IsMultipleOf (count, 2):
            return '%d' % count
        if MathToolkit.IsPowerOf (count, 2):
            return 'SMUNIX_PP_NODE_%d' % int (count / 2)
        if MathToolkit.IsMultipleOf (count, 4):
            return 'SMUNIX_PP_NODE_%d' % (count - 2)
        if MathToolkit.IsMultipleOf (count, 2):
            return 'SMUNIX_PP_NODE_%d' % (count - 1)
        return 'SMUNIX_PP_NODE_%d' % count
    #----------------------------------------------------------------------
    def FourthParameter(self, count):
        """"""
        if not MathToolkit.IsMultipleOf (count, 2):
            return '%d' % int (count + 1)
        if MathToolkit.IsPowerOf (count, 2):
            return 'SMUNIX_PP_NODE_%d' % int (count / 2 * 3)
        if MathToolkit.IsMultipleOf (count, 4):
            return 'SMUNIX_PP_NODE_%d' % (count + 2)
        if MathToolkit.IsMultipleOf (count, 2):
            return 'SMUNIX_PP_NODE_%d' % (count + 1)
        return 'SMUNIX_PP_NODE_%d' % count
    #----------------------------------------------------------------------
    def ThirdAndFourthParameters(self, count):
        """"""
        if not MathToolkit.IsMultipleOf (count, 2):
            return '%d' % int (count), '%d' % int (count + 1) 
        if MathToolkit.IsPowerOf (count, 2):
            return 'SMUNIX_PP_NODE_%d' % int (count / 2), 'SMUNIX_PP_NODE_%d' % int (count / 2 * 3) 
        if MathToolkit.IsMultipleOf (count, 4):
            return 'SMUNIX_PP_NODE_%d' % (count - 2), 'SMUNIX_PP_NODE_%d' % (count + 2) 
        if MathToolkit.IsMultipleOf (count, 2):
            return 'SMUNIX_PP_NODE_%d' % (count - 1), 'SMUNIX_PP_NODE_%d' % (count + 1) 
        return 'SMUNIX_PP_NODE_%d' % count, 'SMUNIX_PP_NODE_%d' % count 
        
    #----------------------------------------------------------------------
    def Output(self):
        """"""
        import math
        lCount = self.mHigher
        while lCount >= 1:
            res = self.mPattern % self.ParametersToFill (lCount)
            lCount -= 1
            yield res
        pass
    pass

########################################################################
class StaticLinesGenerator (PatternGenerator):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, staticLines):
        """Constructor"""
        self.mStaticLines = staticLines
        pass
    #----------------------------------------------------------------------
    def Output(self):
        """"""
        yield self.mStaticLines
        pass
    pass

########################################################################
class AggregateGenerator (PatternGenerator):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        self.mGenerators = args
        pass
    #----------------------------------------------------------------------
    def Output(self):
        """"""
        for g in self.mGenerators:
            for l in g.Output ():
                yield l
        pass
    pass
pass

########################################################################
class DecHppGenerator (PatternGenerator):
    """"""
    PATTERN = '#  define SMUNIX_PP_DEC_%d %d'
    #----------------------------------------------------------------------
    def __init__(self, number):
        """Constructor"""
        self.mNumber = number
        pass
    #----------------------------------------------------------------------
    def Output(self):
        """"""
        while self.mNumber >= 0:
            if self.mNumber == 0:
                yield DecHppGenerator.PATTERN % (self.mNumber, self.mNumber)
            else:
                yield DecHppGenerator.PATTERN % (self.mNumber, self.mNumber - 1)
            self.mNumber -= 1
            pass
        pass
    pass
pass

########################################################################
class IncHppGenerator (PatternGenerator):
    """"""
    PATTERN = '#  define SMUNIX_PP_INC_%d %d'
    #----------------------------------------------------------------------
    def __init__(self, number):
        """Constructor"""
        self.mNumber = number
        pass
    #----------------------------------------------------------------------
    def Output(self):
        """"""
        while self.mNumber >= 0:
            yield IncHppGenerator.PATTERN % (self.mNumber, self.mNumber + 1)
            self.mNumber -= 1
            pass
        pass
    pass
pass

#----------------------------------------------------------------------
def TestIsPowerOf():
    """"""
    return MathToolkit.IsPowerOf (16, 4) and MathToolkit.IsPowerOf (16, 2) and MathToolkit.IsPowerOf (9, 3) and not MathToolkit.IsPowerOf (8, 3)

if __name__ == '__main__':
    engines = []
    autoRecHppGenerator = AggregateGenerator (FileHeaderCommentGenerator ('AutoRec.hpp'), 
                                             IfndefDefGuardGenerator ('_SMUNIX_PP_AUTO_REC_HPP__'),
                                             CharGenerator ('#', 2),
                                             NodeEntryGenerator (), 
                                             CharGenerator ('#', 2),
                                             Node_XXX (),
                                             CharGenerator ('#', 2),
                                             EndifGuardGenerator ('_SMUNIX_PP_AUTO_REC_HPP__'))
    engines.append (Engine(autoRecHppGenerator, 'AutoRec.hpp'))
    decHppGenerator = AggregateGenerator (FileHeaderCommentGenerator ('Dec.hpp'), 
                                             IfndefDefGuardGenerator ('_SMUNIX_PP_DEC_HPP__'),
                                             CharGenerator ('#', 2),
                                             StaticLinesGenerator ('#  define SMUNIX_PP_DEC(x) SMUNIX_PP_DEC_I(x)\n#  define SMUNIX_PP_DEC_I(x) SMUNIX_PP_DEC_ ## x'),
                                             CharGenerator ('#', 2),
                                             DecHppGenerator (256),
                                             CharGenerator ('#', 2),
                                             EndifGuardGenerator ('_SMUNIX_PP_DEC_HPP__'))
    engines.append (Engine(decHppGenerator, 'Dec.hpp'))
    incHppGenerator = AggregateGenerator (FileHeaderCommentGenerator ('Inc.hpp'), 
                                             IfndefDefGuardGenerator ('_SMUNIX_PP_INC_HPP__'),
                                             CharGenerator ('#', 2),
                                             StaticLinesGenerator ('#  define SMUNIX_PP_INC(x) SMUNIX_PP_INC_I(x)\n#  define SMUNIX_PP_INC_I(x) SMUNIX_PP_INC_ ## x'),
                                             CharGenerator ('#', 2),
                                             IncHppGenerator (256),
                                             CharGenerator ('#', 2),
                                             EndifGuardGenerator ('_SMUNIX_PP_INC_HPP__'))
    engines.append (Engine(incHppGenerator, 'Inc.hpp'))
    
    for e in engines:
        e.Run ()