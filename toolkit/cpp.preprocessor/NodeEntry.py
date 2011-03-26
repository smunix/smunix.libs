import math

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
        
#----------------------------------------------------------------------
def TestIsPowerOf():
    """"""
    return MathToolkit.IsPowerOf (16, 4) and MathToolkit.IsPowerOf (16, 2) and MathToolkit.IsPowerOf (9, 3) and not MathToolkit.IsPowerOf (8, 3)

if __name__ == '__main__':
    aggregateGenerator = AggregateGenerator (NodeEntryGenerator (), 
                                             CharGenerator ('#', 2),
                                             Node_XXX ())
    e = Engine(aggregateGenerator, 'AutoRec.hpp')
    e.Run ()   