@ECHO ON
call conda activate FTDesign
call python -m uvicorn main:app
@cmd /k