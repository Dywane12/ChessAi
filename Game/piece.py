class Piece:
    '''
    Class piece
    '''
    def __init__(self, type, position, color):
        self.__type = type
        self.__x_pos = position[0]
        self.__y_pos = position[1]
        self.__color = color

    def getType(self):
        return self.__type

    def getPosition(self):
        return [self.__x_pos, self.__y_pos]

    def getIsWhite(self):
        return self.__color