"""
author @ kumar dahal
date: Jun 7 2023
this code is written to handle the exception which will return line number of error

"""
import os
import sys

class ASLDException(Exception):
    
    def __init__(self, error_message:Exception,error_detail:sys):
        super().__init__(error_message)
        self.error_message = ASLDException.get_detailed_error_message(error_message=error_message,
                                                                       error_detail=error_detail
                                                                        )


    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_detail:sys)->str:
        """
        error_message: Exception object
        error_detail: object of sys module
        """
        #retrieve information about an exception that was raised during the processing
        _,_ ,exec_tb = error_detail.exc_info()

        #eturns the line number in the source code where the current frame is executing.
        exception_block_line_number = exec_tb.tb_frame.f_lineno

        #traceback module that represents the current line number in the current traceback frame.
        try_block_line_number = exec_tb.tb_lineno

        #returns the filename associated with the code object that is being executed in the current traceback frame.
        file_name = exec_tb.tb_frame.f_code.co_filename
        
        #format of error message
        error_message = f"""
        Error occured in script: 
        [ {file_name} ] at 
        try block line number: [{try_block_line_number}] and exception block line number: [{exception_block_line_number}] 
        error message: [{error_message}]
        """
        return error_message
    
    #method is used to return a string representation of the object.
    def __str__(self):
        return self.error_message

    #method is used to return a string representation of the object. 
    def __repr__(self) -> str:
        return ASLDException.__name__.str()
